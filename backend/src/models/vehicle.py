# src/models/vehicle.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List # Importe List

from uuid import UUID, uuid4

class Vehicle(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    plate: str
    model: str
    brand: str
    year: int
    color: Optional[str] = None

    owner_id: UUID = Field(foreign_key="client.id")
    owner: Optional["Client"] = Relationship(back_populates="vehicles")
    
    # ADICIONADO: A relação para a lista de serviços
    services: List["Service"] = Relationship(back_populates="vehicle_rel")