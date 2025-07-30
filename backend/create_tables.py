# src/create_tables.py

from sqlmodel import SQLModel
from src.core.db import engine

from src.models.clients import clients
from backend.src.models.scheduling import appointments
from src.models.service import service 
from src.models.users import users


def create_db_and_tables():
    print("Iniciando a criação das tabelas no banco de dados...")
    
    # A linha mágica que cria as tabelas
    SQLModel.metadata.create_all(engine)
    
    print("Tabelas criadas com sucesso!")

# Permite que o script seja executado diretamente
if __name__ == "__main__":
    create_db_and_tables()