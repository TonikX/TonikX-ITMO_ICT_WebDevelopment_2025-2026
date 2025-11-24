# КурКод - Backend (Spring Boot)

Backend-часть системы управления птицефермой. Реализует REST API для работы с пользователями, ролями, курами, сотрудниками, контрактами, цехами, клетками и аналитическими отчетами.

## Содержание

- [Описание](#описание)
- [Технологии](#технологии)
- [Требования](#требования)
- [Быстрый старт](#быстрый-старт)
  - [Запуск через Docker](#запуск-через-docker)
  - [Локальный запуск](#локальный-запуск)
- [Структура проекта](#структура-проекта)
- [Конфигурация](#конфигурация)
- [База данных и миграции](#база-данных-и-миграции)
- [API Документация](#api-документация)
- [Безопасность и аутентификация](#безопасность-и-аутентификация)
- [Разработка](#разработка)
- [Типичные проблемы](#типичные-проблемы)

## Описание

КурКод - это система управления птицефермой, которая позволяет:
- Управлять курами, породами и их перемещениями между клетками
- Отслеживать производство яиц по месяцам
- Управлять работниками, их паспортами и трудовыми договорами
- Организовывать структуру цехов, рядов и клеток
- Назначать работников на обслуживание клеток
- Управлять рационами питания
- Получать аналитические отчеты для директора
- Управлять пользователями и ролями с системой аутентификации JWT

## Технологии

### Основной стек
- **Java 21** - язык программирования
- **Spring Boot 3.5.6** - фреймворк
- **PostgreSQL 16** - база данных
- **Liquibase** - управление миграциями БД

### Зависимости
- **Spring Boot Starters:**
  - `spring-boot-starter-web` - REST API
  - `spring-boot-starter-data-jpa` - работа с БД
  - `spring-boot-starter-security` - безопасность
  - `spring-boot-starter-validation` - валидация

- **База данных:**
  - `postgresql` - драйвер PostgreSQL
  - `liquibase-core` - миграции БД

- **Безопасность:**
  - `jjwt-api`, `jjwt-impl`, `jjwt-jackson` (0.11.5) - JWT токены

- **Документация:**
  - `springdoc-openapi-starter-webmvc-ui` (2.8.13) - Swagger UI

- **Утилиты:**
  - `lombok` - уменьшение boilerplate кода
  - `mapstruct` (1.5.5.Final) - маппинг объектов
  - `commons-lang3` (3.18.0) - дополнительные утилиты

## Требования

### Для локального запуска
- **Java 21** (JDK)
- **Maven 3.6+** (или используйте `mvnw` из проекта)
- **PostgreSQL 14+** (локально или в Docker)

### Для Docker
- **Docker** 20.10+
- **Docker Compose** 2.0+

## Быстрый старт

### Запуск через Docker

Самый простой способ запустить приложение - использовать Docker Compose.

#### 1. Клонируйте репозиторий (если еще не сделали)

```bash
git clone <repository-url>
cd kurkod/apps/backend
```

#### 2. Соберите и запустите контейнеры

```bash
# Сборка и запуск
docker-compose up --build

# Или в фоновом режиме
docker-compose up -d --build
```

#### 3. Проверьте статус

```bash
# Просмотр логов
docker-compose logs -f app

# Проверка статуса контейнеров
docker-compose ps
```

#### 4. Доступ к приложению

После запуска приложение будет доступно по адресу:
- **API**: http://localhost:8080
- **Swagger UI**: http://localhost:8080/swagger-ui.html
- **PostgreSQL**: localhost:5432

#### 5. Остановка

```bash
# Остановка контейнеров
docker-compose down

# Остановка с удалением volumes (удалит данные БД)
docker-compose down -v
```

#### Конфигурация Docker Compose

В `docker-compose.yml` настроены следующие сервисы:

- **db** (PostgreSQL):
  - Порт: 5432 (внутренний)
  - База данных: `kurkod_db`
  - Пользователь: `kurkod`
  - Пароль: `kurkod`

- **app** (Spring Boot приложение):
  - Порт: 8080
  - Профиль: `dev`
  - Автоматически подключается к БД через переменные окружения

### Локальный запуск

#### 1. Установите зависимости

- Установите **Java 21** (JDK)
- Установите **PostgreSQL 14+** или используйте Docker для БД:
  ```bash
  docker run -d --name postgres -e POSTGRES_DB=kurkod_db -e POSTGRES_USER=kurkod -e POSTGRES_PASSWORD=kurkod -p 5432:5432 postgres:16-alpine
  ```

#### 2. Настройте переменные окружения

Создайте файл `.env` или экспортируйте переменные:

**Windows (cmd.exe):**
```cmd
set SPRING_PROFILES_ACTIVE=dev
set DB_URL=jdbc:postgresql://localhost:5432/kurkod_db
set DB_USER=kurkod
set DB_PASSWORD=kurkod
set SERVER_PORT=8189
set JWT_SECRET=your-secret-key-change-in-production-min-256-bits
set JWT_LIFETIME=PT1H
set JPA_SHOW_SQL=false
set LOG_LEVEL_APP=INFO
```

**Linux/Mac:**
```bash
export SPRING_PROFILES_ACTIVE=dev
export DB_URL=jdbc:postgresql://localhost:5432/kurkod_db
export DB_USER=kurkod
export DB_PASSWORD=kurkod
export SERVER_PORT=8189
export JWT_SECRET=your-secret-key-change-in-production-min-256-bits
export JWT_LIFETIME=PT1H
export JPA_SHOW_SQL=false
export LOG_LEVEL_APP=INFO
```

#### 3. Запустите приложение

**Вариант 1: Через Maven Wrapper (рекомендуется)**
```bash
# Windows
mvnw.cmd spring-boot:run

# Linux/Mac
./mvnw spring-boot:run
```

**Вариант 2: Сборка JAR и запуск**
```bash
# Сборка
mvnw.cmd clean package -DskipTests

# Запуск
java -jar target/kurkod-0.0.1-SNAPSHOT.jar
```

**Вариант 3: Через IDE**
- Откройте проект в IntelliJ IDEA или Eclipse
- Запустите класс `KurkodApplication`

#### 4. Проверьте работу

Откройте в браузере:
- **Swagger UI**: http://localhost:8189/swagger-ui.html
- **API Docs**: http://localhost:8189/v3/api-docs

## Структура проекта

```
src/
├── main/
│   ├── java/io/github/artsobol/kurkod/
│   │   ├── KurkodApplication.java          # Точка входа Spring Boot
│   │   │
│   │   ├── common/                          # Общие утилиты и константы
│   │   │   ├── constants/                   # Константы приложения
│   │   │   ├── enum_converter/              # Конвертеры enum
│   │   │   ├── error/                       # Обработка ошибок
│   │   │   ├── exception/                   # Кастомные исключения
│   │   │   ├── logging/                     # Утилиты логирования
│   │   │   ├── util/                        # Вспомогательные утилиты
│   │   │   └── validation/                  # Валидаторы
│   │   │
│   │   ├── security/                        # Безопасность и JWT
│   │   │   ├── config/                      # Конфигурация Security
│   │   │   ├── error/                       # Ошибки безопасности
│   │   │   ├── facade/                      # Фасады безопасности
│   │   │   ├── filter/                      # JWT фильтры
│   │   │   ├── handler/                     # Обработчики безопасности
│   │   │   ├── jwt/                         # JWT утилиты
│   │   │   └── validation/                  # Валидаторы доступа
│   │   │
│   │   └── web/                             # Web слой
│   │       ├── advice/                      # Глобальные обработчики исключений
│   │       ├── config/                      # Конфигурация web
│   │       ├── controller/                  # REST контроллеры
│   │       │   ├── iam/                     # Аутентификация и пользователи
│   │       │   ├── breed/                   # Породы кур
│   │       │   ├── chicken/                 # Куры
│   │       │   ├── chickenmovement/         # Перемещения кур
│   │       │   ├── worker/                  # Работники
│   │       │   ├── passport/                # Паспорта
│   │       │   ├── employmentcontract/      # Трудовые договоры
│   │       │   ├── staff/                   # Штат
│   │       │   ├── workshop/                # Цеха
│   │       │   ├── rows/                    # Ряды
│   │       │   ├── cage/                    # Клетки
│   │       │   ├── diet/                    # Рационы
│   │       │   ├── eggproductionmonth/      # Производство яиц
│   │       │   ├── dismissal/               # Увольнения
│   │       │   └── report/                  # Отчеты
│   │       │
│   │       ├── cookie/                      # Работа с cookies
│   │       ├── response/                    # Стандартные ответы API
│   │       │
│   │       └── domain/                      # Доменная модель
│   │           ├── auth/                    # Аутентификация
│   │           ├── iam/                     # Identity & Access Management
│   │           │   ├── user/                # Пользователи
│   │           │   ├── role/                # Роли
│   │           │   ├── admin/               # Административные операции
│   │           │   └── refreshtoken/       # Refresh токены
│   │           │
│   │           ├── breed/                   # Породы
│   │           ├── chicken/                 # Куры
│   │           ├── chickenmovement/          # Перемещения кур
│   │           ├── worker/                  # Работники
│   │           ├── passport/                # Паспорта
│   │           ├── employmentcontract/      # Трудовые договоры
│   │           ├── staff/                   # Штат
│   │           ├── workshop/                # Цеха
│   │           ├── rows/                    # Ряды
│   │           ├── cage/                    # Клетки
│   │           ├── diet/                   # Рационы
│   │           ├── eggproductionmonth/      # Производство яиц
│   │           ├── dismissal/               # Увольнения
│   │           └── report/                  # Отчеты
│   │               ├── farm/                # Отчеты по ферме
│   │               ├── breed/                # Отчеты по породам
│   │               ├── chicken/             # Отчеты по курам
│   │               └── worker/              # Отчеты по работникам
│   │
│   └── resources/
│       ├── application.yml                  # Основная конфигурация
│       ├── errors_en.properties            # Сообщения об ошибках (EN)
│       ├── errors_ru.properties            # Сообщения об ошибках (RU)
│       └── db/
│           └── changelog/                  # Миграции Liquibase
│               ├── db.changelog-master.yaml
│               └── changeset/
│                   └── 1.0/                # Версия 1.0 миграций
│                       ├── 001-create-breed.yaml
│                       ├── 002-create-chicken.yaml
│                       ├── 003-create-staff.yaml
│                       └── ...             # Остальные миграции
│
└── test/                                    # Тесты
    └── java/io/github/artsobol/kurkod/
```

### Архитектура доменов

Каждый домен (breed, chicken, worker и т.д.) следует единой структуре:

```
domain/
└── {domain}/
    ├── error/                    # Специфичные ошибки домена
    ├── mapper/                   # MapStruct мапперы (Entity <-> DTO)
    ├── model/
    │   ├── dto/                  # Data Transfer Objects
    │   ├── entity/                # JPA сущности
    │   └── request/               # Request модели (Post, Put, Patch)
    ├── repository/                # JPA репозитории
    └── service/
        ├── api/                   # Интерфейсы сервисов
        └── impl/                  # Реализации сервисов
```

## Конфигурация

### Файлы конфигурации

Основной файл конфигурации: `src/main/resources/application.yml`

### Переменные окружения

Все настройки можно переопределить через переменные окружения:

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `SPRING_PROFILES_ACTIVE` | Активный профиль Spring | `dev` |
| `SERVER_PORT` | Порт приложения | `8189` |
| `DB_URL` | URL базы данных | - |
| `DB_USER` | Пользователь БД | - |
| `DB_PASSWORD` | Пароль БД | - |
| `JWT_SECRET` | Секретный ключ для JWT | - |
| `JWT_LIFETIME` | Время жизни access токена | `PT1H` (1 час) |
| `JPA_SHOW_SQL` | Показывать SQL запросы | `true` |
| `LOG_LEVEL_APP` | Уровень логирования приложения | `TRACE` |
| `LOG_LEVEL_WEB` | Уровень логирования web | `DEBUG` |
| `LOG_LEVEL_SQL` | Уровень логирования SQL | `DEBUG` |
| `SWAGGER_SERVER` | URL сервера для Swagger | `http://localhost:${server.port}` |

### Профили Spring

- **dev** (по умолчанию) - разработка, подробное логирование
- **prod** - продакшн, минимальное логирование

### Важные замечания

 **Безопасность**: Никогда не храните секреты и пароли в репозитории. Используйте переменные окружения или секретные менеджеры.

 **JWT_SECRET**: Должен быть минимум 256 бит (32 символа) для безопасности. В продакшне используйте криптографически стойкий ключ.

## База данных и миграции

### Liquibase

Проект использует **Liquibase** для управления миграциями БД. Миграции находятся в `src/main/resources/db/changelog/`.

### Автоматическое применение

Миграции применяются автоматически при старте приложения, если:
- База данных существует
- Указаны корректные credentials
- Liquibase включен (`spring.liquibase.enabled=true`)

### Структура миграций

Миграции организованы по версиям в директории `changeset/1.0/`:
- `001-create-breed.yaml` - создание таблицы пород
- `002-create-chicken.yaml` - создание таблицы кур
- `003-create-staff.yaml` - создание таблицы штата
- `004-create-worker.yaml` - создание таблицы работников
- `005-create-employment-contract.yaml` - трудовые договоры
- `006-create-passport.yaml` - паспорта
- `007-create-users.yaml` - пользователи
- `008-create-role.yaml` - роли
- `009-create-user-role.yaml` - связь пользователей и ролей
- `010-insert-roles.yaml` - начальные роли
- `011-create-workshop.yaml` - цеха
- `012-create-rows.yaml` - ряды
- `013-create-cage.yaml` - клетки
- `014-create-egg-production-month.yaml` - производство яиц
- `015-create-chicken-movement.yaml` - перемещения кур
- `016-create-dismissal.yaml` - увольнения
- `017-create-current-chicken-position-view.yaml` - представление текущих позиций
- `018-create-report-chicken-by-workshop-and-breed-view.yaml` - отчетное представление
- `019-create-refresh-token.yaml` - refresh токены
- `020-create-report-breed-by-avg-diff-view.yaml` - отчет по породам
- `021-create-report-chicken-eggs-stats-view.yaml` - статистика яиц
- `022-add-cage-field-by-chicken.yaml` - добавление поля клетки
- `023-create-chicken-cage-check-function.yaml` - функция проверки
- `024-create-chicken-cage-check-trigger.yaml` - триггер проверки
- `025-create-worker-cage.yaml` - назначение клеток работникам
- `026-create-diet.yaml` - рационы
- `027-create-breed-diet.yaml` - связь пород и рационов
- `028-create-breed-egg-diff-report.yaml` - отчет по разнице пород

### Первый запуск

При первом запуске:
1. Создайте пустую базу данных `kurkod_db`
2. Укажите корректные credentials в переменных окружения
3. Запустите приложение - Liquibase создаст всю схему автоматически

## API Документация

### Swagger UI

Интерактивная документация API доступна после запуска приложения:
- **URL**: http://localhost:8189/swagger-ui.html (локально)
- **URL**: http://localhost:8080/swagger-ui.html (Docker)

Swagger UI позволяет:
- Просматривать все доступные эндпоинты
- Тестировать API прямо в браузере
- Видеть схемы запросов и ответов
- Авторизоваться через JWT токен

### OpenAPI JSON

Спецификация OpenAPI в формате JSON:
- **URL**: http://localhost:8189/v3/api-docs

### Подробная документация

Полная документация всех эндпоинтов находится в файле:
- **[docs/API.md](docs/API.md)**

### Основные эндпоинты

- **Аутентификация**: `/auth/*`
- **Пользователи**: `/api/v1/users/*`
- **Работники**: `/api/v1/workers/*`
- **Куры**: `/api/v1/chickens/*`
- **Породы**: `/api/v1/breeds/*`
- **Цеха**: `/api/v1/workshops/*`
- **Ряды**: `/api/v1/workshops/{workshopId}/rows/*`
- **Клетки**: `/api/v1/rows/{rowId}/cage/*`
- **Отчеты**: `/api/v1/reports/director/*`

Полный список см. в [docs/API.md](docs/API.md).

## Безопасность и аутентификация

### JWT (JSON Web Tokens)

Приложение использует JWT для аутентификации:
- **Access Token** - короткоживущий токен для доступа к API
- **Refresh Token** - долгоживущий токен для обновления access token

### Получение токена

1. **Регистрация**:
   ```http
   POST /auth/register
   Content-Type: application/json
   
   {
     "username": "user",
     "email": "user@example.com",
     "password": "password",
     "confirmPassword": "password"
   }
   ```

2. **Вход**:
   ```http
   POST /auth/login
   Content-Type: application/json
   
   {
     "email": "user@example.com",
     "password": "password"
   }
   ```

3. **Обновление токена**:
   ```http
   GET /auth/refresh/token?token=<refreshToken>
   ```

### Использование токена

После получения токена, передавайте его в заголовке:
```http
Authorization: Bearer <access-token>
```

Или используйте cookie `Authorization` (HttpOnly, Secure), которая устанавливается автоматически.

### Роли

Система поддерживает следующие роли:
- `ROLE_USER` - обычный пользователь
- `ROLE_DIRECTOR` - директор (доступ к отчетам)
- `ROLE_SUPER_ADMIN` - супер администратор

### Оптимистичная блокировка

Для операций обновления и удаления используется оптимистичная блокировка через ETag:
1. Получите ресурс (в заголовке ответа будет `ETag`)
2. При обновлении передайте `If-Match: <etag>` в заголовке запроса
3. Если версия изменилась, получите ошибку 412 Precondition Failed

## Разработка

### Сборка проекта

```bash
# Полная сборка с тестами
mvnw.cmd clean verify

# Сборка без тестов
mvnw.cmd clean package -DskipTests

# Только тесты
mvnw.cmd test
```

### Форматирование кода

Проект использует стандартные настройки форматирования Java. Рекомендуется настроить автоформатирование в IDE.

### Логирование

Уровни логирования настраиваются через переменные окружения:
- `LOG_LEVEL_APP` - логи приложения
- `LOG_LEVEL_WEB` - логи Spring Web
- `LOG_LEVEL_SQL` - SQL запросы
- `LOG_LEVEL_BINDER` - биндинг параметров
- `LOG_LEVEL_DISPATCHER` - DispatcherServlet

### Тестирование

```bash
# Запуск всех тестов
mvnw.cmd test

# Запуск конкретного теста
mvnw.cmd test -Dtest=ClassNameTest

# Запуск с покрытием (требует плагин)
mvnw.cmd clean test jacoco:report
```

### Добавление нового домена

1. Создайте структуру в `web/domain/{domain}/`
2. Добавьте Entity, DTO, Request модели
3. Создайте Repository, Service (api + impl)
4. Создайте Mapper (MapStruct)
5. Создайте Controller
6. Добавьте миграцию Liquibase
7. Добавьте обработку ошибок в `error/`

## Типичные проблемы

### Проблема: Connection refused к БД

**Решение:**
- Проверьте, что PostgreSQL запущен
- Проверьте правильность `DB_URL`, `DB_USER`, `DB_PASSWORD`
- Для Docker: убедитесь, что контейнер БД запущен (`docker-compose ps`)

### Проблема: Liquibase ошибки миграций

**Решение:**
- Убедитесь, что база данных пуста при первом запуске
- Проверьте, что все миграции в правильном порядке
- Очистите таблицу `databasechangelog` если нужно пересоздать схему

### Проблема: Access denied при вызове эндпоинтов

**Решение:**
- Получите JWT токен через `/auth/login` или `/auth/register`
- Передавайте токен в заголовке `Authorization: Bearer <token>`
- Проверьте, что токен не истек
- Убедитесь, что у пользователя есть нужные роли

### Проблема: Swagger UI не открывается

**Решение:**
- Проверьте, что приложение запущено на правильном порту
- Проверьте `SWAGGER_SERVER` в переменных окружения
- Убедитесь, что `springdoc-openapi` в зависимостях

### Проблема: Ошибка 412 Precondition Failed

**Решение:**
- Это нормальное поведение при конфликте версий (оптимистичная блокировка)
- Получите актуальную версию ресурса (GET запрос)
- Используйте новый ETag из заголовка ответа

### Проблема: Docker контейнер не запускается

**Решение:**
- Проверьте логи: `docker-compose logs app`
- Убедитесь, что порт 8080 свободен
- Проверьте, что Dockerfile правильно собран
- Убедитесь, что JAR файл существует: `mvnw.cmd clean package -DskipTests`

### Проблема: JWT ошибки

**Решение:**
- Проверьте, что `JWT_SECRET` установлен и достаточно длинный (минимум 32 символа)
- Убедитесь, что используется тот же секрет для генерации и проверки токенов
- Проверьте время жизни токена (`JWT_LIFETIME`)

## Дополнительная информация

### Версии

- **Java**: 21
- **Spring Boot**: 3.5.6
- **PostgreSQL**: 16 (в Docker)
- **Liquibase**: последняя версия из Spring Boot

