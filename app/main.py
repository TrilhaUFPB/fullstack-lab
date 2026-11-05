"""API de eventos usada em todas as etapas do projeto."""

import tempfile
from datetime import date
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import Base, make_engine
from app.db_session import find_event, get_session
from app.models import Event, Registration
from app.registrations import router as registrations_router 


class EventInput(BaseModel):
    """Dados enviados pelo cliente ao cadastrar um evento."""

    title: str
    date: date
    capacity: int = Field(gt=0)


    @field_validator("title")
    @classmethod
    def title_nao_vazio(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("O título não pode ser vazio")
        return value


def event_to_dict(session: Session, event: Event) -> dict:
    """Monta a resposta de uma evento, com as vagas calculadas no banco."""
    taken = session.scalar(select(func.count()).select_from(Registration).where(Registration.event_id == event.id))
    return {
        "id": event.id,
        "title": event.title,
        "date": event.date,
        "capacity": event.capacity,
        "available_slots": event.capacity - taken,
    }


def create_app(database_url: str | None = None) -> FastAPI:
    """Cria uma API com dados isolados para cada execução ou teste. Sem URL, usa um banco temporário só desta instância."""

    if database_url is None:
        folder = Path(tempfile.mkdtemp(prefix='eventos-'))
        database_url = f"sqlite:///{(folder / 'events.db').as_posix()}"

    app = FastAPI(title="Eventos do Trilha")
    engine = make_engine(database_url)
    Base.metadata.create_all(engine)
    app.state.engine = engine


    @app.get("/events")
    def list_events(session: Session = Depends(get_session)):
        events = session.scalars(select(Event).order_by(Event.id)).all()
        return [event_to_dict(session, event) for event in events]


    @app.get("/events/{event_id}")
    def get_event(event_id: int, session: Session = Depends(get_session)):
        event = find_event(session, event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        return event_to_dict(session, event)
    

    # Atividade 1: valide título e capacidade, gere um ID e guarde o
    # evento em `events`. A resposta deve conter id, title, date e capacity.
    # Os testes mostram os casos de sucesso e de entrada inválida.
    @app.post("/events", status_code=201)
    def create_event(data: EventInput, session: Session = Depends(get_session)):
        event = Event(title=data.title, date=data.date, capacity=data.capacity)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event_to_dict(session, event)

    app.include_router(registrations_router)

    return app


app = create_app("sqlite:///events.db")
