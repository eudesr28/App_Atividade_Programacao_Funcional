import pytest
import uuid
from App.database.data import create_user, create_appointment, get_appointment, update_appointment

@pytest.fixture
def user():
    unique_email = f"user_{uuid.uuid4().hex[:6]}@test.com"
    unique_phone = f"9{uuid.uuid4().int % 1000000000:09}"
    user_id = create_user(
        name="Teste Agendamento",
        email=unique_email,
        phone=unique_phone,
        dob="1990-01-01",
        password="Senha@123!"
    )
    return user_id

def test_create_and_get_appointment(user):
    appt_id = create_appointment(user, "Serviço A", "2025-10-01", "10:00")
    appt = get_appointment(user)
    assert appt is not None
    assert appt["service"] == "Serviço A"
    assert appt["date"] == "2025-10-01"
    assert appt["time"] == "10:00"

def test_update_appointment(user):
    appt_id = create_appointment(user, "Serviço B", "2025-10-02", "11:00")
    update_appointment(appt_id, "Serviço C", "2025-10-03", "12:00")
    appt = get_appointment(user)
    assert appt["service"] == "Serviço C"
    assert appt["date"] == "2025-10-03"
    assert appt["time"] == "12:00"
