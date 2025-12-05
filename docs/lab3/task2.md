# Часть 2: Django REST Framework

### 1. Создание проекта

Сначала создал виртуальное окружение и установил Django + DRF:

```bash
mkdir simple_django_3_2
cd simple_django_3_2
python3 -m venv project-env
source project-env/bin/activate
pip install django djangorestframework
```

Потом создал сам проект и приложение:

```bash
django-admin startproject warriors_project .
python manage.py startapp warriors_app
```

### 2. Настройка settings.py

Добавил в `INSTALLED_APPS`:

- `rest_framework`
- `warriors_app`

### 3. Модели

В `models.py` создал 4 модели:

| Модель | Описание |
|--------|----------|
| **Profession** | Профессия воина (title, description) |
| **Skill** | Умение (title) |
| **Warrior** | Сам воин (race, name, level, связи с Profession и Skill) |
| **SkillOfWarrior** | Промежуточная таблица для ManyToMany связи воин-скилл с дополнительным полем level |

### 4. Сериализаторы

Тут пришлось повозиться. Сделал несколько сериализаторов:

| Сериализатор | Назначение |
|--------------|------------|
| `WarriorSerializer` | Базовый |
| `ProfessionSerializer`, `SkillSerializer` | Для связанных моделей |
| `WarriorProfessionSerializer` | Воин + вложенная профессия |
| `WarriorSkillSerializer` | Воин + вложенные скилы |
| `WarriorDetailSerializer` | Полная инфа о воине (профессия + скилы с уровнями) |

### 5. Views (представления)

Использовал `APIView` как было в задании. Получились такие классы:

- `WarriorAPIView` — GET всех воинов
- `ProfessionCreateView` — POST создания профессии
- `SkillAPIView` — GET всех скилов
- `SkillCreateView` — POST создания скила
- `WarriorProfessionAPIView` — GET воинов с профессиями
- `WarriorSkillAPIView` — GET воинов со скилами
- `WarriorDetailAPIView` — GET/PUT/PATCH/DELETE для конкретного воина

---

## API Endpoints

Все эндпоинты висят на `/war/`:

| Эндпоинт | Метод | Что делает |
|----------|-------|------------|
| `/war/warriors/` | GET | Все воины |
| `/war/profession/create/` | POST | Создать профессию |
| `/war/skills/` | GET | Все скилы |
| `/war/skill/create/` | POST | Создать скилл |
| `/war/warriors/professions/` | GET | Воины + профессии |
| `/war/warriors/skills/` | GET | Воины + скилы |
| `/war/warrior/<id>/` | GET | Детали воина |
| `/war/warrior/<id>/` | PUT | Обновить воина |
| `/war/warrior/<id>/` | PATCH | Частично обновить |
| `/war/warrior/<id>/` | DELETE | Удалить воина |

---

## Трудности

1. **Вложенные сериализаторы** — не сразу понял как правильно связать SkillOfWarrior со Skill'ами чтобы выводились и скилы и уровни
2. **source в сериализаторе** — долго искал как достучаться до `skillofwarrior_set`
3. **Разница PUT и PATCH** — PUT требует все поля, PATCH может частично обновлять. Решил через `partial=True`

---

## Запуск

```bash
cd simple_django_3_2
source project-env/bin/activate
python manage.py runserver
```

Потом можно тыкать в браузере `http://127.0.0.1:8000/war/warriors/` — DRF сам генерит красивый интерфейс для тестирования API.
