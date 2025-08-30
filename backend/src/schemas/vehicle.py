# src/schemas/vehicle.py

from pydantic import BaseModel
from typing import Optional
from uuid import UUID


# Schema para criar um veículo. O owner_id virá do URL.
class VehicleCreate(BaseModel):
    plate: str
    model: str
    brand: str
    year: int
    color: Optional[str] = None


# Schema para atualizar um veículo. Todos os campos são opcionais.
class VehicleUpdate(BaseModel):
    plate: Optional[str] = None
    model: Optional[str] = None
    brand: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None


# Schema para ler/retornar os dados de um veículo.
class VehicleRead(VehicleCreate):
    id: UUID
    owner_id: UUID

    class Config:
        from_attributes = True
