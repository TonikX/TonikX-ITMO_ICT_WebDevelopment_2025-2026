# Django REST Framework API Documentation

## Описание проекта

Этот проект демонстрирует использование Django REST Framework для создания RESTful API. Проект включает модели для воинов, профессий и навыков.

## Модели

### Warrior (Воин)
- `race` - раса воина (student, developer, teamlead)
- `name` - имя воина
- `level` - уровень воина
- `profession` - профессия (связь с моделью Profession)
- `skill` - навыки (связь ManyToMany с моделью Skill через SkillOfWarrior)

### Profession (Профессия)
- `title` - название профессии
- `description` - описание профессии

### Skill (Навык)
- `title` - название навыка

### SkillOfWarrior (Навык воина)
- `skill` - навык
- `warrior` - воин
- `level` - уровень освоения навыка

## API Endpoints

### 1. Навыки (Skills)

#### GET /warriors/skills/
Получить список всех навыков
```json
{
    "Skills": [
        {
            "id": 1,
            "title": "Python"
        },
        {
            "id": 2,
            "title": "Django"
        }
    ]
}
```

#### POST /warriors/skills/
Создать новый навык
```json
{
    "skill": {
        "title": "JavaScript"
    }
}
```

### 2. Воины (Warriors)

#### GET /warriors/warriors/
Получить список всех воинов (базовая информация)
```json
{
    "Warriors": [
        {
            "id": 1,
            "race": "s",
            "name": "Иван",
            "level": 5,
            "profession": 1,
            "skill": []
        }
    ]
}
```

#### GET /warriors/warriors/list/
Получить список воинов (Generic API View)

#### GET /warriors/warriors/with_profession/
Получить список воинов с полной информацией о профессиях
```json
{
    "results": [
        {
            "id": 1,
            "race": "student",
            "name": "Иван",
            "level": 5,
            "profession": {
                "id": 1,
                "title": "Программист",
                "description": "Разработка программного обеспечения"
            },
            "skill": [
                {
                    "skill": {
                        "id": 1,
                        "title": "Python"
                    },
                    "level": 3
                }
            ]
        }
    ]
}
```

#### GET /warriors/warriors/with_skills/
Получить список воинов с полной информацией о навыках

#### GET /warriors/warriors/{id}/
Получить полную информацию о конкретном воине по ID

#### POST /warriors/warriors/create/
Создать нового воина
```json
{
    "race": "d",
    "name": "Петр",
    "level": 3,
    "profession": 1
}
```

#### PUT /warriors/warriors/{id}/update/
Обновить информацию о воине

#### DELETE /warriors/warriors/{id}/delete/
Удалить воина

#### GET/PUT/DELETE /warriors/warriors/{id}/full/
Полный CRUD для воина (получение, обновление, удаление)

### 3. Профессии (Professions)

#### POST /warriors/profession/create/
Создать новую профессию (APIView)
```json
{
    "profession": {
        "title": "Веб-разработчик",
        "description": "Создание веб-приложений"
    }
}
```

#### POST /warriors/profession/generic_create/
Создать новую профессию (Generic API View)
```json
{
    "title": "Мобильный разработчик",
    "description": "Разработка мобильных приложений"
}
```

## Примеры использования

### 1. Создание навыка
```bash
curl -X POST http://localhost:8000/warriors/skills/ \
  -H "Content-Type: application/json" \
  -d '{"skill": {"title": "React"}}'
```

### 2. Получение воинов с профессиями
```bash
curl http://localhost:8000/warriors/warriors/with_profession/
```

### 3. Создание воина
```bash
curl -X POST http://localhost:8000/warriors/warriors/create/ \
  -H "Content-Type: application/json" \
  -d '{"race": "d", "name": "Алексей", "level": 7, "profession": 1}'
```

### 4. Получение информации о конкретном воине
```bash
curl http://localhost:8000/warriors/warriors/1/
```

### 5. Обновление воина
```bash
curl -X PUT http://localhost:8000/warriors/warriors/1/update/ \
  -H "Content-Type: application/json" \
  -d '{"race": "t", "name": "Алексей", "level": 8, "profession": 1}'
```

### 6. Удаление воина
```bash
curl -X DELETE http://localhost:8000/warriors/warriors/1/delete/
```

## Сериализаторы

Проект использует различные типы сериализаторов:

1. **ModelSerializer** - для базовой сериализации моделей
2. **Nested Serializers** - для получения связанных данных
3. **SlugRelatedField** - для отображения связанных объектов по определенному полю
4. **Depth Serializers** - для автоматического включения связанных данных

## Особенности реализации

1. **Оптимизация запросов** - использование `select_related` и `prefetch_related` для уменьшения количества запросов к БД
2. **Валидация данных** - автоматическая валидация через сериализаторы
3. **Гибкость API** - различные уровни детализации данных
4. **RESTful принципы** - соответствие стандартам REST API

## Запуск проекта

1. Активируйте виртуальное окружение:
```bash
venv\Scripts\activate
```

2. Перейдите в папку проекта:
```bash
cd car_owners_project
```

3. Примените миграции:
```bash
python manage.py migrate
```

4. Запустите сервер:
```bash
python manage.py runserver
```

5. Откройте браузер и перейдите по адресу: http://localhost:8000/warriors/
