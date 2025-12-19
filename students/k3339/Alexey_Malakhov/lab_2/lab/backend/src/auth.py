from fastapi import Request
from authx import AuthX, AuthXConfig, token  # используем подмодуль token

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


def get_current_user(request: Request):
    try:
        jwt_token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
        if not jwt_token:
            return None

        # используем decode_token — он есть в твоей версии
        payload = token.decode_token(jwt_token, key=config.JWT_SECRET_KEY)

        return payload.get("sub")  # email, если создавался с uid=email
    except Exception as e:
        print("TOKEN ERROR:", e)
        return None
