# src/models/service.py

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from datetime import date
from typing import List, Optional
from uuid import UUID, uuid4

class Service(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    type: List[str] = Field(sa_column=Column(JSON))
    description: str
    status: str
    
    # Relação com Veículo
    vehicle_id: UUID = Field(foreign_key="vehicle.id")
    vehicle_rel: Optional["Vehicle"] = Relationship(back_populates="services")
    
    # ADICIONADO DE VOLTA: Relação com Cliente
    client_id: UUID = Field(foreign_key="client.id")
    client: Optional["Client"] = Relationship(back_populates="services")

    # Campos de referência
    model_vehicle: str 
    
    date_start: date = Field(default_factory=date.today)
    date_end: Optional[date] = None
    price: float
    payment_condition: str
    observation: Optional[str] = None
    assurance: bool
    assurance_time: Optional[int] = None
    assurance_start: Optional[date] = None