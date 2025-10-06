from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc, Float
from app.db import models
from app.db.models import Review, Room, Hotel


class HotelRepository:
    def get_paginated(
        self,
        db: Session,
        *,
        page: int = 1,
        per_page: int = 5,
        sort: str = "rating",
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ):
        q = (
            db.query(
                Hotel,
                func.min(Room.price).label("min_room_price"),
                func.avg(Review.rating.cast(Float)).label("avg_rating"),
            )
            .outerjoin(Room, Room.hotel_id == Hotel.id)
            .outerjoin(Review, Review.hotel_id == Hotel.id)
            .group_by(Hotel.id)
        )

        if min_price is not None:
            q = q.having(func.min(Room.price) >= min_price)
        if max_price is not None:
            q = q.having(func.min(Room.price) <= max_price)

        if sort == "rating":
            q = q.order_by(func.coalesce(func.avg(Review.rating), 0).desc())
        elif sort == "price_asc":
            q = q.order_by(func.coalesce(func.min(Room.price), 1e12).asc())
        elif sort == "price_desc":
            q = q.order_by(func.coalesce(func.min(Room.price), 0).desc())

        total = q.count()
        items = q.offset((page - 1) * per_page).limit(per_page).all()
        total_pages = max((total + per_page - 1) // per_page, 1)
        return items, total_pages

    def get_by_id(self, db: Session, hotel_id: int):
        return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()


hotel_repo = HotelRepository()
