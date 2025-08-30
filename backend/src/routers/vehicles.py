# src/routers/vehicles.py

from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID

from src.core.db import get_session
from src.core.security import get_current_user
from src.models.users import Users
from src.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleRead
from src.repositories import vehicles_crud

# Aninharemos estas rotas sob /clients/{client_id}
router = APIRouter(tags=["Vehicles"])


@router.post(
    "/clients/{client_id}/vehicles/", response_model=VehicleRead, status_code=201
)
def route_create_vehicle(
    client_id: UUID,
    vehicle_in: VehicleCreate,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """Cria um novo veículo para um cliente específico."""
    return vehicles_crud.create_vehicle_for_client(session, client_id, vehicle_in)


@router.get("/clients/{client_id}/vehicles/", response_model=list[VehicleRead])
def route_get_vehicles_for_client(
    client_id: UUID,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """Obtém a lista de veículos de um cliente específico."""
    return vehicles_crud.get_vehicles_by_client_id(session, client_id)


# Rotas para gerir um veículo específico pelo seu próprio ID
@router.put("/vehicles/{vehicle_id}", response_model=VehicleRead)
def route_update_vehicle(
    vehicle_id: UUID,
    vehicle_in: VehicleUpdate,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """Atualiza um veículo específico."""
    return vehicles_crud.update_vehicle_by_id(session, vehicle_id, vehicle_in)


@router.delete("/vehicles/{vehicle_id}", status_code=204)
def route_delete_vehicle(
    vehicle_id: UUID,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """Deleta um veículo específico."""
    vehicles_crud.delete_vehicle_by_id(session, vehicle_id)
    return
