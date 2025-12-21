# Краткая шпаргалка по проекту "Табло авиарейсов"

## Быстрая навигация

### Хочу изменить внешний вид (дизайн, цвета, стили)
→ `templates/` - все HTML и CSS здесь
- `templates/base.html` - общий дизайн (навигация, стили кнопок, цвета)
- `templates/home.html` - главная страница с карточками рейсов
- `templates/flights/flight_detail.html` - страница рейса

### Хочу изменить логику работы (что происходит при клике)
→ `flights/views.py` - вся логика здесь
- `home()` - главная страница + поиск
- `create_reservation()` - создание брони
- `FlightDetailView` - страница рейса

### Хочу изменить структуру данных (добавить поле)
→ `flights/models.py` - структура БД
- Изменил? → `python manage.py makemigrations` → `python manage.py migrate`

### Хочу изменить формы (что вводит пользователь)
→ `flights/forms.py` - все формы
- `UserRegistrationForm` - регистрация
- `FlightSearchForm` - поиск
- `ReservationForm` - бронирование
- `ReviewForm` - отзывы

### Хочу изменить URL-адреса
→ `flights/urls.py` - все маршруты приложения
→ `airport_project/urls.py` - главные маршруты

### Хочу изменить админ-панель
→ `flights/admin.py` - настройки админки

---

## Структура файлов (ЧТО ГДЕ)

```
main_lab/
│
├── flights/                    ← ПРИЛОЖЕНИЕ (основной код)
│   ├── models.py              ← ДАННЫЕ (что хранится в БД)
│   ├── views.py               ← ЛОГИКА (что делает сайт)
│   ├── forms.py               ← ФОРМЫ (что вводит пользователь)
│   ├── urls.py                ← АДРЕСА (какие страницы есть)
│   ├── admin.py               ← АДМИНКА (панель управления)
│   └── migrations/            ← ИСТОРИЯ изменений БД
│
├── templates/                  ← ВНЕШНИЙ ВИД (HTML + CSS)
│   ├── base.html              ← ОБЩИЙ дизайн (шапка, стили)
│   ├── home.html              ← ГЛАВНАЯ страница
│   ├── flights/               ← Страницы РЕЙСОВ
│   ├── reservations/          ← Страницы БРОНИРОВАНИЙ
│   ├── reviews/               ← Страницы ОТЗЫВОВ
│   └── registration/          ← Страницы ВХОДА/РЕГИСТРАЦИИ
│
├── airport_project/            ← НАСТРОЙКИ проекта
│   ├── settings.py            ← Все настройки Django
│   └── urls.py                ← Главные URL
│
├── db.sqlite3                  ← БАЗА ДАННЫХ (файл)
├── manage.py                   ← Управление проектом
└── load_test_data.py          ← Загрузка тестовых данных
```

---

## Основные файлы и их назначение

### 1. `flights/models.py` - ЧТО ХРАНИТСЯ

```python
class User(AbstractUser):          # ПОЛЬЗОВАТЕЛИ
    phone_number = ...              # телефон
    passport_number = ...           # паспорт
    date_of_birth = ...            # дата рождения

class Flight(models.Model):         # РЕЙСЫ
    flight_number = ...             # номер (SU1234)
    airline = ...                   # авиакомпания
    departure_city = ...            # откуда
    arrival_city = ...              # куда
    departure_time = ...            # когда вылет
    price = ...                     # цена
    total_seats = ...               # мест всего

class Reservation(models.Model):    # БРОНИ
    user = ForeignKey(User)         # кто забронировал
    flight = ForeignKey(Flight)     # какой рейс
    status = ...                    # статус (pending/confirmed)
    ticket_number = ...             # номер билета

class Review(models.Model):         # ОТЗЫВЫ
    user = ForeignKey(User)         # кто написал
    flight = ForeignKey(Flight)     # на какой рейс
    rating = ...                    # оценка 1-10
    text = ...                      # текст отзыва
```

**Когда менять:**
- Добавить новое поле → изменить модель → makemigrations → migrate

---

### 2. `flights/views.py` - ЧТО ПРОИСХОДИТ

#### Функциональные view (def)

```python
def home(request):
    """ГЛАВНАЯ СТРАНИЦА - показать все рейсы + поиск"""
    # получить форму поиска
    # получить рейсы из БД
    # если есть фильтры - применить
    # отдать в шаблон

def create_reservation(request, flight_id):
    """СОЗДАТЬ БРОНЬ - пользователь бронирует рейс"""
    # проверить: есть уже бронь?
    # проверить: есть места?
    # если POST - сохранить бронь
    # если GET - показать форму

def my_reservations(request):
    """МОИ БРОНИ - показать все брони пользователя"""
    # получить брони текущего пользователя
    # отдать в шаблон
```

#### Классовые view (class)

```python
class FlightListView(ListView):
    """СПИСОК РЕЙСОВ - все рейсы с поиском"""
    model = Flight                  # какая модель
    template_name = '...'           # какой шаблон
    paginate_by = 10                # по 10 на странице

class FlightDetailView(DetailView):
    """ДЕТАЛИ РЕЙСА - один рейс подробно"""
    model = Flight
    # + список пассажиров
    # + отзывы
    # + проверка брони
```

**Когда менять:**
- Изменить логику работы
- Добавить проверки
- Изменить фильтрацию

---

### 3. `templates/` - КАК ВЫГЛЯДИТ

#### `base.html` - ОБЩИЙ ШАБЛОН

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        /* ВСЕ СТИЛИ ЗДЕСЬ */
        body { background: #2c2c2c; }
        .btn-primary { color: white; }
        .navbar { ... }
    </style>
</head>
<body>
    <nav>
        <!-- НАВИГАЦИЯ -->
        Главная | Рейсы | Вход | Регистрация
    </nav>
    
    {% block content %}
        <!-- СЮДА ВСТАВЛЯЕТСЯ СОДЕРЖИМОЕ СТРАНИЦ -->
    {% endblock %}
</body>
</html>
```

**Когда менять:**
- Изменить цвета → секция `<style>`
- Изменить навигацию → секция `<nav>`
- Добавить общие элементы

#### `home.html` - ГЛАВНАЯ СТРАНИЦА

```html
{% extends 'base.html' %}  <!-- наследуем base.html -->

{% block extra_css %}
<style>
    .flight-card {           /* КАРТОЧКА РЕЙСА */
        display: flex;
        flex-direction: column;
    }
    .seats-info {            /* БЛОК "ДОСТУПНО МЕСТ" */
        margin-top: auto;    /* прижать к низу */
    }
</style>
{% endblock %}

{% block content %}
<div class="hero">
    <h1>Табло авиарейсов</h1>
</div>

<div class="search-form">
    <!-- ФОРМА ПОИСКА -->
    {{ form.departure_city }}
    {{ form.arrival_city }}
    <button>Искать</button>
</div>

<div class="flight-grid">
    {% for flight in flights %}
    <div class="flight-card">
        <!-- КАРТОЧКА РЕЙСА -->
        <div>{{ flight.flight_number }}</div>
        <div>{{ flight.departure_city }} → {{ flight.arrival_city }}</div>
        
        <div class="seats-info">
            Доступно мест: {{ flight.available_seats }}
        </div>
        
        <a href="{% url 'flight_detail' flight.pk %}">
            Подробнее
        </a>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

**Django Template Language:**
- `{{ variable }}` - вывести переменную
- `{% for item in list %}` - цикл
- `{% if condition %}` - условие
- `{% url 'name' %}` - ссылка по имени
- `{{ date|date:"d.m.Y" }}` - фильтр форматирования

---

### 4. `flights/forms.py` - ЧТО ВВОДИТ ПОЛЬЗОВАТЕЛЬ

```python
class UserRegistrationForm(UserCreationForm):
    """РЕГИСТРАЦИЯ - новый пользователь"""
    class Meta:
        model = User
        fields = ['username', 'email', 'password', ...]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class FlightSearchForm(forms.Form):
    """ПОИСК РЕЙСОВ - фильтрация"""
    departure_city = forms.CharField(required=False)
    arrival_city = forms.CharField(required=False)
    departure_date = forms.DateField(required=False)

class ReviewForm(forms.ModelForm):
    """ОТЗЫВ - написать отзыв на рейс"""
    class Meta:
        model = Review
        fields = ['flight_date', 'rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
```

**Когда менять:**
- Добавить/убрать поля
- Изменить валидацию
- Изменить виджеты (внешний вид)

---

### 5. `flights/urls.py` - КАКИЕ СТРАНИЦЫ ЕСТЬ

```python
urlpatterns = [
    # ГЛАВНАЯ
    path('', views.home, name='home'),
    
    # АУТЕНТИФИКАЦИЯ
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # РЕЙСЫ
    path('flights/', views.FlightListView.as_view(), name='flight_list'),
    path('flights/<int:pk>/', views.FlightDetailView.as_view(), name='flight_detail'),
    
    # БРОНИ
    path('flights/<int:flight_id>/reserve/', views.create_reservation, name='create_reservation'),
    path('my_reservations/', views.my_reservations, name='my_reservations'),
    path('reservations/<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    
    # ОТЗЫВЫ
    path('flights/<int:flight_id>/review/', views.create_review, name='create_review'),
    path('my_reviews/', views.my_reviews, name='my_reviews'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]
```

**Формат URL:**
- `path('адрес/', view_функция, name='имя')`
- `<int:pk>` - целое число из URL
- `name='имя'` - для использования в шаблонах: `{% url 'имя' %}`

---

### 6. `flights/admin.py` - ПАНЕЛЬ УПРАВЛЕНИЯ

```python
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """АДМИНКА ПОЛЬЗОВАТЕЛЕЙ"""
    list_display = ('username', 'email', 'phone_number')  # что показывать в списке
    search_fields = ('username', 'email')                  # по чему искать

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    """АДМИНКА РЕЙСОВ"""
    list_display = ('flight_number', 'airline', 'departure_city', 'price')
    list_filter = ('airline', 'departure_city')            # фильтры справа

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """АДМИНКА БРОНЕЙ"""
    actions = ['confirm_reservations']                     # массовые действия
    
    def confirm_reservations(self, request, queryset):
        """Подтвердить выбранные брони"""
        queryset.update(is_confirmed=True, status='confirmed')
```

**Доступ к админке:**
- URL: http://127.0.0.1:8000/admin/
- Логин: admin / Пароль: admin

---

## Поток работы (КАК ЭТО РАБОТАЕТ)

### Пример: Пользователь бронирует рейс

```
1. КЛИК на "Забронировать"
   ↓
2. URL: /flights/5/reserve/
   ↓
3. Django смотрит в flights/urls.py
   → находит: path('flights/<int:flight_id>/reserve/', ...)
   ↓
4. Вызывает: views.create_reservation(request, flight_id=5)
   ↓
5. View проверяет:
   - Пользователь авторизован? (@login_required)
   - Уже есть бронь? (проверка в БД)
   - Есть свободные места? (flight.is_available)
   ↓
6. Если ОК:
   - Создает объект Reservation
   - Сохраняет в БД
   - Перенаправляет на "Мои брони"
   ↓
7. Показывает страницу с сообщением "Бронь создана!"
```

---

## База данных (ЧТО ВНУТРИ)

### Работа с БД через Django ORM

```python
# СОЗДАТЬ
flight = Flight.objects.create(
    flight_number='SU1234',
    airline='Аэрофлот',
    departure_city='Москва',
    price=5000
)

# ПОЛУЧИТЬ ОДИН
flight = Flight.objects.get(pk=1)
flight = Flight.objects.get(flight_number='SU1234')

# ПОЛУЧИТЬ ВСЕ
flights = Flight.objects.all()

# ФИЛЬТРОВАТЬ
flights = Flight.objects.filter(departure_city='Москва')
flights = Flight.objects.filter(price__lte=10000)  # цена <= 10000
flights = Flight.objects.filter(airline__icontains='Аэро')  # содержит "Аэро"

# СОРТИРОВАТЬ
flights = Flight.objects.order_by('departure_time')
flights = Flight.objects.order_by('-price')  # по убыванию

# СВЯЗИ (ForeignKey)
reservation = Reservation.objects.get(pk=1)
print(reservation.user.username)      # получить пользователя
print(reservation.flight.flight_number)  # получить рейс

flight = Flight.objects.get(pk=1)
reservations = flight.reservations.all()  # все брони рейса

# ОБНОВИТЬ
flight.price = 6000
flight.save()

# или массово:
Flight.objects.filter(airline='Аэрофлот').update(price=5000)

# УДАЛИТЬ
flight.delete()
```

### Миграции (изменение структуры БД)

```bash
# 1. Изменили models.py
# 2. Создать файл миграции
python manage.py makemigrations

# 3. Применить миграцию
python manage.py migrate

# Посмотреть SQL
python manage.py sqlmigrate flights 0001
```

---

## Команды для работы

```bash
# ЗАПУСК СЕРВЕРА
python manage.py runserver

# РАБОТА С БД
python manage.py makemigrations    # создать миграции
python manage.py migrate           # применить миграции
python manage.py createsuperuser   # создать админа

# КОНСОЛЬ Django (для тестирования)
python manage.py shell
>>> from flights.models import Flight
>>> Flight.objects.all()

# ЗАГРУЗИТЬ ТЕСТОВЫЕ ДАННЫЕ
python load_test_data.py

# СОБРАТЬ СТАТИЧЕСКИЕ ФАЙЛЫ (для продакшена)
python manage.py collectstatic
```

---

## Часто используемые вещи

### Изменить цвета
→ `templates/base.html` → секция `<style>` → найти цвета (#2c2c2c, #d4a574, #f5f5f5)

### Добавить поле в модель
1. `flights/models.py` → добавить поле
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `flights/admin.py` → добавить в `list_display`
5. `templates/` → показать в шаблонах

### Изменить текст на странице
→ `templates/` → найти нужный HTML файл → изменить текст

### Добавить новую страницу
1. `flights/views.py` → создать view
2. `flights/urls.py` → добавить path
3. `templates/` → создать шаблон
4. `templates/base.html` → добавить ссылку в навигацию

### Изменить логику (проверки, условия)
→ `flights/views.py` → найти нужный view → изменить код

---

## Отладка и поиск ошибок

### Ошибка в браузере
1. Прочитать сообщение ошибки
2. Посмотреть строку файла
3. Проверить синтаксис Python/HTML

### Изменения не применяются
1. Сделать Hard Refresh: `Cmd+Shift+R` (Mac) или `Ctrl+F5` (Win)
2. Перезапустить сервер: `Ctrl+C` → `python manage.py runserver`

### Ошибка в БД
1. Проверить миграции: `python manage.py migrate`
2. Если нужно - удалить БД и создать заново:
   ```bash
   rm db.sqlite3
   python manage.py migrate
   python manage.py createsuperuser
   python load_test_data.py
   ```

### Посмотреть, что в БД
```bash
python manage.py shell
>>> from flights.models import *
>>> Flight.objects.all()
>>> User.objects.all()
>>> Reservation.objects.filter(status='confirmed')
```

---

## Структура Django MTV

```
┌─────────────┐
│   MODELS    │  ← Что хранится (БД)
│ (models.py) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    VIEWS    │  ← Что делается (логика)
│ (views.py)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  TEMPLATES  │  ← Что видит пользователь (HTML)
│ (*.html)    │
└─────────────┘
```

**Поток:**
1. Пользователь открывает URL
2. `urls.py` находит соответствующий view
3. `views.py` получает данные из `models.py`
4. `views.py` отдает данные в `templates/`
5. Шаблон рендерится в HTML
6. HTML отправляется пользователю

---

## Дополнительно

📚 **Полное руководство:** `PROJECT_STRUCTURE_EXPLAINED.md` (88 КБ)
📋 **Эта шпаргалка:** `QUICK_REFERENCE.md`
📖 **Официальная документация Django:** https://docs.djangoproject.com/

---

**Создано:** 2025
**Проект:** Табло авиарейсов (Лабораторная работа №2)
**Автор:** Иванов Виктор

