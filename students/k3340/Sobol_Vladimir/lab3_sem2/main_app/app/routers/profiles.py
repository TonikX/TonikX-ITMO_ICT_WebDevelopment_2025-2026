from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..connection import get_session
from ..models import Profile, ProfileDefault, Skill, ProfileSkillLink, User
from ..schemas import ProfileRead, ProfileWithSkills, AttachSkill
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post("", response_model=ProfileRead, status_code=201)
def create_profile(
    data: ProfileDefault,
    current: User = Depends(get_current_user),
    session=Depends(get_session),
):
    if session.exec(select(Profile).where(Profile.user_id == current.id)).first():
        raise HTTPException(400, "Profile already exists")
    profile = Profile(**data.model_dump(), user_id=current.id)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.get("", response_model=List[ProfileRead])
def list_profiles(session=Depends(get_session)):
    return session.exec(select(Profile)).all()


@router.get("/{profile_id}", response_model=ProfileWithSkills)
def get_profile(profile_id: int, session=Depends(get_session)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(404, "Profile not found")
    return profile


@router.patch("/{profile_id}", response_model=ProfileRead)
def update_profile(
    profile_id: int,
    data: ProfileDefault,
    current: User = Depends(get_current_user),
    session=Depends(get_session),
):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(404, "Profile not found")
    if profile.user_id != current.id:
        raise HTTPException(403, "Forbidden")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(profile, k, v)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.post("/{profile_id}/skills")
def attach_skill(
    profile_id: int,
    payload: AttachSkill,
    current: User = Depends(get_current_user),
    session=Depends(get_session),
):
    profile = session.get(Profile, profile_id)
    if not profile or profile.user_id != current.id:
        raise HTTPException(404, "Profile not found or not yours")
    if not session.get(Skill, payload.skill_id):
        raise HTTPException(404, "Skill not found")
    link = ProfileSkillLink(
        profile_id=profile_id, skill_id=payload.skill_id, level=payload.level
    )
    session.add(link)
    session.commit()
    return {"ok": True, "link": link}
