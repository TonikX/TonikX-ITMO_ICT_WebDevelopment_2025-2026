# Модели данных

В приложении реализованы три основные модели данных: `Tour`, `Reservation` и `Review`.

## Tour (Тур)

Модель представляет информацию о туристическом туре.

### Поля:

- `title` (CharField, max_length=200) - Название тура
- `agency` (CharField, max_length=100) - Турагенство
- `description` (TextField) - Подробное описание тура
- `start_date` (DateField) - Дата начала тура
- `end_date` (DateField) - Дата окончания тура
- `payment_conditions` (TextField) - Условия оплаты
- `country` (CharField, max_length=100) - Страна назначения
- `price` (DecimalField, max_digits=10, decimal_places=2) - Цена тура
- `max_participants` (PositiveIntegerField) - Максимальное количество участников
- `created_at` (DateTimeField, auto_now_add=True) - Дата создания
- `updated_at` (DateTimeField, auto_now=True) - Дата последнего обновления

### Особенности:

- Сортировка по дате начала тура (`ordering = ['start_date']`)
- Метод `__str__` возвращает: `"{title} - {country}"`

## Reservation (Резервирование)

Модель представляет резервирование тура пользователем.

### Поля:

- `tour` (ForeignKey -> Tour) - Связь с туром
- `user` (ForeignKey -> User) - Связь с пользователем
- `participants_count` (PositiveIntegerField, default=1, min=1) - Количество участников
- `status` (CharField, choices) - Статус резервирования
- `created_at` (DateTimeField, auto_now_add=True) - Дата создания
- `updated_at` (DateTimeField, auto_now=True) - Дата последнего обновления

### Статусы резервирования:

- `pending` - Ожидает подтверждения
- `confirmed` - Подтверждено
- `cancelled` - Отменено

### Особенности:

- Валидация количества участников (минимум 1)
- Сортировка по дате создания (новые первыми)
- Метод `__str__` возвращает: `"{username} - {tour_title}"`

### Бизнес-логика:

При создании резервирования проверяется доступность мест:
- Суммируются все участники из резервирований со статусом `pending` и `confirmed`
- Если сумма превышает `max_participants`, резервирование отклоняется

## Review (Отзыв)

Модель представляет отзыв пользователя о туре.

### Поля:

- `tour` (ForeignKey -> Tour) - Связь с туром
- `user` (ForeignKey -> User) - Связь с пользователем
- `rating` (IntegerField, min=1, max=10) - Рейтинг от 1 до 10
- `comment` (TextField) - Текстовый комментарий
- `tour_date` (DateField) - Дата тура
- `created_at` (DateTimeField, auto_now_add=True) - Дата создания отзыва

### Особенности:

- Валидация рейтинга: от 1 до 10
- Сортировка по дате создания (новые первыми)
- Метод `__str__` возвращает: `"{username} - {tour_title} ({rating}/10)"`

## Связи между моделями

```
User (Django)
 ├──> Reservation (Many-to-One)
 └──> Review (Many-to-One)

Tour
 ├──> Reservation (One-to-Many)
 └──> Review (One-to-Many)
```

## Использование в админ-панели

Все модели зарегистрированы в админ-панели Django (`tourism/admin.py`) и доступны для управления через веб-интерфейс администратора.

