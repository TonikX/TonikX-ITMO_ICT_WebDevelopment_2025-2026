from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

metadata = MetaData()

class Base(DeclarativeBase):
    metadata = metadata

# Экспорт CRUD операций
from app.core.db import crud

__all__ = ["Base", "metadata", "crud"]
