# src/routers/services.py

from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID

from src.core.db import get_session
from src.core.security import get_current_user
from src.models.users import Users
from src.schemas.service import ServiceCreate, ServiceUpdate, ServiceRead
from src.repositories import services_crud

router = APIRouter(tags=["Services"])


@router.post(
    "/vehicles/{vehicle_id}/services/", response_model=ServiceRead, status_code=201
)
def route_create_service(
    vehicle_id: UUID,
    service_in: ServiceCreate,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """Cria um novo serviço para um veículo específico."""
    return services_crud.create_service_for_vehicle(session, vehicle_id, service_in)


@router.get("/vehicles/{vehicle_id}/services/", response_model=list[ServiceRead])
def route_get_services_for_vehicle(
    vehicle_id: UUID,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """Obtém a lista de serviços de um veículo específico."""
    return services_crud.get_services_by_vehicle_id(session, vehicle_id)


@router.put("/services/{service_id}", response_model=ServiceRead)
def route_update_service(
    service_id: UUID,
    service_in: ServiceUpdate,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """Atualiza um serviço específico."""
    return services_crud.update_service_by_id(session, service_id, service_in)


@router.delete("/services/{service_id}", status_code=204)
def route_delete_service(
    service_id: UUID,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """Deleta um serviço específico."""
    services_crud.delete_service_by_id(session, service_id)
    return
