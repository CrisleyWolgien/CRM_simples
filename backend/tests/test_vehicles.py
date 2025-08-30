# tests/test_vehicles.py

from fastapi.testclient import TestClient

# As fixtures 'client', 'auth_headers', e 'client_db_id' vêm do conftest.py

def test_create_vehicle_for_client(client: TestClient, auth_headers: dict, client_db_id: str):
    """
    Testa a criação bem-sucedida de um veículo para um cliente existente.
    """
    vehicle_data = {
        "plate": "BRA2E19",
        "model": "Gol",
        "brand": "Volkswagen",
        "year": 2020
    }
    response = client.post(f"/clients/{client_db_id}/vehicles/", json=vehicle_data, headers=auth_headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["plate"] == "BRA2E19"
    assert data["brand"] == "Volkswagen"
    assert data["owner_id"] == client_db_id

def test_get_vehicles_for_client(client: TestClient, auth_headers: dict, client_db_id: str):
    """
    Testa a listagem de veículos para um cliente específico.
    """
    # 1. Adicionar dois veículos ao cliente
    client.post(f"/clients/{client_db_id}/vehicles/", json={"plate": "VEH001", "model": "Mobi", "brand": "Fiat", "year": 2021}, headers=auth_headers)
    client.post(f"/clients/{client_db_id}/vehicles/", json={"plate": "VEH002", "model": "Onix", "brand": "Chevrolet", "year": 2022}, headers=auth_headers)

    # 2. Obter a lista de veículos
    response = client.get(f"/clients/{client_db_id}/vehicles/", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["plate"] == "VEH001"
    assert data[1]["plate"] == "VEH002"

def test_update_vehicle(client: TestClient, auth_headers: dict, client_db_id: str):
    """
    Testa a atualização de um veículo existente.
    """
    # 1. Criar um veículo
    vehicle_data = {"plate": "UPD4T3", "model": "Argo", "brand": "Fiat", "year": 2021}
    response = client.post(f"/clients/{client_db_id}/vehicles/", json=vehicle_data, headers=auth_headers)
    assert response.status_code == 201
    vehicle_id = response.json()["id"]

    # 2. Atualizar a cor e o ano do veículo
    update_data = {"color": "Vermelho", "year": 2022}
    response = client.put(f"/vehicles/{vehicle_id}", json=update_data, headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["color"] == "Vermelho"
    assert data["year"] == 2022
    assert data["plate"] == "UPD4T3" # A matrícula não deve ter mudado

def test_delete_vehicle(client: TestClient, auth_headers: dict, client_db_id: str):
    """
    Testa a remoção de um veículo.
    """
    # 1. Criar um veículo
    vehicle_data = {"plate": "DEL3T3", "model": "Kwid", "brand": "Renault", "year": 2023}
    response = client.post(f"/clients/{client_db_id}/vehicles/", json=vehicle_data, headers=auth_headers)
    assert response.status_code == 201
    vehicle_id = response.json()["id"]

    # 2. Apagar o veículo
    response = client.delete(f"/vehicles/{vehicle_id}", headers=auth_headers)
    assert response.status_code == 204

    # 3. Verificar que o veículo foi mesmo apagado (tentando obtê-lo novamente)
    # Primeiro, obtemos a lista de veículos do cliente e verificamos que está vazia
    response = client.get(f"/clients/{client_db_id}/vehicles/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 0