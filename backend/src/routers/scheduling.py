# src/routers/scheduling.py

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from uuid import UUID
from datetime import date
from typing import Optional

from src.core.db import get_session
from src.core.security import get_current_user
from src.models.users import Users
from src.schemas.scheduling import schedulingCreate, schedulingEdit
from src.models.scheduling import Scheduling as SchedulingModel
from src.repositories import scheduling_crud

router = APIRouter(prefix="/scheduling", tags=["Scheduling"])


@router.post("/", response_model=SchedulingModel, status_code=201)
def route_create_scheduling(
    scheduling_in: schedulingCreate,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """Cria um novo agendamento."""
    return scheduling_crud.create_scheduling(session, scheduling_in)


@router.get("/", response_model=list[SchedulingModel])
def route_get_all_schedulings(
    scheduling_date: Optional[date] = Query(
        None, description="Filtra agendamentos por data (YYYY-MM-DD)"
    ),
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """Obtém a lista de todos os agendamentos, com um filtro opcional por data."""
    return scheduling_crud.get_all_schedulings(session, scheduling_date)


@router.put("/{scheduling_id}", response_model=SchedulingModel)
def route_update_scheduling(
    scheduling_id: UUID,
    scheduling_in: schedulingEdit,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """Atualiza um agendamento específico."""
    return scheduling_crud.update_scheduling_by_id(
        session, scheduling_id, scheduling_in
    )


@router.delete("/{scheduling_id}", status_code=204)
def route_delete_scheduling(
    scheduling_id: UUID,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """Deleta um agendamento específico."""
    scheduling_crud.delete_scheduling_by_id(session, scheduling_id)
    return
