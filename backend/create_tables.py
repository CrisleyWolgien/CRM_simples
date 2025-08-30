# src/create_tables.py

from sqlmodel import SQLModel
from src.core.db import engine

# Importa o pacote de modelos. Isto executa o ficheiro __init__.py
# que, por sua vez, importa todas as classes de modelo individuais.
# Isto torna as classes visíveis para o SQLModel e a sua metadata.


def create_db_and_tables():
    print("Iniciando a criação das tabelas no banco de dados...")

    # Agora o SQLModel.metadata contém todas as suas tabelas
    SQLModel.metadata.create_all(engine)

    print("Tabelas criadas com sucesso!")


# Permite que o script seja executado diretamente
if __name__ == "__main__":
    create_db_and_tables()
