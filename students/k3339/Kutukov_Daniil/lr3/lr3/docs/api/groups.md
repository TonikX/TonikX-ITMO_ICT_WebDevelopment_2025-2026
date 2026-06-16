# Группы

Управление учебными группами.

**Базовый URL:** `/api/groups/`  
**Требуется аутентификация:** Да

## Модель Group

| Поле | Тип | Описание |
|------|-----|----------|
| id | integer | ID группы |
| name | string | Название группы |
| course | integer | Курс (1-4) |
| enrollment_year | integer | Год поступления |

## Список групп

**URL:** `/api/groups/`  
**Метод:** `GET`

### Ответ (200 OK)

```json
[
  {
    "id": 1,
    "name": "ПИ-11",
    "course": 1,
    "enrollment_year": 2024
  },
  {
    "id": 2,
    "name": "ПИ-12",
    "course": 1,
    "enrollment_year": 2024
  }
]
```

## Создание группы

**URL:** `/api/groups/`  
**Метод:** `POST`

### Запрос

```json
{
  "name": "ПИ-13",
  "course": 1,
  "enrollment_year": 2024
}
```

### Ответ (201 Created)

```json
{
  "id": 3,
  "name": "ПИ-13",
  "course": 1,
  "enrollment_year": 2024
}
```

## Детальная информация о группе

**URL:** `/api/groups/{id}/`  
**Метод:** `GET`

### Ответ (200 OK)

```json
{
  "id": 1,
  "name": "ПИ-11",
  "course": 1,
  "enrollment_year": 2024,
  "students": [
    {
      "id": 1,
      "last_name": "Иванов",
      "first_name": "Александр",
      "middle_name": "Дмитриевич",
      "date_of_birth": "2006-05-15"
    },
    {
      "id": 2,
      "last_name": "Петрова",
      "first_name": "Анастасия",
      "middle_name": "Сергеевна",
      "date_of_birth": "2006-08-22"
    }
  ],
  "students_count": 2
}
```

## Получить преподавателей группы

**URL:** `/api/groups/{id}/teachers/`  
**Метод:** `GET`

Возвращает список преподавателей, работающих с группой.

### Ответ (200 OK)

```json
[
  {
    "id": 1,
    "last_name": "Иванов",
    "first_name": "Иван",
    "middle_name": "Иванович",
    "position": "Профессор",
    "classroom": {
      "id": 1,
      "number": "Л-1",
      "capacity": 110
    },
    "subjects": [
      {
        "id": 1,
        "name": "Математический анализ",
        "total_hours": 144
      }
    ]
  }
]
```

## Получить ведомость успеваемости

**URL:** `/api/groups/{id}/grade_sheet/`  
**Метод:** `GET`  
**Параметры:** `semester` (номер семестра 1-8)

Возвращает ведомость успеваемости группы за семестр.

### Пример запроса

```
GET /api/groups/1/grade_sheet/?semester=1
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
  "semester": 1,
  "students": [
    {
      "id": 1,
      "last_name": "Иванов",
      "first_name": "Александр",
      "middle_name": "Дмитриевич",
      "subjects": [
        {
          "subject": {
            "id": 1,
            "name": "Математический анализ"
          },
          "grades": [5, 4, 5, 5],
          "average": 4.75
        },
        {
          "subject": {
            "id": 2,
            "name": "Программирование"
          },
          "grades": [5, 5, 5],
          "average": 5.0
        }
      ]
    }
  ]
}
```

## Статистика по курсам

**URL:** `/api/groups/students_per_course/`  
**Метод:** `GET`

Возвращает количество студентов на каждом курсе.

### Ответ (200 OK)

```json
[
  {
    "course": 1,
    "students_count": 78
  },
  {
    "course": 2,
    "students_count": 65
  },
  {
    "course": 3,
    "students_count": 52
  },
  {
    "course": 4,
    "students_count": 48
  }
]
```

## Обновление группы

**URL:** `/api/groups/{id}/`  
**Методы:** `PUT`, `PATCH`

### Запрос (PATCH)

```json
{
  "course": 2
}
```

### Ответ (200 OK)

```json
{
  "id": 1,
  "name": "ПИ-11",
  "course": 2,
  "enrollment_year": 2024
}
```

## Удаление группы

**URL:** `/api/groups/{id}/`  
**Метод:** `DELETE`

### Ответ (204 No Content)

Группа удалена.
