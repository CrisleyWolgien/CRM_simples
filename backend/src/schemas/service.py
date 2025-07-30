from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    duration: int
    payment_status: Optional[str] = None


class ServiceRead(ServiceCreate):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True


class ServiceEdit(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[int] = None
    payment_status: Optional[str] = None
