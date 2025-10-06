from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import datetime

from app.db.base import get_db
from app.db import models
from app.schemas import bookings as booking_schemas
from app.crud.bookings import booking_repo
from app.auth.deps import get_current_active_user, get_current_active_admin_user

router = APIRouter(tags=["Bookings"])


@router.post("/book")
async def create_booking(
        room_id: int = Form(),
        check_in_date: datetime.date = Form(),
        check_out_date: datetime.date = Form(),
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user)
):
    today = datetime.date.today()
    
    if check_in_date >= check_out_date:
        return RedirectResponse(url=f"/?error=invalid_dates", status_code=status.HTTP_302_FOUND)
    
    if check_in_date < today:
        return RedirectResponse(url=f"/?error=past_checkin", status_code=status.HTTP_302_FOUND)

    booking_in = booking_schemas.BookingCreate(
        room_id=room_id,
        check_in_date=check_in_date,
        check_out_date=check_out_date
    )
    booking_repo.create(db, booking=booking_in, user_id=current_user.id)
    return RedirectResponse(url="/cabinet", status_code=status.HTTP_302_FOUND)


@router.post("/bookings/{booking_id}/cancel")
async def cancel_booking(
        booking_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user)
):
    booking = booking_repo.get_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")

    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    if booking.check_in_date <= datetime.date.today():
        return RedirectResponse(url="/cabinet?error=cancel_forbidden", status_code=status.HTTP_302_FOUND)

    booking_repo.update_status(db, booking_id, models.BookingStatus.cancelled)
    return RedirectResponse(url="/cabinet", status_code=status.HTTP_302_FOUND)


@router.post("/admin/bookings/{booking_id}/confirm")
async def confirm_booking_admin(
        booking_id: int,
        db: Session = Depends(get_db),
        current_admin: models.User = Depends(get_current_active_admin_user)
):
    booking_repo.update_status(db, booking_id, models.BookingStatus.confirmed)
    return RedirectResponse(url="/admin/bookings", status_code=status.HTTP_302_FOUND)


@router.post("/admin/bookings/{booking_id}/reject")
async def reject_booking_admin(
        booking_id: int,
        db: Session = Depends(get_db),
        current_admin: models.User = Depends(get_current_active_admin_user)
):
    booking_repo.update_status(db, booking_id, models.BookingStatus.cancelled)
    return RedirectResponse(url="/admin/bookings", status_code=status.HTTP_302_FOUND)