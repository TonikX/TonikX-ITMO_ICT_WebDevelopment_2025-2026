from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    if not isinstance(password, str):
        password = str(password)
    # кодировка и безопасное обрезание по байтам
    password_bytes = password.encode("utf-8")[:72]
    password = password_bytes.decode("utf-8", errors="ignore")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not isinstance(plain_password, str):
        plain_password = str(plain_password)
    plain_bytes = plain_password.encode("utf-8")[:72]
    plain_password = plain_bytes.decode("utf-8", errors="ignore")
    return pwd_context.verify(plain_password, hashed_password)
