from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import String, cast, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.database import get_session
from src.models.flight import Flight
from src.models.reservation import Reservation
from sqlalchemy import select, func

from src.models.seat import Seat

from src.tools import get_user_from_token
from src.models.review import Review
from src.models.airlane import Airlane

templates = Jinja2Templates(directory="src/templates")
router = APIRouter(prefix="/flights", tags=["Flights"])


def seat_sort_key(seat):
    num = int(''.join(filter(str.isdigit, seat.seat_number)))
    letter = ''.join(filter(str.isalpha, seat.seat_number))
    return (num, letter)


@router.get("/detail/{flight_id}", response_class=HTMLResponse)
async def flight_by_id(
    flight_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    user = await get_user_from_token(request, session)

    result = await session.execute(
        select(Flight)
        .where(Flight.id_flight == flight_id)
        .options(
            selectinload(Flight.airline),
            selectinload(Flight.reviews),
            selectinload(Flight.seats).selectinload(Seat.reservation).selectinload(Reservation.user),
        )
    )

    flight = result.scalars().first()
    if not flight:
        raise HTTPException(status_code=404, detail="Рейс не найден")

    all_reserved_seat_ids = {seat.id_seat for seat in flight.seats if seat.reservation}
    flight_users = {seat.reservation.user for seat in flight.seats if seat.reservation}

    if user:
        user_reserved_seats = sorted(
            [seat for seat in flight.seats if seat.reservation and seat.reservation.user == user],
            key=seat_sort_key,
        )
    else:
        user_reserved_seats = []

    return templates.TemplateResponse(
        "flight/flight_detailed.html",
        {
            "request": request,
            "flight": flight,
            "reserved_seat_ids": all_reserved_seat_ids,
            "user": user,
            "flight_users": flight_users,
            "user_reserved_seats": user_reserved_seats,
            "reviews": flight.reviews,
        },
    )


@router.get("", response_class=HTMLResponse)
async def flights(
    request: Request,
    session: AsyncSession = Depends(get_session),
    page: int = 1,
    type: str | None = None,
    per_page: int = 10,
    search: str | None = None,
):
    user = await get_user_from_token(request, session)

    base_query = (
        select(Flight).options(selectinload(Flight.airline)).join(Airlane, Flight.airline_id == Airlane.id_airline)
    )

    # фильтр по типу рейса
    if type == "departures":
        base_query = base_query.filter(Flight.flight_type == "departure")
    elif type == "arrivals":
        base_query = base_query.filter(Flight.flight_type == "arrival")

    # простой поиск
    if search:
        like_pattern = f"%{search.lower()}%"
        base_query = base_query.filter(
            or_(
                func.lower(Flight.flight_number).like(like_pattern),
                func.lower(Flight.destination).like(like_pattern),
                func.lower(Airlane.name).like(like_pattern),
            )
        )

    # считаем общее количество строк
    count_query = select(func.count()).select_from(base_query.subquery())
    total = (await session.execute(count_query)).scalar_one()

    # пагинация
    offset = (page - 1) * per_page
    query = base_query.limit(per_page).offset(offset)

    result = await session.execute(query)
    flights = result.scalars().all()

    total_pages = (total + per_page - 1) // per_page

    return templates.TemplateResponse(
        "flight/flights.html",
        {
            "request": request,
            "flights": flights,
            "filter_type": type or "all",
            "user": user,
            "page": page,
            "total_pages": total_pages,
            "search": search or "",
        },
    )
