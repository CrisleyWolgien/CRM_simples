from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class createClient(BaseModel):
    name: str
    email: EmailStr
    phone: int
    date_joined: date
    last_service: date


class updateClient(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[int] = None
    date_joined: Optional[date] = None
    last_service: Optional[date] = None
