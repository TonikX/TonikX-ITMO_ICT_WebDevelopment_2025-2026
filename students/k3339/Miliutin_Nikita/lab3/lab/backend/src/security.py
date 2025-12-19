# src/core/security.py
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import jwt
from passlib.context import CryptContext

# >>> вынеси в env при первой возможности
SECRET_KEY = "CHANGE_ME_TO_LONG_RANDOM_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
# <<<

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return _pwd.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return _pwd.verify(password, hashed_password)


def create_access_token(
    *,
    subject: str,
    expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
    extra: Optional[dict[str, Any]] = None,
) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes)

    payload: dict[str, Any] = {"sub": subject, "iat": now, "exp": expire}
    if extra:
        payload.update(extra)

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
