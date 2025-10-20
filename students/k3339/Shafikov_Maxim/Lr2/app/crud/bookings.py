from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from app.db import models
from app.schemas import bookings as booking_schemas
import math
from datetime import date, timedelta


class BookingRepository:
    def create(self, db: Session, booking: booking_schemas.BookingCreate, user_id: int):
        db_booking = models.Booking(**booking.model_dump(), user_id=user_id, status=models.BookingStatus.pending)
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking

    def get_by_user_paginated(self, db: Session, user_id: int, page: int, per_page: int):
        offset = (page - 1) * per_page
        query = db.query(models.Booking).filter(models.Booking.user_id == user_id)
        total = query.count()
        total_pages = math.ceil(total / per_page)
        bookings = query.order_by(desc(models.Booking.check_in_date)).offset(offset).limit(per_page).all()
        return bookings, total_pages

    def get_by_id(self, db: Session, booking_id: int):
        return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

    def update_status(self, db: Session, booking_id: int, status: models.BookingStatus):
        booking = self.get_by_id(db, booking_id)
        if booking:
            booking.status = status
            db.commit()
            db.refresh(booking)
        return booking

    def get_pending_paginated(self, db: Session, page: int, per_page: int):
        offset = (page - 1) * per_page
        query = db.query(models.Booking).filter(models.Booking.status == models.BookingStatus.pending)
        total = query.count()
        total_pages = math.ceil(total / per_page)
        bookings = query.order_by(models.Booking.id).offset(offset).limit(per_page).all()
        return bookings, total_pages

    def get_guests_for_last_month(self, db: Session, hotel_id: int, page: int, per_page: int):
        last_month = date.today() - timedelta(days=30)
        offset = (page - 1) * per_page

        room_ids = db.query(models.Room.id).filter(models.Room.hotel_id == hotel_id).subquery()

        query = db.query(models.Booking).join(models.User).filter(
            models.Booking.room_id.in_(room_ids),
            models.Booking.status.in_(
                [models.BookingStatus.confirmed, models.BookingStatus.checked_in, models.BookingStatus.checked_out]),
            or_(
                models.Booking.check_in_date >= last_month,
                models.Booking.check_out_date >= last_month
            )
        )

        total = query.count()
        total_pages = math.ceil(total / per_page)

        guests = query.order_by(desc(models.Booking.check_in_date)).offset(offset).limit(per_page).all()

        guest_data = []
        for booking in guests:
            review = db.query(models.Review.rating).filter(
                and_(
                    models.Review.user_id == booking.user_id,
                    models.Review.hotel_id == hotel_id
                )
            ).first()
            guest_data.append({
                "booking": booking,
                "rating": review.rating if review else "N/A"
            })

        return guest_data, total_pages


booking_repo = BookingRepository()
