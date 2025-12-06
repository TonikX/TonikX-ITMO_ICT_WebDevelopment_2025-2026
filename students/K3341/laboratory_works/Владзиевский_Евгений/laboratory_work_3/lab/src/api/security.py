from datetime import timedelta

from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer

from src import config

access_policy = JwtAccessBearer(
    secret_key=config.JWT_SECRET_KEY,
    auto_error=True,
    access_expires_delta=timedelta(hours=2)
)
refresh_policy = JwtRefreshBearer(
    secret_key=config.JWT_SECRET_KEY,
    auto_error=True,
    refresh_expires_delta=timedelta(hours=config.JWT_EXPIRE_HOURS)
)