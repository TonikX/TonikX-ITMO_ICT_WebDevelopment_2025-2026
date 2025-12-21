# Подробное объяснение структуры проекта "Табло авиарейсов"

## Оглавление
1. [Общая архитектура Django](#общая-архитектура-django)
2. [Структура проекта](#структура-проекта)
3. [Модели (Models)](#модели-models)
4. [Представления (Views)](#представления-views)
5. [Формы (Forms)](#формы-forms)
6. [Шаблоны (Templates)](#шаблоны-templates)
7. [URL-маршрутизация](#url-маршрутизация)
8. [Админ-панель](#админ-панель)
9. [Настройки проекта](#настройки-проекта)
10. [База данных](#база-данных)

---

## Общая архитектура Django

Django использует архитектурный паттерн **MTV (Model-Template-View)**, аналог MVC:

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐      ┌──────────────┐
│   Browser   │─────▶│  urls.py     │─────▶│  views.py   │─────▶│  models.py   │
│  (Клиент)   │      │  (Маршруты)  │      │  (Логика)   │      │  (Данные)    │
└─────────────┘      └──────────────┘      └─────────────┘      └──────────────┘
       ▲                                           │                      │
       │                                           ▼                      ▼
       │                                    ┌─────────────┐      ┌──────────────┐
       └────────────────────────────────────│ templates/  │◀─────│  Database    │
                                            │ (HTML)      │      │  (SQLite)    │
                                            └─────────────┘      └──────────────┘
```

**Поток запроса:**
1. Пользователь открывает URL в браузере
2. Django находит соответствующий маршрут в `urls.py`
3. Вызывается соответствующая функция/класс из `views.py`
4. View обращается к `models.py` для получения данных из БД
5. View передает данные в шаблон (template)
6. Шаблон рендерится в HTML и отправляется пользователю

---

## Структура проекта

```
main_lab/
├── venv/                          # виртуальное окружение Python
│   └── ...                        # изолированные пакеты проекта
│
├── airport_project/               # основной проект Django
│   ├── __init__.py               # делает папку Python-пакетом
│   ├── settings.py               # настройки проекта
│   ├── urls.py                   # главный URL-конфиг
│   ├── asgi.py                   # для асинхронных серверов
│   └── wsgi.py                   # для синхронных серверов (Apache, Nginx)
│
├── flights/                       # приложение "Рейсы"
│   ├── migrations/               # миграции БД (история изменений схемы)
│   │   ├── 0001_initial.py      # первая миграция
│   │   └── ...                  # последующие миграции
│   ├── __init__.py              # делает папку Python-пакетом
│   ├── admin.py                 # настройка админ-панели
│   ├── apps.py                  # конфигурация приложения
│   ├── models.py                # модели данных (схема БД)
│   ├── views.py                 # логика обработки запросов
│   ├── forms.py                 # формы для ввода данных
│   ├── urls.py                  # URL-маршруты приложения
│   └── tests.py                 # тесты приложения
│
├── templates/                     # HTML-шаблоны
│   ├── base.html                # базовый шаблон (общая структура)
│   ├── home.html                # главная страница
│   ├── flights/                 # шаблоны рейсов
│   │   ├── flight_list.html    # список рейсов
│   │   └── flight_detail.html  # детали рейса
│   ├── reservations/            # шаблоны бронирований
│   │   ├── create_reservation.html
│   │   ├── my_reservations.html
│   │   └── cancel_reservation.html
│   ├── reviews/                 # шаблоны отзывов
│   │   ├── create_review.html
│   │   ├── my_reviews.html
│   │   └── delete_review.html
│   └── registration/            # шаблоны аутентификации
│       ├── register.html       # регистрация
│       └── login.html          # вход
│
├── db.sqlite3                    # файл базы данных SQLite
├── manage.py                     # утилита управления Django
├── load_test_data.py            # скрипт загрузки тестовых данных
├── .gitignore                   # файлы, игнорируемые Git
└── README.md                    # документация проекта
```

---

## Модели (Models)

**Файл:** `flights/models.py`

Модели определяют структуру базы данных. Каждая модель = таблица в БД.

### User (Пользователь)

```python
class User(AbstractUser):
    """расширенная модель пользователя"""
    phone_number = models.CharField(...)      # номер телефона
    passport_number = models.CharField(...)   # номер паспорта
    date_of_birth = models.DateField(...)     # дата рождения
```

**Что это значит:**
- Наследуется от `AbstractUser` (встроенная модель Django)
- Получает все стандартные поля: `username`, `password`, `email`, `first_name`, `last_name`
- Добавляет 3 дополнительных поля

**В БД создается таблица:**
```sql
CREATE TABLE flights_user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(150),
    password VARCHAR(128),
    email VARCHAR(254),
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    phone_number VARCHAR(20),
    passport_number VARCHAR(20),
    date_of_birth DATE
);
```

### Flight (Рейс)

```python
class Flight(models.Model):
    """модель рейса"""
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.CharField(max_length=50)
    departure_city = models.CharField(max_length=50)
    arrival_city = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    flight_type = models.CharField(max_length=10, choices=FLIGHT_TYPE_CHOICES)
    gate_number = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.PositiveIntegerField(default=150)
```

**Поля:**
- `flight_number` - уникальный номер рейса (SU1234, S71001)
- `airline` - название авиакомпании
- `departure_city`, `arrival_city` - города отправления/прибытия
- `departure_time`, `arrival_time` - время отправления/прибытия
- `flight_type` - тип рейса (departure=отлет, arrival=прилет)
- `gate_number` - номер выхода на посадку
- `price` - цена билета
- `total_seats` - общее количество мест

**Вычисляемые свойства (не хранятся в БД):**

```python
@property
def available_seats(self):
    """количество доступных мест"""
    reserved = self.reservations.filter(is_confirmed=True, status='confirmed').count()
    return self.total_seats - reserved
```
- Считает свободные места = всего мест - подтвержденные брони

```python
@property
def is_available(self):
    """доступен ли рейс для бронирования"""
    return self.available_seats > 0
```
- Проверяет, есть ли свободные места

### Reservation (Резервирование)

```python
class Reservation(models.Model):
    """модель резервирования"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_confirmed = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    ticket_number = models.CharField(max_length=20)
    seat_number = models.CharField(max_length=5)
```

**Связи:**
- `user` - ForeignKey к User (один пользователь → много бронирований)
- `flight` - ForeignKey к Flight (один рейс → много бронирований)
- `unique_together = ('user', 'flight')` - один пользователь может забронировать рейс только один раз

**Статусы:**
- `pending` - ожидает подтверждения
- `confirmed` - подтверждено
- `cancelled` - отменено

### Review (Отзыв)

```python
class Review(models.Model):
    """модель отзыва"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    flight_date = models.DateField()
    text = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
```

**Особенности:**
- `rating` - оценка от 1 до 10 (валидаторы проверяют это)
- `unique_together = ('user', 'flight')` - один пользователь = один отзыв на рейс

---

## Представления (Views)

**Файл:** `flights/views.py`

Views обрабатывают HTTP-запросы и возвращают ответы.

### Функциональные представления

```python
def home(request):
    """главная страница с поиском рейсов"""
    form = FlightSearchForm(request.GET or None)
    flights = Flight.objects.all()
    
    if form.is_valid():
        # фильтрация по параметрам
        departure_city = form.cleaned_data.get('departure_city')
        if departure_city:
            flights = flights.filter(departure_city__icontains=departure_city)
        # ... и другие фильтры
    
    # добавляем средний рейтинг
    flights = flights.annotate(avg_rating=Avg('reviews__rating'))
    
    return render(request, 'home.html', {'form': form, 'flights': flights})
```

**Что происходит:**
1. Создается форма поиска из GET-параметров (`?departure_city=Москва`)
2. Получаем все рейсы из БД
3. Если форма валидна, фильтруем рейсы
4. Добавляем аннотацию (средний рейтинг) используя агрегацию
5. Рендерим шаблон с данными

**Аннотация `annotate(avg_rating=Avg('reviews__rating'))`:**
- Для каждого рейса вычисляет средний рейтинг из всех отзывов
- `reviews__rating` - обращение через связь (ForeignKey)
- Эквивалентно SQL: `SELECT AVG(rating) FROM reviews WHERE flight_id = ...`

```python
@login_required
def create_reservation(request, flight_id):
    """создание резервирования"""
    flight = get_object_or_404(Flight, pk=flight_id)
    
    # проверяем существующее резервирование
    existing = Reservation.objects.filter(user=request.user, flight=flight).first()
    if existing:
        messages.warning(request, 'у вас уже есть резервирование на этот рейс!')
        return redirect('flight_detail', pk=flight_id)
    
    # проверяем доступность мест
    if not flight.is_available:
        messages.error(request, 'нет свободных мест')
        return redirect('flight_detail', pk=flight_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user, flight=flight)
        if form.is_valid():
            form.save()
            messages.success(request, 'резервирование создано!')
            return redirect('my_reservations')
    else:
        form = ReservationForm(user=request.user, flight=flight)
    
    return render(request, 'reservations/create_reservation.html', {'form': form, 'flight': flight})
```

**Что происходит:**
1. `@login_required` - декоратор, требующий авторизации
2. `get_object_or_404` - получить объект или вернуть 404 ошибку
3. Проверки: уже есть бронь? есть места?
4. Если POST-запрос - обрабатываем форму
5. Если GET-запрос - показываем пустую форму
6. `messages` - система сообщений Django для уведомлений

### Классовые представления

```python
class FlightListView(ListView):
    """список всех рейсов"""
    model = Flight
    template_name = 'flights/flight_list.html'
    context_object_name = 'flights'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(avg_rating=Avg('reviews__rating'))
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(flight_number__icontains=search) |
                Q(airline__icontains=search) |
                Q(departure_city__icontains=search) |
                Q(arrival_city__icontains=search)
            )
        return queryset
```

**Преимущества классовых представлений:**
- Меньше кода
- Встроенная пагинация (`paginate_by = 10`)
- Можно переопределять методы (`get_queryset`, `get_context_data`)
- `Q` объекты - для сложных OR-запросов

```python
class FlightDetailView(DetailView):
    """детальная информация о рейсе"""
    model = Flight
    template_name = 'flights/flight_detail.html'
    context_object_name = 'flight'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flight = self.get_object()
        
        # добавляем дополнительные данные
        if self.request.user.is_authenticated:
            context['user_reservation'] = Reservation.objects.filter(
                user=self.request.user,
                flight=flight
            ).first()
        
        context['reservations'] = flight.reservations.filter(is_confirmed=True)
        context['reviews'] = flight.reviews.all()
        context['avg_rating'] = flight.reviews.aggregate(Avg('rating'))['rating__avg']
        
        return context
```

**Что происходит:**
- `get_context_data` - добавляет дополнительные переменные в шаблон
- `self.get_object()` - получает объект Flight по ID из URL
- `flight.reservations` - обратная связь (related_name)
- `aggregate` - агрегирующая функция, возвращает словарь

---

## Формы (Forms)

**Файл:** `flights/forms.py`

Формы валидируют и обрабатывают ввод пользователя.

### UserRegistrationForm

```python
class UserRegistrationForm(UserCreationForm):
    """форма регистрации пользователя"""
    
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'phone_number', 'passport_number', 'date_of_birth'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+79123456789'}),
        }
```

**Наследование от UserCreationForm:**
- Автоматически добавляет поля `password1` и `password2`
- Валидирует совпадение паролей
- Хеширует пароль при сохранении

**Meta класс:**
- `model` - с какой моделью связана форма
- `fields` - какие поля показывать
- `widgets` - HTML-виджеты для полей (атрибуты, стили)

### FlightSearchForm

```python
class FlightSearchForm(forms.Form):
    """форма поиска рейсов"""
    
    departure_city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'город отлета'})
    )
    arrival_city = forms.CharField(required=False, ...)
    departure_date = forms.DateField(required=False, ...)
    flight_type = forms.ChoiceField(choices=[('', 'любой')] + Flight.FLIGHT_TYPE_CHOICES, required=False)
```

**Обычная форма (не ModelForm):**
- Не связана напрямую с моделью
- Используется только для фильтрации
- `required=False` - все поля необязательные

### ReservationForm

```python
class ReservationForm(forms.ModelForm):
    """форма резервирования рейса"""
    
    class Meta:
        model = Reservation
        fields = []  # пустой список - нет видимых полей
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.flight = kwargs.pop('flight', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        reservation = super().save(commit=False)
        reservation.user = self.user
        reservation.flight = self.flight
        if commit:
            reservation.save()
        return reservation
```

**Особенности:**
- `fields = []` - форма без видимых полей (только кнопка отправки)
- Переопределен `__init__` - принимает `user` и `flight` как параметры
- Переопределен `save` - устанавливает `user` и `flight` перед сохранением

---

## Шаблоны (Templates)

**Директория:** `templates/`

### base.html - Базовый шаблон

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Авиарейсы{% endblock %}</title>
    <style>
        /* стили... */
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar">
        <!-- навигация -->
    </nav>
    
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

**Блоки (blocks):**
- `{% block title %}` - заголовок страницы
- `{% block extra_css %}` - дополнительные стили
- `{% block content %}` - основное содержимое

**Другие шаблоны наследуются:**

```html
{% extends 'base.html' %}

{% block title %}Главная{% endblock %}

{% block content %}
    <h1>Содержимое страницы</h1>
{% endblock %}
```

### home.html - Главная страница

**Структура:**
1. **Hero-секция** - заголовок и описание
2. **Форма поиска** - фильтрация рейсов
3. **Сетка карточек рейсов** - отображение результатов

**Django Template Language (DTL):**

```django
{% for flight in flights %}
    <div class="flight-card">
        <div class="flight-number">{{ flight.flight_number }}</div>
        <div>{{ flight.departure_city }} → {{ flight.arrival_city }}</div>
        
        {% if flight.is_available %}
            <span>Доступно мест: {{ flight.available_seats }}</span>
        {% else %}
            <span>Мест нет</span>
        {% endif %}
    </div>
{% endfor %}
```

**Теги и фильтры:**
- `{% for %}` - цикл
- `{% if %}` - условие
- `{{ variable }}` - вывод переменной
- `{{ date|date:"d.m.Y" }}` - фильтр форматирования
- `{% url 'name' %}` - генерация URL по имени

**CSS Flexbox для прижатия кнопки:**

```css
.flight-card {
    display: flex;
    flex-direction: column;  /* вертикальная ориентация */
}

/* Кнопка */
style="margin-top: auto;"  /* прижимается к низу */
```

**Как работает:**
1. `.flight-card` - flex-контейнер с вертикальным направлением
2. Все элементы располагаются сверху вниз
3. `margin-top: auto` у кнопки - она отталкивается от предыдущих элементов вниз

### flight_detail.html - Детали рейса

**Разделы:**
1. Информация о рейсе
2. Бронирование (если авторизован)
3. Список пассажиров (таблица)
4. Отзывы

**Условная логика:**

```django
{% if user.is_authenticated %}
    {% if user_reservation %}
        <p>У вас есть бронь</p>
    {% else %}
        {% if flight.is_available %}
            <a href="{% url 'create_reservation' flight.pk %}">Забронировать</a>
        {% else %}
            <p>Мест нет</p>
        {% endif %}
    {% endif %}
{% else %}
    <a href="{% url 'login' %}">Войти</a>
{% endif %}
```

---

## URL-маршрутизация

### airport_project/urls.py - Главный URL-конфиг

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('flights.urls')),  # подключаем URLs приложения
]
```

**Как работает:**
- `path('admin/', ...)` - `/admin/` → админ-панель
- `include('flights.urls')` - все URL из `flights/urls.py` с префиксом ``

### flights/urls.py - URL приложения

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('flights/', views.FlightListView.as_view(), name='flight_list'),
    path('flights/<int:pk>/', views.FlightDetailView.as_view(), name='flight_detail'),
    
    path('flights/<int:flight_id>/reserve/', views.create_reservation, name='create_reservation'),
    path('my_reservations/', views.my_reservations, name='my_reservations'),
    path('reservations/<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    
    path('flights/<int:flight_id>/review/', views.create_review, name='create_review'),
    path('my_reviews/', views.my_reviews, name='my_reviews'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]
```

**Параметры в URL:**
- `<int:pk>` - целое число, передается в view как `pk`
- `<int:flight_id>` - целое число, передается как `flight_id`

**Именованные URL:**
- `name='home'` - можно использовать в шаблонах: `{% url 'home' %}`
- `name='flight_detail'` - с параметром: `{% url 'flight_detail' flight.pk %}`

**В views получаем параметры:**

```python
def create_reservation(request, flight_id):  # ← из URL
    flight = get_object_or_404(Flight, pk=flight_id)
```

---

## Админ-панель

**Файл:** `flights/admin.py`

### CustomUserAdmin

```python
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """кастомная админка для расширенной модели пользователя"""
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('дополнительная информация', {
            'fields': ('phone_number', 'passport_number', 'date_of_birth')
        }),
    )
```

**Что это дает:**
- `@admin.register(User)` - регистрирует модель в админке
- `list_display` - какие поля показывать в списке
- `fieldsets` - группировка полей на странице редактирования
- Наследование от `BaseUserAdmin` - сохраняет стандартные поля

### FlightAdmin

```python
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'departure_city', 'arrival_city', 'departure_time', 'available_seats_display')
    list_filter = ('airline', 'departure_city', 'arrival_city', 'flight_type')
    search_fields = ('flight_number', 'airline', 'departure_city', 'arrival_city')
    
    def available_seats_display(self, obj):
        return f"{obj.available_seats}/{obj.total_seats}"
    available_seats_display.short_description = 'свободных мест'
```

**Возможности:**
- `list_filter` - фильтры в правой панели
- `search_fields` - поиск по полям
- Кастомные методы для отображения (`available_seats_display`)

### ReservationAdmin

```python
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    actions = ['confirm_reservations', 'cancel_reservations']
    
    def confirm_reservations(self, request, queryset):
        """подтвердить выбранные резервирования"""
        updated = queryset.update(is_confirmed=True, status='confirmed')
        self.message_user(request, f'подтверждено резервирований: {updated}')
    confirm_reservations.short_description = 'подтвердить выбранные резервирования'
```

**Actions (действия):**
- Массовые операции над выбранными объектами
- `queryset.update()` - обновление в один SQL-запрос
- `self.message_user()` - сообщение администратору

---

## Настройки проекта

**Файл:** `airport_project/settings.py`

### Важные настройки

```python
# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',          # админ-панель
    'django.contrib.auth',           # аутентификация
    'django.contrib.contenttypes',   # типы контента
    'django.contrib.sessions',       # сессии
    'django.contrib.messages',       # сообщения
    'django.contrib.staticfiles',    # статические файлы
    'flights',                       # наше приложение
]

# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # где искать шаблоны
        'APP_DIRS': True,                  # искать в приложениях
        'OPTIONS': {
            'context_processors': [        # глобальные переменные
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Локализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Кастомная модель пользователя
AUTH_USER_MODEL = 'flights.User'

# Перенаправления
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'flight_list'
LOGOUT_REDIRECT_URL = 'flight_list'
```

---

## База данных

**Файл:** `db.sqlite3`

### Миграции

**Создание миграций:**
```bash
python manage.py makemigrations
```
- Анализирует изменения в `models.py`
- Создает файл миграции в `migrations/`

**Применение миграций:**
```bash
python manage.py migrate
```
- Выполняет SQL-команды для изменения схемы БД

**Пример миграции:**
```python
class Migration(migrations.Migration):
    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('flight_number', models.CharField(max_length=10)),
                ('airline', models.CharField(max_length=50)),
                # ...
            ],
        ),
    ]
```

### ORM (Object-Relational Mapping)

Django ORM переводит Python-код в SQL:

```python
# Python
flights = Flight.objects.filter(departure_city='Москва').order_by('departure_time')

# SQL
SELECT * FROM flights_flight 
WHERE departure_city = 'Москва' 
ORDER BY departure_time;
```

**Основные операции:**

```python
# Создание
flight = Flight.objects.create(flight_number='SU1234', airline='Аэрофлот', ...)

# Получение одного объекта
flight = Flight.objects.get(pk=1)
flight = get_object_or_404(Flight, pk=1)  # или 404 ошибка

# Получение всех
flights = Flight.objects.all()

# Фильтрация
flights = Flight.objects.filter(airline='Аэрофлот')
flights = Flight.objects.filter(departure_city__icontains='Моск')  # LIKE %Моск%

# Исключение
flights = Flight.objects.exclude(flight_type='arrival')

# Сортировка
flights = Flight.objects.order_by('departure_time')
flights = Flight.objects.order_by('-departure_time')  # обратный порядок

# Агрегация
from django.db.models import Avg, Count
avg_rating = Flight.objects.aggregate(Avg('reviews__rating'))
flight_count = User.objects.annotate(num_flights=Count('reservations'))

# Связи (ForeignKey)
reservation.user  # получить связанного пользователя
reservation.flight  # получить связанный рейс
flight.reservations.all()  # все брони рейса (обратная связь)
user.reservations.all()  # все брони пользователя

# Обновление
flight.price = 10000
flight.save()
# или массово:
Flight.objects.filter(airline='Аэрофлот').update(price=5000)

# Удаление
flight.delete()
Flight.objects.filter(departure_city='Москва').delete()
```

---

## Дополнительные файлы

### manage.py

Утилита командной строки Django:

```bash
python manage.py runserver           # запуск сервера
python manage.py makemigrations      # создать миграции
python manage.py migrate             # применить миграции
python manage.py createsuperuser     # создать админа
python manage.py shell               # Python-консоль с Django
python manage.py collectstatic       # собрать статические файлы
```

### load_test_data.py

Скрипт для загрузки тестовых данных:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airport_project.settings')
django.setup()  # инициализация Django

from flights.models import User, Flight, Reservation, Review

# Создание объектов
user = User.objects.create_user(username='test', password='123')
flight = Flight.objects.create(flight_number='SU1234', ...)
```

---

## Поток работы приложения

### Пример: Бронирование рейса

1. **Пользователь открывает:** `http://127.0.0.1:8000/flights/5/reserve/`

2. **Django находит маршрут:**
```python
path('flights/<int:flight_id>/reserve/', views.create_reservation, name='create_reservation')
```

3. **Вызывается view:**
```python
def create_reservation(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    # ... логика ...
    return render(request, 'reservations/create_reservation.html', context)
```

4. **View получает данные из БД:**
```python
flight = Flight.objects.get(pk=5)
```

5. **View проверяет условия:**
- Пользователь авторизован? (`@login_required`)
- Есть уже бронь? (проверка в БД)
- Есть свободные места? (`flight.is_available`)

6. **Если POST-запрос (отправка формы):**
```python
form = ReservationForm(request.POST, user=request.user, flight=flight)
if form.is_valid():
    reservation = form.save()  # сохранение в БД
    messages.success(request, 'Бронь создана!')
    return redirect('my_reservations')
```

7. **Если GET-запрос:**
```python
form = ReservationForm(user=request.user, flight=flight)
return render(request, 'reservations/create_reservation.html', {'form': form, 'flight': flight})
```

8. **Шаблон рендерится:**
```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Забронировать</button>
</form>
```

9. **HTML возвращается браузеру**

---

## Безопасность

### CSRF Protection

```html
<form method="post">
    {% csrf_token %}  <!-- обязательный токен -->
    ...
</form>
```
- Защита от Cross-Site Request Forgery
- Django генерирует уникальный токен для каждой сессии
- Проверяет токен при POST-запросах

### SQL Injection Protection

Django ORM автоматически экранирует параметры:

```python
# Безопасно:
Flight.objects.filter(airline=user_input)

# НЕ ДЕЛАЙТЕ ТАК:
Flight.objects.raw(f"SELECT * FROM flights WHERE airline = '{user_input}'")
```

### XSS Protection

Шаблоны автоматически экранируют HTML:

```django
{{ user_comment }}  <!-- <script> → &lt;script&gt; -->
```

### Аутентификация

```python
@login_required  # требует авторизации
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    # только брони текущего пользователя
```

---

## Заключение

Проект использует все ключевые концепции Django:

1. **Models** - структура данных
2. **Views** - бизнес-логика
3. **Templates** - представление
4. **Forms** - валидация ввода
5. **Admin** - управление данными
6. **Authentication** - безопасность
7. **ORM** - работа с БД

Каждый компонент связан с другими, образуя целостную систему.

