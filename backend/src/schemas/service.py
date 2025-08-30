# src/schemas/service.py

from typing import List, Optional
from datetime import date
from pydantic import BaseModel, EmailStr # Adicionado EmailStr para consistência, embora não usado aqui
from uuid import UUID # Adicionado UUID

class ServiceCreate(BaseModel):
    type: List[str]
    description: str
    status: str
    # O campo 'vehicle' foi removido daqui, pois obtemos o veículo pelo URL.
    date_end: Optional[date] = None
    price: float
    payment_condition: str
    observation: Optional[str] = None
    assurance: bool
    assurance_time: Optional[int] = None
    assurance_start: Optional[date] = None


class ServiceRead(ServiceCreate):
    id: UUID # Adicionado ID para a resposta
    client_id: UUID # Adicionado client_id para a resposta
    date_start: date

    class Config:
        from_attributes = True


class ServiceUpdate(BaseModel):
    type: Optional[List[str]] = None
    description: Optional[str] = None
    status: Optional[str] = None
    date_end: Optional[date] = None
    price: Optional[float] = None
    payment_condition: Optional[str] = None
    observation: Optional[str] = None
    assurance: Optional[bool] = None
    assurance_time: Optional[int] = None
    assurance_start: Optional[date] = None