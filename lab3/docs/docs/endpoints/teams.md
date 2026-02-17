# Endpoints: Команды

## Получить список команд

### GET `/api/teams/`

Возвращает список команд.

**Права доступа:** Аутентифицированные пользователи

**Особенности:**
- Капитаны видят только свою команду
- Остальные роли видят все команды

**Ответ 200 OK:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Команда Победителей",
      "captain": 1,
      "captain_username": "captain1",
      "captain_email": "captain1@example.com",
      "motto": "Мы лучшие!",
      "selected_task": 1,
      "selected_task_title": "Разработка мобильного приложения",
      "members": [
        {
          "id": 1,
          "first_name": "Иван",
          "last_name": "Иванов",
          "email": "ivan@example.com",
          "created_at": "2024-01-01T12:00:00Z"
        }
      ],
      "members_count": 3,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

## Получить команду

### GET `/api/teams/{id}/`

Возвращает детальную информацию о команде, включая решения.

**Права доступа:** Аутентифицированные пользователи

**Ответ 200 OK:**
```json
{
  "id": 1,
  "name": "Команда Победителей",
  "captain": 1,
  "captain_username": "captain1",
  "captain_email": "captain1@example.com",
  "motto": "Мы лучшие!",
  "selected_task": 1,
  "selected_task_title": "Разработка мобильного приложения",
  "members": [...],
  "members_count": 3,
  "solutions": [
    {
      "id": 1,
      "team": 1,
      "team_name": "Команда Победителей",
      "task": 1,
      "task_title": "Разработка мобильного приложения",
      "description": "Описание решения",
      "file": "/media/solutions/solution.zip",
      "file_url": "http://localhost:8000/media/solutions/solution.zip",
      "evaluations_count": 2,
      "average_score": 8.5,
      "published_at": "2024-01-02T10:00:00Z",
      "updated_at": "2024-01-02T10:00:00Z"
    }
  ],
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

## Создать команду

### POST `/api/teams/`

Создает новую команду. Капитан автоматически назначается из текущего пользователя.

**Права доступа:** Только капитаны

**Тело запроса:**
```json
{
  "name": "Моя команда",
  "motto": "Девиз команды"
}
```

**Ответ 201 Created:**
```json
{
  "id": 2,
  "name": "Моя команда",
  "captain": 1,
  "captain_username": "captain1",
  "captain_email": "captain1@example.com",
  "motto": "Девиз команды",
  "selected_task": null,
  "selected_task_title": null,
  "members": [],
  "members_count": 0,
  "created_at": "2024-01-01T16:00:00Z",
  "updated_at": "2024-01-01T16:00:00Z"
}
```

## Обновить команду

### PATCH `/api/teams/{id}/`

Обновляет информацию о команде.

**Права доступа:** Только капитан этой команды

**Тело запроса:**
```json
{
  "name": "Обновленное название",
  "motto": "Новый девиз"
}
```

## Выбрать задачу

### PATCH `/api/teams/{id}/select_task/`

Выбирает задачу для команды.

**Права доступа:** Только капитан этой команды

**Тело запроса:**
```json
{
  "task_id": 1
}
```

**Ответ 200 OK:**
```json
{
  "id": 1,
  "selected_task": 1,
  "selected_task_title": "Разработка мобильного приложения",
  ...
}
```

## Добавить участника в команду

### POST `/api/teams/{id}/add_member/`

Добавляет участника в команду.

**Права доступа:** Только капитан этой команды

**Тело запроса:**
```json
{
  "first_name": "Петр",
  "last_name": "Петров",
  "email": "petr@example.com"
}
```

**Ответ 201 Created:**
```json
{
  "id": 2,
  "team": 1,
  "first_name": "Петр",
  "last_name": "Петров",
  "email": "petr@example.com",
  "created_at": "2024-01-01T17:00:00Z"
}
```

## Управление участниками команды

### GET `/api/team-members/`

Получить список участников команд.

**Параметры запроса:**
- `team` - ID команды для фильтрации

**Особенности:**
- Капитаны видят только участников своей команды

### POST `/api/team-members/`

Создать участника команды.

**Права доступа:** Только капитан команды

**Тело запроса:**
```json
{
  "team": 1,
  "first_name": "Сергей",
  "last_name": "Сергеев",
  "email": "sergey@example.com"
}
```

### PATCH `/api/team-members/{id}/`

Обновить информацию об участнике.

**Права доступа:** Только капитан команды

### DELETE `/api/team-members/{id}/`

Удалить участника из команды.

**Права доступа:** Только капитан команды
