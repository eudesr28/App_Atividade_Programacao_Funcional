import sys
import os

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.data import create_user, init_db

# Inicializa o banco (cria tabelas se não existirem)
init_db()

# Cria usuário admin, evitando duplicação
admin_id = create_user(
    name="Administrador",
    email="admin@dominio.com",
    phone="0000000000",
    dob="1990-01-01",
    password="Admin@123",
    is_admin=1
)

print(f"Admin criado com ID {admin_id}")
