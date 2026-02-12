# Модели данных

## Обзор

Система использует 5 основных моделей для хранения данных о гонках, участниках, автомобилях, регистрациях и комментариях.

## Схема базы данных

```
User (Django встроенная модель)
  │
  ├── ParticipantProfile (1:1)
  │     │
  │     ├── Car (1:N)
  │     │
  │     └── Registration (1:N)
  │           │
  │           └── Race (N:1)
  │                 │
  │                 └── Comment (1:N)
  │                       │
  │                       └── User (N:1)
```

---

## 1. ParticipantProfile (Профиль участника)

**Описание:** Расширенная информация о пользователе как участнике гонок.

### Поля модели

| Поле | Тип | Описание |
|------|-----|----------|
| `user` | OneToOneField(User) | Связь с пользователем Django |
| `full_name` | CharField(200) | ФИО участника |
| `team_name` | CharField(200) | Название команды (необязательно) |
| `description` | TextField | Описание участника (необязательно) |
| `experience_years` | PositiveIntegerField | Опыт в годах (по умолчанию 0) |
| `participant_class` | CharField(2) | Класс участника: A, B, C (по умолчанию C) |

### Связи

- **1:1** с `User` (Django)
- **1:N** с `Car` (автомобили участника)
- **1:N** с `Registration` (регистрации на гонки)

### Методы

- `__str__()` - возвращает `full_name` или `username`

### Пример использования

```python
profile = ParticipantProfile.objects.create(
    user=user,
    full_name="Иван Иванов",
    team_name="Команда Победа",
    experience_years=5,
    participant_class='A'
)
```

---

## 2. Car (Автомобиль)

**Описание:** Информация об автомобиле участника.

### Поля модели

| Поле | Тип | Описание |
|------|-----|----------|
| `owner` | ForeignKey(ParticipantProfile) | Владелец автомобиля |
| `name` | CharField(200) | Название автомобиля |
| `description` | TextField | Описание автомобиля (необязательно) |

### Связи

- **N:1** с `ParticipantProfile` (владелец)
- **1:N** с `Registration` (использование в регистрациях)

### Методы

- `__str__()` - возвращает `"{name} ({owner})"`

### Пример использования

```python
car = Car.objects.create(
    owner=profile,
    name="Ferrari F1-2024",
    description="Спортивный автомобиль для гонок"
)
```

---

## 3. Race (Гонка)

**Описание:** Информация о гонке.

### Поля модели

| Поле | Тип | Описание |
|------|-----|----------|
| `title` | CharField(200) | Название гонки |
| `date` | DateTimeField | Дата и время гонки (необязательно) |
| `location` | CharField(200) | Место проведения (необязательно) |
| `description` | TextField | Описание гонки (необязательно) |

### Связи

- **1:N** с `Registration` (регистрации участников)
- **1:N** с `Comment` (комментарии к гонке)

### Методы

- `__str__()` - возвращает `"{title} — {date}"` или `"{title} — дата не указана"`

### Пример использования

```python
from django.utils import timezone
from datetime import timedelta

race = Race.objects.create(
    title="Гран-при Москвы",
    date=timezone.now() + timedelta(days=30),
    location="Москва, Автодром",
    description="Ежегодная гонка в столице России"
)
```

---

## 4. Registration (Регистрация)

**Описание:** Регистрация участника на гонку.

### Поля модели

| Поле | Тип | Описание |
|------|-----|----------|
| `race` | ForeignKey(Race) | Гонка |
| `participant` | ForeignKey(ParticipantProfile) | Участник |
| `car` | ForeignKey(Car) | Автомобиль (необязательно) |
| `registered_at` | DateTimeField | Дата регистрации (автоматически) |
| `finish_time_ms` | BigIntegerField | Время заезда в миллисекундах (необязательно) |
| `position` | PositiveIntegerField | Позиция (место) в гонке (необязательно) |

### Ограничения

- **unique_together:** (`race`, `participant`) - один участник может зарегистрироваться на гонку только один раз

### Связи

- **N:1** с `Race` (гонка)
- **N:1** с `ParticipantProfile` (участник)
- **N:1** с `Car` (автомобиль)

### Методы

- `__str__()` - возвращает `"{participant} @ {race.title}"`

### Пример использования

```python
registration = Registration.objects.create(
    race=race,
    participant=profile,
    car=car,
    position=1,
    finish_time_ms=120000  # 2 минуты
)
```

---

## 5. Comment (Комментарий)

**Описание:** Комментарий пользователя к гонке.

### Поля модели

| Поле | Тип | Описание |
|------|-----|----------|
| `race` | ForeignKey(Race) | Гонка |
| `commentator` | ForeignKey(User) | Автор комментария |
| `text` | TextField | Текст комментария |
| `comment_type` | CharField(10) | Тип комментария: coop, race, other |
| `rating` | PositiveSmallIntegerField | Рейтинг от 1 до 10 (по умолчанию 5) |
| `created_at` | DateTimeField | Дата создания (автоматически) |

### Типы комментариев

- `'coop'` - Вопрос о сотрудничестве
- `'race'` - Вопрос о гонках
- `'other'` - Иное

### Связи

- **N:1** с `Race` (гонка)
- **N:1** с `User` (автор комментария)

### Методы

- `save()` - автоматически ограничивает рейтинг от 1 до 10
- `__str__()` - возвращает `"Комментарий от {commentator} к {race}"`

### Пример использования

```python
comment = Comment.objects.create(
    race=race,
    commentator=user,
    text="Отличная гонка! Жду следующего года.",
    comment_type='race',
    rating=9
)
```

---

## Вспомогательные константы

### COMMENT_TYPES

```python
COMMENT_TYPES = [
    ('coop', 'Вопрос о сотрудничестве'),
    ('race', 'Вопрос о гонках'),
    ('other', 'Иное'),
]
```

### CLASS_CHOICES

```python
CLASS_CHOICES = [
    ('A', 'Класс A'),
    ('B', 'Класс B'),
    ('C', 'Класс C'),
]
```

---

## Миграции

Все модели имеют соответствующие миграции в директории `racing/migrations/`.

### Создание новых миграций

```bash
python manage.py makemigrations
```

### Применение миграций

```bash
python manage.py migrate
```

---

## Индексы и оптимизация

### Используемые индексы

- Автоматические индексы на ForeignKey полях
- Уникальный индекс на паре (`race`, `participant`) в модели Registration

### Рекомендации по оптимизации

Для больших объемов данных рекомендуется добавить индексы:

```python
class Meta:
    indexes = [
        models.Index(fields=['date'], name='race_date_idx'),
        models.Index(fields=['position'], name='registration_position_idx'),
    ]
```

---

## Валидация данных

### На уровне модели

- `rating` в Comment автоматически ограничивается от 1 до 10 в методе `save()`
- `unique_together` в Registration предотвращает дублирование регистраций

### На уровне формы

- Валидация через Django Forms
- Проверка наличия автомобилей перед регистрацией
- Проверка наличия профиля перед комментированием

