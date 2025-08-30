# src/repositories/clients_crud.py

from sqlmodel import Session, select
from fastapi import HTTPException
from uuid import UUID

from src.models.clients import Client
from src.schemas.clients import createClient, updateClient


def create_client(session: Session, client_in: createClient) -> Client:
    """Adiciona um novo cliente à base de dados."""
    # model_validate converte o schema Pydantic para o modelo SQLModel
    db_client = Client.model_validate(client_in)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client


def get_all_clients(session: Session) -> list[Client]:
    """Retorna todos os clientes da base de dados."""
    return list(session.exec(select(Client)))


def get_client_by_id(session: Session, client_id: UUID) -> Client | None:
    """Busca um cliente pelo seu ID."""
    # session.get é a forma mais eficiente de obter um objeto pela sua chave primária
    return session.get(Client, client_id)


def update_client_by_id(
    session: Session, client_id: UUID, client_in: updateClient
) -> Client:
    """Atualiza um cliente existente."""
    db_client = get_client_by_id(session, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Obtém os dados do schema, excluindo campos não definidos para não substituir por None
    client_data = client_in.model_dump(exclude_unset=True)
    for key, value in client_data.items():
        setattr(db_client, key, value)

    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client


def delete_client_by_id(session: Session, client_id: UUID) -> None:
    """Deleta um cliente."""
    db_client = get_client_by_id(session, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    session.delete(db_client)
    session.commit()
    return
