from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..connection import get_session
from ..models import Team, TeamDefault, TeamMemberLink, Project, User
from ..schemas import TeamRead, TeamWithMembers, AddTeamMember
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/teams", tags=["teams"])


class _TeamCreatePayload(TeamDefault):
    project_id: int


@router.get("", response_model=List[TeamRead])
def list_teams(session=Depends(get_session)):
    return session.exec(select(Team)).all()


@router.get("/{team_id}", response_model=TeamWithMembers)
def get_team(team_id: int, session=Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(404, "Team not found")
    return team


@router.post("", response_model=TeamRead, status_code=201)
def create_team(
    data: _TeamCreatePayload,
    current: User = Depends(get_current_user),
    session=Depends(get_session),
):
    project = session.get(Project, data.project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    if project.owner_id != current.id:
        raise HTTPException(403, "Only project owner can create teams")
    team = Team.model_validate(data)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.post("/{team_id}/members")
def add_member(
    team_id: int,
    data: AddTeamMember,
    current: User = Depends(get_current_user),
    session=Depends(get_session),
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(404, "Team not found")
    project = session.get(Project, team.project_id)
    if project.owner_id != current.id:
        raise HTTPException(403, "Only project owner can add members")
    if not session.get(User, data.user_id):
        raise HTTPException(404, "User not found")
    link = TeamMemberLink(team_id=team_id, user_id=data.user_id, role=data.role)
    session.add(link)
    session.commit()
    return {"ok": True, "link": link}
