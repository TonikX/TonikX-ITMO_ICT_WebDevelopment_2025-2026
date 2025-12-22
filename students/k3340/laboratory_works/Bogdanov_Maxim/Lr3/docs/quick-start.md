# Быстрый старт

## Запуск через Docker (рекомендуется)

```bash
# Клонируйте репозиторий
git clone <repo-url>
cd students/k3340/laboratory_works/Bogdanov_Maxim/Lr3

# Запустите все сервисы
docker compose up -d

# Проверьте статус
curl http://localhost:8080/health/live
```

API доступен на `http://localhost:8080`

Swagger UI: `http://localhost:8080/swagger/`

## Первые шаги

### 1. Регистрация

```bash
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@school.com",
    "password": "admin123",
    "role": "admin"
  }'
```

Сохраните `access_token` из ответа.

### 2. Получение данных

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     http://localhost:8080/api/v1/teachers
```

## Локальная разработка

### Требования

- Go 1.25+
- PostgreSQL 15+

### Установка

```bash
# Установите зависимости
go mod download

# Создайте БД
psql -U postgres -c "CREATE DATABASE school_db"

# Примените миграции
make migrate-up

# Запустите приложение
make run
```

## Конфигурация

Создайте `.env` файл:

```env
JWT_SECRET=your-secret-key
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=school_db
```

## Команды Make

```bash
make run              # Запуск
make test             # Тесты
make migrate-up       # Применить миграции
make migrate-down     # Откатить миграции
make swagger          # Обновить Swagger
```

