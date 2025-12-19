from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.models.flight import Flight
from src.models.reservation import Reservation
from src.models.seat import Seat
from src.models.user import User

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import selectinload

from src.auth import get_current_user


async def get_user_from_token(request: Request, session: AsyncSession):
    """Возвращает объект пользователя или None."""
    sub = get_current_user(request)
    if not sub:
        return None
    # пробуем найти по id, если не число — по email
    return (
        await session.get(User, int(sub))
        if sub.isdigit()
        else (await session.execute(select(User).where(User.email == sub))).scalars().first()
    )
