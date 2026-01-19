# Tour Agency API

FastAPI приложение для управления турагентством с системой бронирования туров и отзывов.

## Технологии

- **FastAPI** - современный веб-фреймворк для Python
- **SQLAlchemy 2.0** - ORM для работы с базой данных
- **Alembic** - управление миграциями БД
- **PostgreSQL** - реляционная база данных
- **asyncpg** - асинхронный драйвер для PostgreSQL
- **JWT** - аутентификация по токенам
- **Pydantic** - валидация данных
- **aiohttp** - асинхронные HTTP запросы

## Структура проекта

```
laboratory_work_3/

```

## Модели данных

### User (Пользователь)
- id, username, email, hashed_password, is_active, created_at

### UserProfile (Профиль пользователя)
- id, user_id, date_of_birth

### Tour (Тур)
- id, title, agency, description, start_date, end_date, price, city, payment_terms

### Reservation (Бронирование)
- id, tour_id, user_id, created_at, guests, notes, confirmed

### Review (Отзыв)
- id, tour_id, user_id, text, rating (1-10), created_at

## Установка и запуск

### 1. Клонирование и настройка окружения

```bash
# Создаём виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Устанавливаем зависимости
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env`:
```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=tour_agency_db
DB_PORT=5432

SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Запуск с Docker Compose (рекомендуется)

```bash
# Запускаем PostgreSQL и приложение
docker-compose up -d

# Применяем миграции
docker-compose exec app alembic upgrade head
```

### 4. Запуск без Docker

```bash
# Создаём БД вручную
createdb tour_agency_db

# Применяем миграции
alembic upgrade head

# Запускаем приложение
uvicorn app.main:app --reload
```

## API Endpoints

### Аутентификация

- `POST /auth/register` - Регистрация нового пользователя
- `POST /auth/login` - Авторизация и получение JWT токена
- `GET /auth/me` - Информация о текущем пользователе
- `GET /auth/me/profile` - Профиль пользователя
- `PUT /auth/me/profile` - Обновление профиля

### Туры

- `GET /tours/` - Список туров (с фильтрацией по городу)
- `GET /tours/{id}` - Детали тура
- `POST /tours/` - Создание тура (требуется авторизация)
- `PUT /tours/{id}` - Обновление тура (требуется авторизация)
- `DELETE /tours/{id}` - Удаление тура (требуется авторизация)

### Бронирования

- `POST /reservations/` - Создание бронирования (требуется авторизация)
- `GET /reservations/my` - Мои бронирования
- `GET /reservations/{id}` - Детали бронирования
- `PUT /reservations/{id}` - Обновление бронирования
- `DELETE /reservations/{id}` - Удаление бронирования

### Отзывы

- `POST /reviews/` - Создание отзыва (требуется авторизация)
- `GET /reviews/tour/{tour_id}` - Отзывы на тур
- `GET /reviews/{id}` - Детали отзыва
- `PUT /reviews/{id}` - Обновление отзыва
- `DELETE /reviews/{id}` - Удаление отзыва

## Работа с Alembic

```bash
# Создание новой миграции
alembic revision --autogenerate -m "Description"

# Применение миграций
alembic upgrade head

# Откат последней миграции
alembic downgrade -1

# Просмотр истории
alembic history
```

## Документация API

После запуска приложения доступна автоматическая документация:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Примеры использования

### Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Авторизация

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

### Создание тура (с токеном)

```bash
curl -X POST "http://localhost:8000/tours/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Тур в Париж",
    "agency": "Dream Tours",
    "description": "Незабываемое путешествие",
    "start_date": "2025-06-01",
    "end_date": "2025-06-07",
    "price": 1500.00,
    "city": "Париж",
    "payment_terms": "Оплата 50% при бронировании"
  }'
```

## Особенности реализации

### Асинхронность
Все операции с БД выполняются асинхронно через `asyncpg` и SQLAlchemy 2.0

### Безопасность
- Пароли хешируются с помощью bcrypt
- JWT токены для аутентификации
- Валидация данных через Pydantic
- Защита endpoints с помощью OAuth2

### CRUD паттерн
Разделение логики на слои:
- **Models** - SQLAlchemy модели
- **Schemas** - Pydantic схемы для валидации
- **CRUD** - функции для работы с БД
- **API** - endpoints для клиентов

## Тестирование

API можно тестировать через встроенный Swagger UI или используя curl/Postman.

## Автор

Субботин Александр, K3339

## Лицензия

MIT
