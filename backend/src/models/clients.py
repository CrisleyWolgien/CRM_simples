from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from typing import List, Optional
from uuid import UUID, uuid4
from models.vehicle import Vehicle
from models.service import Service


class Client(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    email: str
    phone: str
    notes: Optional[str] = None
    join_date: date = Field(default_factory=date.today)

    vehicles: List["Vehicle"] = Relationship(back_populates="owner")
    services: List["Service"] = Relationship(back_populates="client")
