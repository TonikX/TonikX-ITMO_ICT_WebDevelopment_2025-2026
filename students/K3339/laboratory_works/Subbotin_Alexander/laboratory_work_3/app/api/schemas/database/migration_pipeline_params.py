from pydantic import BaseModel, Field


class MigrationPipelineParams(BaseModel):
    """Parameters schema for migration pipeline"""
    clear_database_first: bool = Field(
        True,
        description="Нужно ли очистить базу перед запуском миграции",
        json_schema_extra={"example": True},
    )
    migration_limit: int = Field(
        10_000,
        description="Максимальное количество туров для миграции",
        json_schema_extra={"example": 10_000},
        ge=0
    )