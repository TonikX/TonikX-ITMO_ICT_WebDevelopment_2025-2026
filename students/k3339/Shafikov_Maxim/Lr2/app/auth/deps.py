from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.db.base import get_db
from app.core.config import settings
from app.crud.users import user_repo
from app.schemas.users import TokenData


async def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = user_repo.get_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user=Depends(get_current_user_from_cookie)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return current_user


async def get_current_active_admin_user(current_user=Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user