from sqlmodel import SQLModel, Field
from datetime import datetime, date
from typing import Optional
from pydantic import EmailStr
from uuid import UUID, uuid4


class Scheduling(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str  # nome do cliente
    email: EmailStr  # email do cliente
    phone: str  # telefone do cliente
    date: date  # data do agendamento
    time: datetime  # hora do agendamento
    description: Optional[str] = None  # descrição do agendamento
