# src/routers/clients.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID

from src.core.db import get_session
from src.core.security import get_current_user
from src.models.users import Users
from src.schemas.clients import (
    createClient,
    updateClient,
    ReadClient,
    ClientReadWithVehicles,
)
from src.repositories import clients_crud

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/", status_code=201, response_model=ReadClient)
def route_create_client(
    client_in: createClient,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),  # Protege a rota
):
    """
    Cria um novo cliente. Apenas para usuários autenticados.
    """
    new_client = clients_crud.create_client(session=session, client_in=client_in)
    return new_client


@router.get("/", response_model=list[ReadClient])
def route_get_all_clients(
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),  # Protege a rota
):
    """
    Retorna todos os clientes. Apenas para usuários autenticados.
    """
    clients = clients_crud.get_all_clients(session=session)
    return clients


@router.get("/{client_id}", response_model=ClientReadWithVehicles)
def route_get_client_by_id(
    client_id: UUID,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """
    Obtém os detalhes de um cliente específico.
    """
    client = clients_crud.get_client_by_id(session, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client


@router.put("/{client_id}", response_model=ReadClient)
def route_update_client(
    client_id: UUID,
    client_in: updateClient,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """
    Atualiza um cliente existente.
    """
    updated_client = clients_crud.update_client_by_id(session, client_id, client_in)
    return updated_client


@router.delete("/{client_id}", status_code=204)
def route_delete_client(
    client_id: UUID,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """
    Deleta um cliente.
    """
    clients_crud.delete_client_by_id(session, client_id)
    # Para DELETE, não se retorna conteúdo, apenas o status 204
    return
