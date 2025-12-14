# О проекте

## Описание

Этот проект представляет собой полнофункциональное REST API, созданное с использованием Django REST Framework. Проект реализует систему управления воинами, их профессиями и навыками, демонстрируя различные подходы к созданию API.

## Задачи практического задания

### Задание 1: APIView для скиллов
- Реализация методов GET и POST для навыков
- Создание сериализаторов для валидации данных
- Обработка ошибок и возврат соответствующих статус-кодов

### Задание 2: Generic API Views
- Вывод полной информации о всех войнах и их профессиях
- Вывод полной информации о всех войнах и их скилах
- Вывод полной информации о войне по ID с профессиями и скиллами
- Удаление воина по ID
- Редактирование информации о войне

## Архитектура проекта

### Модели данных

#### Warrior (Воин)
```python
class Warrior(models.Model):
    race = models.CharField(max_length=1, choices=race_types)
    name = models.CharField(max_length=120)
    level = models.IntegerField(default=0)
    profession = models.ForeignKey('Profession', on_delete=models.CASCADE)
    skill = models.ManyToManyField('Skill', through='SkillOfWarrior')
```

#### Profession (Профессия)
```python
class Profession(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
```

#### Skill (Навык)
```python
class Skill(models.Model):
    title = models.CharField(max_length=120)
```

#### SkillOfWarrior (Навык воина)
```python
class SkillOfWarrior(models.Model):
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    warrior = models.ForeignKey('Warrior', on_delete=models.CASCADE)
    level = models.IntegerField()
```

## Технические особенности

### Сериализаторы
- **ModelSerializer** - для базовой сериализации
- **Nested Serializers** - для связанных данных
- **SlugRelatedField** - для отображения связанных объектов
- **Depth Serializers** - для автоматического включения связанных данных

### Представления
- **APIView** - полный контроль над логикой
- **Generic API Views** - готовые решения для стандартных операций
- **Оптимизация запросов** - использование `select_related` и `prefetch_related`

### RESTful принципы
- Правильные HTTP методы (GET, POST, PUT, DELETE)
- Стандартные статус-коды HTTP
- JSON формат данных
- Stateless архитектура

Проект демонстрирует:
- Понимание принципов REST API
- Практическое применение Django REST Framework
- Работу с различными типами сериализаторов
- Оптимизацию запросов к базе данных
- Создание документации для API