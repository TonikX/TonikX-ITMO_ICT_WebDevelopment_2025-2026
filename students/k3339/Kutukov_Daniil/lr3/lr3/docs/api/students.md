# Студенты

**Базовый URL:** `/api/students/`  
**Требуется аутентификация:** Да

## Модель

| Поле | Тип | Описание |
|------|-----|----------|
| id | integer | ID студента |
| last_name | string | Фамилия |
| first_name | string | Имя |
| middle_name | string | Отчество |
| date_of_birth | date | Дата рождения |
| group | integer | ID группы |

## Эндпоинты

### Список студентов
`GET /api/students/`

### Создать студента
`POST /api/students/`

```json
{
  "last_name": "Иванов",
  "first_name": "Александр",
  "middle_name": "Дмитриевич",
  "date_of_birth": "2006-05-15",
  "group": 1
}
```

### Получить студента (детально)
`GET /api/students/{id}/`

### Получить оценки студента
`GET /api/students/{id}/grades/?semester={semester}`

Параметр `semester` опциональный.

### Обновить студента
`PUT/PATCH /api/students/{id}/`

### Удалить студента
`DELETE /api/students/{id}/`
