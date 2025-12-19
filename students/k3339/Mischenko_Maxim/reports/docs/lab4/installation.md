# Установка и запуск

## Системные требования

Для запуска приложения необходимо наличие следующего программного обеспечения:
- Docker
- Docker Compose

## Структура проекта

Проект состоит из следующих компонентов:
- `airline_admin` - Django приложение (бэкенд)
- `airline_client` - Vue.js приложение (фронтенд)
- `docker-compose.yml` - конфигурация Docker Compose

## Установка

1. Клонируйте репозиторий или перейдите в директорию проекта:
   ```bash
   cd Lr4
   ```

2. Запустите приложение с помощью Docker Compose:
   ```bash
   docker-compose up -d
   ```

Эта команда запустит все необходимые сервисы:
- PostgreSQL база данных
- Django приложение на порту 8000
- Vue.js приложение на порту 5173

## Инициализация базы данных

После первого запуска необходимо выполнить миграции базы данных:

```bash
docker-compose exec db psql -U postgres -d airlines -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
docker-compose exec airline_admin python manage.py migrate
```

## Создание суперпользователя

Для доступа к административной панели Django необходимо создать суперпользователя:

```bash
docker-compose exec airline_admin python manage.py createsuperuser
```

## Доступ к приложению

После запуска приложение будет доступно по следующим адресам:
- Фронтенд: http://localhost:5173
- Бэкенд API: http://localhost:8000
- Административная панель Django: http://localhost:8000/admin
- Документация API (Swagger): http://localhost:8000/swagger
- Документация API (ReDoc): http://localhost:8000/redoc

## Остановка приложения

Для остановки приложения выполните команду:

```bash
docker-compose down
```

## Просмотр логов

Для просмотра логов сервисов выполните команду:

```bash
docker-compose logs -f
```

## Пересборка приложения

Если вы внесли изменения в код приложения, необходимо пересобрать контейнеры:

```bash
docker-compose down
docker-compose up --build -d
```

## Решение проблем

### Порт уже занят

Если порты 5432, 8000 или 5173 уже заняты, необходимо остановить конфликтующие сервисы или изменить порты в файле `docker-compose.yml`.

### Ошибка подключения к базе данных

Убедитесь, что сервис базы данных запущен:
```bash
docker-compose ps
```

Если база данных не запущена, попробуйте перезапустить все сервисы:
```bash
docker-compose down
docker-compose up -d
```

### Проблемы с миграциями

Если возникают ошибки при выполнении миграций, попробуйте сбросить базу данных:
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec airline_admin python manage.py migrate