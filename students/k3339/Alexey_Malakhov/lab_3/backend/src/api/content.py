import subprocess
from pathlib import Path
from typing import List

import aiofiles
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectin_polymorphic
from src.config import CONTENT_ROOT
from src.database import get_session
from src.models.author import Author
from src.models.content import Content, ContentType, Photo, Video
from src.schemas.content import (
    ContentUnion,
    PhotoRead,
    VideoRead,
)

router = APIRouter(prefix="/content", tags=["Content"])


@router.get('/', response_model=List[ContentUnion])
async def get_content(
    author: str | None = None,
    session: AsyncSession = Depends(get_session)
):
    """Получить список всего контента или контент конкретного автора"""
    query = (
        select(Content)
        .options(selectin_polymorphic(Content, [Photo, Video]))
        .order_by(Content.created_at.desc()) 
    )

    if author:
        query = query.where(Content.author.has(Author.handle == author))

    result = await session.execute(query)
    content = result.scalars().all() 

    return content


@router.get('/{content_id}', response_model=ContentUnion)
async def get_content_by_id(
    content_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Получить информацию о контенте по его ID"""
    query = (
        select(Content)
        .options(selectin_polymorphic(Content, [Photo, Video]))
        .where(Content.id == content_id)
    )
    result = await session.execute(query)
    content = result.scalars().first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return content

async def _save_upload(file: UploadFile, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(dst, "wb") as out:
        while chunk := await file.read(1024 * 1024):
            await out.write(chunk)
    await file.close()

@router.post('/photo', response_model=PhotoRead, status_code=201)
async def create_photo(
    author_id: int = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    """Загрузить фото для автора"""
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(400, "Only jpeg/png allowed")

    photo = Photo(
        type=ContentType.photo,
        width=None,   # будет рассчитано
        height=None,  # будет рассчитано
        author_id=author_id,
    )
    session.add(photo)
    await session.commit()
    await session.refresh(photo)

    ext = ".jpg" if file.content_type == "image/jpeg" else ".png"
    file_path = CONTENT_ROOT / f"photos/{photo.id}/hd{ext}"
    await _save_upload(file, file_path)

    # вычисляем размеры
    try:
        with Image.open(file_path) as img:
            photo.width, photo.height = img.size
        await session.commit()
        await session.refresh(photo)
    except Exception:
        pass  # если не смогли — оставим None

    return photo


@router.post('/video', response_model=VideoRead, status_code=201)
async def create_video(
    author_id: int = Form(...),
    file: UploadFile = File(...),
    thumbnail: UploadFile | None = File(None),
    session: AsyncSession = Depends(get_session)
):
    """Загрузить видео для автора с опциональной обложкой"""
    if file.content_type not in {"video/mp4"}:
        raise HTTPException(400, "Only mp4 allowed")

    video = Video(
        type=ContentType.video,
        duration=None,           # будет рассчитано
        author_id=author_id,
    )
    session.add(video)
    await session.commit()
    await session.refresh(video)

    # сохраняем видео
    video_path = CONTENT_ROOT / f"videos/{video.id}/hd.mp4"
    await _save_upload(file, video_path)

    # пытаемся вычислить длительность через ffprobe, если установлен
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(video_path)
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        duration_sec = float(result.stdout.strip())
        video.duration = int(duration_sec)
        await session.commit()
        await session.refresh(video)
    except Exception:
        pass  # если нет ffprobe или ошибка — оставим duration=None

    # сохраняем thumbnail, если прислали
    if thumbnail:
        thumb_path = CONTENT_ROOT / f"videos/{video.id}/metadata/thumbnails/cover.jpg"
        await _save_upload(thumbnail, thumb_path)

    return video


@router.get("/{content_id}/stream", response_class=FileResponse)
async def content_stream(
    content_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Получить файл контента (фото или видео) для просмотра"""
    # достаём контент
    query = (
        select(Content)
        .options(selectin_polymorphic(Content, [Photo, Video]))
        .where(Content.id == content_id)
    )
    result = await session.execute(query)
    content = result.scalars().first()

    if not content:
        raise HTTPException(404, "Content not found")

    # строим путь к файлу
    if content.type == ContentType.photo:
        rel_path = f"photos/{content.id}/hd.jpg"
        mime_type = "image/jpeg"
    elif content.type == ContentType.video:
        rel_path = f"videos/{content.id}/hd.mp4"
        mime_type = "video/mp4"
    else:
        raise HTTPException(400, "Unsupported content type")

    file_path = CONTENT_ROOT / rel_path

    if not file_path.is_file():
        raise HTTPException(404, "File not found")

    return FileResponse(
        path=file_path,
        media_type=mime_type,
    )