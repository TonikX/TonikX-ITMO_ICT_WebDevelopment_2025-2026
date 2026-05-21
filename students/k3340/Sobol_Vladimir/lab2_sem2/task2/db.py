"""SQLite + SQLModel: хранилище результатов парсинга."""
from datetime import datetime
from pathlib import Path
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine

DB_PATH = Path(__file__).parent / "parsed_pages.db"
ENGINE = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})


class ParsedPage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(index=True)
    title: str
    approach: str
    fetched_at: datetime = Field(default_factory=datetime.utcnow)


def init_db() -> None:
    SQLModel.metadata.create_all(ENGINE)


def save_page(url: str, title: str, approach: str) -> None:
    with Session(ENGINE) as session:
        session.add(ParsedPage(url=url, title=title, approach=approach))
        session.commit()
