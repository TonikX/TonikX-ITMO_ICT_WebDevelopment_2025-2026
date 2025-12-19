from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy import Integer, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.models.author import Author
from src.models.interaction import Comment, Like
from src.models.post import Post
from src.models.subscription import Subscription
from src.models.user import User
from src.schemas.analitycs import (
    AuthorsBySubscribersSchema,
    PaidContentRatioSchema,
    TopPostSchema,
    TopUserSchema,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/authors-by-subscribers", response_model=List[AuthorsBySubscribersSchema])
async def get_authors_by_subscribers(
    min_subscribers: int = Query(100, ge=1),
    session: AsyncSession = Depends(get_session)
):
    """
    Авторы с определенным количеством подписчиков и более
    Показывает список авторов и количество их подписчиков
    """
    query = (
        select(
            Author.id.label("author_id"),
            Author.name.label("author_name"),
            Author.handle.label("author_handle"),
            func.count(Subscription.id).label("subscribers_count")
        )
        .join(Subscription, Subscription.author_id == Author.id)
        .group_by(Author.id, Author.name, Author.handle)
        .having(func.count(Subscription.id) >= min_subscribers)
        .order_by(desc("subscribers_count"))
    )
    
    result = await session.execute(query)
    rows = result.all()
    
    return [
        AuthorsBySubscribersSchema(
            author_id=row.author_id,
            author_name=row.author_name,
            author_handle=row.author_handle,
            subscribers_count=row.subscribers_count
        )
        for row in rows
    ]


@router.get("/authors-paid-content-ratio", response_model=List[PaidContentRatioSchema])
async def get_authors_paid_content_ratio(
    limit: int = Query(10, ge=1, le=100),
    min_posts: int = Query(5, ge=1),
    session: AsyncSession = Depends(get_session)
):
    """
    Авторы с платным контентом - показывает соотношение платных и бесплатных постов
    Полезно для анализа монетизации
    """
    query = (
        select(
            Author.id.label("author_id"),
            Author.name.label("author_name"),
            Author.handle.label("author_handle"),
            func.sum(Post.is_free_post.cast(Integer)).label("free_count"),
            func.sum((~Post.is_free_post).cast(Integer)).label("paid_count"),
            func.count(Post.id).label("total_posts")
        )
        .join(Post, Post.author_id == Author.id)
        .group_by(Author.id, Author.name, Author.handle)
        .having(
            (func.count(Post.id) >= min_posts) &
            (func.sum((~Post.is_free_post).cast(Integer)) > 0)
        )
        .order_by(desc("paid_count"))
        .limit(limit)
    )
    
    result = await session.execute(query)
    rows = result.all()
    
    return [
        PaidContentRatioSchema(
            author_id=row.author_id,
            author_name=row.author_name,
            author_handle=row.author_handle,
            free_posts_count=row.free_count or 0,
            paid_posts_count=row.paid_count or 0,
            total_posts_count=row.total_posts,
            paid_ratio=(
                (row.paid_count or 0) / row.total_posts
                if row.total_posts > 0 else 0
            )
        )
        for row in rows
    ]


@router.get("/top-users", response_model=List[TopUserSchema])
async def get_top_users(
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session)
):
    """Топ пользователей по активности (лайки + комментарии)"""
    query = (
        select(
            User.id.label("user_id"),
            User.name.label("user_name"),
            func.count(func.distinct(Like.id)).label("likes_count"),
            func.count(func.distinct(Comment.id)).label("comments_count")
        )
        .outerjoin(Like, Like.user_id == User.id)
        .outerjoin(Comment, Comment.user_id == User.id)
        .group_by(User.id, User.name)
        .order_by(desc(func.count(func.distinct(Like.id)) + func.count(func.distinct(Comment.id))))
        .limit(limit)
    )
    
    result = await session.execute(query)
    rows = result.all()
    
    return [
        TopUserSchema(
            user_id=row.user_id,
            user_name=row.user_name,
            activity_score=row.likes_count + row.comments_count,
            likes_given=row.likes_count,
            comments_made=row.comments_count
        )
        for row in rows
    ]


@router.get("/top-posts", response_model=List[TopPostSchema])
async def get_top_posts(
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session)
):
    """Топ постов по реакциям (лайки + комментарии)"""
    query = (
        select(
            Post.id.label("post_id"),
            Post.text.label("post_text"),
            Author.name.label("author_name"),
            Post.likes_count.label("likes_count"),
            Post.comments_count.label("comments_count"),
            (Post.likes_count + Post.comments_count).label("total_reactions")
        )
        .join(Author, Author.id == Post.author_id)
        .order_by(desc("total_reactions"))
        .limit(limit)
    )
    
    result = await session.execute(query)
    rows = result.all()
    
    return [
        TopPostSchema(
            post_id=row.post_id,
            post_text=row.post_text,
            author_name=row.author_name,
            likes_count=row.likes_count,
            comments_count=row.comments_count,
            total_reactions=row.total_reactions
        )
        for row in rows
    ]
