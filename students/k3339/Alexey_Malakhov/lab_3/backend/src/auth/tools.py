import jwt
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.auth import config, security
from src.database import get_session
from src.models.user import User


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> User:
    """Получение текущего пользователя из JWT токена в cookie"""
    
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    
    try:
        # Декодируем токен напрямую через jwt
        payload = jwt.decode(
            token, 
            config.JWT_SECRET_KEY, 
            algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Authentication failed: {str(e)}"
        )
    
    # Временная отладка - посмотрим что в payload
    print(f"DEBUG: Token payload = {payload}")
    
    # Проверяем payload после декодирования
    # Попробуем разные варианты ключей
    user_id = payload.get("uid") or payload.get("sub") or payload.get("user_id")
    
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token payload. Available keys: {list(payload.keys())}"
        )
    
    # Преобразуем в integer, если это строка
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid user ID format"
        )
    
    # Получаем пользователя из БД
    query = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = query.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    
    return user