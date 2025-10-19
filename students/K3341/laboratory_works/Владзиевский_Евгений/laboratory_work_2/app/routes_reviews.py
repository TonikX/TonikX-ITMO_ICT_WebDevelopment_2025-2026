from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import Session, select
from app.db import engine
from app.models import Review, Conference, User
from app.schemas import ReviewCreate
from app.auth import get_current_user

router = APIRouter()

@router.post('/reviews', status_code=201)
def create_review(payload: ReviewCreate, current_user = Depends(get_current_user)):
    with Session(engine) as session:
        conf = session.get(Conference, payload.conference_id)
        if not conf:
            raise HTTPException(status_code=404, detail='Conference not found')
        review = Review(conference_id=payload.conference_id, user_id=current_user.id, text=payload.text, rating=payload.rating)
        session.add(review)
        session.commit()
        session.refresh(review)
        return {"id": review.id, "created_at": review.created_at}

@router.get('/conferences/{conf_id}/reviews')
def list_reviews(conf_id: int, limit: int = Query(50, ge=1, le=500), offset: int = Query(0, ge=0)):
    with Session(engine) as session:
        q = select(Review).where(Review.conference_id == conf_id).offset(offset).limit(limit)
        items = session.exec(q).all()
        out = []
        for r in items:
            user = session.get(User, r.user_id)
            out.append({
                "id": r.id,
                "conference_dates": {"start_date": r.conference.start_date, "end_date": r.conference.end_date} if r.conference else None,
                "text": r.text,
                "rating": r.rating,
                "commentator": {"id": user.id, "username": user.username, "display_name": user.display_name} if user else None,
                "created_at": r.created_at,
            })
        return out
