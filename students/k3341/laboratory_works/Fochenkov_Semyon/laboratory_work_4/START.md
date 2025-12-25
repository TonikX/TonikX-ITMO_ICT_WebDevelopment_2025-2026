# Инструкция по запуску лабораторной работы 4

## Обзор проекта

Лабораторная работа 4 состоит из двух частей:
1. **Backend (Django REST API)** - работает на порту 8000
2. **Frontend (Vue.js + Vite)** - работает на порту 5173

## Шаг 1: Подготовка окружения

### 1.1. Активация виртуального окружения Python

```bash
cd /Users/simon/TonikX-ITMO_ICT_WebDevelopment_2025-2026
source venv/bin/activate
```

### 1.2. Установка зависимостей Python

```bash
cd students/k3341/laboratory_works/Fochenkov_Semyon/laboratory_work_4
pip install -r requirements.txt
```

## Шаг 2: Настройка и запуск Backend (Django)

### 2.1. Переход в директорию Django проекта

```bash
cd printing_house
```

### 2.2. Применение миграций базы данных

```bash
python manage.py migrate
```

### 2.3. Создание тестового пользователя (опционально)

```bash
python create_test_user.py
```

**Данные для входа:**
- Имя пользователя: `testuser`
- Пароль: `password123`

### 2.4. Создание тестовых данных (опционально)

```bash
python create_sample_data.py
# или
python create_newspaper_data.py
```

### 2.5. Запуск Django сервера

```bash
python manage.py runserver
```

Backend будет доступен по адресу: **http://localhost:8000**

**Важно:** Оставьте этот терминал открытым!

## Шаг 3: Настройка и запуск Frontend (Vue.js)

### 3.1. Откройте новый терминал

В новом окне терминала выполните:

### 3.2. Переход в директорию Frontend

```bash
cd /Users/simon/TonikX-ITMO_ICT_WebDevelopment_2025-2026/students/k3341/laboratory_works/Fochenkov_Semyon/laboratory_work_4/frontend
```

### 3.3. Установка зависимостей Node.js

```bash
pnpm install
```

Если у вас не установлен `pnpm`, установите его:
```bash
npm install -g pnpm
```

### 3.4. Запуск Frontend сервера разработки

```bash
pnpm dev
```

Frontend будет доступен по адресу: **http://localhost:5173**

## Шаг 4: Использование приложения

1. Откройте браузер и перейдите на **http://localhost:5173**
2. Зарегистрируйте нового пользователя или войдите используя:
   - Имя пользователя: `testuser`
   - Пароль: `password123`

## Полезные команды

### Backend

- **Применить миграции:** `python manage.py migrate`
- **Создать суперпользователя:** `python manage.py createsuperuser`
- **Запустить сервер:** `python manage.py runserver`
- **Создать тестового пользователя:** `python create_test_user.py`
- **Создать тестовые данные:** `python create_sample_data.py`

### Frontend

- **Запустить dev сервер:** `pnpm dev`
- **Собрать для production:** `pnpm build`
- **Предпросмотр production сборки:** `pnpm preview`
- **Проверка типов:** `pnpm type-check`
- **Линтинг:** `pnpm lint`

## API Endpoints

После запуска Backend доступны следующие endpoints:

- **API:** http://localhost:8000/api/
- **Аутентификация:** http://localhost:8000/auth/
- **Админ-панель:** http://localhost:8000/admin/

## Устранение проблем

### Проблема: Порт 8000 уже занят

```bash
python manage.py runserver 8001
```

Затем обновите `API_BASE_URL` в `frontend/src/services/api.ts` на `http://localhost:8001`

### Проблема: Порт 5173 уже занят

Vite автоматически предложит использовать другой порт, или вы можете указать его явно:

```bash
pnpm dev --port 3000
```

### Проблема: Ошибки CORS

Убедитесь, что в `printing_house/printing_house/settings.py` в `CORS_ALLOWED_ORIGINS` указан правильный порт Frontend.

### Проблема: База данных не найдена

Выполните миграции:
```bash
cd printing_house
python manage.py migrate
```

## Структура проекта

```
laboratory_work_4/
├── printing_house/          # Django Backend
│   ├── core/                # Основное приложение
│   ├── printing_house/      # Настройки проекта
│   ├── manage.py
│   └── db.sqlite3          # База данных
├── frontend/                # Vue.js Frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
└── requirements.txt         # Python зависимости
```

