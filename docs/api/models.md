# Модели данных

## Обзор моделей

Проект использует четыре основные модели для представления данных о воинах, их профессиях и навыках.

## Warrior (Воин)

### Описание
Основная модель, представляющая воина с его характеристиками.

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | AutoField | Уникальный идентификатор | Автоматический |
| `race` | CharField | Раса воина | max_length=1, choices |
| `name` | CharField | Имя воина | max_length=120 |
| `level` | IntegerField | Уровень воина | default=0 |
| `profession` | ForeignKey | Профессия | CASCADE, null=True |
| `skill` | ManyToManyField | Навыки | through='SkillOfWarrior' |

### Выборы для поля `race`

```python
race_types = (
    ('s', 'student'),
    ('d', 'developer'),
    ('t', 'teamlead'),
)
```

### Пример данных
```json
{
    "id": 1,
    "race": "s",
    "name": "Иван Петров",
    "level": 5,
    "profession": 1,
    "skill": [1, 2, 3]
}
```

## Profession

### Описание
Модель профессии, связанная с воинами через ForeignKey.

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | AutoField | Уникальный идентификатор | Автоматический |
| `title` | CharField | Название профессии | max_length=120 |
| `description` | TextField | Описание профессии | - |

### Пример данных
```json
{
    "id": 1,
    "title": "Программист",
    "description": "Разработка программного обеспечения"
}
```

## Skill

### Описание
Модель навыка, связанная с воинами через промежуточную модель.

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | AutoField | Уникальный идентификатор | Автоматический |
| `title` | CharField | Название навыка | max_length=120 |

### Пример данных
```json
{
    "id": 1,
    "title": "Python"
}
```

## SkillOfWarrior

### Описание
Промежуточная модель для связи воина и навыка с дополнительной информацией об уровне освоения.

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | AutoField | Уникальный идентификатор | Автоматический |
| `skill` | ForeignKey | Навык | CASCADE |
| `warrior` | ForeignKey | Воин | CASCADE |
| `level` | IntegerField | Уровень освоения | - |

### Пример данных
```json
{
    "id": 1,
    "skill": 1,
    "warrior": 1,
    "level": 5
}
```

## Связи между моделями

### Warrior ↔ Profession
```python
# Один ко многим
profession = models.ForeignKey('Profession', on_delete=models.CASCADE)
```

### Warrior ↔ Skill
```python
# Многие ко многим через промежуточную модель
skill = models.ManyToManyField('Skill', through='SkillOfWarrior')
```

## Методы моделей

### Warrior

#### `__str__()`
```python
def __str__(self):
    return self.name
```

#### `get_race_display()`
```python
# Возвращает человекочитаемое название расы
warrior.get_race_display()  # "student", "developer", "teamlead"
```

### Profession

#### `__str__()`
```python
def __str__(self):
    return self.title
```

### Skill

#### `__str__()`
```python
def __str__(self):
    return self.title
```

### SkillOfWarrior

#### `__str__()`
```python
def __str__(self):
    return f"{self.warrior.name} - {self.skill.title} (уровень {self.level})"
```

## Запросы к моделям

### Базовые запросы

```python
# Получить всех воинов
warriors = Warrior.objects.all()

# Получить воина по ID
warrior = Warrior.objects.get(id=1)

# Фильтрация по расе
developers = Warrior.objects.filter(race='d')

# Фильтрация по уровню
high_level = Warrior.objects.filter(level__gte=5)
```

### Оптимизированные запросы

```python
# С предзагрузкой связанных данных
warriors = Warrior.objects.select_related('profession').prefetch_related('skillofwarrior_set__skill').all()

# Агрегация
from django.db.models import Count, Avg
warriors_with_skills = Warrior.objects.annotate(skill_count=Count('skill'))
avg_level = Warrior.objects.aggregate(avg_level=Avg('level'))
```

## Мета-классы

### Warrior
```python
class Meta:
    verbose_name = 'Воин'
    verbose_name_plural = 'Воин'
```

### Profession
```python
class Meta:
    verbose_name = 'Профессия'
    verbose_name_plural = 'Профессии'
```

### Skill
```python
class Meta:
    verbose_name = 'Умение'
    verbose_name_plural = 'Умения'
```

### SkillOfWarrior
```python
class Meta:
    verbose_name = 'Умение воина'
    verbose_name_plural = 'Умения воинов'
```