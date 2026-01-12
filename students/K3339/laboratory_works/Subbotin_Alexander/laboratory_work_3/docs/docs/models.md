# Модели данных

Описание всех моделей данных, используемых в Tour Agency API.

## User (Пользователь)

Основная модель пользователя системы.

**Таблица:** `users`

| Поле | Тип | Описание |
|------|-----|----------|
| id | Integer | Уникальный идентификатор (PK) |
| username | String(150) | Имя пользователя (уникальное) |
| email | String(255) | Email адрес (уникальное) |
| hashed_password | String(255) | Хешированный пароль |
| is_active | Boolean | Активен ли пользователь |
| created_at | Timestamp | Дата создания |

**Связи:**
- `profile` → UserProfile (один к одному)
- `reservations` → Reservation (один ко многим)
- `reviews` → Review (один ко многим)

---

## UserProfile (Профиль пользователя)

Дополнительная информация о пользователе.

**Таблица:** `user_profiles`

| Поле | Тип | Описание |
|------|-----|----------|
| id | Integer | Уникальный идентификатор (PK) |
| user_id | Integer | ID пользователя (FK → users.id) |
| date_of_birth | Date | Дата рождения (опционально) |

**Связи:**
- `user` → User (один к одному)

---

## Tour (Тур)

Информация о туристическом туре.

**Таблица:** `tours`

| Поле | Тип | Описание |
|------|-----|----------|
| id | Integer | Уникальный идентификатор (PK) |
| title | String(200) | Название тура |
| agency | String(200) | Название агентства |
| description | Text | Подробное описание |
| start_date | Date | Дата начала тура |
| end_date | Date | Дата окончания тура |
| price | Decimal(10,2) | Цена тура |
| city | String(100) | Город |
| payment_terms | Text | Условия оплаты (опционально) |

**Связи:**
- `reservations` → Reservation (один ко многим)
- `reviews` → Review (один ко многим)

**Индексы:**
- `city` для оптимизации поиска по городу

---

## Reservation (Бронирование)

Бронирование тура пользователем.

**Таблица:** `reservations`

| Поле | Тип | Описание |
|------|-----|----------|
| id | Integer | Уникальный идентификатор (PK) |
| tour_id | Integer | ID тура (FK → tours.id) |
| user_id | Integer | ID пользователя (FK → users.id) |
| created_at | Timestamp | Дата создания бронирования |
| guests | Integer | Количество гостей (≥ 1) |
| notes | Text | Дополнительные заметки |
| confirmed | Boolean | Подтверждено ли бронирование |

**Связи:**
- `tour` → Tour (многие к одному)
- `user` → User (многие к одному)

**Правила CASCADE:**
- При удалении тура → удаляются все бронирования
- При удалении пользователя → удаляются все его бронирования

---

## Review (Отзыв)

Отзыв пользователя на тур.

**Таблица:** `reviews`

| Поле | Тип | Описание |
|------|-----|----------|
| id | Integer | Уникальный идентификатор (PK) |
| tour_id | Integer | ID тура (FK → tours.id) |
| user_id | Integer | ID пользователя (FK → users.id, nullable) |
| text | Text | Текст отзыва |
| rating | SmallInteger | Оценка (1-10) |
| created_at | Timestamp | Дата создания |

**Связи:**
- `tour` → Tour (многие к одному)
- `user` → User (многие к одному)

**Правила CASCADE:**
- При удалении тура → удаляются все отзывы
- При удалении пользователя → user_id становится NULL (отзыв сохраняется)

**Сортировка:**
- По умолчанию: `-created_at` (новые первыми)

---

## Диаграмма связей

```
┌─────────────┐         ┌──────────────────┐
│    User     │────1:1──│  UserProfile     │
│             │         │                  │
│ id          │         │ id               │
│ username    │         │ user_id (FK)     │
│ email       │         │ date_of_birth    │
│ password    │         └──────────────────┘
└──────┬──────┘
       │
       │ 1:N
       │
┌──────▼───────────┐        ┌──────────────┐
│  Reservation     │───N:1──│     Tour     │
│                  │        │              │
│ id               │        │ id           │
│ tour_id (FK)     │◄───────│ title        │
│ user_id (FK)     │        │ agency       │
│ guests           │        │ description  │
│ confirmed        │        │ start_date   │
└──────────────────┘        │ end_date     │
                            │ price        │
┌──────────────────┐        │ city         │
│     Review       │───N:1──│              │
│                  │        └──────────────┘
│ id               │
│ tour_id (FK)     │
│ user_id (FK)     │
│ text             │
│ rating           │
└──────────────────┘
```

---

## SQL схема (PostgreSQL)

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- User profiles table
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date_of_birth DATE
);

-- Tours table
CREATE TABLE tours (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    agency VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    city VARCHAR(100) NOT NULL,
    payment_terms TEXT
);

-- Reservations table
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    tour_id INTEGER NOT NULL REFERENCES tours(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    guests INTEGER NOT NULL CHECK (guests > 0),
    notes TEXT DEFAULT '',
    confirmed BOOLEAN DEFAULT FALSE
);

-- Reviews table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    tour_id INTEGER NOT NULL REFERENCES tours(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    text TEXT NOT NULL,
    rating SMALLINT NOT NULL CHECK (rating >= 1 AND rating <= 10),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for better performance
CREATE INDEX idx_tours_city ON tours(city);
CREATE INDEX idx_reservations_user_id ON reservations(user_id);
CREATE INDEX idx_reservations_tour_id ON reservations(tour_id);
CREATE INDEX idx_reviews_tour_id ON reviews(tour_id);
CREATE INDEX idx_reviews_created_at ON reviews(created_at DESC);
```

---

## Валидация данных

### User
- `username`: 3-150 символов, уникальное
- `email`: валидный email, уникальное
- `password`: минимум 6 символов (при создании)

### Tour
- `price`: > 0, до 2 знаков после запятой
- `end_date`: должна быть >= `start_date`
- `title`, `agency`: максимум 200 символов
- `city`: максимум 100 символов

### Reservation
- `guests`: >= 1
- `tour_id`: должен существовать в таблице tours

### Review
- `rating`: от 1 до 10 включительно
- `text`: не пустое
- `tour_id`: должен существовать в таблице tours

---

## Миграции

Все изменения схемы БД управляются через Alembic:

```bash
# Создание миграции после изменения моделей
alembic revision --autogenerate -m "Описание изменений"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

Файлы миграций находятся в `alembic/versions/`.
