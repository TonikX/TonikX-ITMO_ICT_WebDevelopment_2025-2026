# Endpoints: Задачи

## Получить список задач

### GET `/api/tasks/`

Возвращает список всех задач.

**Права доступа:** Аутентифицированные пользователи

**Параметры запроса:**
- Нет

**Ответ 200 OK:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Разработка мобильного приложения",
      "description": "Создать мобильное приложение для управления задачами",
      "created_by": 1,
      "created_by_username": "admin",
      "curator": 2,
      "curator_username": "curator1",
      "consultation_link": "https://zoom.us/j/123456789",
      "files": [],
      "links": [],
      "teams_count": 5,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

## Получить задачу

### GET `/api/tasks/{id}/`

Возвращает детальную информацию о задаче.

**Права доступа:** Аутентифицированные пользователи

**Ответ 200 OK:**
```json
{
  "id": 1,
  "title": "Разработка мобильного приложения",
  "description": "Создать мобильное приложение для управления задачами",
  "created_by": 1,
  "created_by_username": "admin",
  "curator": 2,
  "curator_username": "curator1",
  "consultation_link": "https://zoom.us/j/123456789",
  "files": [
    {
      "id": 1,
      "file": "/media/task_files/requirements.pdf",
      "file_url": "http://localhost:8000/media/task_files/requirements.pdf",
      "name": "Требования к проекту",
      "uploaded_at": "2024-01-01T13:00:00Z"
    }
  ],
  "links": [
    {
      "id": 1,
      "url": "https://example.com/docs",
      "title": "Документация API",
      "created_at": "2024-01-01T13:00:00Z"
    }
  ],
  "teams_count": 5,
  "solutions": [...],
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

## Создать задачу

### POST `/api/tasks/`

Создает новую задачу.

**Права доступа:** Только главный администратор

**Тело запроса:**
```json
{
  "title": "Новая задача",
  "description": "Описание задачи",
  "curator": null
}
```

**Ответ 201 Created:**
```json
{
  "id": 2,
  "title": "Новая задача",
  "description": "Описание задачи",
  "created_by": 1,
  "created_by_username": "admin",
  "curator": null,
  "curator_username": null,
  "consultation_link": null,
  "files": [],
  "links": [],
  "teams_count": 0,
  "created_at": "2024-01-01T14:00:00Z",
  "updated_at": "2024-01-01T14:00:00Z"
}
```

## Обновить задачу

### PATCH `/api/tasks/{id}/`

Обновляет задачу (например, назначение куратора).

**Права доступа:** Только главный администратор

**Тело запроса:**
```json
{
  "curator": 2
}
```

## Добавить файл к задаче

### POST `/api/tasks/{id}/add_file/`

Добавляет файл к задаче.

**Права доступа:** Только куратор этой задачи

**Тело запроса (multipart/form-data):**
```
task: 1
file: <файл>
name: "Название файла"
```

**Ответ 201 Created:**
```json
{
  "id": 2,
  "task": 1,
  "file": "/media/task_files/new_file.pdf",
  "file_url": "http://localhost:8000/media/task_files/new_file.pdf",
  "name": "Название файла",
  "uploaded_at": "2024-01-01T15:00:00Z"
}
```

## Добавить ссылку к задаче

### POST `/api/tasks/{id}/add_link/`

Добавляет ссылку к задаче.

**Права доступа:** Только куратор этой задачи

**Тело запроса:**
```json
{
  "url": "https://example.com/resource",
  "title": "Полезный ресурс"
}
```

**Ответ 201 Created:**
```json
{
  "id": 2,
  "task": 1,
  "url": "https://example.com/resource",
  "title": "Полезный ресурс",
  "created_at": "2024-01-01T15:00:00Z"
}
```

## Установить ссылку на консультацию

### PATCH `/api/tasks/{id}/set_consultation_link/`

Устанавливает ссылку на консультацию для задачи.

**Права доступа:** Только куратор этой задачи

**Тело запроса:**
```json
{
  "consultation_link": "https://zoom.us/j/987654321"
}
```

**Ответ 200 OK:**
```json
{
  "id": 1,
  "consultation_link": "https://zoom.us/j/987654321",
  ...
}
```

## Управление файлами задач

### GET `/api/task-files/`

Получить список файлов задач.

**Параметры запроса:**
- `task` - ID задачи для фильтрации

### DELETE `/api/task-files/{id}/`

Удалить файл задачи.

**Права доступа:** Только куратор задачи

## Управление ссылками задач

### GET `/api/task-links/`

Получить список ссылок задач.

**Параметры запроса:**
- `task` - ID задачи для фильтрации

### DELETE `/api/task-links/{id}/`

Удалить ссылку задачи.

**Права доступа:** Только куратор задачи
