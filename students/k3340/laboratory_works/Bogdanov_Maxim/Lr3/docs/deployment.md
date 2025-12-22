# Развертывание

## Docker (рекомендуется)

### Быстрый запуск

```bash
docker compose up -d
```

### Сервисы

- **postgres** - База данных (порт 5432)
- **migrate** - Автоматические миграции
- **api** - API сервер (порт 8080)

### Конфигурация

Создайте `.env` файл:

```env
JWT_SECRET=your-production-secret-key
```

### Команды

```bash
# Запуск
docker compose up -d

# Остановка
docker compose down

# Логи
docker compose logs -f api

# Пересборка
docker compose build

# Перезапуск
docker compose restart api
```

## Без Docker

### Требования

- Go 1.25+
- PostgreSQL 15+
- Make

### Установка

```bash
# Клонирование
git clone <repo-url>
cd students/k3340/laboratory_works/Bogdanov_Maxim/Lr3

# Зависимости
go mod download

# БД
createdb school_db

# Миграции
make migrate-up

# Запуск
make run
```

## Переменные окружения

### Обязательные

```env
JWT_SECRET=your-secret-key-min-32-chars
```

### Основные

```env
# Приложение
APP_ENV=production
APP_DEBUG=false

# HTTP
HTTP_PORT=8080
HTTP_HOST=0.0.0.0

# База данных
DB_HOST=postgres
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=secure_password
DB_NAME=school_db
DB_SSLMODE=require

# JWT
JWT_ACCESS_TOKEN_EXPIRY=15m
JWT_REFRESH_TOKEN_EXPIRY=168h

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

## Мониторинг

### Health checks

```bash
# Liveness
curl http://localhost:8080/health/live

# Readiness
curl http://localhost:8080/health/ready

# Полная проверка
curl http://localhost:8080/health
```

### Логи

```bash
# Docker
docker compose logs -f api

# Прямой запуск
# Логи выводятся в stdout
```

## Решение проблем

### Порт занят

```bash
# Проверить порт
netstat -ano | findstr :8080  # Windows
lsof -i :8080                  # Linux/Mac
```

### БД не подключается

```bash
# Проверить PostgreSQL
docker compose logs postgres

# Тест подключения
psql "postgres://postgres:postgres@localhost:5432/school_db"
```

### Миграции не применяются

```bash
# Логи миграций
docker compose logs migrate

# Применить вручную
make migrate-up
```

### Health check падает

```bash
# Проверить логи
docker compose logs api

# Проверить БД
docker compose exec postgres psql -U postgres -c "SELECT 1"
```

## Масштабирование

### Горизонтальное

Приложение stateless, можно запустить несколько инстансов:

```yaml
# docker-compose.yml
services:
  api:
    deploy:
      replicas: 3
```

### Load Balancer

Используйте nginx или HAProxy для распределения нагрузки между инстансами.

### Kubernetes

Проект готов к развертыванию в Kubernetes. Требуется создать:
- Deployment для API
- Service для API
- StatefulSet для PostgreSQL (или внешняя БД)
- ConfigMap для конфигурации
- Secret для JWT_SECRET и паролей

