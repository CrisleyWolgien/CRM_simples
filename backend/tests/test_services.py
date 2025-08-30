# tests/test_services.py

from fastapi.testclient import TestClient

# As fixtures vêm do conftest.py e são injetadas automaticamente pelo pytest

def test_create_service_for_vehicle(client: TestClient, auth_headers: dict, vehicle_db_id: str):
    """
    Testa a criação bem-sucedida de um serviço para um veículo.
    """
    service_data = {
        "type": ["Revisão", "Troca de óleo"],
        "description": "Revisão completa de 20.000km",
        "status": "Agendado",
        "price": 550.0,
        "payment_condition": "3x no cartão",
        "assurance": True,
        "assurance_time": 3 # 3 meses de garantia
    }
    response = client.post(f"/vehicles/{vehicle_db_id}/services/", json=service_data, headers=auth_headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Revisão completa de 20.000km"
    assert data["status"] == "Agendado"
    assert data["type"] == ["Revisão", "Troca de óleo"]
    assert "id" in data

def test_get_services_for_vehicle(client: TestClient, auth_headers: dict, vehicle_db_id: str):
    """
    Testa a listagem de serviços para um veículo específico.
    """
    # 1. Adicionar dois serviços ao veículo
    service1 = {"type": ["Funilaria"], "description": "Reparar porta", "status": "Em andamento", "price": 1200.0, "payment_condition": "PIX", "assurance": False}
    service2 = {"type": ["Pintura"], "description": "Pintar capô", "status": "Concluído", "price": 800.0, "payment_condition": "Dinheiro", "assurance": True, "assurance_time": 6}
    
    client.post(f"/vehicles/{vehicle_db_id}/services/", json=service1, headers=auth_headers)
    client.post(f"/vehicles/{vehicle_db_id}/services/", json=service2, headers=auth_headers)

    # 2. Obter a lista de serviços
    response = client.get(f"/vehicles/{vehicle_db_id}/services/", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["description"] == "Reparar porta"
    assert data[1]["description"] == "Pintar capô"

def test_update_service_status(client: TestClient, auth_headers: dict, vehicle_db_id: str):
    """
    Testa a atualização do status de um serviço.
    """
    # 1. Criar um serviço
    service_data = {"type": ["Mecânica"], "description": "Trocar pastilhas de freio", "status": "Orçamento", "price": 300.0, "payment_condition": "Aguardando", "assurance": False}
    response = client.post(f"/vehicles/{vehicle_db_id}/services/", json=service_data, headers=auth_headers)
    assert response.status_code == 201
    service_id = response.json()["id"]

    # 2. Atualizar o status do serviço
    update_data = {"status": "Aprovado"}
    response = client.put(f"/services/{service_id}", json=update_data, headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Aprovado"
    assert data["description"] == "Trocar pastilhas de freio" # Não deve ter mudado

def test_delete_service(client: TestClient, auth_headers: dict, vehicle_db_id: str):
    """
    Testa a remoção de um serviço.
    """
    # 1. Criar um serviço
    service_data = {"type": ["Elétrica"], "description": "Verificar bateria", "status": "Diagnóstico", "price": 50.0, "payment_condition": "Aguardando", "assurance": False}
    response = client.post(f"/vehicles/{vehicle_db_id}/services/", json=service_data, headers=auth_headers)
    assert response.status_code == 201
    service_id = response.json()["id"]

    # 2. Apagar o serviço
    response = client.delete(f"/services/{service_id}", headers=auth_headers)
    assert response.status_code == 204

    # 3. Verificar que o serviço foi mesmo apagado
    response = client.get(f"/vehicles/{vehicle_db_id}/services/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 0