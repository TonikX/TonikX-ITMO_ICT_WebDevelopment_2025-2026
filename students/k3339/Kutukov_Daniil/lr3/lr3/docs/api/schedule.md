# Расписание

Управление расписанием занятий.

**Базовый URL:** `/api/schedules/`  
**Требуется аутентификация:** Да

## Модель Schedule

| Поле | Тип | Описание |
|------|-----|----------|
| id | integer | ID записи расписания |
| group | integer | ID группы |
| subject | integer | ID дисциплины |
| teacher | integer | ID преподавателя |
| classroom | integer | ID кабинета |
| day_of_week | integer | День недели (1-6) |
| lesson_number | integer | Номер урока (1-6) |

## Список записей расписания

**URL:** `/api/schedules/`  
**Метод:** `GET`

### Ответ (200 OK)

```json
[
  {
    "id": 1,
    "group": {
      "id": 1,
      "name": "ПИ-11",
      "course": 1,
      "enrollment_year": 2024
    },
    "subject": {
      "id": 1,
      "name": "Математический анализ",
      "total_hours": 144
    },
    "teacher": {
      "id": 1,
      "last_name": "Иванов",
      "first_name": "Иван",
      "middle_name": "Иванович",
      "position": "Профессор"
    },
    "classroom": {
      "id": 1,
      "number": "Л-1",
      "capacity": 110
    },
    "day_of_week": 1,
    "day_name": "Понедельник",
    "lesson_number": 1
  }
]
```

## Создание записи расписания

**URL:** `/api/schedules/`  
**Метод:** `POST`

### Запрос

```json
{
  "group": 1,
  "subject": 1,
  "teacher": 1,
  "classroom": 1,
  "day_of_week": 1,
  "lesson_number": 1
}
```

### Ответ (201 Created)

```json
{
  "id": 10,
  "group": 1,
  "subject": 1,
  "teacher": 1,
  "classroom": 1,
  "day_of_week": 1,
  "lesson_number": 1
}
```

## Получить расписание группы на день

**URL:** `/api/schedules/group_day_schedule/`  
**Метод:** `GET`  
**Параметры:** `group` (ID группы), `day` (день недели 1-6)

### Пример запроса

```
GET /api/schedules/group_day_schedule/?group=1&day=1
```

### Ответ (200 OK)

```json
{
  "group": {
    "id": 1,
    "name": "ПИ-11",
    "course": 1,
    "enrollment_year": 2024
  },
  "day_of_week": 1,
  "day_name": "Понедельник",
  "lessons": [
    {
      "id": 1,
      "subject": {
        "id": 1,
        "name": "Математический анализ",
        "total_hours": 144
      },
      "teacher": {
        "id": 1,
        "last_name": "Иванов",
        "first_name": "Иван",
        "middle_name": "Иванович",
        "position": "Профессор"
      },
      "classroom": {
        "id": 1,
        "number": "Л-1",
        "capacity": 110
      },
      "lesson_number": 1
    },
    {
      "id": 2,
      "subject": {
        "id": 2,
        "name": "Программирование",
        "total_hours": 180
      },
      "teacher": {
        "id": 2,
        "last_name": "Петрова",
        "first_name": "Мария",
        "middle_name": "Сергеевна",
        "position": "Доцент"
      },
      "classroom": {
        "id": 10,
        "number": "К-1",
        "capacity": 15
      },
      "lesson_number": 2
    }
  ]
}
```

## Получить информацию о конкретном уроке

**URL:** `/api/schedules/lesson_info/`  
**Метод:** `GET`  
**Параметры:** `group` (ID группы), `day` (день недели), `lesson` (номер урока)

### Пример запроса

```
GET /api/schedules/lesson_info/?group=1&day=1&lesson=1
```

### Ответ (200 OK)

```json
{
  "id": 1,
  "group": {
    "id": 1,
    "name": "ПИ-11",
    "course": 1,
    "enrollment_year": 2024
  },
  "subject": {
    "id": 1,
    "name": "Математический анализ",
    "total_hours": 144
  },
  "teacher": {
    "id": 1,
    "last_name": "Иванов",
    "first_name": "Иван",
    "middle_name": "Иванович",
    "position": "Профессор"
  },
  "classroom": {
    "id": 1,
    "number": "Л-1",
    "capacity": 110
  },
  "day_of_week": 1,
  "day_name": "Понедельник",
  "lesson_number": 1
}
```

## Обновление записи расписания

**URL:** `/api/schedules/{id}/`  
**Методы:** `PUT`, `PATCH`

### Запрос (PATCH)

```json
{
  "classroom": 5
}
```

### Ответ (200 OK)

```json
{
  "id": 1,
  "group": 1,
  "subject": 1,
  "teacher": 1,
  "classroom": 5,
  "day_of_week": 1,
  "lesson_number": 1
}
```

## Удаление записи расписания

**URL:** `/api/schedules/{id}/`  
**Метод:** `DELETE`

### Ответ (204 No Content)

Запись удалена.

## Ограничения

- Для одной группы не может быть двух занятий одновременно (день + урок)
- День недели: 1 (Понедельник) - 6 (Суббота)
- Номер урока: 1-6
