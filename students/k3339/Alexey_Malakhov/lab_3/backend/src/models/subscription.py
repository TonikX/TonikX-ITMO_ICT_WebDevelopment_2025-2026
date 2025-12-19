import datetime

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base, IdMixin, TimestampMixin


class Subscription(Base, TimestampMixin, IdMixin):
    __tablename__ = "subscriptions"

    subscriber_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    
    started_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    expires_at: Mapped[datetime.datetime | None] = mapped_column(nullable=True)  # None = бесконечная подписка
    renewable: Mapped[bool] = mapped_column(default=True)  # True = будет продлена, False = отменена

    subscriber: Mapped["User"] = relationship(back_populates="subscriptions")
    author: Mapped["Author"] = relationship(back_populates="subscribers")

    __table_args__ = (
        UniqueConstraint("subscriber_id", "author_id", name="uq_subscriptions_user_author"),
    )