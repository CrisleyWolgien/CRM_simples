# src/repositories/services_crud.py

from sqlmodel import Session, select
from fastapi import HTTPException
from uuid import UUID

from src.models.service import Service
from src.models.vehicle import Vehicle
from src.schemas.service import ServiceCreate, ServiceUpdate

def create_service_for_vehicle(
    session: Session, vehicle_id: UUID, service_in: ServiceCreate
) -> Service:
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    service_data = service_in.model_dump()
    if vehicle.id is None:
        raise HTTPException(status_code=400, detail="ID do veículo está ausente")
    db_service = Service(
        **service_data,
        vehicle_id=vehicle.id,
        client_id=vehicle.owner_id, # CORREÇÃO: Adicionar o client_id
        model_vehicle=f"{vehicle.brand} {vehicle.model}"
    )
    
    session.add(db_service)
    session.commit()
    session.refresh(db_service)
    return db_service

def get_services_by_vehicle_id(session: Session, vehicle_id: UUID) -> list[Service]:
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        return []
    return vehicle.services

def update_service_by_id(session: Session, service_id: UUID, service_in: ServiceUpdate) -> Service:
    db_service = session.get(Service, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    
    service_data = service_in.model_dump(exclude_unset=True)
    for key, value in service_data.items():
        setattr(db_service, key, value)
        
    session.add(db_service)
    session.commit()
    session.refresh(db_service)
    return db_service

def delete_service_by_id(session: Session, service_id: UUID) -> None:
    db_service = session.get(Service, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
        
    session.delete(db_service)
    session.commit()
    return