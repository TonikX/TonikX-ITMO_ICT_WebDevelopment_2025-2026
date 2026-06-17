import os
from sqlmodel import SQLModel, Session, create_engine

DB_URL = os.getenv(
    "DB_ADMIN",
    "postgresql+psycopg2://postgres:postgres@db:5432/partners_db",
)
engine = create_engine(DB_URL, echo=False, pool_pre_ping=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
