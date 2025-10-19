from fastapi import APIRouter, Query
from typing import Optional, List
from sqlmodel import Session, select
from app.db import engine
from app.models import Registration, User, Conference

router = APIRouter()

@router.get('/participants')
def participants_table(conference_id: Optional[int] = Query(None), limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    with Session(engine) as session:
        q = select(Registration)
        if conference_id:
            q = q.where(Registration.conference_id == conference_id)
        q = q.offset(offset).limit(limit)
        regs = session.exec(q).all()
        out = []
        for r in regs:
            user = session.get(User, r.user_id)
            conf = session.get(Conference, r.conference_id)
            out.append({
                "registration_id": r.id,
                "conference": {"id": conf.id, "title": conf.title} if conf else None,
                "user": {"id": user.id, "username": user.username, "display_name": user.display_name} if user else None,
                "title": r.title,
                "status": r.status,
                "created_at": r.created_at,
            })
        return out
