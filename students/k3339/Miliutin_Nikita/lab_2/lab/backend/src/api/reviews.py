from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.tools import get_user_from_token
from sqlalchemy import select
from src.models.reservation import Reservation
from src.models.flight import Flight
from src.models.ticket import Ticket
from src.models.review import Review

templates = Jinja2Templates(directory="src/templates")
router = APIRouter(prefix="/review", tags=["Review"])


@router.post("")
async def create_review(
    request: Request,
    flight_id: int = Form(...),
    rating: int = Form(...),
    comment: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    user = await get_user_from_token(request, session)
    if not user:
        raise HTTPException(status_code=401, detail="Неавторизован")

    # Проверяем, что пользователь регистрировался на рейс и рейс завершен
    registration_check = await session.execute(
        select(Ticket).where(Ticket.id_user == user.id_user).where(Ticket.id_flight == flight_id)
    )
    ticket = registration_check.scalars().first()

    flight_status_check = await session.execute(
        select(Flight).where(Flight.id_flight == flight_id).where(Flight.flight_status == "landed")
    )
    flight = flight_status_check.scalars().first()

    if not ticket or not flight:
        raise HTTPException(status_code=400, detail="Невозможно оставить отзыв")

    # Создаем отзыв
    review = Review(
        id_user=user.id_user, id_flight=flight.id_flight, rating=rating, comment=comment, created_at=datetime.utcnow()
    )
    session.add(review)
    await session.commit()

    return RedirectResponse(url=f"/flights/detail/{flight.id_flight}", status_code=303)
