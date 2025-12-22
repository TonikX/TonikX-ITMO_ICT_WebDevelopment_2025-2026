# Docker развертывание

## Структура Docker Compose

Проект использует Docker Compose для оркестрации сервисов:

- **postgres** - база данных PostgreSQL
- **migrate** - применение миграций
- **api** - основное приложение
- **seed** - заполнение БД тестовыми данными

## Конфигурация

Все настройки можно изменить через переменные окружения в файле `.env` или напрямую в `docker-compose.yml`.

## Команды

### Запуск

```bash
docker compose up -d
```

### Остановка

```bash
docker compose down
```

### Просмотр логов

```bash
docker compose logs -f api
```

### Пересборка

```bash
docker compose build
docker compose up -d
```

### Применение миграций вручную

```bash
docker compose exec migrate migrate -path /migrations -database "postgres://user:pass@postgres:5432/school_db?sslmode=disable" up
```

### Заполнение БД данными

```bash
docker compose exec api /app/seed
```

## Production развертывание

Для production рекомендуется:

1. Использовать секреты для паролей и токенов
2. Настроить reverse proxy (nginx)
3. Использовать SSL/TLS сертификаты
4. Настроить мониторинг и логирование
5. Использовать managed PostgreSQL вместо контейнера

