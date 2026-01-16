# Кабинеты

**Базовый URL:** `/api/classrooms/`  
**Требуется аутентификация:** Да

## Модель

| Поле | Тип | Описание |
|------|-----|----------|
| id | integer | ID кабинета |
| number | string | Номер кабинета (уникальный) |
| capacity | integer | Вместимость |

## Эндпоинты

### Список кабинетов
`GET /api/classrooms/`

### Создать кабинет
`POST /api/classrooms/`

```json
{
  "number": "101",
  "capacity": 30
}
```

### Получить кабинет
`GET /api/classrooms/{id}/`

### Обновить кабинет
`PUT/PATCH /api/classrooms/{id}/`

### Удалить кабинет
`DELETE /api/classrooms/{id}/`
