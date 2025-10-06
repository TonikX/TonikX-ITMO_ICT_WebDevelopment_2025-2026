from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.db import models
from app.schemas import reviews as review_schemas
import math


class ReviewRepository:
    def create(self, db: Session, review: review_schemas.ReviewCreate, hotel_id: int, user_id: int):
        db_review = models.Review(
            **review.model_dump(),
            hotel_id=hotel_id,
            user_id=user_id
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review

    def get_by_hotel_paginated(self, db: Session, hotel_id: int, page: int, per_page: int):
        offset = (page - 1) * per_page

        query = db.query(models.Review).filter(models.Review.hotel_id == hotel_id)
        total_reviews = query.count()
        total_pages = math.ceil(total_reviews / per_page)

        reviews = query.order_by(desc(models.Review.id)).offset(offset).limit(per_page).all()
        return reviews, total_pages


review_repo = ReviewRepository()
