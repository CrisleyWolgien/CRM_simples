# src/schemas/clients.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from uuid import UUID
from .vehicle import VehicleRead


class createClient(BaseModel):
    name: str
    email: EmailStr
    phone: str  # <- ALTERADO de int para str
    notes: Optional[str] = None
    # Removido date_joined, pois o modelo já o define com um valor padrão


class updateClient(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None  # <- ALTERADO de int para str
    notes: Optional[str] = None


class ReadClient(BaseModel):
    id: UUID  # Adicionado para que possamos ver o ID na resposta
    name: str
    email: EmailStr
    phone: str  # <- ALTERADO de int para str
    join_date: date
    notes: Optional[str] = None

    # Adicionando uma configuração para permitir a leitura de modelos ORM
    class Config:
        from_attributes = True


class ClientReadWithVehicles(ReadClient):
    vehicles: list[VehicleRead] = []
