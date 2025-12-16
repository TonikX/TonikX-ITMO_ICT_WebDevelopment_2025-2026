# API for warriors
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from main import Warrior, Skill, Profession, get_session

router = APIRouter(prefix="/api", tags=["warriors"])


# Pydantic
class WarriorCreate(BaseModel):
    race: str
    name: str
    level: int = 0
    profession_id: int | None = None


class ProfessionRead(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True


class WarriorRead(BaseModel):
    id: int
    race: str
    name: str
    level: int
    profession: ProfessionRead | None

    class Config:
        from_attributes = True


# Схемы для скилов
class SkillCreate(BaseModel):
    title: str


class SkillRead(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


# Схемы для профессий
class ProfessionCreate(BaseModel):
    title: str
    description: str | None = None


# Ручки для воинов
@router.get("/warriors", response_model=list[WarriorRead])
async def list_warriors(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Warrior))
    return result.scalars().all()


@router.get("/warriors/{warrior_id}", response_model=WarriorRead)
async def get_warrior(warrior_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Warrior).where(Warrior.id == warrior_id)
    )
    warrior = result.scalar_one_or_none()
    if warrior is None:
        raise HTTPException(status_code=404, detail="Warrior not found")
    return warrior


@router.post("/warriors", response_model=WarriorRead, status_code=201)
async def create_warrior(data: WarriorCreate, session: AsyncSession = Depends(get_session)):
    warrior = Warrior(
        race=data.race,
        name=data.name,
        level=data.level,
        profession_id=data.profession_id,
    )
    session.add(warrior)
    await session.commit()
    await session.refresh(warrior)
    return warrior


@router.put("/warriors/{warrior_id}", response_model=WarriorRead)
async def update_warrior(warrior_id: int, data: WarriorCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Warrior).where(Warrior.id == warrior_id)
    )
    warrior = result.scalar_one_or_none()
    if warrior is None:
        raise HTTPException(status_code=404, detail="Warrior not found")

    setattr(warrior, "race", data.race)
    setattr(warrior, "name", data.name)
    setattr(warrior, "level", data.level)
    setattr(warrior, "profession_id", data.profession_id)

    session.add(warrior)
    await session.commit()
    await session.refresh(warrior)
    return warrior


@router.delete("/warriors/{warrior_id}", status_code=204)
async def delete_warrior(warrior_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Warrior).where(Warrior.id == warrior_id)
    )
    warrior = result.scalar_one_or_none()
    if warrior is None:
        raise HTTPException(status_code=404, detail="Warrior not found")

    await session.delete(warrior)
    await session.commit()
    return {"detail": "Warrior deleted successfully"}


@router.get("/warriors-with-professions", response_model=list[WarriorRead])
async def list_warriors_with_professions(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Warrior).options(joinedload(Warrior.profession))
    )
    warriors = result.scalars().all()
    return warriors


@router.get("/warriors/{warrior_id}/details", response_model=WarriorRead)
async def get_warrior_details(warrior_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Warrior)
        .options(
            joinedload(Warrior.profession),
            joinedload(Warrior.skills)
        )
        .where(Warrior.id == warrior_id)
    )
    warrior = result.unique().scalar_one_or_none()
    if warrior is None:
        raise HTTPException(status_code=404, detail="Warrior not found")
    return warrior


# Ручки для скилов
@router.get("/skills", response_model=list[SkillRead])
async def list_skills(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Skill))
    return result.scalars().all()


@router.post("/skills", response_model=SkillRead, status_code=201)
async def create_skill(data: SkillCreate, session: AsyncSession = Depends(get_session)):
    skill = Skill(title=data.title)
    session.add(skill)
    await session.commit()
    await session.refresh(skill)
    return skill


# Ручки для профессий
@router.get("/professions", response_model=list[ProfessionRead])
async def list_professions(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Profession))
    return result.scalars().all()


@router.post("/professions", response_model=ProfessionRead, status_code=201)
async def create_profession(data: ProfessionCreate, session: AsyncSession = Depends(get_session)):
    profession = Profession(
        title=data.title,
        description=data.description,
    )
    session.add(profession)
    await session.commit()
    await session.refresh(profession)
    return profession