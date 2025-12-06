from sqlalchemy import func, distinct, case
from sqlalchemy.orm import selectinload, with_expression

from src.db.schemas import User, Post, Like, Comment


def post_options(user_id: int):
    return [selectinload(Post.user).selectinload(User.images),
            selectinload(Post.images),
            with_expression(Post.like_count, func.count(distinct(Like.id))),
            with_expression(Post.comment_count, func.count(distinct(Comment.id))),
            with_expression(Post.is_liked, func.sum(distinct(case((Like.user_id == user_id, 1), else_=0))))]
