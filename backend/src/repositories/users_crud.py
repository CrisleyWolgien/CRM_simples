from sqlmodel import Session, select

from src.models.users import Users
from src.schemas.users import createUser


def create_user(session: Session, user_in: createUser, hashed_password: str) -> Users:
    user_data = user_in.model_dump()
    user_data.pop("password")

    db_user = Users(**user_data, password=hashed_password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def get_user_by_email(session: Session, email: str) -> Users | None:
    return session.exec(select(Users).where(Users.email == email)).first()
