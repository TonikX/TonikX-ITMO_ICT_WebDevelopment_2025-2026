from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.core.database import get_async_session
from app.core.settings.security import verify_password, create_access_token, decode_token
from app.core.settings.config import settings
from app.api.schemas import UserCreate, UserResponse, Token, UserProfileCreate, UserProfileResponse
from app.core.db import crud

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    user = await crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    
    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Регистрация нового пользователя.
    
    - **username**: имя пользователя (3-150 символов)
    - **email**: email адрес
    - **password**: пароль (минимум 6 символов)
    """
    # Проверяем, существует ли пользователь
    existing_user = await crud.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    existing_email = await crud.get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Создаём пользователя
    user = await crud.create_user(
        db, 
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )
    
    # Создаём профиль пользователя
    await crud.create_user_profile(db, user_id=user.id)
    
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Авторизация пользователя и получение JWT токена.
    
    - **username**: имя пользователя
    - **password**: пароль
    """
    user = await crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user = Depends(get_current_user)
):
    """
    Получение информации о текущем авторизованном пользователе.
    """
    return current_user


@router.get("/me/profile", response_model=UserProfileResponse)
async def get_my_profile(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получение профиля текущего пользователя.
    """
    profile = await crud.get_user_profile(db, user_id=current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile


@router.put("/me/profile", response_model=UserProfileResponse)
async def update_my_profile(
    profile_data: UserProfileCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Обновление профиля текущего пользователя.
    
    - **date_of_birth**: дата рождения (опционально)
    """
    profile = await crud.update_user_profile(
        db, 
        user_id=current_user.id,
        date_of_birth=profile_data.date_of_birth
    )
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile
