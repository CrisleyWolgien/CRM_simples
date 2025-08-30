# src/repositories/vehicles_crud.py

from sqlmodel import Session, select
from fastapi import HTTPException
from uuid import UUID

from src.models.vehicle import Vehicle
from src.schemas.vehicle import VehicleCreate, VehicleUpdate


def create_vehicle_for_client(
    session: Session, client_id: UUID, vehicle_in: VehicleCreate
) -> Vehicle:
    """Cria um novo veículo associado a um cliente."""
    # Cria o dicionário de dados do veículo e adiciona o owner_id
    vehicle_data = vehicle_in.model_dump()
    db_vehicle = Vehicle(**vehicle_data, owner_id=client_id)

    session.add(db_vehicle)
    session.commit()
    session.refresh(db_vehicle)
    return db_vehicle


def get_vehicles_by_client_id(session: Session, client_id: UUID) -> list[Vehicle]:
    """Retorna todos os veículos de um cliente específico."""
    statement = select(Vehicle).where(Vehicle.owner_id == client_id)
    vehicles = session.exec(statement).all()
    return list(vehicles)


def get_vehicle_by_id(session: Session, vehicle_id: UUID) -> Vehicle | None:
    """Busca um veículo pelo seu ID."""
    return session.get(Vehicle, vehicle_id)


def update_vehicle_by_id(
    session: Session, vehicle_id: UUID, vehicle_in: VehicleUpdate
) -> Vehicle:
    """Atualiza um veículo existente."""
    db_vehicle = get_vehicle_by_id(session, vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    vehicle_data = vehicle_in.model_dump(exclude_unset=True)
    for key, value in vehicle_data.items():
        setattr(db_vehicle, key, value)

    session.add(db_vehicle)
    session.commit()
    session.refresh(db_vehicle)
    return db_vehicle


def delete_vehicle_by_id(session: Session, vehicle_id: UUID) -> None:
    """Deleta um veículo."""
    db_vehicle = get_vehicle_by_id(session, vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    session.delete(db_vehicle)
    session.commit()
    return
