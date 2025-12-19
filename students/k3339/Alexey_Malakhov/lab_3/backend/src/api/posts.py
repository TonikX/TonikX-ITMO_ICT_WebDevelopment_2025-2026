import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import aiofiles
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    Request,
    UploadFile,
)
from PIL import Image
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from src.auth import get_current_user
from src.config import CONTENT_ROOT
from src.database import get_session
from src.models.author import Author
from src.models.content import Content, ContentType, Photo, Video
from src.models.post import Post
from src.models.subscription import Subscription
from src.models.user import User
from src.schemas.post import PostRead
from src.schemas.posts_response import PostsResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/posts", tags=["Posts"])


async def has_access_to_post(user_id: int, post: Post, session: AsyncSession) -> bool:
    """Проверить, имеет ли пользователь доступ к посту"""
    if post.is_free_post:
        return True
    
    subscription = await session.execute(
        select(Subscription).where(
            Subscription.subscriber_id == user_id,
            Subscription.author_id == post.author_id,
            (Subscription.expires_at.is_(None)) | (Subscription.expires_at > datetime.utcnow())
        ) 
    )
    return subscription.scalar_one_or_none() is not None


async def get_current_user_optional(request: Request, session: AsyncSession = Depends(get_session)):
    try:
        return await get_current_user(request, session)
    except HTTPException:
        return None

@router.get('/', response_model=PostsResponse)
async def get_posts(
    author_id: int | None = None,
    current_user: User | None = Depends(get_current_user_optional),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session)
):
    """Получить ленту постов с пагинацией, показывает бесплатные и посты по подписке"""
    # Получаем список ID авторов, на которых подписан пользователь
    subscribed_author_ids = set()
    user_author_id = None
    
    if current_user:
        subscriptions_result = await session.execute(
            select(Subscription.author_id).where(
                Subscription.subscriber_id == current_user.id,
                (Subscription.expires_at.is_(None)) | (Subscription.expires_at > datetime.utcnow())
            )
        )
        subscribed_author_ids = set(subscriptions_result.scalars().all())
        
        # Проверяем, является ли текущий пользователь автором
        author_result = await session.execute(
            select(Author.id).where(Author.user_id == current_user.id)
        )
        author_data = author_result.scalar_one_or_none()
        if author_data:
            user_author_id = author_data

    base_query = (
        select(Post)
        .options(
            joinedload(Post.author),
            selectinload(Post.contents),
        )
        .order_by(Post.created_at.desc())
    )

    if author_id:
        base_query = base_query.where(Post.author_id == author_id)
    else:
        # Показываем: бесплатные посты ИЛИ посты от авторов, на которых подписан ИЛИ свои посты
        if current_user:
            from sqlalchemy import or_
            if user_author_id:
                # Если пользователь является автором, показываем его посты + подписки + бесплатные
                if subscribed_author_ids:
                    base_query = base_query.where(
                        or_(
                            Post.is_free_post,
                            Post.author_id.in_(subscribed_author_ids),
                            Post.author_id == user_author_id
                        )
                    )
                else:
                    base_query = base_query.where(
                        or_(
                            Post.is_free_post,
                            Post.author_id == user_author_id
                        )
                    )
            elif subscribed_author_ids:
                # Только подписки и бесплатные
                base_query = base_query.where(
                    or_(
                        Post.is_free_post,
                        Post.author_id.in_(subscribed_author_ids)
                    )
                )
            else:
                # Только бесплатные
                base_query = base_query.where(Post.is_free_post)
        else:
            # Если пользователь не залогинен - только бесплатные
            base_query = base_query.where(Post.is_free_post)

    offset = (page - 1) * per_page
    query = base_query.offset(offset).limit(per_page)

    result = await session.execute(query)
    posts = list(result.unique().scalars().all())

    # Получаем список постов, которые лайкнул текущий пользователь
    liked_post_ids = set()
    if current_user:
        from src.models.interaction import Like
        liked_result = await session.execute(
            select(Like.post_id).where(Like.user_id == current_user.id)
        )
        liked_post_ids = set(liked_result.scalars().all())

    # Конвертируем в Pydantic модели и скрываем текст платных постов
    posts_data = []
    for post in posts:
        post_dict = PostRead.model_validate(post).model_dump()
        # Устанавливаем is_liked
        post_dict['is_liked'] = post.id in liked_post_ids
        # Если пост платный и у пользователя нет доступа - скрываем текст и контент
        # Но свои посты показываем полностью
        if not post.is_free_post and post.author_id not in subscribed_author_ids and post.author_id != user_author_id:
            post_dict['text'] = "Платный пост"
            post_dict['contents'] = []  # Скрываем фото/видео
        posts_data.append(PostRead.model_validate(post_dict))

    # Подсчет общего количества
    count_stmt = select(func.count(Post.id))
    if author_id:
        count_stmt = count_stmt.where(Post.author_id == author_id)
    else:
        if current_user:
            from sqlalchemy import or_
            if user_author_id:
                if subscribed_author_ids:
                    count_stmt = count_stmt.where(
                        or_(
                            Post.is_free_post,
                            Post.author_id.in_(subscribed_author_ids),
                            Post.author_id == user_author_id
                        )
                    )
                else:
                    count_stmt = count_stmt.where(
                        or_(
                            Post.is_free_post,
                            Post.author_id == user_author_id
                        )
                    )
            elif subscribed_author_ids:
                count_stmt = count_stmt.where(
                    or_(
                        Post.is_free_post,
                        Post.author_id.in_(subscribed_author_ids)
                    )
                )
            else:
                count_stmt = count_stmt.where(Post.is_free_post)
        else:
            count_stmt = count_stmt.where(Post.is_free_post)

    total_items = (await session.execute(count_stmt)).scalar_one()
    total_pages = (total_items + per_page - 1) // per_page

    return {
        "posts": posts_data,
        "pagination": {
            "totalPages": total_pages,
            "totalItems": total_items,
            "hasMore": page < total_pages,
            "currentPage": page,
        },
    }


@router.get('/{post_id}', response_model=PostRead)
async def get_post_by_id(
    post_id: int,
    current_user: User | None = Depends(get_current_user_optional),
    session: AsyncSession = Depends(get_session)
):
    """Получить пост по ID с проверкой доступа"""
    query = (
        select(Post)
        .options(
            selectinload(Post.contents),
            selectinload(Post.author),
        )
        .where(Post.id == post_id)
    )
    result = await session.execute(query)
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Проверяем доступ
    if current_user and not await has_access_to_post(current_user.id, post, session):
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Проверяем, лайкнул ли пользователь этот пост
    is_liked = False
    if current_user:
        from src.models.interaction import Like
        liked_result = await session.execute(
            select(Like).where(
                Like.user_id == current_user.id,
                Like.post_id == post_id
            )
        )
        is_liked = liked_result.scalar_one_or_none() is not None
    
    post_dict = PostRead.model_validate(post).model_dump()
    post_dict['is_liked'] = is_liked
    
    return PostRead.model_validate(post_dict)


@router.post('/', response_model=PostRead, status_code=201)
async def create_post(
    text: str = Form(...),
    is_free_post: bool = Form(False),
    files: Optional[List[UploadFile]] = File(None),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Создать новый пост с текстом и медиафайлами (до 10 файлов)"""
    # Получаем автора текущего пользователя
    query = select(Author).where(Author.user_id == current_user.id)
    result = await session.execute(query)
    author = result.scalars().first()
    
    if not author:
        raise HTTPException(status_code=404, detail="Author profile not found for current user")

    # Create the post first
    post = Post(
        text=text,
        author_id=author.id,
        is_free_post=is_free_post,
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)

    logger.info(f"Files received: {files}")
    
    # Filter out empty files
    if files:
        files = [f for f in files if f and hasattr(f, 'filename') and f.filename]
        logger.info(f"Filtered files: {len(files)} files")

    # Handle uploaded files (max 10)
    BASE_DIR = Path(__file__).resolve().parents[2]
    CONTENT_ROOT = BASE_DIR / "content"

    async def _save_upload(file: UploadFile, dst: Path) -> None:
        dst.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(dst, "wb") as out:
            while chunk := await file.read(1024 * 1024):
                await out.write(chunk)
        await file.close()

    if files and len(files) > 0:
        if len(files) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 files allowed")

        for idx, file in enumerate(files):
            logger.info(f"Processing file {idx + 1}: {file.filename}, type: {file.content_type}")
            
            # Determine type
            content_obj = None
            if file.content_type and file.content_type.startswith("image/"):
                content_obj = Photo(
                    type=ContentType.photo,
                    width=None,
                    height=None,
                    author_id=author.id,
                    post_id=post.id,
                )
                session.add(content_obj)
                await session.commit()
                await session.refresh(content_obj)
                
                logger.info(f"Created Photo content ID: {content_obj.id}")

                file_path = CONTENT_ROOT / f"photos/{content_obj.id}/hd.jpg"
                await _save_upload(file, file_path)
                logger.info(f"Saved photo to: {file_path}")

                try:
                    with Image.open(file_path) as img:
                        content_obj.width, content_obj.height = img.size
                    await session.commit()
                    logger.info(f"Updated photo dimensions: {content_obj.width}x{content_obj.height}")
                except Exception as e:
                    logger.error(f"Error processing image: {e}")

            elif file.content_type == "video/mp4":
                content_obj = Video(
                    type=ContentType.video,
                    duration=None,
                    author_id=author.id,
                    post_id=post.id,
                )
                session.add(content_obj)
                await session.commit()
                await session.refresh(content_obj)
                
                logger.info(f"Created Video content ID: {content_obj.id}")

                video_path = CONTENT_ROOT / f"videos/{content_obj.id}/hd.mp4"
                await _save_upload(file, video_path)
                logger.info(f"Saved video to: {video_path}")

                try:
                    result = subprocess.run(
                        [
                            "ffprobe",
                            "-v",
                            "error",
                            "-show_entries",
                            "format=duration",
                            "-of",
                            "default=noprint_wrappers=1:nokey=1",
                            str(video_path),
                        ],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    duration_sec = float(result.stdout.strip())
                    content_obj.duration = int(duration_sec)
                    await session.commit()
                    logger.info(f"Updated video duration: {content_obj.duration}s")
                except Exception as e:
                    logger.error(f"Error processing video: {e}")
            else:
                logger.warning(f"Unsupported file type: {file.content_type}")
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    await session.refresh(post, ["contents", "author"])
    logger.info(f"Post created with {len(post.contents)} contents")

    # Устанавливаем is_liked = False для нового поста
    post_dict = PostRead.model_validate(post).model_dump()
    post_dict['is_liked'] = False
    
    return PostRead.model_validate(post_dict)

@router.put('/{post_id}', response_model=PostRead)
async def update_post(
    post_id: int,
    text: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Редактировать текст своего поста"""
    # Проверка существования поста (подгружаем автора)
    post = await session.get(Post, post_id, options=[selectinload(Post.contents), selectinload(Post.author)])
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Только автор может редактировать — сравниваем по user.id, чтобы избежать ленивой загрузки
    if not post.author or post.author.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    # Обновляем текст, если передан
    if text is not None and text != post.text:
        post.text = text
        session.add(post)
        await session.commit()

    await session.refresh(post, ["contents", "author"])
    
    # Проверяем, лайкнул ли пользователь этот пост
    from src.models.interaction import Like
    liked_result = await session.execute(
        select(Like).where(
            Like.user_id == current_user.id,
            Like.post_id == post_id
        )
    )
    is_liked = liked_result.scalar_one_or_none() is not None
    
    post_dict = PostRead.model_validate(post).model_dump()
    post_dict['is_liked'] = is_liked
    
    return PostRead.model_validate(post_dict)

@router.delete('/{post_id}', status_code=204)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Удалить свой пост"""
    post = await session.get(Post, post_id, options=[selectinload(Post.author)])
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if not post.author or post.author.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    await session.delete(post)
    await session.commit()
    return None