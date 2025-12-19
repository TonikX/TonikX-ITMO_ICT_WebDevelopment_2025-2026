from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.auth import get_current_user
from src.database import get_session
from src.models.interaction import Comment, Like
from src.models.post import Post
from src.models.user import User
from src.schemas.comment import CommentCreate, CommentRead
from src.schemas.user import UserRead

router = APIRouter(prefix="/posts", tags=["Interactions"])


@router.post("/{post_id}/like", status_code=201)
async def like_post(
    post_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Поставить лайк на пост"""
    # Проверяем существование поста
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Проверяем, не лайкнул ли уже пользователь этот пост
    query = select(Like).where(
        Like.user_id == current_user.id,
        Like.post_id == post_id
    )
    result = await session.execute(query)
    existing_like = result.scalar_one_or_none()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked")
    
    # Создаем лайк
    like = Like(user_id=current_user.id, post_id=post_id)
    session.add(like)
    await session.commit()
    
    return {"message": "Post liked successfully"}


@router.delete("/{post_id}/like", status_code=200)
async def unlike_post(
    post_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Убрать свой лайк с поста"""
    # Ищем лайк
    query = select(Like).where(
        Like.user_id == current_user.id,
        Like.post_id == post_id
    )
    result = await session.execute(query)
    like = result.scalar_one_or_none()
    
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    
    # Удаляем лайк (метод sync)
    await session.delete(like)
    await session.commit()
    
    return {"message": "Like removed successfully"}


@router.get("/{post_id}/likes", response_model=List[int])
async def get_post_likes(
    post_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Получить список ID пользователей, лайкнувших пост"""
    # Проверяем существование поста
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Получаем лайки с подгрузкой пользователей (если нужно), но возвращаем только id пользователей
    query = select(Like).where(Like.post_id == post_id).options(selectinload(Like.user))
    result = await session.execute(query)
    likes = result.scalars().all()
    
    # Возвращаем список user_id
    user_ids = [like.user_id for like in likes]
    
    return user_ids


@router.post("/{post_id}/comments", response_model=CommentRead, status_code=201)
async def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Добавить комментарий к посту"""
    # Проверяем существование поста
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Создаем комментарий
    comment = Comment(
        text=comment_data.text,
        user_id=current_user.id,
        post_id=post_id
    )
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    
    # Возвращаем комментарий с именем пользователя
    return CommentRead(
        id=comment.id,
        text=comment.text,
        user_id=comment.user_id,
        user_name=current_user.name,
        post_id=comment.post_id,
        created_at=comment.created_at
    )


@router.delete("/{post_id}/comments/{comment_id}", status_code=200)
async def delete_comment(
    post_id: int,
    comment_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Удалить свой комментарий или комментарий на своем посте"""
    # Ищем комментарий с подгрузкой поста и автора поста
    query = (
        select(Comment)
        .where(Comment.id == comment_id, Comment.post_id == post_id)
        .options(selectinload(Comment.post).selectinload(Post.author))
    )
    result = await session.execute(query)
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Проверяем, что пользователь - автор комментария ИЛИ автор поста
    is_comment_author = comment.user_id == current_user.id
    is_post_author = comment.post.author.user_id == current_user.id
    
    if not (is_comment_author or is_post_author):
        raise HTTPException(status_code=403, detail="Not allowed")
    
    # Удаляем комментарий
    await session.delete(comment)
    await session.commit()
    
    return {"message": "Comment deleted successfully"}


@router.get("/{post_id}/comments", response_model=List[CommentRead])
async def get_post_comments(
    post_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Получить все комментарии к посту"""
    # Проверяем существование поста
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Получаем комментарии с подгрузкой пользователей
    query = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .options(selectinload(Comment.user))
        .order_by(Comment.created_at.desc())
    )
    result = await session.execute(query)
    comments = result.scalars().all()
    
    # Формируем ответ
    return [
        CommentRead(
            id=comment.id,
            text=comment.text,
            user_id=comment.user_id,
            user_name=comment.user.name,
            post_id=comment.post_id,
            created_at=comment.created_at
        )
        for comment in comments
    ]