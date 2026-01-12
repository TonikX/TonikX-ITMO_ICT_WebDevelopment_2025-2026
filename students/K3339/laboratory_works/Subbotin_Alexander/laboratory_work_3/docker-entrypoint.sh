#!/usr/bin/env bash
set -e

# Ждём, пока Postgres не станет доступен
until pg_isready --host="$POSTGRES_SERVER" --port="$POSTGRES_PORT" --username="$POSTGRES_USER" --dbname="$POSTGRES_DB"; do
  echo "Waiting for Postgres..."
  sleep 2
done

# Применяем все миграции Alembic
alembic upgrade head

# Запускаем FastAPI
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000
