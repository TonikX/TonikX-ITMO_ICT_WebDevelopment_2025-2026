from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


def find_dotenv(filename=".env", max_parent_levels=5) -> str | None:
    """
    Finds the .env file by searching upwards in the directory tree.
    """
    current_dir = Path(__file__).parent.resolve()
    for _ in range(max_parent_levels):
        env_path = current_dir / filename
        if env_path.exists():
            return str(env_path)
        current_dir = current_dir.parent
    return None


class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    """
    _env_file = find_dotenv()

    model_config = SettingsConfigDict(
        env_file=_env_file if _env_file else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    DB_SERVER: str = "localhost"
    POSTGRES_DB: str = "tour_agency_db"
    POSTGRES_PORT: int = 5432

    # Security settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.DB_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


# Create settings instance
settings = Settings()
