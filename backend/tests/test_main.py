# tests/test_main.py

from fastapi.testclient import TestClient
# Não precisamos de importar o client, o Pytest fá-lo-á por nós

def test_read_root(client: TestClient):
    """Testa se o endpoint raiz está a funcionar corretamente."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo ao CRM para Mecânicas!"}