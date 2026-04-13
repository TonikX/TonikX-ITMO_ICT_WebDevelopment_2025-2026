from enum import Enum
from typing import Optional, List
from pydantic import BaseModel


class ExperienceLevel(str, Enum):
    junior = "junior"
    middle = "middle"
    senior = "senior"


class Skill(BaseModel):
    id: int
    name: str
    description: str


class Profession(BaseModel):
    id: int
    title: str
    description: str


class User(BaseModel):
    id: int
    username: str
    level: ExperienceLevel
    profession: Profession
    skills: Optional[List[Skill]] = []
