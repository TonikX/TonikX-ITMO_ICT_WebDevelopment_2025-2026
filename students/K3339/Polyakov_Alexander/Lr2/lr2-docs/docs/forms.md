# Формы

В приложении используются Django формы для обработки пользовательского ввода. Все формы определены в `tourism/forms.py`.

## UserRegistrationForm

Форма регистрации нового пользователя.

### Базовый класс
- `UserCreationForm` (Django)

### Поля:
- `username` - Имя пользователя
- `email` - Email адрес (обязательное поле)
- `password1` - Пароль
- `password2` - Подтверждение пароля

### Особенности:
- Все поля используют Bootstrap класс `form-control`
- Email является обязательным полем
- Автоматическая валидация сложности пароля от Django

### Использование:
```python
form = UserRegistrationForm(request.POST)
if form.is_valid():
    user = form.save()
    login(request, user)
```

## UserLoginForm

Форма входа в систему.

### Базовый класс
- `AuthenticationForm` (Django)

### Поля:
- `username` - Имя пользователя
- `password` - Пароль

### Особенности:
- Использует стандартную аутентификацию Django
- Все поля используют Bootstrap класс `form-control`

### Использование:
```python
form = UserLoginForm(data=request.POST)
if form.is_valid():
    user = form.get_user()
    login(request, user)
```

## ReservationForm

Форма для создания и редактирования резервирования.

### Базовый класс
- `ModelForm`

### Модель
- `Reservation`

### Поля:
- `participants_count` - Количество участников

### Виджеты:
- `NumberInput` с атрибутами:
  - `min=1`
  - `max=10`
  - `class='form-control'`

### Особенности:
- Автоматическая валидация модели (минимум 1 участник)
- Используется для создания и редактирования резервирований

### Использование:
```python
# Создание
form = ReservationForm(request.POST)
if form.is_valid():
    reservation = form.save(commit=False)
    reservation.tour = tour
    reservation.user = request.user
    reservation.save()

# Редактирование
form = ReservationForm(request.POST, instance=reservation)
```

## ReviewForm

Форма для добавления отзыва о туре.

### Базовый класс
- `ModelForm`

### Модель
- `Review`

### Поля:
- `rating` - Рейтинг (1-10)
- `comment` - Текстовый комментарий
- `tour_date` - Дата тура

### Виджеты:
- `rating`: `NumberInput` с `min=1`, `max=10`, `class='form-control'`
- `comment`: `Textarea` с `rows=4`, `class='form-control'`
- `tour_date`: `DateInput` с `type='date'`, `class='form-control'`

### Особенности:
- Валидация рейтинга: от 1 до 10 (на уровне модели и формы)
- Дата тура выбирается через HTML5 date picker

### Использование:
```python
form = ReviewForm(request.POST)
if form.is_valid():
    review = form.save(commit=False)
    review.tour = tour
    review.user = request.user
    review.save()
```

## Общие принципы

### Стилизация Bootstrap

Все формы используют класс `form-control` для единообразного оформления в стиле Bootstrap 5.

### Валидация

1. **На уровне формы**: Автоматическая валидация через `is_valid()`
2. **На уровне модели**: Валидаторы в моделях (MinValueValidator, MaxValueValidator)
3. **На уровне бизнес-логики**: Проверка доступности мест для резервирований

### Обработка ошибок

Ошибки валидации отображаются через шаблоны Django с использованием `{{ form.errors }}`.

### Методы сохранения

- `form.save()` - для стандартных форм
- `form.save(commit=False)` - когда нужно установить дополнительные поля перед сохранением (например, `tour` и `user` для резервирований и отзывов)

