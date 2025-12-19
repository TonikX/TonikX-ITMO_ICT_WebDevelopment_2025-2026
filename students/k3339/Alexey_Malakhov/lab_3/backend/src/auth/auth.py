from datetime import timedelta

from authx import AuthX, AuthXConfig, token  # используем подмодуль token
from fastapi import Request

config = AuthXConfig()
config.JWT_SECRET_KEY = "web_lab_1234567890"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)  # Устанавливаем время жизни токена

security = AuthX(config=config)