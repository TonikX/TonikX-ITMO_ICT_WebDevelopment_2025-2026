from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..connection import get_session
from ..models import Project, ProjectDefault, User
from ..schemas import ProjectRead, ProjectWithTeams
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=List[ProjectRead])
def list_projects(session=Depends(get_session)):
    return session.exec(select(Project)).all()


@router.get("/{project_id}", response_model=ProjectWithTeams)
def get_project(project_id: int, session=Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    return project


@router.post("", response_model=ProjectRead, status_code=201)
def create_project(
    data: ProjectDefault,
    current: User = Depends(get_current_user),
    session=Depends(get_session),
):
    project = Project(**data.model_dump(), owner_id=current.id)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int,
    data: ProjectDefault,
    current: User = Depends(get_current_user),
    session=Depends(get_session),
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    if project.owner_id != current.id:
        raise HTTPException(403, "Forbidden")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(project, k, v)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    current: User = Depends(get_current_user),
    session=Depends(get_session),
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    if project.owner_id != current.id:
        raise HTTPException(403, "Forbidden")
    session.delete(project)
    session.commit()
    return {"ok": True}
