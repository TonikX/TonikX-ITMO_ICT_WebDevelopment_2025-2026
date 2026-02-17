# Лабораторная работа 4: Интерфейсы

## Общая схема приложения

Frontend построен на Vue Router и разделен на страницы:

- `/` — главная
- `/login` — вход
- `/register` — регистрация
- `/profile` — профиль пользователя
- `/tasks` и `/tasks/:id` — задачи
- `/teams` и `/teams/:id` — команды
- `/solutions` и `/solutions/:id` — решения
- `/evaluations` — раздел оценок (для роли `jury`)

## Навигация и доступ

Компонент `Navigation.vue` отображает пункты меню в зависимости от авторизации и роли:

- Гость: `Вход`, `Регистрация`
- Авторизованный пользователь: `Профиль`, `Задачи`, `Команды`, `Решения`
- Роль `jury`: дополнительно `Оценки`

## Авторизация и профиль

### Вход (`/login`)

- Поля: `email`, `password`
- Запрос: `POST /api/auth/token/login/`
- После успеха:
  - токен сохраняется в `localStorage.authToken`
  - данные пользователя загружаются через `GET /api/auth/users/me/`

### Регистрация (`/register`)

- Запрос: `POST /api/auth/users/`
- Поддерживаемые поля: `username`, `email`, `first_name`, `last_name`, `role`, `password`, `password_retype`

### Профиль (`/profile`)

- Загрузка профиля: `GET /api/auth/users/me/`
- Обновление: `PATCH /api/auth/users/me/`
- Редактируемые поля: `username`, `email`, `first_name`, `last_name`

## Интерфейс задач

### Страница списка (`/tasks`)

- Получение списка: `GET /api/tasks/`
- Для роли `admin` доступна форма создания:
  - `POST /api/tasks/`
  - Передаются `title`, `description`, `created_by`

### Карточка задачи (`/tasks/:id`)

- Детали: `GET /api/tasks/{id}/`
- Для куратора текущей задачи доступны действия:
  - добавить файл: `POST /api/tasks/{id}/add_file/`
  - добавить ссылку: `POST /api/tasks/{id}/add_link/`
  - установить ссылку консультации: `PATCH /api/tasks/{id}/set_consultation_link/`

## Интерфейс команд

### Страница списка (`/teams`)

- Получение списка: `GET /api/teams/`
- Для роли `captain` доступно создание:
  - `POST /api/teams/`
  - Передаются `name`, `motto`, `captain`

### Карточка команды (`/teams/:id`)

- Детали: `GET /api/teams/{id}/`
- Если капитан просматривает свою команду, доступны:
  - выбор задачи: `PATCH /api/teams/{id}/select_task/`
  - добавление участника: `POST /api/teams/{id}/add_member/`

## Интерфейс решений

### Страница списка (`/solutions`)

- Получение списка: `GET /api/solutions/`
- Для `captain` доступна отправка решения:
  - `POST /api/solutions/`
  - Передаются `team`, `task`, `description`, опционально `file`

### Карточка решения (`/solutions/:id`)

- Детали: `GET /api/solutions/{id}/`
- Для `jury` доступна форма оценки:
  - `POST /api/evaluations/`
  - Передаются `solution`, `jury`, `score`, `comment`

## Интерфейс оценок (`/evaluations`)

Раздел доступен роли `jury`:

- решения по дате: `GET /api/evaluations/solutions_by_date/`
- свои оценки: `GET /api/evaluations/my_evaluations/`

## Особенности интеграции с backend

- Для списков в DRF используется пагинация, frontend поддерживает ответы в формате `results`.
- Для запросов с авторизацией используется заголовок `Authorization: Token <token>`.
- При `401` токен сбрасывается, пользователь отправляется на `/login`.
