from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.tools import get_user_from_token
from sqlalchemy import delete
from sqlalchemy import select
from src.models.reservation import Reservation

templates = Jinja2Templates(directory="src/templates")
router = APIRouter(prefix="/book", tags=["Book"])


@router.post("")
async def book(
    request: Request,
    seat_id: int = Form(...),
    flight_id: int = Form(...),
    session: AsyncSession = Depends(get_session),
):
    user = await get_user_from_token(request, session)

    if user:
        reservation = Reservation(id_user=user.id_user, id_seat=seat_id, id_flight=flight_id)

        session.add(reservation)
        await session.commit()

    response = RedirectResponse(url=f"/flights/detail/{flight_id}", status_code=303)
    return response


@router.post("/delete")
async def delete_reservation(
    request: Request,
    seat_id: int = Form(...),
    flight_id: int = Form(...),
    session: AsyncSession = Depends(get_session),
):
    user = await get_user_from_token(request, session)
    if not user:
        raise HTTPException(status_code=401, detail="Неавторизован")

    # Проверяем, что бронь существует и принадлежит пользователю
    result = await session.execute(
        select(Reservation)
        .where(Reservation.id_seat == seat_id)
        .where(Reservation.id_user == user.id_user)
        .where(Reservation.id_flight == flight_id)
    )
    reservation = result.scalars().first()

    if not reservation:
        raise HTTPException(status_code=403, detail="Нет доступа к удалению этой брони")

    # Удаляем
    await session.delete(reservation)
    await session.commit()

    return RedirectResponse(url=f"/flights/detail/{flight_id}", status_code=303)
