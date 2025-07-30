from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field


class ServiceCreate(BaseModel):
    type: List[str]
    description: str
    status: str
    vehicle: str
    date_end: Optional[date] = None
    price: float
    payment_condition: str
    observation: Optional[str] = None
    assurance: bool
    assurance_time: Optional[int] = None
    assurance_start: Optional[date] = None


class ServiceRead(ServiceCreate):
    client: str
    date_start: date


class ServiceUpdate(BaseModel):
    type: Optional[List[str]] = None
    description: Optional[str] = None
    status: Optional[str] = None
    vehicle: Optional[str] = None
    date_end: Optional[date] = None
    price: Optional[float] = None
    payment_condition: Optional[str] = None
    observation: Optional[str] = None
    assurance: Optional[bool] = None
    assurance_time: Optional[int] = None
    assurance_start: Optional[date] = None
