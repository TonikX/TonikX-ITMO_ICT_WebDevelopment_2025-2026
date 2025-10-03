from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    DATABASE_URL: str | None = None
    SECRET_KEY: str = "change_me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    ADMIN_EMAIL: str = "admin"
    ADMIN_PASSWORD: str = "admin"

    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_url(cls, v, values):
        if isinstance(v, str) and v.strip():
            return v

        user = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        db = values.get("POSTGRES_DB")
        host = values.get("POSTGRES_HOST") or "db"
        port = values.get("POSTGRES_PORT") or 5432

        if user and password and db:
            return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

        raise ValueError(
            "DATABASE_URL is not set and POSTGRES_* variables are missing. "
            "Provide DATABASE_URL or POSTGRES_USER/POSTGRES_PASSWORD/POSTGRES_DB."
        )


settings = Settings()
