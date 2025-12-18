# Представления и URL

Приложение использует представления на основе функций (Function-Based Views).

## URL маршруты

Все URL маршруты определены в `tourism/urls.py` и подключены к главному роутеру в `Lr2/urls.py`.

### Публичные маршруты

#### `tour_list` - Список туров
- **URL**: `/`
- **Представление**: `views.tour_list`
- **Описание**: Отображает список всех туров с поиском и пагинацией (6 туров на страницу)
- **Фильтры**: Поиск по названию, стране или агентству через GET-параметр `search`

#### `tour_detail` - Детали тура
- **URL**: `/tour/<int:tour_id>/`
- **Представление**: `views.tour_detail`
- **Описание**: Показывает детальную информацию о туре и список отзывов (5 на страницу)

#### `tours_by_country` - Статистика по странам
- **URL**: `/tours-by-country/`
- **Представление**: `views.tours_by_country`
- **Описание**: Показывает количество проданных туров (с confirmed резервированиями) по каждой стране

#### `register` - Регистрация
- **URL**: `/register/`
- **Представление**: `views.register_view`
- **Описание**: Форма регистрации нового пользователя

#### `login` - Вход
- **URL**: `/login/`
- **Представление**: `views.login_view`
- **Описание**: Форма входа в систему

#### `logout` - Выход
- **URL**: `/logout/`
- **Представление**: `views.logout_view`
- **Описание**: Выход из системы

### Защищенные маршруты (требуют авторизации)

#### `make_reservation` - Создание резервирования
- **URL**: `/tour/<int:tour_id>/reserve/`
- **Представление**: `views.make_reservation`
- **Декоратор**: `@login_required`
- **Описание**: Форма для создания резервирования тура с проверкой доступности мест

#### `my_reservations` - Мои резервирования
- **URL**: `/my-reservations/`
- **Представление**: `views.my_reservations`
- **Декоратор**: `@login_required`
- **Описание**: Список всех резервирований текущего пользователя (10 на страницу)

#### `edit_reservation` - Редактирование резервирования
- **URL**: `/reservation/<int:reservation_id>/edit/`
- **Представление**: `views.edit_reservation`
- **Декоратор**: `@login_required`
- **Описание**: Редактирование собственного резервирования

#### `delete_reservation` - Удаление резервирования
- **URL**: `/reservation/<int:reservation_id>/delete/`
- **Представление**: `views.delete_reservation`
- **Декоратор**: `@login_required`
- **Описание**: Удаление собственного резервирования

#### `add_review` - Добавление отзыва
- **URL**: `/tour/<int:tour_id>/review/`
- **Представление**: `views.add_review`
- **Декоратор**: `@login_required`
- **Описание**: Форма для добавления отзыва о туре

### Административные маршруты (требуют staff статус)

#### `admin_reservations` - Управление резервированиями
- **URL**: `/manage/reservations/`
- **Представление**: `views.admin_reservations`
- **Декоратор**: `@login_required` + проверка `is_staff`
- **Описание**: Список всех резервирований с фильтрацией по статусу (20 на страницу)

#### `confirm_reservation` - Подтверждение резервирования
- **URL**: `/manage/reservation/<int:reservation_id>/confirm/`
- **Представление**: `views.confirm_reservation`
- **Декоратор**: `@login_required` + проверка `is_staff`
- **Описание**: Изменяет статус резервирования на `confirmed`

#### `cancel_reservation_admin` - Отмена резервирования (админ)
- **URL**: `/manage/reservation/<int:reservation_id>/cancel/`
- **Представление**: `views.cancel_reservation_admin`
- **Декоратор**: `@login_required` + проверка `is_staff`
- **Описание**: Изменяет статус резервирования на `cancelled`

#### `reservations_by_country` - Резервирования по стране
- **URL**: `/country/<str:country>/reservations/`
- **Представление**: `views.reservations_by_country`
- **Декоратор**: `@login_required` + проверка `is_staff`
- **Описание**: Список подтвержденных резервирований для конкретной страны (20 на страницу)

## Ключевые особенности реализации

### Пагинация

Использование `Django.core.paginator.Paginator`:
- Список туров: 6 на страницу
- Отзывы: 5 на страницу
- Резервирования пользователя: 10 на страницу
- Административные списки: 20 на страницу

### Поиск

Фильтрация туров через Q-объекты Django:

```python
tours = tours.filter(
    Q(title__icontains=search_query) |
    Q(country__icontains=search_query) |
    Q(agency__icontains=search_query)
)
```

### Валидация доступности мест

Перед созданием резервирования проверяется сумма участников:

```python
total_reserved = Reservation.objects.filter(
    tour=tour, 
    status__in=['pending', 'confirmed']
).aggregate(total=Sum('participants_count'))['total'] or 0

if total_reserved + reservation.participants_count <= tour.max_participants:
    # Резервирование возможно
```

### Система сообщений

Использование Django messages framework для уведомлений пользователей:
- `messages.success()` - успешные операции
- `messages.error()` - ошибки
- `messages.info()` - информационные сообщения

### Перенаправления

- Неавторизованные пользователи перенаправляются на `/login/`
- После входа/регистрации - на список туров
- После операций - на соответствующие страницы

## Настройки аутентификации

В `Lr2/settings.py`:

```python
LOGIN_URL = 'tourism:login'
LOGIN_REDIRECT_URL = 'tourism:tour_list'
LOGOUT_REDIRECT_URL = 'tourism:tour_list'
```

