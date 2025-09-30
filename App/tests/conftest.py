import sys
import os
import pytest
import sqlite3
import uuid

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from database.data import DB_NAME, init_db

# -------------------------------
# Banco temporário para testes
# -------------------------------
TEST_DB = os.path.join(os.path.dirname(DB_NAME), "test_agenda.db")

@pytest.fixture(autouse=True)
def setup_test_db():
    """
    Cria o banco de teste e inicializa as tabelas antes de cada teste.
    Remove o banco ao final do teste.
    """
    import database.data as data_module
    data_module.DB_NAME = TEST_DB

    # Remove banco antigo, se existir
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    init_db()

    yield  

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

@pytest.fixture(autouse=True)
def clear_db():
    """
    Garante que cada teste começa com o banco limpo.
    """
    if os.path.exists(TEST_DB):
        conn = sqlite3.connect(TEST_DB)
        cur = conn.cursor()
        cur.execute("DELETE FROM users")
        cur.execute("DELETE FROM appointments")
        conn.commit()
        conn.close()
