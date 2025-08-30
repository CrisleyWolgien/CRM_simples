# tests/conftest.py

from sqlmodel import create_engine, SQLModel, Session
from fastapi.testclient import TestClient
import pytest

from src.main import app
from src.core.db import get_session
from src import models # Importa todos os modelos para que sejam criados

# URL da base de dados de teste (em memória)
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def override_get_session():
    """Substitui a dependência get_session para usar a base de dados de teste."""
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(name="session")
def session_fixture():
    """Cria e limpa as tabelas para cada teste."""
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Cria um TestClient que usa a sessão de teste."""
    # O yield aqui garante que o código do teste é executado
    yield TestClient(app)

@pytest.fixture(name="auth_headers")
def auth_headers_fixture(client: TestClient):
    """
    Cria um utilizador de teste, faz login e retorna os headers de autorização.
    """
    # Criar um utilizador
    user_data = {
        "username": "testuser_auth", 
        "email": "auth@example.com", 
        "password": "password123"
    }
    client.post("/users/", json=user_data)

    # Fazer login para obter o token
    login_data = {"username": "auth@example.com", "password": "password123"}
    response = client.post("/login/token", data=login_data)
    token = response.json()["access_token"]
    
    # Retornar os headers prontos para usar
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(name="client_db_id")
def client_db_id_fixture(client: TestClient, auth_headers: dict) -> str:
    """
    Cria um cliente de teste e retorna o seu ID.
    Depende do cliente e dos headers de autenticação.
    """
    client_data = {
        "name": "Cliente Padrão para Testes",
        "email": "clientfixture@test.com",
        "phone": "123123123"
    }
    response = client.post("/clients/", json=client_data, headers=auth_headers)
    assert response.status_code == 201
    return response.json()["id"]

@pytest.fixture(name="vehicle_db_id")
def vehicle_db_id_fixture(client: TestClient, auth_headers: dict, client_db_id: str) -> str:
    """
    Cria um veículo de teste para um cliente e retorna o ID do veículo.
    """
    vehicle_data = {
        "plate": "FIX7U43",
        "model": "Cronos",
        "brand": "Fiat",
        "year": 2023
    }
    response = client.post(
        f"/clients/{client_db_id}/vehicles/", 
        json=vehicle_data, 
        headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()["id"]