"""Modelos relacionais que serão completados na atividade 2."""

import datetime

from sqlalchemy import (Integer,
                        CheckConstraint,
                        Date,
                        ForeignKey,
                        String,
                        UniqueConstraint,
) 
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
        CheckConstraint("capacity > 0", name="ck_events_capacity_positive"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Complete os campos title, date e capacity e suas restrições.
    title: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Complete os campos name e email.
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)


class Registration(Base):
    __tablename__ = "registrations"
    __table_args__ = (
        UniqueConstraint("event_id", "user_id", name="up_registration_event_user"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Relacione event_id e user_id às tabelas corretas e impeça duplicatas.
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    