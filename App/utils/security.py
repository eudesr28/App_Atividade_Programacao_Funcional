import hmac
import hashlib, os, re

def make_password_validator(min_len=8):
    regex_letter = re.compile(r"[A-Za-z]")
    regex_digit = re.compile(r"\d")
    regex_special = re.compile(r"[^\w\s]")

    def validate(pwd: str):
        if len(pwd) < min_len:
            return False, f"A senha deve ter pelo menos {min_len} caracteres."
        if not regex_letter.search(pwd):
            return False, "A senha deve conter pelo menos uma letra."
        if not regex_digit.search(pwd):
            return False, "A senha deve conter pelo menos um número."
        if not regex_special.search(pwd):
            return False, "A senha deve conter pelo menos um caractere especial."
        return True, ""
    return validate

validate_password = make_password_validator(8)


def hash_password(password: str, salt: bytes = None):
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return salt, dk


def verify_password(password, salt, stored_hash):
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return hmac.compare_digest(dk, stored_hash) 
