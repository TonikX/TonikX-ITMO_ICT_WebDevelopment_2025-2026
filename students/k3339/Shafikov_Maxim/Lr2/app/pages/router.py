from fastapi import APIRouter, Request, Depends, Query, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import datetime

from app.db.base import get_db
from app.db import models
from app.db.models import Hotel, Room
from app.crud.hotels import hotel_repo
from app.crud.reviews import review_repo
from app.crud.bookings import booking_repo
from app.schemas.reviews import ReviewCreate
from app.auth.deps import get_current_user_from_cookie, get_current_active_user, get_current_active_admin_user

router = APIRouter(tags=["Pages"])
templates = Jinja2Templates(directory="app/templates")


def require_admin(request: Request):
    user = getattr(request.state, "user", None)
    if not user or not getattr(user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Admins only")
    return user


@router.get("/admin/hotels/new", response_class=HTMLResponse)
def new_hotel_page(
    request: Request,
    _=Depends(require_admin)
):
    return templates.TemplateResponse("admin_new_hotel.html", {"request": request})


@router.post("/admin/hotels/new")
def create_hotel(
    request: Request,
    name: str = Form(...),
    owner: str = Form(...),
    address: str = Form(...),
    description: str = Form(""),
    amenities: str = Form(""),
    room_types: str = Form(""),
    price: float = Form(None),
    capacity: int = Form(None),
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    hotel = Hotel(
        name=name,
        owner=owner,
        address=address,
        description=description,
    )
    db.add(hotel)
    db.flush()

    if price is not None and capacity is not None:
        room = Room(
            hotel_id=hotel.id,
            room_type=(room_types or "Стандарт"),
            price=price,
            capacity=capacity,
            amenities=amenities,
        )
        db.add(room)

    db.commit()

    return RedirectResponse(url="/admin/bookings", status_code=303)


@router.post("/admin/hotels")
def admin_create_hotel(
    request: Request,
    name: str = Form(...),
    address: str = Form(...),
    owner: str = Form(""),
    description: str = Form(""),
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    hotel = Hotel(name=name.strip(), address=address.strip(), owner=owner.strip(), description=description.strip())
    db.add(hotel)
    db.commit()
    db.refresh(hotel)
    return RedirectResponse(url="/admin/hotels", status_code=303)


@router.get("/", response_class=HTMLResponse)
async def get_main_page(
        request: Request,
        db: Session = Depends(get_db),
        page: int = 1,
        sort: str = Query("rating", enum=["rating", "price_asc", "price_desc"]),
        min_price: str = Query(None),
        max_price: str = Query(None)
):
    min_price_float = None
    max_price_float = None
    
    if min_price and min_price.strip():
        try:
            min_price_float = float(min_price)
        except ValueError:
            min_price_float = None
    
    if max_price and max_price.strip():
        try:
            max_price_float = float(max_price)
        except ValueError:
            max_price_float = None
    
    per_page = 5
    hotels_with_stats, total_pages = hotel_repo.get_paginated(
        db=db,
        page=page,
        per_page=per_page,
        sort=sort,
        min_price=min_price_float,
        max_price=max_price_float,
    )
    return templates.TemplateResponse("index.html", {
        "request": request,
        "hotels": hotels_with_stats,
        "page": page,
        "total_pages": total_pages,
        "sort": sort,
        "min_price": min_price,
        "max_price": max_price,
    })


@router.get("/hotel/{hotel_id}", response_class=HTMLResponse)
async def get_hotel_page(
        request: Request,
        hotel_id: int,
        db: Session = Depends(get_db),
        reviews_page: int = 1,
        guests_page: int = 1
):
    hotel = hotel_repo.get_by_id(db, hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Отель не найден")

    per_page = 5
    reviews, total_reviews_pages = review_repo.get_by_hotel_paginated(db, hotel_id, reviews_page, per_page)

    guests_data = None
    total_guests_pages = 0
    current_user = request.state.user
    if current_user and current_user.is_admin:
        guests_data, total_guests_pages = booking_repo.get_guests_for_last_month(
            db, hotel_id, guests_page, per_page
        )

    return templates.TemplateResponse("hotel_detail.html", {
        "request": request,
        "hotel": hotel,
        "reviews": reviews,
        "reviews_page": reviews_page,
        "total_reviews_pages": total_reviews_pages,
        "guests_data": guests_data,
        "guests_page": guests_page,
        "total_guests_pages": total_guests_pages
    })


@router.post("/hotel/{hotel_id}/review")
async def add_review(
        hotel_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),
        rating: int = Form(),
        text: str = Form(),
        stay_start: datetime.date = Form(),
        stay_end: datetime.date = Form()
):
    today = datetime.date.today()
    
    if stay_start >= stay_end:
        return RedirectResponse(url=f"/hotel/{hotel_id}?error=invalid_dates", status_code=status.HTTP_302_FOUND)
    
    if stay_end > today:
        return RedirectResponse(url=f"/hotel/{hotel_id}?error=future_stay", status_code=status.HTTP_302_FOUND)
    
    review_in = ReviewCreate(
        rating=rating,
        text=text,
        stay_period_start=stay_start,
        stay_period_end=stay_end
    )
    review_repo.create(db, review=review_in, hotel_id=hotel_id, user_id=current_user.id)
    return RedirectResponse(url=f"/hotel/{hotel_id}", status_code=status.HTTP_302_FOUND)


@router.get("/cabinet", response_class=HTMLResponse)
async def get_cabinet(
        request: Request,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),
        page: int = 1
):
    per_page = 5
    bookings, total_pages = booking_repo.get_by_user_paginated(db, current_user.id, page, per_page)
    today = datetime.date.today()
    return templates.TemplateResponse("cabinet.html", {
        "request": request,
        "bookings": bookings,
        "page": page,
        "total_pages": total_pages,
        "today": today
    })


@router.get("/admin/bookings", response_class=HTMLResponse)
async def get_admin_bookings_page(
        request: Request,
        db: Session = Depends(get_db),
        current_admin: models.User = Depends(get_current_active_admin_user),
        page: int = 1
):
    per_page = 5
    pending_bookings, total_pages = booking_repo.get_pending_paginated(db, page, per_page)
    return templates.TemplateResponse("admin_bookings.html", {
        "request": request,
        "bookings": pending_bookings,
        "page": page,
        "total_pages": total_pages,
    })