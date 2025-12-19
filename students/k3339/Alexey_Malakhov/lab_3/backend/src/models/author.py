import datetime
from venv import create

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base, IdMixin, TimestampMixin, str_256


class Author(Base, TimestampMixin, IdMixin):
    __tablename__ = "authors"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    name: Mapped[str_256 | None]
    handle: Mapped[str_256]  # @name или site.com/author/name
    bio: Mapped[str_256 | None]
    is_verified: Mapped[bool]

    contents: Mapped[list["Content"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    subscribers: Mapped[list["Subscription"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    author_profile: Mapped["User | None"] = relationship(
        "User",
        back_populates="author_profile",
        uselist=False,
    )