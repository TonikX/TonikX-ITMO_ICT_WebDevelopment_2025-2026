from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_hash_password(password: str):
    return pwd_context.hash(password)

