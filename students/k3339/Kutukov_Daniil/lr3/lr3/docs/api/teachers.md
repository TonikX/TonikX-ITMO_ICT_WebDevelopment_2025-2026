# Преподаватели

**Базовый URL:** `/api/teachers/`  
**Требуется аутентификация:** Да

## Модель

| Поле | Тип | Описание |
|------|-----|----------|
| id | integer | ID преподавателя |
| last_name | string | Фамилия |
| first_name | string | Имя |
| middle_name | string | Отчество |
| position | string | Должность |
| classroom | integer | ID кабинета |
| subjects | array | Список ID дисциплин |

## Эндпоинты

### Список преподавателей
`GET /api/teachers/`

### Создать преподавателя
`POST /api/teachers/`

```json
{
  "last_name": "Иванов",
  "first_name": "Иван",
  "middle_name": "Иванович",
  "position": "Профессор",
  "classroom": 1,
  "subjects": [1, 2]
}
```

### Получить преподавателя (детально)
`GET /api/teachers/{id}/`

Возвращает детальную информацию с вложенными объектами кабинета и дисциплин.

### Группы по предмету
`GET /api/teachers/{id}/subject_groups/?subject={subject_id}`

Получить группы, где преподаватель ведет определенный предмет.

### Обновить преподавателя
`PUT/PATCH /api/teachers/{id}/`

### Удалить преподавателя
`DELETE /api/teachers/{id}/`
