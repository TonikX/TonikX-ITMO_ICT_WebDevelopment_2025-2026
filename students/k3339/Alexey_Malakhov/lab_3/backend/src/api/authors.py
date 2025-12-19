from pathlib import Path
from typing import List

import aiofiles
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from PIL import Image
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth import get_current_user
from src.config import CONTENT_ROOT
from src.database import get_session
from src.models.author import Author
from src.models.user import User
from src.schemas.author import AuthorRead

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get('/', response_model=List[AuthorRead])
async def get_authors(
    user_id: int | None = None,
    session: AsyncSession = Depends(get_session)
):
    """Получить список всех авторов"""
    query = select(Author).order_by(Author.created_at.asc())
    if user_id is not None:
        query = query.where(Author.user_id == user_id)
    result = await session.execute(query)
    authors = result.scalars().all()
    return authors


@router.get('/{author_id}', response_model=AuthorRead)
async def get_author_by_id(
    author_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Получить информацию об авторе по его ID"""
    author = await session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

async def _save_upload(file: UploadFile, dst: Path) -> None:
    """Сохранить загруженный файл на диск"""
    dst.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(dst, "wb") as out:
        while chunk := await file.read(1024 * 1024):
            await out.write(chunk)
    await file.close()

@router.get('/{author_id}/avatar', response_class=FileResponse)
async def avatar_stream(
    author_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Получить аватар автора в виде изображения"""
    author = await session.get(Author, author_id)

    if not author:
        raise HTTPException(404, "Author not found")

    rel_path = f"author/{author.id}/hd.jpg"
    mime_type = "image/jpeg"

    file_path = CONTENT_ROOT / rel_path

    if not file_path.is_file():
        raise HTTPException(404, "File not found")

    return FileResponse(
        path=file_path,
        media_type=mime_type,
    )


@router.post('/', response_model=AuthorRead, status_code=201)
async def create_author(
    name: str = Form(...),
    handle: str = Form(...),
    bio: str = Form(None),
    is_verified: bool = Form(False),
    avatar: UploadFile | None = File(None),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Создать профиль автора для текущего пользователя"""
    # проверяем, есть ли уже профиль автора у пользователя
    existing_author_query = select(Author).where(Author.user_id == current_user.id)
    existing_author_result = await session.execute(existing_author_query)
    existing_author = existing_author_result.scalars().first()
    
    if existing_author:
        raise HTTPException(status_code=400, detail="У вас уже есть профиль автора")
    
    # создаем автора
    author = Author(
        name=name,
        handle=handle,
        bio=bio,
        is_verified=is_verified,
        user_id=current_user.id
    )
    session.add(author)
    await session.commit()
    await session.refresh(author)
    
    # если загружена аватарка, сохраняем ее
    if avatar and avatar.filename:
        # Проверяем тип файла
        if avatar.content_type not in {"image/jpeg", "image/png", "image/jpg"}:
            raise HTTPException(400, "Only jpeg/png images allowed for avatar")
        
        # сохраняем файл
        avatar_path = CONTENT_ROOT / f"author/{author.id}/hd.jpg"
        await _save_upload(avatar, avatar_path)
        
        try:
            with Image.open(avatar_path) as _img:
                # можно добавить ресайз или другую обработку
                pass
        except Exception:
            pass
    
    return author


@router.delete('/{author_id}', status_code=200)
async def delete_author(
    author_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Удалить свой профиль автора"""
    # получаем автора
    author = await session.get(Author, author_id)
    
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    # проверяем, что текущий пользователь является владельцем профиля автора
    if author.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Вы не можете удалить чужой профиль автора")
    
    # удаляем автора
    await session.delete(author)
    await session.commit()
    
    return JSONResponse(
        content={"message": "Профиль автора успешно удален"},
        status_code=200
    )