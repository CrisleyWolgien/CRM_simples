# src/repositories/scheduling_crud.py

from sqlmodel import Session, select
from fastapi import HTTPException
from uuid import UUID
from datetime import date

from src.models.scheduling import Scheduling
from src.schemas.scheduling import schedulingCreate, schedulingEdit


def create_scheduling(session: Session, scheduling_in: schedulingCreate) -> Scheduling:
    """Cria um novo agendamento."""
    db_scheduling = Scheduling.model_validate(scheduling_in)
    session.add(db_scheduling)
    session.commit()
    session.refresh(db_scheduling)
    return db_scheduling


def get_all_schedulings(
    session: Session, scheduling_date: date | None = None
) -> list[Scheduling]:
    """Retorna todos os agendamentos, com filtro opcional por data."""
    statement = select(Scheduling)
    if scheduling_date:
        statement = statement.where(Scheduling.date == scheduling_date)
    schedulings = session.exec(statement).all()
    return list(schedulings)


def update_scheduling_by_id(
    session: Session, scheduling_id: UUID, scheduling_in: schedulingEdit
) -> Scheduling:
    """Atualiza um agendamento existente."""
    db_scheduling = session.get(Scheduling, scheduling_id)
    if not db_scheduling:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    scheduling_data = scheduling_in.model_dump(exclude_unset=True)
    for key, value in scheduling_data.items():
        setattr(db_scheduling, key, value)

    session.add(db_scheduling)
    session.commit()
    session.refresh(db_scheduling)
    return db_scheduling


def delete_scheduling_by_id(session: Session, scheduling_id: UUID) -> None:
    """Deleta um agendamento."""
    db_scheduling = session.get(Scheduling, scheduling_id)
    if not db_scheduling:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    session.delete(db_scheduling)
    session.commit()
    return
