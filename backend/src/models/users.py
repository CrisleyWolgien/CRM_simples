from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr
from uuid import UUID, uuid4

class users(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    username: str  # nome de usuário
    email: EmailStr  # email do usuário
    password: str  # senha do usuário
