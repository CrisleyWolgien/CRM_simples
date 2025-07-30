from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date


class createClient(BaseModel):
    name: str
    email: EmailStr
    phone: int
    date_joined: date
    notes: Optional[str] = None


class updateClient(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[int] = None
    date_joined: Optional[date] = None
    notes: Optional[str] = None

class ReadClient(BaseModel):
    name: str
    email: EmailStr
    phone: int
    date_joined: date
    notes: Optional[str] = None
    vehicles: List[str]
    services: List[str]