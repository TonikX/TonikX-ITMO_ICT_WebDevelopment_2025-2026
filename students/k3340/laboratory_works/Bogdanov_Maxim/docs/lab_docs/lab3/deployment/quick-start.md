# Быстрый старт

## Запуск через Docker (рекомендуется)

Самый простой способ запустить приложение - использовать Docker Compose.

```bash
cd students/k3340/laboratory_works/Bogdanov_Maxim/Lr3

# Запустить все сервисы
docker compose up -d

# Проверить статус
curl http://localhost:8080/health/live
```

После запуска:
- API доступен на `http://localhost:8080`
- Swagger UI: `http://localhost:8080/swagger/`
- PostgreSQL доступна на `localhost:5432`

## Первые шаги

### 1. Регистрация пользователя

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

### 2. Заполнение базы данных тестовыми данными

```bash
docker compose exec api /app/seed
```

### 3. Получение данных

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     http://localhost:8080/api/v1/teachers
```

## Локальная разработка

### Требования

- Go 1.25+
- PostgreSQL 15+
- Make (опционально)

### Установка

```bash
# Клонировать репозиторий
git clone <repo-url>
cd students/k3340/laboratory_works/Bogdanov_Maxim/Lr3

# Установить зависимости
go mod download

# Настроить переменные окружения
cp env.example .env
# Отредактировать .env файл
```

### Запуск

```bash
# Применить миграции
make migrate-up

# Запустить приложение
go run cmd/api/main.go
```

