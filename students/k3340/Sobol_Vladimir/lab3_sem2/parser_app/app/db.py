"""Подключение парсер-сервиса к общей БД Postgres.

Таблица ParsedPage создаётся миграцией main_app (на startup). Здесь
объявляем минимальный mapper того же имени, чтобы можно было писать.
"""
import os
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine

DB_URL = os.getenv(
    "DB_ADMIN",
    "postgresql+psycopg2://postgres:postgres@db:5432/partners_db",
)
engine = create_engine(DB_URL, echo=False, pool_pre_ping=True)


class ParsedPage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(index=True)
    title: str
    source: str = Field(default="http")
    fetched_at: datetime = Field(default_factory=datetime.utcnow)


def save_page(url: str, title: str, source: str = "http") -> ParsedPage:
    with Session(engine) as session:
        page = ParsedPage(url=url, title=title, source=source)
        session.add(page)
        session.commit()
        session.refresh(page)
        return page
