from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..connection import get_session
from ..models import Skill, SkillDefault
from ..schemas import SkillRead

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("", response_model=List[SkillRead])
def list_skills(session=Depends(get_session)):
    return session.exec(select(Skill)).all()


@router.post("", response_model=SkillRead, status_code=201)
def create_skill(data: SkillDefault, session=Depends(get_session)):
    skill = Skill.model_validate(data)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill


@router.delete("/{skill_id}")
def delete_skill(skill_id: int, session=Depends(get_session)):
    obj = session.get(Skill, skill_id)
    if not obj:
        raise HTTPException(404, "Skill not found")
    session.delete(obj)
    session.commit()
    return {"ok": True}
