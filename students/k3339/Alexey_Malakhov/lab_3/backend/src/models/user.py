from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base, IdMixin, TimestampMixin, str_256


class User(Base, TimestampMixin, IdMixin):
    __tablename__ = "users"
    
    name: Mapped[str] = mapped_column(String(128))

    email: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    
    likes: Mapped[list["Like"]] = relationship(
        "Like",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    subscriptions: Mapped[list["Subscription"]] = relationship("Subscription", back_populates="subscriber")
    author_profile: Mapped["Author | None"] = relationship(
        "Author",
        back_populates="author_profile",
        uselist=False,
        cascade="all, delete-orphan",
    )