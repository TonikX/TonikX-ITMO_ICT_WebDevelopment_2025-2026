from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class ExperienceLevel(str, Enum):
    junior = "junior"
    middle = "middle"
    senior = "senior"


class ProfileSkillLink(SQLModel, table=True):
    profile_id: Optional[int] = Field(default=None, foreign_key="profile.id", primary_key=True)
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)
    level: ExperienceLevel = Field(default=ExperienceLevel.junior)


class ProfessionDefault(SQLModel):
    title: str
    description: Optional[str] = None


class Profession(ProfessionDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profiles: List["Profile"] = Relationship(back_populates="profession")


class SkillDefault(SQLModel):
    name: str
    description: Optional[str] = None


class Skill(SkillDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profiles: List["Profile"] = Relationship(back_populates="skills", link_model=ProfileSkillLink)


class ProfileDefault(SQLModel):
    username: str
    bio: Optional[str] = None
    level: ExperienceLevel = ExperienceLevel.junior
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")


class Profile(ProfileDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profession: Optional[Profession] = Relationship(back_populates="profiles")
    skills: List[Skill] = Relationship(back_populates="profiles", link_model=ProfileSkillLink)


class ProfileWithProfession(ProfileDefault):
    id: int
    profession: Optional[Profession] = None


class ProfileWithAll(ProfileDefault):
    id: int
    profession: Optional[Profession] = None
    skills: List[Skill] = []
