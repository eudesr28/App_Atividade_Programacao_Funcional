import os
import sqlite3
from utils.security import hash_password, verify_password, validate_password

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   

DATA_DIR = os.path.join(BASE_DIR, "..", "data")         

os.makedirs(DATA_DIR, exist_ok=True)                    


DB_NAME = os.path.join(DATA_DIR, "agenda.db")


def with_db(fn):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_NAME)
        try:
            result = fn(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    return wrapper


@with_db
def init_db(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            dob TEXT NOT NULL,
            pwd_salt BLOB NOT NULL,
            pwd_hash BLOB NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            service TEXT NOT NULL,
            appt_date TEXT NOT NULL,
            appt_time TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)


@with_db
def create_user(conn, name, email, phone, dob, password, is_admin=0):
    ok, msg = validate_password(password)
    if not ok:
        raise ValueError(msg)
    salt, h = hash_password(password)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (name, email, phone, dob, pwd_salt, pwd_hash, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name.strip(), email.strip().lower(), phone.strip(), dob, salt, h, is_admin))
    return cur.lastrowid


@with_db
def get_user_by_login(conn, login, password):
    cur = conn.cursor()
    norm = lambda s: s.strip().lower()  

    if "@" in login:
        cur.execute("SELECT id, name, email, phone, dob, pwd_salt, pwd_hash, is_admin FROM users WHERE email = ?", (norm(login),))
    else:
        cur.execute("SELECT id, name, email, phone, dob, pwd_salt, pwd_hash, is_admin FROM users WHERE phone = ?", (login.strip(),))

    row = cur.fetchone()
    if not row:
        return None
    uid, name, email, phone, dob, salt, h, is_admin = row
    if verify_password(password, salt, h):
        return {"id": uid, "name": name, "email": email, "phone": phone, "dob": dob, "is_admin": is_admin}
    return None


@with_db
def get_user_by_id(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, phone, dob FROM users WHERE id = ?", (user_id,))
    r = cur.fetchone()
    if not r:
        return None
    return {"id": r[0], "name": r[1], "email": r[2], "phone": r[3], "dob": r[4]}


@with_db
def get_appointment(conn, user_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT id, service, appt_date, appt_time
        FROM appointments WHERE user_id = ?
        ORDER BY id DESC LIMIT 1
    """, (user_id,))
    r = cur.fetchone()
    if not r:
        return None
    return {"id": r[0], "service": r[1], "date": r[2], "time": r[3]}


@with_db
def create_appointment(conn, user_id, service, appt_date, appt_time):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO appointments (user_id, service, appt_date, appt_time)
        VALUES (?, ?, ?, ?)
    """, (user_id, service, appt_date, appt_time))
    return cur.lastrowid


@with_db
def update_appointment(conn, appt_id, service, appt_date, appt_time):
    cur = conn.cursor()
    cur.execute("""
        UPDATE appointments
        SET service = ?, appt_date = ?, appt_time = ?
        WHERE id = ?
    """, (service, appt_date, appt_time, appt_id))
