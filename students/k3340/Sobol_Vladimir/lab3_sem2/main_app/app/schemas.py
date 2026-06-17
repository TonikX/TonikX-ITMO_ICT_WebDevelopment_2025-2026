from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel
from .models import (
    UserDefault, ProfileDefault, SkillDefault, ProjectDefault, TeamDefault,
    ExperienceLevel, TeamRole,
)


class UserCreate(UserDefault):
    password: str


class UserRead(UserDefault):
    id: int


class PasswordChange(SQLModel):
    old_password: str
    new_password: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(SQLModel):
    username: str
    password: str


class SkillRead(SkillDefault):
    id: int


class ProfileRead(ProfileDefault):
    id: int
    user_id: int


class ProfileWithSkills(ProfileRead):
    skills: List[SkillRead] = []
    user: Optional[UserRead] = None


class AttachSkill(SQLModel):
    skill_id: int
    level: ExperienceLevel = ExperienceLevel.junior


class ProjectRead(ProjectDefault):
    id: int
    owner_id: int


class TeamRead(TeamDefault):
    id: int
    project_id: int


class TeamWithMembers(TeamRead):
    members: List[UserRead] = []


class ProjectWithTeams(ProjectRead):
    owner: Optional[UserRead] = None
    teams: List[TeamRead] = []


class AddTeamMember(SQLModel):
    user_id: int
    role: TeamRole = TeamRole.member


# ---------------- Parser ----------------
class ParseRequest(SQLModel):
    url: str


class ParsedPageRead(SQLModel):
    id: int
    url: str
    title: str
    source: str
    fetched_at: datetime
