# Publishing House API - Лабораторная работа 3

REST API для информационного обслуживания типографии. Система управляет сотрудниками, авторами, книгами, контрактами и заказами.

## Технологический стек

- **Django 5.2** - веб-фреймворк (совместим с Python 3.14)
- **Django REST Framework 3.14+** - RESTful API
- **Djoser** - аутентификация по токенам
- **PostgreSQL** - СУБД
- **drf-spectacular** - документация API

## Установка и настройка

### 1. Клонирование репозитория

```bash
cd students/k3340/laboratory_works/Якшин_Артемий/laboratory_work_3/publishing_house
```

### 2. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux/Mac
# или
venv\Scripts\activate  # Для Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка PostgreSQL

Создайте базу данных:

```sql
CREATE DATABASE publishing_db;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE publishing_db TO postgres;
```

### 5. Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env` и укажите данные вашей базы данных:

```
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=publishing_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 6. Применение миграций

```bash
python manage.py migrate
```

### 7. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 8. Заполнение тестовыми данными (опционально)

```bash
python manage.py populate_db
```

Эта команда создаст:
- 7 сотрудников (3 менеджера, 4 редактора)
- 12 авторов
- 16 книг с контрактами
- Связи книга-автор и книга-редактор
- 7 заказчиков
- 10 заказов с позициями

### 9. Запуск сервера

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: `http://localhost:8000`

## Структура API

### Базовый URL: `/api/v1/`

### Аутентификация (Djoser)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/v1/auth/users/` | Регистрация нового пользователя |
| POST | `/api/v1/auth/token/login/` | Получение токена (вход) |
| POST | `/api/v1/auth/token/logout/` | Удаление токена (выход) |
| GET | `/api/v1/auth/users/me/` | Информация о текущем пользователе |

### CRUD Endpoints

| Ресурс | Endpoint | Методы |
|--------|----------|--------|
| Сотрудники | `/api/v1/employees/` | GET, POST, PUT, PATCH, DELETE |
| Авторы | `/api/v1/authors/` | GET, POST, PUT, PATCH, DELETE |
| Книги | `/api/v1/books/` | GET, POST, PUT, PATCH, DELETE |
| Контракты | `/api/v1/contracts/` | GET, POST, PUT, PATCH, DELETE |
| Заказчики | `/api/v1/customers/` | GET, POST, PUT, PATCH, DELETE |
| Заказы | `/api/v1/orders/` | GET, POST, PUT, PATCH, DELETE |
| Книга-Автор | `/api/v1/book-authors/` | GET, POST, PUT, PATCH, DELETE |
| Книга-Редактор | `/api/v1/book-editors/` | GET, POST, PUT, PATCH, DELETE |
| Позиции заказа | `/api/v1/order-items/` | GET, POST, PUT, PATCH, DELETE |

### Отчеты

| Отчет | Endpoint | Параметры |
|-------|----------|-----------|
| Книги по автору | `/api/v1/reports/books-by-author/` | `author_id` |
| Ответственные редакторы | `/api/v1/reports/chief-editors/` | - |
| Редакторы каждой книги | `/api/v1/reports/editors-per-book/` | - |
| Контракты по месяцам | `/api/v1/reports/contracts-by-month/` | `year` (optional) |
| Топ менеджеры | `/api/v1/reports/top-managers/` | `start_date`, `end_date` |
| Квартальный отчет | `/api/v1/reports/quarterly-contracts/` | `quarter`, `year` (optional) |

## Примеры использования API

### 1. Регистрация и аутентификация

**Регистрация:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123"
  }'
```

**Получение токена:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123"
  }'
```

Ответ:
```json
{
  "auth_token": "your_authentication_token_here"
}
```

**Использование токена:**
```bash
curl http://localhost:8000/api/v1/books/ \
  -H "Authorization: Token your_authentication_token_here"
```

### 2. Работа с книгами

**Получить список книг:**
```bash
curl http://localhost:8000/api/v1/books/
```

**Получить детали книги:**
```bash
curl http://localhost:8000/api/v1/books/1/
```

**Создать книгу:**
```bash
curl -X POST http://localhost:8000/api/v1/books/ \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Новая книга",
    "isbn": "978-5-12345-678-9",
    "pages": 300,
    "has_illustrations": false,
    "publication_date": "2024-12-01",
    "cover_price": "599.00",
    "description": "Описание книги",
    "genre": "Роман",
    "language": "RU"
  }'
```

### 3. Работа с контрактами

**Создать контракт:**
```bash
curl -X POST http://localhost:8000/api/v1/contracts/ \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "contract_number": "CONTRACT-2024-0001",
    "book": 1,
    "manager": 1,
    "signed_date": "2024-12-01",
    "status": "ACTIVE",
    "advance_payment": "100000.00",
    "total_budget": "300000.00",
    "expiry_date": "2025-12-01",
    "notes": "Примечания к контракту"
  }'
```

**Важно:** Менеджер (manager) должен иметь роль 'MANAGER', иначе будет ошибка валидации.

### 4. Связывание книги с авторами

**Добавить автора к книге:**
```bash
curl -X POST http://localhost:8000/api/v1/book-authors/ \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "book": 1,
    "author": 1,
    "author_order": 1,
    "royalty_percentage": "100.00"
  }'
```

**Важно:** Сумма royalty_percentage для всех авторов книги не должна превышать 100%.

### 5. Назначение редакторов

**Назначить редактора:**
```bash
curl -X POST http://localhost:8000/api/v1/book-editors/ \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "book": 1,
    "editor": 4,
    "is_chief_editor": true
  }'
```

**Важно:**
- Редактор (editor) должен иметь роль 'EDITOR'
- Только один редактор может быть ответственным (is_chief_editor=true) для каждой книги

### 6. Отчеты

**Отчет 1: Книги по автору**
```bash
curl "http://localhost:8000/api/v1/reports/books-by-author/?author_id=1" \
  -H "Authorization: Token your_token"
```

**Отчет 2: Ответственные редакторы**
```bash
curl http://localhost:8000/api/v1/reports/chief-editors/ \
  -H "Authorization: Token your_token"
```

**Отчет 3: Количество редакторов каждой книги**
```bash
curl http://localhost:8000/api/v1/reports/editors-per-book/ \
  -H "Authorization: Token your_token"
```

**Отчет 4: Контракты по месяцам**
```bash
curl "http://localhost:8000/api/v1/reports/contracts-by-month/?year=2024" \
  -H "Authorization: Token your_token"
```

**Отчет 5: Топ менеджеры**
```bash
curl "http://localhost:8000/api/v1/reports/top-managers/?start_date=2024-01-01&end_date=2024-12-31" \
  -H "Authorization: Token your_token"
```

**Отчет 6: Квартальный отчет**
```bash
curl "http://localhost:8000/api/v1/reports/quarterly-contracts/?quarter=1&year=2024" \
  -H "Authorization: Token your_token"
```

## API Documentation

После запуска сервера документация API доступна по адресам:
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **Schema (JSON)**: `http://localhost:8000/api/schema/`

## Django Admin

Административная панель доступна по адресу: `http://localhost:8000/admin/`

Функции админки:
- Управление всеми моделями
- Inline-редактирование связей
- Поиск и фильтрация
- Кастомные методы отображения

## Модели данных

### Основные модели:

1. **Employee** - Сотрудники (менеджеры, редакторы)
2. **Author** - Авторы книг
3. **Book** - Книги
4. **Contract** - Контракты на издание
5. **Customer** - Заказчики
6. **Order** - Заказы на покупку

### Промежуточные модели:

7. **BookAuthor** - Связь книга-автор (с порядком и процентом гонорара)
8. **BookEditor** - Связь книга-редактор (с отметкой ответственного)
9. **OrderItem** - Позиции заказа

## Критические валидации

### Contract (Контракт):
- Менеджер должен иметь роль 'MANAGER'
- Аванс не может превышать общий бюджет

### BookEditor (Редактор книги):
- Редактор должен иметь роль 'EDITOR'
- Только один ответственный редактор на книгу

### BookAuthor (Автор книги):
- Сумма процентов гонорара всех авторов книги ≤ 100%
- Уникальность порядка авторов на обложке

### OrderItem (Позиция заказа):
- Автоматический расчет subtotal = quantity * unit_price

## Фильтрация и поиск

Большинство endpoints поддерживают:
- **Фильтрацию**: `?role=MANAGER`, `?status=ACTIVE`
- **Поиск**: `?search=Пушкин`
- **Сортировку**: `?ordering=title`, `?ordering=-publication_date`
- **Пагинацию**: `?page=2`, `?page_size=20`

Пример:
```bash
curl "http://localhost:8000/api/v1/employees/?role=MANAGER&ordering=last_name"
```

## Тестирование

```bash
# Запуск тестов (если реализованы)
python manage.py test

# Проверка миграций
python manage.py check

# Показать SQL для миграций
python manage.py sqlmigrate publishing 0001
```

## Troubleshooting

### Проблема с подключением к PostgreSQL

Убедитесь что:
1. PostgreSQL запущен: `sudo service postgresql status`
2. База данных создана
3. Правильные credentials в `.env`

### Ошибка миграций

```bash
# Откатить миграции
python manage.py migrate publishing zero

# Пересоздать миграции
python manage.py makemigrations
python manage.py migrate
```

### Ошибка импорта модулей

```bash
# Переустановить зависимости
pip install -r requirements.txt --force-reinstall
```

## Авторы

- **Студент:** Якшин Артемий
- **Группа:** К3340
- **Предмет:** Web-разработка
- **Работа:** Лабораторная работа №3

## Лицензия

Проект создан в учебных целях.
