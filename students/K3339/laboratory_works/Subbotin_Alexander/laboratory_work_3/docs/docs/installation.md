# Установка и запуск

## Требования

- Python 3.11+
- PostgreSQL 15+
- Docker и Docker Compose (рекомендуется)

## Вариант 1: Запуск с Docker (рекомендуется)

### Шаг 1: Клонирование репозитория

```bash
git clone <repository-url>
cd laboratory_work_3
```

### Шаг 2: Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```env
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=db
DB_NAME=tour_agency_db
DB_PORT=5432

SECRET_KEY=your-secret-key-here-generate-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

!!! tip "Генерация SECRET_KEY"
    Для генерации безопасного ключа используйте:
    ```bash
    python -c "import secrets; print(secrets.token_hex(32))"
    ```

### Шаг 3: Запуск контейнеров

```bash
docker-compose up -d
```

Эта команда:
- Создаст контейнер с PostgreSQL
- Создаст контейнер с FastAPI приложением
- Настроит сеть между контейнерами

### Шаг 4: Применение миграций

```bash
docker-compose exec app alembic upgrade head
```

### Шаг 5: Проверка работы

Откройте в браузере:
- [http://localhost:8000/docs](http://localhost:8000/docs) - Swagger UI
- [http://localhost:8000/health](http://localhost:8000/health) - Health check

## Вариант 2: Локальный запуск (без Docker)

### Шаг 1: Установка PostgreSQL

Установите PostgreSQL 15+ и создайте базу данных:

```bash
psql -U postgres
CREATE DATABASE tour_agency_db;
\q
```

### Шаг 2: Создание виртуального окружения

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Шаг 3: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 4: Настройка .env

Создайте `.env` с настройками для локального подключения:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=tour_agency_db
DB_PORT=5432

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Шаг 5: Применение миграций

```bash
alembic upgrade head
```

### Шаг 6: Запуск приложения

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Работа с Alembic

### Создание новой миграции

После изменения моделей создайте миграцию:

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Применение миграций

```bash
# Применить все миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1

# Откатить все миграции
alembic downgrade base
```

### Просмотр истории миграций

```bash
alembic history

# С подробной информацией
alembic history --verbose
```

### Просмотр текущей версии

```bash
alembic current
```

## Остановка и очистка

### Остановка контейнеров

```bash
docker-compose down
```

### Остановка с удалением volumes (БД)

```bash
docker-compose down -v
```

### Пересборка контейнеров

```bash
docker-compose up -d --build
```

## Просмотр логов

```bash
# Все сервисы
docker-compose logs -f

# Только приложение
docker-compose logs -f app

# Только база данных
docker-compose logs -f db
```

## Подключение к базе данных

### Через Docker

```bash
docker-compose exec db psql -U postgres -d tour_agency_db
```

### Локально

```bash
psql -U postgres -d tour_agency_db
```

## Проблемы и решения

### Ошибка подключения к БД

!!! warning "ConnectionRefusedError"
    Если видите ошибку подключения, убедитесь что:
    
    1. PostgreSQL запущен
    2. Порт 5432 не занят
    3. Настройки в `.env` корректны

```bash
# Проверка статуса контейнеров
docker-compose ps

# Перезапуск
docker-compose restart
```

### Порт 8000 уже занят

Измените порт в `docker-compose.yaml`:

```yaml
ports:
  - "8001:8000"  # Используем 8001 вместо 8000
```

### Ошибки миграций

```bash
# Откатите и примените заново
alembic downgrade base
alembic upgrade head
```

## Тестирование API

После запуска протестируйте базовые endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Регистрация
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"test123"}'

# Список туров
curl http://localhost:8000/tours/
```

## Следующие шаги

После успешной установки:

1. Изучите [документацию API](api/auth.md)
2. Протестируйте endpoints в [Swagger UI](http://localhost:8000/docs)
3. Посмотрите [примеры использования](examples.md)
