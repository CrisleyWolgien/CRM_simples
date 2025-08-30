from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


class createUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class updateUser(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


class loginUser(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: UUID
    username: str
    email: EmailStr
