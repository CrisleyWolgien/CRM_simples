from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.core.db import get_session
from src.schemas.users import createUser
from src.services import user_service
from src.core.security import get_current_user
from src.models.users import Users
from src.schemas.users import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=201)
def route_create_user(user_in: createUser, session: Session = Depends(get_session)):
    new_user = user_service.create_new_user(session=session, user_in=user_in)

    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}


@router.get("/me", response_model=UserRead)
def read_users_me(current_user: Users = Depends(get_current_user)):
    """
    Retorna os dados do usuário atualmente autenticado.
    """
    return current_user
