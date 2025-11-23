# Проект Warriors - Task 2

Документация по проекту Warriors - система управления воинами с использованием Django REST Framework.

## Описание проекта

Проект Warriors представляет собой REST API для управления информацией о воинах, их профессиях и навыках. Проект реализован с использованием Django и Django REST Framework.

## Структура проекта

```
warriors_project/
├── warriors_app/          # Основное приложение
│   ├── models.py         # Модели данных
│   ├── serializers.py    # Сериализаторы DRF
│   ├── views.py          # Представления (Generic Views)
│   └── urls.py           # URL маршруты
└── warriors_project/     # Настройки проекта
    ├── settings.py      # Конфигурация Django
    └── urls.py           # Главные URL маршруты
```

## Модели данных

### Warrior (Воин)

Основная модель, представляющая воина в системе.

**Поля:**
- `race` - Раса воина (student, developer, teamlead)
- `name` - Имя воина
- `level` - Уровень воина
- `skill` - Навыки (ManyToMany через SkillOfWarrior)
- `profession` - Профессия (ForeignKey к Profession)

### Profession (Профессия)

Модель профессии воина.

**Поля:**
- `title` - Название профессии
- `description` - Описание профессии

### Skill (Навык)

Модель навыка.

**Поля:**
- `title` - Наименование навыка

### SkillOfWarrior (Навык воина)

Промежуточная модель для связи воина и навыка с уровнем освоения.

**Поля:**
- `skill` - Навык (ForeignKey)
- `warrior` - Воин (ForeignKey)
- `level` - Уровень освоения навыка

## API Endpoints

### 1. Список воинов с профессиями

**GET** `/war/warriors/profession/`

Возвращает список всех воинов с информацией об их профессиях.

**Пример ответа:**
```json
[
  {
    "id": 1,
    "name": "Иван",
    "race": "s",
    "level": 5,
    "profession": {
      "id": 1,
      "title": "Программист",
      "description": "Разработчик ПО"
    }
  }
]
```

### 2. Список воинов с навыками

**GET** `/war/warriors/skill/`

Возвращает список всех воинов с информацией об их навыках.

**Пример ответа:**
```json
[
  {
    "id": 1,
    "name": "Иван",
    "race": "s",
    "level": 5,
    "skill": [
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
]
```

### 3. Детальная информация о воине

**GET** `/war/warriors/<id>/`

Возвращает полную информацию о воине, включая профессию и все навыки.

**Пример ответа:**
```json
{
  "id": 1,
  "name": "Иван",
  "race": "s",
  "level": 5,
  "profession": {
    "id": 1,
    "title": "Программист",
    "description": "Разработчик ПО"
  },
  "skill": [
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

### 4. Обновление воина

**PUT/PATCH** `/war/warriors/<id>/`

Обновляет информацию о воине.

**Пример запроса:**
```json
{
  "name": "Петр",
  "race": "d",
  "level": 10,
  "profession": 1
}
```

### 5. Удаление воина

**DELETE** `/war/warriors/<id>/`

Удаляет воина из системы.

## Реализация

### Сериализаторы

Проект использует несколько сериализаторов для разных целей:

1. **WarriorSerializer** - базовый сериализатор для создания/обновления
2. **WarriorProfessionSerializer** - для вывода воинов с профессиями
3. **WarriorSkillSerializer** - для вывода воинов с навыками
4. **WarriorDetailSerializer** - для детального просмотра (включает все связи)

### Представления (Views)

Используются Generic Views из DRF:

- **WarriorListProfessionView** (ListAPIView) - список воинов с профессиями
- **WarriorListSkillView** (ListAPIView) - список воинов с навыками
- **WarriorDetailView** (RetrieveUpdateDestroyAPIView) - детальный просмотр, обновление и удаление

### Динамический выбор сериализатора

В `WarriorDetailView` реализован динамический выбор сериализатора:
- Для GET запросов используется `WarriorDetailSerializer` (с вложенными объектами)
- Для PUT/PATCH/DELETE используется `WarriorSerializer` (плоский формат)

## Скриншоты

### Главная страница API

![Главная страница](images/Снимок%20экрана%202025-11-18%20в%2016.14.07.png)

### Список воинов с профессиями

![Список воинов с профессиями](images/Снимок%20экрана%202025-11-18%20в%2016.14.53.png)

### Детальная информация о воине

![Детальная информация](images/Снимок%20экрана%202025-11-18%20в%2016.23.50.png)

## Технологии

- **Django 5.2.8** - веб-фреймворк
- **Django REST Framework 3.16.1** - инструментарий для создания REST API
- **SQLite** - база данных

## Установка и запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Выполните миграции:
```bash
python manage.py migrate
```

3. Запустите сервер разработки:
```bash
python manage.py runserver
```

4. API будет доступно по адресу: `http://127.0.0.1:8000/war/`

