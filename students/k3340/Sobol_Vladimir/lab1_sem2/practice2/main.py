from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select
from typing_extensions import TypedDict

from connection import init_db, get_session
from models import (
    Profile, ProfileDefault, ProfileWithProfession, ProfileWithAll,
    Profession, ProfessionDefault,
    Skill, SkillDefault,
    ProfileSkillLink, ExperienceLevel,
)

app = FastAPI(title="Partner Finder — practice 2")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


# ---------------- Profiles ----------------
@app.get("/profiles_list")
def profiles_list(session=Depends(get_session)) -> List[Profile]:
    return session.exec(select(Profile)).all()


@app.get("/profile/{profile_id}", response_model=ProfileWithAll)
def profile_get(profile_id: int, session=Depends(get_session)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(404, "Profile not found")
    return profile


@app.post("/profile")
def profile_create(
    profile: ProfileDefault, session=Depends(get_session)
) -> TypedDict("Response", {"status": int, "data": Profile}):
    obj = Profile.model_validate(profile)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return {"status": 200, "data": obj}


@app.patch("/profile/{profile_id}", response_model=ProfileWithProfession)
def profile_update(profile_id: int, profile: ProfileDefault, session=Depends(get_session)):
    db_obj = session.get(Profile, profile_id)
    if not db_obj:
        raise HTTPException(404, "Profile not found")
    for k, v in profile.model_dump(exclude_unset=True).items():
        setattr(db_obj, k, v)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


@app.delete("/profile/{profile_id}")
def profile_delete(profile_id: int, session=Depends(get_session)):
    obj = session.get(Profile, profile_id)
    if not obj:
        raise HTTPException(404, "Profile not found")
    session.delete(obj)
    session.commit()
    return {"ok": True}


# ---------------- Professions ----------------
@app.get("/professions_list")
def professions_list(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()


@app.get("/profession/{profession_id}")
def profession_get(profession_id: int, session=Depends(get_session)) -> Profession:
    obj = session.get(Profession, profession_id)
    if not obj:
        raise HTTPException(404, "Profession not found")
    return obj


@app.post("/profession")
def profession_create(
    prof: ProfessionDefault, session=Depends(get_session)
) -> TypedDict("Response", {"status": int, "data": Profession}):
    obj = Profession.model_validate(prof)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return {"status": 200, "data": obj}


# ---------------- Skills ----------------
@app.get("/skills_list")
def skills_list(session=Depends(get_session)) -> List[Skill]:
    return session.exec(select(Skill)).all()


@app.post("/skill")
def skill_create(
    skill: SkillDefault, session=Depends(get_session)
) -> TypedDict("Response", {"status": int, "data": Skill}):
    obj = Skill.model_validate(skill)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return {"status": 200, "data": obj}


@app.delete("/skill/{skill_id}")
def skill_delete(skill_id: int, session=Depends(get_session)):
    obj = session.get(Skill, skill_id)
    if not obj:
        raise HTTPException(404, "Skill not found")
    session.delete(obj)
    session.commit()
    return {"ok": True}


# ---------------- M2M: прикрепить навык к профилю ----------------
@app.post("/profile/{profile_id}/skill/{skill_id}")
def attach_skill(
    profile_id: int,
    skill_id: int,
    level: ExperienceLevel = ExperienceLevel.junior,
    session=Depends(get_session),
):
    if not session.get(Profile, profile_id) or not session.get(Skill, skill_id):
        raise HTTPException(404, "Profile or skill not found")
    link = ProfileSkillLink(profile_id=profile_id, skill_id=skill_id, level=level)
    session.add(link)
    session.commit()
    return {"ok": True, "link": link}
