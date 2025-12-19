import datetime
from typing import Annotated

from sqlalchemy import String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

str_256 = Annotated[str, 256]

class Base(DeclarativeBase):
    type_annotaion_map = {
        str_256: String(256)
    }

class TimestampMixin:
    """Миксин для добавления полей created_at и updated_at"""
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now()::timestamp)")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now()::timestamp)"),
        onupdate=lambda: datetime.datetime.now().replace(tzinfo=None)  # Убираем временную зону
    )

class IdMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # TODO: сделать обфускацию айдишников
