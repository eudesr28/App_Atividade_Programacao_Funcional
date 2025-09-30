import pytest
import uuid
from App.database.data import create_user, get_user_by_login, get_user_by_id
from utils.security import validate_password

def test_validate_password_ok():
    ok, msg = validate_password("Senha@Forte123!")
    assert ok is True

def test_validate_password_fail():
    ok, msg = validate_password("123")
    assert ok is False

def test_create_and_get_user():
    unique_email = f"user_{uuid.uuid4().hex[:6]}@test.com"
    unique_phone = f"9{uuid.uuid4().int % 1000000000:09}"
    user_id = create_user(
        name="Eudes Silva",
        email=unique_email,
        phone=unique_phone,
        dob="2000-01-01",
        password="Senha@Forte123!"
    )
    user = get_user_by_id(user_id)
    assert user["name"] == "Eudes Silva"
    assert user["email"] == unique_email

def test_login_user():
    unique_email = f"user_{uuid.uuid4().hex[:6]}@test.com"
    unique_phone = f"9{uuid.uuid4().int % 1000000000:09}"
    password = "Outra@Senha123!"
    create_user(
        name="Maria Heloisa",
        email=unique_email,
        phone=unique_phone,
        dob="1999-05-05",
        password=password
    )
    # Login correto
    user = get_user_by_login(unique_email, password)
    assert user is not None
    assert user["name"] == "Maria Heloisa"

    # Login com senha incorreta
    user_fail = get_user_by_login(unique_email, "senha@Errada")
    assert user_fail is None
