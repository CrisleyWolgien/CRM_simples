from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from uuid import UUID, uuid4
from models.clients import Client


class Vehicle(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    plate: str
    model: str
    brand: str
    year: int
    color: Optional[str] = None

    owner_id: int = Field(foreign_key="client_id")
    owner: Optional[Client] = Relationship(back_populates="vehicles")
