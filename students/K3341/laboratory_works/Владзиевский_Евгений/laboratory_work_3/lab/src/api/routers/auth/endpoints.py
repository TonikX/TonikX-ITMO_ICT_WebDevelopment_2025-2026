from datetime import timedelta

from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routers.auth import models
from src.api.routers.auth.utils import get_hash_password, verify_password
from src.api.security import access_policy, refresh_policy
from src.api.sessions import get_db_session
from src.db import crud

router = APIRouter(
    tags=["auth"],
)


@router.post("/register", response_model=models.TokenResponse)
async def register(user: models.UserCreate, session: AsyncSession = Depends(get_db_session)):
    res = await crud.get_user_by_login(session, user.login)
    if res:
        raise HTTPException(status_code=400, detail="Login already registered")
    hashed_password = get_hash_password(user.password)
    res = await crud.add_user(session, user.login, user.name, hashed_password)
    subject = {"login": user.login, "name": user.name, "id": res.id}
    access_token = access_policy.create_access_token(subject=subject)
    refresh_token = refresh_policy.create_refresh_token(subject=subject)

    return {"user_id":res.id, "access_token": access_token, "refresh_token": refresh_token}


@router.post("/login", response_model=models.TokenResponse)
async def login(user: models.UserLogin, session: AsyncSession = Depends(get_db_session)):
    res = await crud.get_user_by_login(session, user.login)
    if res:
        if verify_password(user.password, res.password):
            subject = {"login": res.login, "name": res.name, "id": res.id}
            access_token = access_policy.create_access_token(subject=subject)
            refresh_token = refresh_policy.create_refresh_token(subject=subject)
            return {"user_id": res.id, "access_token": access_token, "refresh_token": refresh_token}
    raise HTTPException(status_code=400, detail="Incorrect login or password")


@router.post("/refresh", response_model=models.TokenResponse)
def refresh(credentials: JwtAuthorizationCredentials = Security(refresh_policy)):
    access_token = access_policy.create_access_token(subject=credentials.subject)
    refresh_token = refresh_policy.create_refresh_token(subject=credentials.subject, expires_delta=timedelta(days=2))

    return {"user_id": credentials.subject['id'], "access_token": access_token, "refresh_token": refresh_token}
