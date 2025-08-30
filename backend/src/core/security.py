# src/core/security.py

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session

from src.core.db import get_session
from src.models.users import Users
from src.repositories import users_crud

load_dotenv()

# --- HASHING DE SENHAS ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde à senha criptografada."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha."""
    return pwd_context.hash(password)


# --- CONFIGURAÇÕES E FUNÇÕES JWT ---
SECRET_KEY = os.getenv("SECRET_KEY", "uma_chave_secreta_padrao")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# A URL onde o cliente/frontend irá obter o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um novo token de acesso."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> Users:
    """Decodifica o token JWT para obter o email e retorna o objeto User."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Usando o operador "morsa" para atribuir e verificar ao mesmo tempo
        if not (email := payload.get("sub")):
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = users_crud.get_user_by_email(session, email=email)
    if user is None:
        raise credentials_exception

    return user
