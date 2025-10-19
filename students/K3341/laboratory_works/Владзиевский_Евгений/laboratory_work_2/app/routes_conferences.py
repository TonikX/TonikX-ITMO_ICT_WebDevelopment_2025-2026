from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from datetime import date
from sqlmodel import Session, select
from app.db import engine
from app.schemas import ConferenceCreate, ConferenceRead
from app.models import Conference, Topic, ConferenceTopicLink
from app.auth import get_current_user

router = APIRouter()

@router.post('/conferences', status_code=201)
def create_conference(payload: ConferenceCreate, user = Depends(get_current_user)):
    # only admin may create conferences
    if not user or getattr(user, 'role', None) != 'admin':
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail='Only admin may create conferences')
    with Session(engine) as session:
        conf = Conference(
            title=payload.title,
            description=payload.description,
            location_name=payload.location_name,
            location_description=payload.location_description,
            start_date=payload.start_date,
            end_date=payload.end_date,
            conditions=payload.conditions,
        )
        # ensure topics exist or create them
        topic_objs: List[Topic] = []
        for tname in payload.topics:
            t = session.exec(select(Topic).where(Topic.name == tname)).first()
            if not t:
                t = Topic(name=tname)
                session.add(t)
                session.flush()
            topic_objs.append(t)

        conf.topics = topic_objs
        session.add(conf)
        session.commit()
        session.refresh(conf)
        return {"id": conf.id}

@router.get('/conferences', response_model=List[ConferenceRead])
def list_conferences(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    topic: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    search: Optional[str] = Query(None),
):
    with Session(engine) as session:
        q = select(Conference)
        if topic:
            q = q.join(ConferenceTopicLink).join(Topic).where(Topic.name == topic)
        if location:
            q = q.where(Conference.location_name.contains(location))
        if date_from:
            q = q.where(Conference.end_date >= date_from)
        if date_to:
            q = q.where(Conference.start_date <= date_to)
        if search:
            q = q.where((Conference.title.contains(search)) | (Conference.description.contains(search)))
        q = q.offset(offset).limit(limit)
        results = session.exec(q).all()

        out: List[ConferenceRead] = []
        for conf in results:
            topics = [t.name for t in conf.topics]
            out.append(ConferenceRead(id=conf.id, title=conf.title, start_date=conf.start_date, end_date=conf.end_date, location_name=conf.location_name, topics=topics))
        return out

@router.get('/conferences/{conf_id}')
def get_conference(conf_id: int):
    with Session(engine) as session:
        conf = session.get(Conference, conf_id)
        if not conf:
            raise HTTPException(status_code=404, detail='Conference not found')
        return conf
