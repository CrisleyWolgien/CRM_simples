from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date



class schedulingCreate(BaseModel):
    name: str  # nome do cliente
    email: EmailStr  # email do cliente
    phone: str  # telefone do cliente
    dateSchedulingCreate: date  # data do agendamento
    time: datetime  # hora do agendamento
    description: Optional[str] = None  # descrição do agendamento


class schedulingEdit(BaseModel):
    name: Optional[str] = None  # nome do cliente
    email: Optional[EmailStr] = None  # email do cliente
    phone: Optional[str] = None  # telefone do cliente
    dateSchedulingCreate: Optional[date] = None  # data do agendamento
    time: Optional[datetime] = None  # hora do agendamento
    description: Optional[str] = None  # descrição do agendamento
