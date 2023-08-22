"""
This module contains all database entities for the application
"""
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from work_journal.core.app_config import db

engine = db.engine


class Base(DeclarativeBase):
    """
    This is a bare copy of the SQLAlchemy ORM's DeclarativeBase class used to
    track the database's metadata.
    See:  https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#establishing-a-declarative-base
    """

    pass


@dataclass
class Journal(Base):
    """
    This table tracks actual journal entries
    """

    __tablename__ = "journal"

    id: Mapped[int] = mapped_column(primary_key=True)
    ts: Mapped[datetime]
    # Not giving log a string length, might need to change this for a different dbms
    log: Mapped[str]


@dataclass
class Config(Base):
    """
    This table contains project configuration (but obviously not database config!)
    """

    __tablename__ = "config"
    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str]
    value: Mapped[str]
