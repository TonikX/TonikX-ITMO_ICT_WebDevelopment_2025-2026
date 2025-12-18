# Система управления библиотекой

## Описание проекта

Веб-приложение для управления библиотекой, состоящее из:

- **Backend**: Django REST Framework API с PostgreSQL
- **Frontend**: React приложение на TypeScript с использованием Vite, Material-UI и React Router

## Требования

### Для Backend:
- Python 3.8+
- PostgreSQL 12+

### Для Frontend:
- Node.js 18+ (включает npm)
- npm

## Настройка Backend

### 1. Установка зависимостей

Перейдите в директорию `Lr3` и создайте виртуальное окружение:

```bash
cd Lr3
python -m venv venv
```

Активируйте виртуальное окружение:

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

### 2. Настройка PostgreSQL

Убедитесь, что PostgreSQL установлен и запущен. Создайте базу данных:

```sql
CREATE DATABASE library_db;
CREATE USER library_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;
```

### 3. Настройка переменных окружения

Создайте файл `.env` в директории `Lr3/` со следующим содержимым:

```env
# База данных
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Django настройки
SECRET_KEY=your-secret-key-here-min-50-characters-long
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT настройки
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
JWT_ALGORITHM=HS256

# Секретный ключ для регистрации сотрудников
STAFF_REGISTRATION_KEY=your-registration-key-here
```

### 4. Применение миграций

Примените миграции базы данных:

```bash
python manage.py migrate
```

### 5. Создание суперпользователя (опционально)

Для доступа к Django Admin панели:

```bash
python manage.py createsuperuser
```

### 6. Запуск Backend сервера

Запустите Django development server:

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: `http://localhost:8000`

**API документация (Swagger):** `http://localhost:8000/api/schema/swagger-ui/`

## Настройка Frontend

### 1. Установка зависимостей

Перейдите в директорию `lr4_frontend`:

```bash
cd Lr4
```

Установите зависимости:

```bash
npm install
```

### 2. Настройка переменных окружения

Создайте файл `.env` в директории `lr4_frontend/`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Запуск Frontend сервера

Запустите development server:

```bash
npm run dev
```

Frontend будет доступен по адресу: `http://localhost:3000`

## Первый запуск

### 1. Создание первого сотрудника

После запуска backend и frontend:

1. Откройте браузер и перейдите на `http://localhost:3000`
2. Перейдите на страницу регистрации сотрудника: `/register-staff`
3. Заполните форму регистрации, используя `STAFF_REGISTRATION_KEY` из `.env` файла backend

### 2. Вход в систему

1. Перейдите на страницу входа: `/login`
2. Введите логин и пароль созданного сотрудника
3. После успешного входа вы будете перенаправлены на главную страницу

## Основные функции системы

- **Управление книгами**: Каталог книг, авторы, издательства, разделы
- **Управление экземплярами**: Регистрация экземпляров, списание книг
- **Управление читателями**: Регистрация, редактирование, деактивация
- **Выдача книг**: Выдача и прием книг от читателей
- **Аналитика**: Просроченные выдачи, редкие книги, статистика

## Скрипты разработки

### Backend

```bash
# Применить миграции
python manage.py migrate

# Создать миграции
python manage.py makemigrations

# Запустить сервер
python manage.py runserver

# Создать суперпользователя
python manage.py createsuperuser
```

### Frontend

```bash
# Запустить development server
npm run dev

# Собрать production build
npm run build

# Предпросмотр production build
npm run preview
```

## Технический стек

### Backend
- **Django 5.2** - веб-фреймворк
- **Django REST Framework** - API framework
- **djangorestframework-simplejwt** - JWT аутентификация
- **PostgreSQL** - база данных
- **drf-spectacular** - генерация OpenAPI документации
- **django-cors-headers** - обработка CORS

### Frontend
- **React 18** - UI библиотека
- **TypeScript** - типизированный JavaScript
- **Vite** - сборщик и dev server
- **Material-UI (MUI)** - компоненты UI
- **React Router** - маршрутизация
- **Axios** - HTTP клиент
- **React Hook Form** - управление формами
- **Yup** - валидация форм



