from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Column, String
from datetime import date
from typing import List, Optional
from uuid import UUID, uuid4
from models.clients import Client


class Service(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    type: List[str] = Field(sa_column=Column(ARRAY(String)))
    description: str
    status: str
    client_id: int = Field(foreign_key="client.id")
    client: Optional[Client] = Relationship(back_populates="clients")
    vehicle: str
    model_vehicle: str
    date_start: date = Field(default_factory=date.today)
    date_end: Optional[date] = None
    price: float
    payment_condition: str
    observation: Optional[str] = None
    assurance: bool
    assurance_time: Optional[int] = None
    assurance_start: Optional[date] = None
