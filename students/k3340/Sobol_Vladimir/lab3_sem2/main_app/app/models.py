from enum import Enum
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class ExperienceLevel(str, Enum):
    junior = "junior"
    middle = "middle"
    senior = "senior"


class TeamRole(str, Enum):
    owner = "owner"
    member = "member"
    mentor = "mentor"


# ---------------- Ассоциативные сущности с доп. полями ----------------
class ProfileSkillLink(SQLModel, table=True):
    profile_id: Optional[int] = Field(default=None, foreign_key="profile.id", primary_key=True)
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)
    level: ExperienceLevel = Field(default=ExperienceLevel.junior)


class TeamMemberLink(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    role: TeamRole = Field(default=TeamRole.member)
    joined_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------- User ----------------
class UserDefault(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)


class User(UserDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    profile: Optional["Profile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete", "uselist": False},
    )
    projects: List["Project"] = Relationship(back_populates="owner")
    teams: List["Team"] = Relationship(back_populates="members", link_model=TeamMemberLink)


# ---------------- Profile ----------------
class ProfileDefault(SQLModel):
    bio: Optional[str] = None
    experience_years: int = 0
    interests: Optional[str] = None


class Profile(ProfileDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)

    user: Optional[User] = Relationship(back_populates="profile")
    skills: List["Skill"] = Relationship(back_populates="profiles", link_model=ProfileSkillLink)


# ---------------- Skill ----------------
class SkillDefault(SQLModel):
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None


class Skill(SkillDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profiles: List[Profile] = Relationship(back_populates="skills", link_model=ProfileSkillLink)


# ---------------- Project ----------------
class ProjectDefault(SQLModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None


class Project(ProjectDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner: Optional[User] = Relationship(back_populates="projects")
    teams: List["Team"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )


# ---------------- Team ----------------
class TeamDefault(SQLModel):
    name: str
    description: Optional[str] = None


class Team(TeamDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")

    project: Optional[Project] = Relationship(back_populates="teams")
    members: List[User] = Relationship(back_populates="teams", link_model=TeamMemberLink)


# ---------------- Parser result (lab3) ----------------
class ParsedPage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(index=True)
    title: str
    source: str = Field(default="http")  # http | celery
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
