# Обзор API

## Введение

Django REST Framework API предоставляет полный набор endpoints для управления воинами, их профессиями и навыками. API построен на принципах REST и обеспечивает стандартизированный интерфейс для взаимодействия с данными.

## Архитектура API

### Базовый URL
```
http://localhost:8000/warriors/
```

### Основные компоненты

- **Модели** - структура данных
- **Сериализаторы** - преобразование данных
- **Представления** - логика обработки запросов
- **URL маршруты** - маршрутизация запросов

## Модели данных

### Warrior (Воин)
```python
{
    "id": 1,
    "race": "student",
    "name": "Иван Петров",
    "level": 5,
    "profession": 1,
    "skill": [1, 2, 3]
}
```

### Profession (Профессия)
```python
{
    "id": 1,
    "title": "Программист",
    "description": "Разработка программного обеспечения"
}
```

### Skill (Навык)
```python
{
    "id": 1,
    "title": "Python"
}
```

### SkillOfWarrior (Навык воина)
```python
{
    "skill": 1,
    "warrior": 1,
    "level": 5
}
```

## HTTP Методы

| Метод | Описание | Пример |
|-------|----------|--------|
| GET | Получение данных | `GET /warriors/warriors/` |
| POST | Создание данных | `POST /warriors/warriors/create/` |
| PUT | Полное обновление | `PUT /warriors/warriors/1/update/` |
| PATCH | Частичное обновление | `PATCH /warriors/warriors/1/update/` |
| DELETE | Удаление данных | `DELETE /warriors/warriors/1/delete/` |

## Статус-коды

| Код | Описание |
|-----|----------|
| 200 | OK - успешный запрос |
| 201 | Created - ресурс создан |
| 204 | No Content - успешное удаление |
| 400 | Bad Request - неверный запрос |
| 404 | Not Found - ресурс не найден |
| 500 | Internal Server Error - ошибка сервера |

## Форматы данных

### Входные данные
```json
{
    "race": "d",
    "name": "Алексей",
    "level": 7,
    "profession": 1
}
```

### Выходные данные
```json
{
    "id": 1,
    "race": "developer",
    "name": "Алексей",
    "level": 7,
    "profession": {
        "id": 1,
        "title": "Программист",
        "description": "Разработка ПО"
    },
    "skill": [
        {
            "skill": {
                "id": 1,
                "title": "Python"
            },
            "level": 5
        }
    ]
}
```

## Фильтрация и поиск

### Параметры запроса
- `?search=name` - поиск по имени
- `?level__gte=5` - уровень больше или равен 5
- `?race=developer` - фильтр по расе
- `?profession=1` - фильтр по профессии

### Примеры
```bash
# Поиск воинов с уровнем >= 5
GET /warriors/warriors/?level__gte=5

# Поиск по расе
GET /warriors/warriors/?race=developer

# Комбинированный поиск
GET /warriors/warriors/?race=developer&level__gte=7
```

## Пагинация

API поддерживает пагинацию для больших наборов данных:

```json
{
    "count": 100,
    "next": "http://localhost:8000/warriors/warriors/?page=2",
    "previous": null,
    "results": [...]
}
```

## Аутентификация

В текущей версии API не требует аутентификации, но поддерживает:
- Session Authentication
- Token Authentication
- Basic Authentication

## Валидация данных

API автоматически валидирует:
- Типы данных
- Обязательные поля
- Ограничения длины
- Уникальность значений
- Связанные объекты

## Производительность

### Оптимизация запросов
- `select_related()` - для ForeignKey
- `prefetch_related()` - для ManyToMany
- Кэширование на уровне сериализаторов

### Примеры оптимизации
```python
# Неоптимизированный запрос
warriors = Warrior.objects.all()

# Оптимизированный запрос
warriors = Warrior.objects.select_related('profession').prefetch_related('skillofwarrior_set__skill').all()
```

## Версионирование

API поддерживает версионирование через URL:
- `v1/` - версия 1.0
- `v2/` - версия 2.0

## Мониторинг

### Логирование
- Все запросы логируются
- Ошибки записываются в лог
- Метрики производительности

### Метрики
- Время ответа
- Количество запросов
- Ошибки по типам
- Популярные endpoints

## Следующие шаги

- [Модели данных](models.md) - подробное описание моделей