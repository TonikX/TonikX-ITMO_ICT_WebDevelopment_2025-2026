import datetime
from typing import Annotated

from sqlalchemy import String, text, ForeignKey, Table, Column, UniqueConstraint, Index
from sqlalchemy.orm import DeclarativeBase, query_expression
from sqlalchemy.orm import Mapped, mapped_column, relationship

created = Annotated[datetime.datetime, mapped_column(server_default=text("now()"))]
modified = Annotated[datetime.datetime, mapped_column(
    server_default=text("now()"),
    onupdate=datetime.datetime.now
)]
is_deleted = Annotated[int, mapped_column(
    server_default=text("0")
)]


class Base(DeclarativeBase):
    pass


image_user_table = Table(
    "user_image",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("image_id", ForeignKey("image.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str | None] = mapped_column(String(256), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    about: Mapped[str | None]
    created_time: Mapped[created]
    modified_time: Mapped[modified]
    is_deleted: Mapped[is_deleted]
    post: Mapped[list["Post"]] = relationship(
        back_populates="user")
    like: Mapped[list["Like"]] = relationship(
        back_populates="user")
    comment: Mapped[list["Comment"]] = relationship(
        back_populates="user")
    images: Mapped[list["Image"]] = relationship(secondary=image_user_table, lazy='selectin')

    def __repr__(self) -> str:
        return str(self)

    def __str__(self):
        return f"User(id={self.id!r}, login={self.login!r}, post={self.post!r}, like={self.like!r}, comment={self.comment!r})"


image_post_table = Table(
    "post_image",
    Base.metadata,
    Column("post_id", ForeignKey("post.id"), primary_key=True),
    Column("image_id", ForeignKey("image.id"), primary_key=True),
)


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str | None] = mapped_column(String(256))
    text: Mapped[str | None]
    created_time: Mapped[created]
    modified_time: Mapped[modified]
    is_deleted: Mapped[is_deleted]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="post", lazy='selectin')
    images: Mapped[list["Image"]] = relationship(secondary=image_post_table, lazy='selectin')
    like: Mapped[list["Like"]] = relationship(
        back_populates="post")
    like_count: Mapped[int] = query_expression()
    is_liked: Mapped[bool] = query_expression()
    comment: Mapped[list["Comment"]] = relationship(
        back_populates="post")
    comment_count: Mapped[int] = query_expression()

    def __repr__(self) -> str:
        return str(self)

    def __str__(self):
        return f"Post(id={self.id!r}, title={self.title!r}, text={self.text!r}, post_image={self.post_image!r})"


class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(nullable=False)
    width: Mapped[int] = mapped_column(nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    created_time: Mapped[created]
    modified_time: Mapped[modified]
    is_deleted: Mapped[is_deleted]

    def __repr__(self) -> str:
        return str(self)

    def __str__(self):
        return f"PostImage(id={self.id!r}, url={self.url!r}, ratio={self.ratio!r})"


class Like(Base):
    __tablename__ = "like"
    __table_args__ = (
        Index("idx_like", "post_id", "user_id", unique=True),
        UniqueConstraint("post_id", "user_id", name="u_like"))

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="like")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="like")
    created_time: Mapped[created]

    def __repr__(self) -> str:
        return str(self)

    def __str__(self):
        return f"Post(id={self.id!r}, user_id={self.user_id!r}, post_id={self.post_id!r})"


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(4096), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="comment")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="comment")
    created_time: Mapped[created]
    modified_time: Mapped[modified]
    is_deleted: Mapped[is_deleted]

    def __repr__(self) -> str:
        return str(self)

    def __str__(self):
        return f"Comment(id={self.id!r}, user_id={self.user_id!r}, post_id={self.post_id!r}, text={self.text!r})"



async def create_reccomended_func(session):
    await session.execute(text("""CREATE OR REPLACE FUNCTION calculate_post_score(p_id INT, C float, X float, F float)
RETURNS INT AS $$
DECLARE
    like_count INT;
    comment_count INT;
    time_passed INTERVAL;
BEGIN
    SELECT COUNT(*)
    INTO like_count
    FROM "like"
    WHERE "post_id" = p_id;

    SELECT COUNT(*)
    INTO comment_count
    FROM "comment"
    WHERE "post_id" = p_id;

    SELECT NOW() - "created_time"
    INTO time_passed
    FROM "post"
    WHERE "id" = p_id;

    RETURN C * like_count + X * comment_count - F * EXTRACT(EPOCH FROM time_passed);
END;
$$ LANGUAGE plpgsql;"""))
    await session.commit()