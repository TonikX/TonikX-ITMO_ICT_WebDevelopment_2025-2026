from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.auth import config, get_current_user, security
from src.auth.passcrypt import hash_password, verify_password
from src.database import get_session
from src.models.author import Author
from src.models.user import User
from src.schemas.auth import (
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    RegisterRequest,
    RegisterResponse,
    UpdateProfileRequest,
)
from src.schemas.user import UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=LoginResponse)
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    """Вход в систему с email и паролем, возвращает JWT токен"""
    query = await session.execute(select(User).where(User.email == data.email))
    result = query.scalars().first()

    if not result or not verify_password(data.password, result.password_hash):
        return JSONResponse(
            content={"error": "Неверный email или пароль"},
            status_code=401,
        )

    token = security.create_access_token(uid=str(result.id))

    response = JSONResponse(
        content={"message": "Login successful", "token": token},
        status_code=200,
    )
    expires_delta = timedelta(hours=3)
    expires_at = int((datetime.utcnow() + expires_delta).timestamp())
    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=int(expires_delta.total_seconds()),
        expires=expires_at,
        path="/",
    )
    return response


@router.post("/register", response_model=RegisterResponse)
async def register_post(
    data: RegisterRequest,
    session: AsyncSession = Depends(get_session),
):
    """Регистрация нового пользователя с автоматическим входом"""
    existing = await session.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    token = security.create_access_token(uid=str(user.id))

    response = JSONResponse(
        content={"message": "Registration successful", "token": token},
        status_code=201,
    )
    expires_delta = timedelta(hours=3)
    expires_at = int((datetime.utcnow() + expires_delta).timestamp())
    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=int(expires_delta.total_seconds()),
        expires=expires_at,
        path="/",
    )
    return response


@router.get("/logout", response_model=LogoutResponse)
async def logout():
    """Выход из системы, удаление токена из cookies"""
    response = JSONResponse(
        content={"message": "Logout successful"},
        status_code=200,
    )
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return response


@router.patch("/me", response_model=UserRead)
async def update_me(
    data: UpdateProfileRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Обновление данных профиля (имя, email, пароль)"""
    # Проверка текущего пароля
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный текущий пароль")

    # Email
    if data.email and data.email != current_user.email:
        existing = await session.execute(select(User).where(User.email == data.email))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email уже используется")
        current_user.email = data.email

    # Имя
    if data.name:
        current_user.name = data.name

    # Пароль
    if data.password:
        current_user.password_hash = hash_password(data.password)

    await session.commit()

    # Возвращаем актуальные данные, включая подписки
    query = (
        select(User)
        .options(selectinload(User.subscriptions))
        .where(User.id == current_user.id)
    )
    result = await session.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Проверяем, является ли пользователь автором
    is_author_query = select(exists().where(Author.user_id == user.id))
    is_author_result = await session.execute(is_author_query)
    user.is_author = is_author_result.scalar()
    
    return user

@router.get("/me", response_model=UserRead)
async def me(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Получить информацию о текущем авторизованном пользователе"""
    query = (
        select(User)
        .options(
            selectinload(User.subscriptions),
        )
        .where(User.id == current_user.id)
    )
    result = await session.execute(query)
    me = result.scalars().first()
    if not me:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Проверяем, является ли пользователь автором
    is_author_query = select(exists().where(Author.user_id == me.id))
    is_author_result = await session.execute(is_author_query)
    me.is_author = is_author_result.scalar()
    
    return me