from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base, IdMixin, TimestampMixin


class Like(Base, TimestampMixin, IdMixin):
    __tablename__ = "likes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="likes")
    post: Mapped["Post"] = relationship(back_populates="likes")

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="uq_likes_user_post"),
    )


class Comment(Base, TimestampMixin, IdMixin):
    __tablename__ = "comments"

    text: Mapped[str] = mapped_column(String(1024))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")
