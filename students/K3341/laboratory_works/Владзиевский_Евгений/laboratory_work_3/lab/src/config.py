import os


def required_env(name):
    value = os.getenv(name)
    if value is None:
        raise Exception(f"Environment variable {name} is required")
    return value
DB_HOST = required_env("DB_HOST")
DB_USER = required_env("DB_USER")
DB_PASSWORD = required_env("DB_PASSWORD")
DB_NAME = required_env("DB_NAME")

S3_URL = required_env("S3_URL")
S3_BUCKET = required_env("S3_BUCKET")
S3_ACCESS_KEY = required_env("S3_ACCESS_KEY")
S3_SECRET_KEY = required_env("S3_SECRET_KEY")
ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg']


DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
JWT_SECRET_KEY = required_env("JWT_SECRET_KEY")
JWT_EXPIRE_HOURS = 24 * 30 # 30 days

