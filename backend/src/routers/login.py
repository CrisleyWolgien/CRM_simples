# src/routers/login.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from src.core.db import get_session
from src.repositories import users_crud
from src.core.security import verify_password, create_access_token

router = APIRouter(tags=["Login"])


@router.post("/login/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    # OAuth2PasswordRequestForm espera 'username' e 'password'
    # Vamos usar 'username' como o campo de email
    user = users_crud.get_user_by_email(session, email=form_data.username)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
