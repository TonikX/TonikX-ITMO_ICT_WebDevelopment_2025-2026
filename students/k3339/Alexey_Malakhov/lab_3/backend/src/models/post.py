from sqlalchemy import ForeignKey, String, func, select
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship
from src.models.base import Base, IdMixin, TimestampMixin


class Post(Base, TimestampMixin, IdMixin):
    __tablename__ = "posts"
    
    text: Mapped[str | None] = mapped_column(String(1024))  # Текст поста
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))  # Автор поста
    is_free_post: Mapped[bool] = mapped_column(default=False)  # Новое поле

    author: Mapped["Author"] = relationship(back_populates="posts")  # Связь с автором
    contents: Mapped[list["Content"]] = relationship(back_populates="post")  # Связь с контентом (один ко многим)

    likes: Mapped[list["Like"]] = relationship(
        "Like",
        back_populates="post",
        cascade="all, delete-orphan",
    )  # Лайки поста
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
    )  # Комментарии к посту

    # Вычисляемое поле для подсчета лайков
    @classmethod
    def __declare_last__(cls):
        # локальный импорт, чтобы не создавать циклический импорт при загрузке модулей
        from src.models.interaction import Comment, Like
        cls.likes_count = column_property(
            select(func.count(Like.id))
            .where(Like.post_id == cls.id)
            .correlate_except(Like)
            .scalar_subquery()
        )
        cls.comments_count = column_property(
            select(func.count(Comment.id))
            .where(Comment.post_id == cls.id)
            .correlate_except(Comment)
            .scalar_subquery()
        )