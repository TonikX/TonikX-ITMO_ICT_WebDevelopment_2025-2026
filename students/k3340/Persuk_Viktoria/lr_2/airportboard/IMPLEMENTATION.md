# Документация по реализации ролей "Пользователь" и "Администратор"

## Обзор

В проекте реализована система ролей с разделением прав между обычными пользователями и администраторами аэропорта. Администратор имеет расширенные права для управления бронированиями, просмотра пассажиров и управления комментариями.

---

## 1. Модель данных для ролей

### AirportAdminProfile

**Файл**: `flight/models.py`

Модель для хранения информации о правах администратора аэропорта:

```python
class AirportAdminProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, ...)
    is_airport_admin = models.BooleanField(default=False)
```

**Особенности**:
- Связь OneToOne с User (один профиль на пользователя)
- Поле `is_airport_admin` определяет права администратора
- Управление через Django Admin

**Миграция**: Необходимо выполнить `python manage.py makemigrations` и `python manage.py migrate`

---

## 2. Утилиты для проверки прав

### Функция `is_airport_admin(user)`

**Файл**: `flight/utils.py`

```python
def is_airport_admin(user):
    """Проверяет, является ли пользователь администратором аэропорта"""
    if not user or not user.is_authenticated:
        return False
    try:
        profile = user.airport_admin_profile
        return profile.is_airport_admin
    except AirportAdminProfile.DoesNotExist:
        return False
```

**Использование**:
- В views для проверки прав доступа
- В шаблонах через context processor

### Context Processor

**Файл**: `flight/context_processors.py`

Добавляет переменную `is_admin` во все шаблоны автоматически:

```python
def airport_admin_context(request):
    return {
        'is_admin': is_airport_admin(request.user) if request.user.is_authenticated else False,
    }
```

**Настройка**: Добавлен в `settings.py` в `TEMPLATES['OPTIONS']['context_processors']`

---

## 3. Формы

### ReservationForm

**Файл**: `flight/forms.py`

Форма для обычных пользователей:
- При создании: только поле `seat_number`
- При редактировании: `seat_number` + `status`

**Особенности**:
- Поле `status` скрыто при создании (устанавливается автоматически как `RESERVED`)
- При редактировании пользователь может изменить статус (например, отменить бронирование)

### AdminReservationForm

**Файл**: `flight/forms.py`

Форма для администраторов:
- Выбор пользователя (`user`)
- Номер места (`seat_number`)
- Номер билета (`ticket_number`)
- Статус (`status`)

**Использование**: Только для администраторов при создании бронирования для других пользователей

### CommentEditForm

**Файл**: `flight/forms.py`

Форма для редактирования комментариев:
- Текст комментария
- Рейтинг (1-10)

**Доступ**: Администраторы могут редактировать любые комментарии, пользователи - только свои

---

## 4. Views (Представления)

### Обычные пользователи

#### `create_reservation(request, flight_id)`
- Создание бронирования для текущего пользователя
- Доступ: только авторизованные пользователи
- Форма: `ReservationForm` (только `seat_number`)

#### `reservation_update(request, pk)`
- Редактирование своего бронирования
- Проверка прав: `request.user == reservation.user`
- Форма: `ReservationForm` с `edit_mode=True` (включает `status`)

#### `reservation_delete(request, pk)`
- Удаление своего бронирования
- Проверка прав: `request.user == reservation.user`

#### `my_reservations(request)`
- Список всех бронирований текущего пользователя
- Пагинация: 10 записей на страницу

#### `add_comment(request, flight_id)`
- Добавление комментария к рейсу
- Автоматически сохраняет: `author`, `flight`, `flight_date`

### Администраторы

#### `flight_passengers(request, flight_id)`
- Страница со списком всех пассажиров рейса
- Доступ: только администраторы (`is_airport_admin`)
- URL: `flights/<id>/passengers/`
- Таблица: User, Seat, Ticket, Status, Updated at, Actions

#### `admin_create_reservation(request, flight_id)`
- Создание бронирования для любого пользователя
- Доступ: только администраторы
- URL: `flights/<id>/admin/reserve/`
- Форма: `AdminReservationForm` (с выбором пользователя и `ticket_number`)

#### `comment_update(request, comment_id)`
- Редактирование комментария
- Администраторы: могут редактировать любые комментарии
- Пользователи: только свои

#### `comment_delete(request, comment_id)`
- Удаление комментария
- Администраторы: могут удалять любые комментарии
- Пользователи: только свои

### Общие

#### `flight_detail(request, flight_id)`
- Детальная страница рейса
- Для администраторов:
  - Статистика (количество бронирований, прошедших регистрацию)
  - Таблица всех пассажиров
  - Кнопки управления
- Для обычных пользователей:
  - Таблица пассажиров скрыта
  - Только кнопки для создания бронирования и комментария

#### `flight_list(request)`
- Список всех рейсов с фильтрацией и поиском
- Для администраторов: дополнительная кнопка "Пассажиры" для каждого рейса

---

## 5. Шаблоны (Templates)

### Базовый шаблон

**Файл**: `templates/flight/base.html`

- Навигационное меню с Bootstrap
- Отображение имени пользователя
- Кнопки входа/выхода

### Список рейсов

**Файл**: `templates/flight/flight_list.html`

**Для администраторов**:
- Кнопка "Пассажиры" рядом с каждой строкой рейса

**Для всех**:
- Фильтры (тип, даты, гейт)
- Поиск (номер рейса, авиакомпания)
- Пагинация

### Детали рейса

**Файл**: `templates/flight/flight_detail.html`

**Для администраторов**:
- Блок статистики (количество бронирований, прошедших регистрацию)
- Кнопки: "Просмотр всех пассажиров", "Добавить пассажира"
- Таблица всех пассажиров с колонкой "Обновлено"
- Кнопки редактирования/удаления для всех комментариев

**Для обычных пользователей**:
- Таблица пассажиров **скрыта**
- Кнопки: "Забронировать место", "Оставить отзыв"
- Кнопки редактирования/удаления только для своих комментариев

### Страница пассажиров (только для админа)

**Файл**: `templates/flight/flight_passengers.html`

- Полная таблица всех пассажиров рейса
- Колонки: User, Seat, Ticket, Status, Updated at, Actions
- Кнопка "Добавить пассажира"

### Форма создания бронирования для админа

**Файл**: `templates/flight/admin_reservation_form.html`

- Выбор пользователя (select)
- Ввод номера места
- Ввод номера билета
- Выбор статуса

### Формы редактирования/удаления комментариев

**Файлы**:
- `templates/flight/comment_edit_form.html`
- `templates/flight/comment_confirm_delete.html`

---

## 6. URLs (Маршрутизация)

**Файл**: `flight/urls.py`

### Новые маршруты для администраторов:

```python
path('flights/<int:flight_id>/passengers/', views.flight_passengers, name='flight_passengers'),
path('flights/<int:flight_id>/admin/reserve/', views.admin_create_reservation, name='admin_create_reservation'),
path('comments/<int:comment_id>/edit/', views.comment_update, name='comment_update'),
path('comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
```

---

## 7. Разделение прав

### Что может обычный пользователь:

✅ Просматривать рейсы (таблица и детали)
✅ Создавать бронирования (только для себя)
✅ Редактировать свои бронирования (место и статус)
✅ Удалять свои бронирования
✅ Добавлять комментарии к рейсам
✅ Просматривать свои бронирования
✅ Редактировать/удалять свои комментарии

### Что НЕ может обычный пользователь:

❌ Видеть таблицу пассажиров рейса
❌ Видеть список пассажиров на отдельной странице
❌ Указывать `ticket_number` при создании бронирования
❌ Создавать бронирования для других пользователей
❌ Редактировать/удалять чужие бронирования
❌ Редактировать/удалять чужие комментарии

### Что может администратор (все права пользователя +):

✅ Видеть таблицу всех пассажиров рейса
✅ Просматривать отдельную страницу со списком пассажиров
✅ Создавать бронирования для любых пользователей
✅ Указывать `ticket_number` при создании бронирования
✅ Редактировать/удалять любые бронирования
✅ Редактировать/удалять любые комментарии
✅ Видеть статистику по рейсам (количество бронирований, прошедших регистрацию)
✅ Использовать расширенный интерфейс (кнопки "Пассажиры", "Добавить пассажира")

### Что НЕ может администратор:

❌ Изменять поле `is_airport_admin` других пользователей через сайт (только через Django Admin)
❌ Создавать/удалять/изменять рейсы (только через Django Admin)

---

## 8. Проверка прав в коде

### В Views:

```python
from .utils import is_airport_admin

# Проверка прав доступа
if not is_airport_admin(request.user):
    raise Http404("Страница не найдена")

# Проверка прав на редактирование
if request.user != reservation.user and not is_airport_admin(request.user):
    messages.error(request, 'Вы не можете редактировать это бронирование.')
    return redirect('my_reservations')
```

### В Шаблонах:

```django
{% if is_admin %}
    <!-- Контент только для администраторов -->
{% endif %}

{% if is_admin or comment.author == user %}
    <!-- Контент для администраторов или автора комментария -->
{% endif %}
```

---

## 9. Настройка администратора

### Через Django Admin:

1. Зайти в `/admin/`
2. Перейти в раздел "Flight" → "Airport admin profiles"
3. Создать новый профиль или отредактировать существующий
4. Выбрать пользователя и установить галочку "Администратор аэропорта"

### Программно (через shell):

```python
from django.contrib.auth.models import User
from flight.models import AirportAdminProfile

user = User.objects.get(username='admin')
profile, created = AirportAdminProfile.objects.get_or_create(user=user)
profile.is_airport_admin = True
profile.save()
```

---

## 10. Миграции

После добавления модели `AirportAdminProfile` необходимо выполнить:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 11. Тестирование

### Проверка для обычного пользователя:

1. Зарегистрироваться/войти
2. Убедиться, что таблица пассажиров не видна на странице рейса
3. Создать бронирование (только для себя)
4. Редактировать/удалить свое бронирование
5. Добавить комментарий
6. Попытаться отредактировать чужой комментарий (должна быть ошибка)

### Проверка для администратора:

1. Войти как администратор (с `is_airport_admin=True`)
2. Убедиться, что видна таблица пассажиров на странице рейса
3. Перейти на страницу "Пассажиры" для рейса
4. Создать бронирование для другого пользователя (с выбором пользователя и `ticket_number`)
5. Редактировать/удалить любое бронирование
6. Редактировать/удалить любой комментарий
7. Проверить статистику на странице рейса

---

## 12. Структура файлов

```
flight/
├── models.py              # Модели (Flight, Reservation, Comment, AirportAdminProfile)
├── views.py               # Все views (пользователи и администраторы)
├── forms.py               # Формы (ReservationForm, AdminReservationForm, CommentEditForm)
├── urls.py                # Маршрутизация
├── admin.py               # Настройка Django Admin
├── utils.py               # Утилиты (is_airport_admin)
└── context_processors.py  # Context processor для is_admin

templates/flight/
├── base.html                      # Базовый шаблон
├── flight_list.html               # Список рейсов
├── flight_detail.html             # Детали рейса
├── flight_passengers.html         # Страница пассажиров (админ)
├── reservation_form.html          # Форма бронирования
├── admin_reservation_form.html    # Форма бронирования для админа
├── comment_edit_form.html         # Форма редактирования комментария
├── comment_confirm_delete.html    # Подтверждение удаления комментария
└── ...
```

---

## 13. Важные моменты

1. **Безопасность**: Все проверки прав выполняются как на уровне views, так и в шаблонах
2. **Контекст**: Переменная `is_admin` доступна во всех шаблонах через context processor
3. **Формы**: Разные формы для пользователей и администраторов
4. **Миграции**: Не забыть выполнить миграции после добавления модели
5. **Админка**: Управление правами администратора только через Django Admin

---

## 14. Примеры использования

### Создание администратора:

```python
# В Django shell или через админку
from flight.models import AirportAdminProfile
from django.contrib.auth.models import User

user = User.objects.create_user('admin_user', 'admin@example.com', 'password')
profile = AirportAdminProfile.objects.create(user=user, is_airport_admin=True)
```

### Проверка прав в кастомном коде:

```python
from flight.utils import is_airport_admin

if is_airport_admin(request.user):
    # Логика для администратора
    pass
```

---

## Заключение

Реализована полная система ролей с четким разделением прав между обычными пользователями и администраторами аэропорта. Все требования из задания выполнены:

✅ Роль "Пользователь" - все функции реализованы
✅ Роль "Администратор" - все функции реализованы
✅ Разделение прав - корректно реализовано
✅ Безопасность - проверки на всех уровнях
✅ Интерфейс - расширенный для администраторов
