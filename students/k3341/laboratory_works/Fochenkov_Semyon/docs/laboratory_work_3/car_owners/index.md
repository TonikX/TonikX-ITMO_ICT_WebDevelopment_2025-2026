# Warriors API

## Описание проекта

Warriors API представляет собой RESTful API для управления воинами, их профессиями и навыками. Проект демонстрирует различные подходы к созданию API с использованием Django REST Framework.

## Основные возможности

- CRUD операции для воинов, профессий и навыков
- Различные уровни детализации данных через сериализаторы
- Оптимизация запросов к базе данных
- Использование APIView и Generic API Views
- Валидация входных данных

## Модели данных

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

### Навыки (Skills)

#### GET /warriors/skills/
Получить список всех навыков

#### POST /warriors/skills/
Создать новый навык

### Воины (Warriors)

#### GET /warriors/warriors/
Получить список всех воинов (базовая информация)

#### GET /warriors/warriors/list/
Получить список воинов (Generic API View)

#### GET /warriors/warriors/with_profession/
Получить список воинов с полной информацией о профессиях

#### GET /warriors/warriors/with_skills/
Получить список воинов с полной информацией о навыках

#### GET /warriors/warriors/{id}/
Получить информацию о воине по ID с профессиями и навыками

#### DELETE /warriors/warriors/{id}/delete/
Удалить воина по ID

#### PUT /warriors/warriors/{id}/update/
Редактировать информацию о воине

## Примеры запросов

### Получение списка навыков

```bash
GET http://localhost:8000/warriors/skills/
```

Ответ:
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

### Создание навыка

```bash
POST http://localhost:8000/warriors/skills/
Content-Type: application/json

{
    "skill": {
        "title": "JavaScript"
    }
}
```

### Получение воинов с профессиями

```bash
GET http://localhost:8000/warriors/warriors/with_profession/
```

Ответ:
```json
{
    "Warriors": [
        {
            "id": 1,
            "race": "s",
            "name": "Иван",
            "level": 5,
            "profession": {
                "id": 1,
                "title": "Программист",
                "description": "Разработка ПО"
            }
        }
    ]
}
```

## Технические особенности

### Сериализаторы
- **ModelSerializer** - для базовой сериализации
- **Nested Serializers** - для связанных данных
- **SlugRelatedField** - для отображения связанных объектов
- **Depth Serializers** - для автоматического включения связанных данных

### Представления
- **APIView** - полный контроль над логикой (для навыков)
- **Generic API Views** - готовые решения для стандартных операций (для воинов)
- **Оптимизация запросов** - использование `select_related` и `prefetch_related`

### RESTful принципы
- Правильные HTTP методы (GET, POST, PUT, DELETE)
- Стандартные статус-коды HTTP
- JSON формат данных
- Stateless архитектура

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install django djangorestframework
```

### 2. Применение миграций

```bash
cd car_owners_project
python manage.py migrate
```

### 3. Создание тестовых данных

```bash
python create_test_data.py
```

### 4. Запуск сервера

```bash
python manage.py runserver
```

API будет доступно по адресу: `http://localhost:8000/warriors/`

