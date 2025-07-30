from sqlmodel import SQLModel, Field
from datetime import datetime, date
from typing import Optional
from pydantic import EmailStr
from uuid import UUID, uuid4

class clients(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str  # nome do cliente
    email: EmailStr  # email do cliente
    phone: str  # telefone do cliente
    date_joined: date  # data de adesão do cliente
    last_service: Optional[date] = None  # última vez que o cliente foi contatado

    def __repr__(self):
        return f"Client(id={self.id}, name={self.name}, email={self.email}, phone={self.phone}, date_joined={self.date_joined}, last_contacted={self.last_service})"