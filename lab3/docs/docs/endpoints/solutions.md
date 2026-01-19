# Endpoints: Решения

## Получить список решений

### GET `/api/solutions/`

Возвращает список решений.

**Права доступа:** Аутентифицированные пользователи

**Особенности:**
- Капитаны видят только решения своей команды
- Кураторы видят решения по своей задаче
- Жюри и админы видят все решения

**Ответ 200 OK:**
```json
{
  "count": 20,
  "next": "http://localhost:8000/api/solutions/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "team": 1,
      "team_name": "Команда Победителей",
      "task": 1,
      "task_title": "Разработка мобильного приложения",
      "description": "Описание решения команды",
      "file": "/media/solutions/solution1.zip",
      "file_url": "http://localhost:8000/media/solutions/solution1.zip",
      "evaluations_count": 3,
      "average_score": 8.33,
      "published_at": "2024-01-02T10:00:00Z",
      "updated_at": "2024-01-02T10:00:00Z"
    }
  ]
}
```

## Получить решение

### GET `/api/solutions/{id}/`

Возвращает детальную информацию о решении, включая все оценки.

**Права доступа:** 
- Капитан команды (только свое решение)
- Куратор задачи (только решения по своей задаче)
- Жюри (все решения)
- Главный админ (все решения)

**Ответ 200 OK:**
```json
{
  "id": 1,
  "team": 1,
  "team_name": "Команда Победителей",
  "task": 1,
  "task_title": "Разработка мобильного приложения",
  "description": "Подробное описание решения команды...",
  "file": "/media/solutions/solution1.zip",
  "file_url": "http://localhost:8000/media/solutions/solution1.zip",
  "evaluations_count": 3,
  "average_score": 8.33,
  "evaluations": [
    {
      "id": 1,
      "solution": 1,
      "solution_team_name": "Команда Победителей",
      "solution_task_title": "Разработка мобильного приложения",
      "jury": 3,
      "jury_username": "jury1",
      "score": 9,
      "comment": "Отличное решение!",
      "created_at": "2024-01-03T10:00:00Z",
      "updated_at": "2024-01-03T10:00:00Z"
    },
    {
      "id": 2,
      "solution": 1,
      "solution_team_name": "Команда Победителей",
      "solution_task_title": "Разработка мобильного приложения",
      "jury": 4,
      "jury_username": "jury2",
      "score": 8,
      "comment": "Хорошая работа, но есть что улучшить",
      "created_at": "2024-01-03T11:00:00Z",
      "updated_at": "2024-01-03T11:00:00Z"
    }
  ],
  "published_at": "2024-01-02T10:00:00Z",
  "updated_at": "2024-01-02T10:00:00Z"
}
```

## Создать решение

### POST `/api/solutions/`

Создает новое решение. Команда автоматически назначается из капитана.

**Права доступа:** Только капитаны

**Тело запроса (multipart/form-data):**
```
task: 1
description: "Описание решения"
file: <файл решения> (опционально)
```

**Ответ 201 Created:**
```json
{
  "id": 2,
  "team": 1,
  "team_name": "Команда Победителей",
  "task": 1,
  "task_title": "Разработка мобильного приложения",
  "description": "Описание решения",
  "file": "/media/solutions/solution2.zip",
  "file_url": "http://localhost:8000/media/solutions/solution2.zip",
  "evaluations_count": 0,
  "average_score": null,
  "published_at": "2024-01-02T18:00:00Z",
  "updated_at": "2024-01-02T18:00:00Z"
}
```

**Ошибки:**
- `400 Bad Request` - Если решение для этой задачи уже существует
- `400 Bad Request` - Если команда не выбрала задачу

## Обновить решение

### PATCH `/api/solutions/{id}/`

Обновляет решение.

**Права доступа:** Только капитан команды, которой принадлежит решение

**Тело запроса:**
```json
{
  "description": "Обновленное описание решения"
}
```

## Удалить решение

### DELETE `/api/solutions/{id}/`

Удаляет решение.

**Права доступа:** Только капитан команды, которой принадлежит решение

**Ответ 204 No Content**

## Получить оценки решения

### GET `/api/solutions/{id}/evaluations/`

Возвращает все оценки для конкретного решения.

**Права доступа:** Те же, что и для просмотра решения

**Ответ 200 OK:**
```json
[
  {
    "id": 1,
    "solution": 1,
    "solution_team_name": "Команда Победителей",
    "solution_task_title": "Разработка мобильного приложения",
    "jury": 3,
    "jury_username": "jury1",
    "score": 9,
    "comment": "Отличное решение!",
    "created_at": "2024-01-03T10:00:00Z",
    "updated_at": "2024-01-03T10:00:00Z"
  }
]
```
