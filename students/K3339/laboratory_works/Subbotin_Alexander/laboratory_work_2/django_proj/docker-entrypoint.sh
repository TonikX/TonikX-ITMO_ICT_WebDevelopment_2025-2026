#!/usr/bin/env bash
set -e

# Ждём, пока Postgres не станет доступен
until pg_isready --host="$POSTGRES_SERVER" --port="$POSTGRES_PORT" --username="$POSTGRES_USER" --dbname="$POSTGRES_DB"; do
  echo "Waiting for Postgres..."
  sleep 2
done

# Применяем все миграции Django
python manage.py makemigrations 
python manage.py migrate
python manage.py createsu

# Запускаем Django
exec python manage.py runserver 0.0.0.0:8000
