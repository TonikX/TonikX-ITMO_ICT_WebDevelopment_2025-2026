# Установка и запуск

## Требования

- Node.js 18+ 
- npm 9+
- Запущенный бэкенд (lab3)

## Установка

### 1. Клонирование и установка зависимостей

```bash
cd lab4
npm install
```

### 2. Настройка окружения

Создайте файл `.env` в корне проекта:

```env
VITE_API_URL=http://localhost:8000
```

### 3. Запуск бэкенда

Перед запуском фронтенда необходимо запустить бэкенд из lab3:

```bash
cd ../lab3
docker-compose up -d
```

Или без Docker:

```bash
cd ../lab3
python manage.py runserver
```

### 4. Запуск фронтенда

```bash
npm run dev
```

Приложение будет доступно по адресу: `http://localhost:5173`

## Режимы запуска

### Разработка

```bash
npm run dev
```

Запускает Vite dev server с горячей перезагрузкой.

### Продакшен сборка

```bash
npm run build
```

Создаёт оптимизированную сборку в директории `dist/`.

### Предпросмотр продакшен сборки

```bash
npm run preview
```

## Настройка CORS

Бэкенд должен разрешать запросы с `http://localhost:5173`. 

В `lab3/hotel_system/settings.py` уже добавлены настройки CORS:

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
```

## Возможные проблемы

### Ошибка CORS

Убедитесь, что:
1. В бэкенде установлен `django-cors-headers`
2. В `INSTALLED_APPS` добавлен `'corsheaders'`
3. В `MIDDLEWARE` добавлен `'corsheaders.middleware.CorsMiddleware'`
4. Настроены `CORS_ALLOWED_ORIGINS`

### Ошибка подключения к API

1. Проверьте, что бэкенд запущен
2. Проверьте адрес API в `.env`
3. Проверьте консоль браузера на наличие ошибок

## Документация

Для просмотра документации:

```bash
pip install mkdocs mkdocs-material
mkdocs serve
```

Документация будет доступна по адресу: `http://localhost:8000`
