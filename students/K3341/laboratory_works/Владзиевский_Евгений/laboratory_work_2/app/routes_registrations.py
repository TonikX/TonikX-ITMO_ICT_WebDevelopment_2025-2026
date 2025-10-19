from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db import engine
from app.models import Registration, Conference, Role
from app.schemas import RegistrationCreate, RegistrationUpdate
from app.auth import get_current_user, require_admin

router = APIRouter()

@router.post('/registrations', status_code=201)
def create_registration(payload: RegistrationCreate, current_user = Depends(get_current_user)):
    with Session(engine) as session:
        conf = session.get(Conference, payload.conference_id)
        if not conf:
            raise HTTPException(status_code=404, detail='Conference not found')
        reg = Registration(user_id=current_user.id, conference_id=payload.conference_id, title=payload.title, abstract=payload.abstract)
        session.add(reg)
        session.commit()
        session.refresh(reg)
        return {"id": reg.id, "created_at": reg.created_at}

@router.patch('/registrations/{reg_id}')
def update_registration(reg_id: int, payload: RegistrationUpdate, current_user = Depends(get_current_user)):
    with Session(engine) as session:
        reg = session.get(Registration, reg_id)
        if not reg:
            raise HTTPException(status_code=404, detail='Registration not found')
        if reg.user_id != current_user.id:
            raise HTTPException(status_code=403, detail='Can edit only your own registrations')
        if payload.title is not None:
            reg.title = payload.title
        if payload.abstract is not None:
            reg.abstract = payload.abstract
        session.add(reg)
        session.commit()
        session.refresh(reg)
        return {"id": reg.id}

@router.delete('/registrations/{reg_id}', status_code=204)
def delete_registration(reg_id: int, current_user = Depends(get_current_user)):
    with Session(engine) as session:
        reg = session.get(Registration, reg_id)
        if not reg:
            raise HTTPException(status_code=404, detail='Registration not found')
        if reg.user_id != current_user.id and current_user.role != Role.admin:
            raise HTTPException(status_code=403, detail='Can delete only your own registrations')
        session.delete(reg)
        session.commit()
        return {}

@router.post('/registrations/{reg_id}/result')
def set_registration_result(reg_id: int, payload: dict, admin = Depends(require_admin)):
    with Session(engine) as session:
        reg = session.get(Registration, reg_id)
        if not reg:
            raise HTTPException(status_code=404, detail='Registration not found')
        reg.status = payload.get('status')
        session.add(reg)
        session.commit()
        session.refresh(reg)
        return {"id": reg.id, "status": reg.status}
