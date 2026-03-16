# Модели данных

## Введение

В Django модели - это классы Python, которые описывают структуру данных. Django автоматически создает таблицы в базе данных на основе этих классов. Каждая модель соответствует одной таблице, а поля модели - это столбцы в этой таблице.

## Схема связей между моделями

```
User (Django) ----1:1---- DriverProfile
                               |
                               | Many-to-One
                               |
Team ----Many-to-One---- DriverProfile ----Many-to-One---- Registration
                               |                                  |
                               |                            Many-to-One
                               |                                  |
                               |                                Race
                               |                                  |
                               |                            One-to-Many
                               |                                  |
                         HeatResult                             Heat
                               |                                  |
                         Many-to-One                              |
                               |                                  |
                               +----------------------------------+
                               
Comment ----Many-to-One---- User
      |
      +----Many-to-One---- Race
```

## Описание моделей

### 1. Team (Команда)

Модель для хранения информации о командах гонщиков.

**Поля:**

| Поле | Тип | Описание |
|------|-----|----------|
| name | CharField(200) | Название команды, уникальное |
| description | TextField | Описание команды, необязательное |

**Пример использования:**

```python
team = Team.objects.create(
    name="Нитро",
    description="Команда профессиональных гонщиков"
)
```

### 2. DriverProfile (Профиль водителя)

Профиль водителя связан с пользователем отношением один-к-одному (1:1). Когда создается новый пользователь, автоматически создается пустой профиль водителя.

**Поля:**

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| user | OneToOneField(User) | Да | Связь с пользователем |
| full_name | CharField(200) | Да | Полное имя водителя |
| car_description | CharField(300) | Нет | Описание автомобиля |
| bio | TextField | Нет | Биография водителя |
| experience_years | PositiveSmallIntegerField | Нет | Опыт в годах |
| driver_class | CharField(1) | Да | Класс: A, B или C |
| team | ForeignKey(Team) | Нет | Команда водителя |

**Классы водителей:**

- **A** - Класс A (профессионалы)
- **B** - Класс B (опытные)
- **C** - Класс C (новички)

**Автоматическое создание:**

Используется сигнал Django `post_save`, который срабатывает после создания пользователя:

```python
@receiver(post_save, sender=User)
def create_or_update_driver_profile(sender, instance, created, **kwargs):
    if created:
        DriverProfile.objects.create(user=instance, full_name='')
```

### 3. Race (Гонка)

Модель для хранения информации о гонках.

**Поля:**

| Поле | Тип | Описание |
|------|-----|----------|
| title | CharField(200) | Название гонки |
| location | CharField(200) | Место проведения |
| date | DateField | Дата проведения |
| description | TextField | Описание гонки |
| is_published | BooleanField | Опубликована ли гонка |

**Сортировка:**

По умолчанию гонки отсортированы по дате в обратном порядке (сначала новые).

**Пример:**

```python
race = Race.objects.create(
    title="Битва Титанов",
    location="Москва, Автодром",
    date="2025-11-20",
    description="Главная гонка сезона",
    is_published=True
)
```

### 4. Heat (Заезд)

В рамках одной гонки может быть несколько заездов (квалификация, полуфинал, финал).

**Поля:**

| Поле | Тип | Описание |
|------|-----|----------|
| race | ForeignKey(Race) | К какой гонке относится |
| name | CharField(100) | Название заезда |
| start_time | DateTimeField | Время старта |
| laps | PositiveSmallIntegerField | Количество кругов |
| status | CharField(20) | Статус заезда |
| info | CharField(300) | Дополнительная информация |

**Статусы заезда:**

- **scheduled** - Запланирован
- **in_progress** - В процессе
- **finished** - Завершен
- **cancelled** - Отменен

### 5. HeatResult (Результат заезда)

Хранит результат конкретного водителя в конкретном заезде.

**Поля:**

| Поле | Тип | Описание |
|------|-----|----------|
| heat | ForeignKey(Heat) | Заезд |
| driver | ForeignKey(DriverProfile) | Водитель |
| finish_time_seconds | DecimalField | Время финиша в секундах |
| position | PositiveSmallIntegerField | Позиция (место) |
| status | CharField(20) | Статус финиша |
| notes | CharField(300) | Примечания |

**Статусы финиша:**

- **finished** - Финишировал
- **dnf** - Не финишировал (Did Not Finish)
- **dsq** - Дисквалифицирован (Disqualified)
- **dns** - Не стартовал (Did Not Start)

**Важная валидация:**

Перед сохранением результата проверяется, что водитель зарегистрирован на эту гонку:

```python
def clean(self):
    if self.heat and self.driver:
        is_registered = Registration.objects.filter(
            driver=self.driver,
            race=self.heat.race,
            active=True
        ).exists()
        
        if not is_registered:
            raise ValidationError(
                f'Водитель {self.driver.full_name} не зарегистрирован на гонку'
            )
```

**Уникальность:**

Один водитель может иметь только один результат в одном заезде. Это обеспечивается ограничением:

```python
constraints = [
    UniqueConstraint(
        fields=['heat', 'driver'],
        name='unique_heat_driver_result'
    )
]
```

### 6. Registration (Регистрация)

Хранит информацию о регистрации водителя на гонку.

**Поля:**

| Поле | Тип | Описание |
|------|-----|----------|
| driver | ForeignKey(DriverProfile) | Водитель |
| race | ForeignKey(Race) | Гонка |
| created_at | DateTimeField | Дата регистрации |
| active | BooleanField | Активна ли регистрация |
| car_number | PositiveSmallIntegerField | Номер машины |

**Уникальность:**

Один водитель может зарегистрироваться на одну гонку только один раз:

```python
constraints = [
    UniqueConstraint(
        fields=['driver', 'race'],
        name='unique_driver_race_registration'
    )
]
```

### 7. Comment (Комментарий)

Отзывы и комментарии пользователей о гонках.

**Поля:**

| Поле | Тип | Описание |
|------|-----|----------|
| race | ForeignKey(Race) | К какой гонке комментарий |
| author | ForeignKey(User) | Автор комментария |
| heat_date | DateField | Дата заезда |
| kind | CharField(20) | Тип комментария |
| rating | PositiveSmallIntegerField | Рейтинг от 1 до 10 |
| text | TextField | Текст комментария |
| created_at | DateTimeField | Дата создания |

**Типы комментариев:**

- **cooperation** - О сотрудничестве
- **race** - О гонке
- **other** - Другое

**Валидация рейтинга:**

Рейтинг должен быть от 1 до 10:

```python
rating = models.PositiveSmallIntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(10)],
    verbose_name='Рейтинг (1-10)'
)
```

## Связи между моделями

### Один-к-одному (OneToOneField)

**DriverProfile - User**

Каждый профиль водителя связан ровно с одним пользователем, и наоборот.

```python
user = models.OneToOneField(User, on_delete=models.CASCADE)
```

Если пользователь удаляется, его профиль тоже удаляется (`CASCADE`).

### Многие-к-одному (ForeignKey)

**DriverProfile - Team**

Много водителей могут быть в одной команде.

```python
team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
```

Если команда удаляется, поле `team` у водителей становится пустым (`SET_NULL`).

**Heat - Race**

Много заездов могут принадлежать одной гонке.

**HeatResult - Heat и HeatResult - DriverProfile**

Один заезд может иметь много результатов, один водитель может иметь много результатов в разных заездах.

**Registration - Driver и Registration - Race**

Один водитель может иметь много регистраций на разные гонки, одна гонка может иметь много регистраций.

## Методы __str__

Для каждой модели определен метод `__str__`, который возвращает строковое представление объекта. Это помогает в админ-панели и при отладке.

Примеры:

```python
# Team
def __str__(self):
    return self.name
# Вернет: "Нитро"

# DriverProfile
def __str__(self):
    return f"{self.full_name} ({self.user.username})"
# Вернет: "Иван Петров (pilot1)"

# Race
def __str__(self):
    return f"{self.title} ({self.date})"
# Вернет: "Битва Титанов (2025-11-20)"
```

## Метаданные моделей

В классе `Meta` задаются дополнительные параметры:

```python
class Meta:
    verbose_name = 'Автогонка'  # Единственное число
    verbose_name_plural = 'Автогонки'  # Множественное число
    ordering = ['-date']  # Сортировка по умолчанию
```

Это влияет на отображение в админ-панели и при запросах к базе.

## Итоги

Всего в проекте 7 основных моделей, которые связаны между собой:

1. **Team** - команды гонщиков
2. **DriverProfile** - профили водителей
3. **Race** - гонки
4. **Heat** - заезды
5. **HeatResult** - результаты
6. **Registration** - регистрации
7. **Comment** - комментарии

Все модели используют стандартные типы полей Django и имеют необходимые валидации для обеспечения целостности данных.



