from sqlmodel import Session
from fastapi import HTTPException

from src.repositories import users_crud
from src.models.users import Users
from src.schemas.users import createUser
from src.core.security import get_password_hash


def create_new_user(session: Session, user_in: createUser) -> Users:
    user_existing = users_crud.get_user_by_email(session, email=user_in.email)
    if user_existing:
        raise HTTPException(status_code=400, detail="Email já em uso")

    hashed_password = get_password_hash(user_in.password)

    return users_crud.create_user(
        session=session, user_in=user_in, hashed_password=hashed_password
    )
