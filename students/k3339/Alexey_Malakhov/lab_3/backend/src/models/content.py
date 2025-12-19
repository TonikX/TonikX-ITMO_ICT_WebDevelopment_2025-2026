import enum
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base, IdMixin, TimestampMixin, str_256


class ContentType(enum.Enum):
    photo = "photo"
    video = "video"

intpk = Annotated[int, mapped_column(ForeignKey("content.id", ondelete="CASCADE"), primary_key=True)]

class Content(Base, TimestampMixin, IdMixin):
    __tablename__ = 'content'

    type: Mapped[ContentType]
    author_id: Mapped[int | None] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    post_id: Mapped[int | None] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))

    author: Mapped["Author"] = relationship(back_populates="contents")
    post: Mapped["Post"] = relationship(back_populates="contents")  # Обратная связь с постом

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "content",
    }


class Photo(Content):
    __tablename__ = "photo"

    id: Mapped[intpk]

    width: Mapped[int | None]
    height: Mapped[int | None]

    __mapper_args__ = {
        "polymorphic_identity": ContentType.photo,
    }


class Video(Content):
    __tablename__ = "video"

    id: Mapped[intpk]

    duration: Mapped[int | None]

    __mapper_args__ = {
        "polymorphic_identity": ContentType.video,
    }