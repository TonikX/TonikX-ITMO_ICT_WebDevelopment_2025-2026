# Архитектура

## Обзор

Проект построен на Clean Architecture с разделением на слои:

```
├── cmd/api/              # Точка входа
├── internal/
│   ├── config/           # Конфигурация
│   ├── domain/           # Бизнес-логика (интерфейсы)
│   ├── usecase/          # Сценарии использования
│   ├── infrastructure/   # Реализация (БД, JWT)
│   └── delivery/http/    # HTTP handlers
├── migrations/           # SQL миграции
└── tests/               # Тесты
```

## Слои

### Domain Layer

Содержит:
- Интерфейсы репозиториев
- Интерфейсы use cases
- Структуры данных (entities)
- Доменные ошибки

Не зависит от внешних библиотек.

### Use Case Layer

Реализует бизнес-логику:
- CRUD операции
- Валидация
- Координация между репозиториями

Зависит только от domain интерфейсов.

### Infrastructure Layer

Реализует технические детали:
- PostgreSQL репозитории
- JWT сервис
- Bcrypt хеширование паролей
- Логирование

### Delivery Layer

HTTP обработка:
- Chi Router
- Handlers
- Middleware (auth, CORS, logging)

## Зависимости

```
Delivery → Use Case → Domain ← Infrastructure
```

Зависимости направлены внутрь к domain слою.

## Ключевые компоненты

### Аутентификация

- JWT токены (access + refresh)
- Bcrypt хеширование паролей
- Role-based access control (RBAC)

### База данных

- PostgreSQL 18
- Connection pooling
- Миграции через golang-migrate

### HTTP сервер

- Chi Router
- Middleware: logging, CORS, auth
- Graceful shutdown

## Технологии

- **Go**: 1.25
- **Chi**: HTTP router
- **PostgreSQL**: База данных
- **JWT**: Аутентификация
- **Swagger**: Документация API
- **Docker**: Контейнеризация

