# tests/test_clients.py

from fastapi.testclient import TestClient
from uuid import uuid4

# A fixture 'client' vem do conftest.py
# A fixture 'auth_headers' também vem do conftest.py

def test_create_client_unauthorized(client: TestClient):
    """
    Testa a tentativa de criar um cliente sem estar autenticado.
    Deve retornar um erro 401 Unauthorized.
    """
    client_data = {"name": "Cliente Sem Auth", "email": "noauth@test.com", "phone": "111"}
    response = client.post("/clients/", json=client_data)
    assert response.status_code == 401

def test_create_and_read_client(client: TestClient, auth_headers: dict):
    """
    Testa a criação de um cliente e depois a sua leitura.
    Cobre os endpoints POST /clients/ e GET /clients/{client_id}.
    """
    # 1. Criar o cliente
    client_data = {
        "name": "Cliente de Teste Completo",
        "email": "completo@teste.com",
        "phone": "987654321"
    }
    response = client.post("/clients/", json=client_data, headers=auth_headers)
    
    assert response.status_code == 201
    created_client = response.json()
    
    assert created_client["name"] == client_data["name"]
    assert created_client["email"] == client_data["email"]
    assert "id" in created_client
    
    client_id = created_client["id"]
    
    # 2. Ler o cliente recém-criado
    response = client.get(f"/clients/{client_id}", headers=auth_headers)
    
    assert response.status_code == 200
    read_client = response.json()
    assert read_client["id"] == client_id
    assert read_client["name"] == client_data["name"]

def test_get_nonexistent_client(client: TestClient, auth_headers: dict):
    """
    Testa a tentativa de obter um cliente com um UUID que não existe.
    Deve retornar um erro 404 Not Found.
    """
    random_id = uuid4()
    response = client.get(f"/clients/{random_id}", headers=auth_headers)
    assert response.status_code == 404

def test_update_client(client: TestClient, auth_headers: dict):
    """
    Testa a atualização de um cliente existente.
    Cobre o endpoint PUT /clients/{client_id}.
    """
    # 1. Primeiro, criar um cliente para poder atualizá-lo
    client_data = {"name": "Cliente Original", "email": "original@teste.com", "phone": "555"}
    response = client.post("/clients/", json=client_data, headers=auth_headers)
    assert response.status_code == 201
    client_id = response.json()["id"]
    
    # 2. Agora, atualizar o nome do cliente
    update_data = {"name": "Cliente Atualizado"}
    response = client.put(f"/clients/{client_id}", json=update_data, headers=auth_headers)
    
    assert response.status_code == 200
    updated_client = response.json()
    assert updated_client["name"] == "Cliente Atualizado"
    assert updated_client["email"] == "original@teste.com" # O email não deve ter mudado

def test_delete_client(client: TestClient, auth_headers: dict):
    """
    Testa a remoção de um cliente.
    Cobre o endpoint DELETE /clients/{client_id}.
    """
    # 1. Criar um cliente para poder apagá-lo
    client_data = {"name": "Cliente a Apagar", "email": "apagar@teste.com", "phone": "000"}
    response = client.post("/clients/", json=client_data, headers=auth_headers)
    assert response.status_code == 201
    client_id = response.json()["id"]
    
    # 2. Apagar o cliente
    response = client.delete(f"/clients/{client_id}", headers=auth_headers)
    assert response.status_code == 204 # 204 No Content é a resposta esperada
    
    # 3. Verificar que o cliente foi mesmo apagado
    response = client.get(f"/clients/{client_id}", headers=auth_headers)
    assert response.status_code == 404