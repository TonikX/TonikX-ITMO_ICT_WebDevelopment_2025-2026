# Лабораторная работа 2. Реализация простого сайта на Django

## Цель работы
Изучить основы работы Django Web Framework, реализовать CRUD-интерфейсы, систему авторизации, работу с базой данных PostgreSQL и развертывание приложения через Docker.

## Описание проекта
Веб-приложение "Туристическое агентство" для управления турами, бронированиями и отзывами. Система позволяет пользователям просматривать доступные туры, бронировать их, оставлять отзывы, а администраторам - управлять всеми данными через админ-панель.

## Структура проекта

```
django_proj/
├── docker-compose.yaml      # Конфигурация Docker
├── Dockerfile               # Образ приложения
├── docker-entrypoint.sh     # Скрипт автоматической инициализации
├── manage.py                # Главный файл управления Django
├── requirements.txt         # Зависимости Python
├── app/                     # Основное приложение
│   ├── models.py           # Модели данных
│   ├── views.py            # Представления (контроллеры)
│   ├── forms.py            # Формы
│   ├── urls.py             # Маршрутизация
│   ├── admin.py            # Конфигурация админ-панели
│   ├── migrations/         # Миграции базы данных
│   └── templates/          # HTML-шаблоны
├── config/                  # Настройки проекта
│   ├── settings.py         # Конфигурация Django
│   └── urls.py             # Главная маршрутизация
└── static/                  # Статические файлы (изображения)
```

## Реализованные модели данных

### 1. UserProfile
Расширение стандартной модели User для хранения дополнительной информации о пользователе.

```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
```

### 2. Tour (Тур)
Основная модель для хранения информации о туристических турах.

```python
class Tour(models.Model):
    title = models.CharField(max_length=200)
    agency = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    payment_terms = models.TextField(blank=True, null=True)
```

**Поля:**
- `title` - название тура
- `agency` - туристическое агентство
- `description` - описание тура
- `start_date` / `end_date` - даты начала и окончания
- `price` - стоимость
- `city` - город
- `payment_terms` - условия оплаты

### 3. Reservation (Бронирование)
Модель для хранения информации о бронированиях туров пользователями.

```python
class Reservation(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    guests = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    confirmed = models.BooleanField(default=False)
```

**Особенности:**
- `confirmed` - статус подтверждения брони администратором (для имитации оплаты)
- `guests` - количество гостей
- Внешние ключи связывают бронирование с туром и пользователем

### 4. Review (Отзыв)
Модель для хранения отзывов пользователей о турах.

```python
class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()  # 1-10
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
```

## Реализованные представления (Views)

### 1. TourListView - Список туров с пагинацией и поиском

```python
class TourListView(ListView):
    model = Tour
    template_name = 'tour_list.html'
    context_object_name = 'tours'
    paginate_by = 8
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                models.Q(title__icontains=q) |
                models.Q(agency__icontains=q) |
                models.Q(city__icontains=q) |
                models.Q(description__icontains=q)
            )
        return qs.order_by('start_date')
```

**Реализовано:**
- Пагинация страниц (8 туров на странице)
- Поиск по названию, агентству, городу и описанию
- Сортировка по дате начала тура

### 2. TourDetailView - Детальная страница тура с отзывами

```python
class TourDetailView(FormMixin, DetailView):
    model = Tour
    template_name = 'tour_detail.html'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Подсчет подтвержденных броней
        total_guests = self.object.reservations.filter(confirmed=True).aggregate(
            total=Sum('guests')
        )['total'] or 0
        ctx['total_guests'] = total_guests
        ctx['reservations_count'] = self.object.reservations.filter(confirmed=True).count()
        # Проверка брони текущего пользователя
        if self.request.user.is_authenticated:
            ctx['user_reservation'] = self.object.reservations.filter(
                user=self.request.user
            ).first()
        return ctx

    def post(self, request, *args, **kwargs):
        # Обработка формы отзыва
        if not request.user.is_authenticated:
            messages.error(request, 'Войдите, чтобы оставить отзыв')
            return redirect('login')
        
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = self.object
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('tour_detail', pk=self.object.pk)
```

**Функционал:**
- Отображение детальной информации о туре
- Список всех отзывов
- Форма для добавления отзыва с рейтингом (1-10)
- Кнопка бронирования
- Статус бронирования пользователя (подтверждено/ожидает)

### 3. SoldByCityView - Статистика продаж по городам

```python
class SoldByCityView(LoginRequiredMixin, TemplateView):
    template_name = 'sold_by_city.html'

    def get_context_data(self, **kwargs):
        # Статистика всех бронирований
        all_reservations = Tour.objects.filter(
            reservations__isnull=False
        ).values('city').annotate(
            total_reservations=Count('reservations', distinct=True),
            total_guests=Sum('reservations__guests'),
            total_income=Sum(
                models.F('reservations__guests') * models.F('price'),
                output_field=models.DecimalField(max_digits=12, decimal_places=2)
            )
        ).order_by('-total_reservations')

        # Статистика подтвержденных бронирований
        confirmed_reservations = Tour.objects.filter(
            reservations__confirmed=True
        ).values('city').annotate(
            confirmed_reservations=Count('reservations', distinct=True),
            confirmed_guests=Sum('reservations__guests'),
            confirmed_income=Sum(
                models.F('reservations__guests') * models.F('price'),
                output_field=models.DecimalField(max_digits=12, decimal_places=2)
            )
        )
        # Объединение данных...
```

**Функционал:**
- Агрегация данных по городам
- Подсчет общего количества броней и подтвержденных отдельно
- Расчет дохода (количество гостей × цена тура)
- Доступ только для авторизованных пользователей

### 4. Остальные представления

- **TourCreateView** - создание тура (только для администраторов)
- **ReservationCreateView** - быстрое бронирование тура
- **ReservationDeleteView** - отмена бронирования
- **UserReservationListView** - список броней пользователя с пагинацией (10 на странице)
- **ProfileUpdateView** - редактирование профиля
- **register** - регистрация нового пользователя

## Формы

### 1. ReviewForm - Форма отзыва с интерактивным слайдером

```python
class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1, 
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'range',
            'min': '1',
            'max': '10',
            'step': '1',
            'oninput': 'this.nextElementSibling.value = this.value'
        }),
        label='Рейтинг (1-10)'
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Напишите ваш отзыв...'
        }),
        label='Текст отзыва'
    )
```

**Особенности:**
- Интерактивный слайдер для выбора рейтинга
- Отображение выбранного значения в реальном времени
- Стилизация через Bootstrap

### 2. RegisterForm - Форма регистрации с валидацией

```python
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True, label='Имя')
    last_name = forms.CharField(max_length=150, required=True, label='Фамилия')
    date_of_birth = forms.DateField(
        required=True, 
        label='Дата рождения', 
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def clean_password1(self):
        pw = self.cleaned_data.get('password1')
        pw_regex = re.compile(r'^(?=.{8,}$)(?=.*[A-Z])(?=.*[@.\+\-_])[A-Za-z0-9@.\+\-_]+$')
        if not pw_regex.match(pw):
            raise ValidationError(
                'Пароль должен содержать минимум 8 символов, '
                'как минимум одну заглавную букву, '
                'состоять только из латинских букв, цифр и символов @ . + - _.'
            )
        return pw
```

**Валидация пароля:**
- Минимум 8 символов
- Хотя бы одна заглавная буква
- Только латинские буквы, цифры и специальные символы (@, ., +, -, _)

## Расширенная админ-панель

### 1. ReservationAdmin - Управление бронированиями

```python
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'tour', 'user', 'guests', 'status_badge', 'created_at', 'notes_short')
    list_filter = ('confirmed', 'created_at', 'tour__city')
    search_fields = ('user__username', 'user__email', 'tour__title')
    actions = ['confirm_reservations', 'unconfirm_reservations']
    list_editable = ('guests',)
    ordering = ('-created_at',)
    
    def status_badge(self, obj):
        if obj.confirmed:
            return format_html('<span style="color: green; font-weight: bold;">✓ Подтверждено</span>')
        return format_html('<span style="color: orange; font-weight: bold;">⏳ Ожидает</span>')
    
    def confirm_reservations(self, request, queryset):
        updated = queryset.update(confirmed=True)
        self.message_user(request, f"✓ Подтверждено броней: {updated}")
```

**Функционал:**
- Цветные бейджи статусов (зеленый/оранжевый)
- Массовое подтверждение броней
- Фильтры по статусу, дате, городу
- Поиск по пользователю и названию тура
- Редактирование количества гостей прямо в списке

### 2. TourAdmin - Управление турами

```python
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'agency', 'city', 'start_date', 'end_date', 'price', 
                    'total_reservations', 'total_guests')
    search_fields = ('title', 'agency', 'city')
    list_filter = ('city', 'agency', 'start_date')
    
    def total_reservations(self, obj):
        return obj.reservations.count()
    
    def total_guests(self, obj):
        total = obj.reservations.aggregate(total=Sum('guests'))['total'] or 0
        return total
```

**Дополнительные колонки:**
- Общее количество броней
- Общее количество гостей

## Шаблоны и интерфейс

### Базовый шаблон с Bootstrap 5

```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Туристическое агентство{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <!-- Навигационное меню Bootstrap -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand" href="{% url 'about' %}">🏖️ Tours</a>
            <div class="navbar-nav">
                <a class="nav-link" href="{% url 'tour_list' %}">Туры</a>
                {% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'user_reservations' %}">Мои брони</a>
                    <a class="nav-link" href="{% url 'profile' %}">Профиль</a>
                    {% if user.is_staff %}
                        <a class="nav-link" href="{% url 'sold_by_city' %}">Статистика</a>
                    {% endif %}
                    <a class="nav-link" href="{% url 'logout' %}">Выход</a>
                {% else %}
                    <a class="nav-link" href="{% url 'login' %}">Вход</a>
                    <a class="nav-link" href="{% url 'register' %}">Регистрация</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

**Особенности интерфейса:**
- Адаптивное меню Bootstrap 5
- Динамическое отображение пунктов меню в зависимости от авторизации
- Отдельное меню для администраторов
- Использование Bootstrap компонентов (cards, alerts, badges, forms)

### Пагинация в шаблоне tour_list.html

```html
<!-- Пагинация Bootstrap -->
{% if is_paginated %}
<nav aria-label="Page navigation">
    <ul class="pagination justify-content-center">
        {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page=1{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}">Первая</a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}">Назад</a>
            </li>
        {% endif %}

        <li class="page-item active">
            <span class="page-link">{{ page_obj.number }} из {{ page_obj.paginator.num_pages }}</span>
        </li>

        {% if page_obj.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}">Вперед</a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}">Последняя</a>
            </li>
        {% endif %}
    </ul>
</nav>
{% endif %}
```

**Функционал пагинации:**
- Кнопки навигации (первая/последняя/назад/вперед)
- Отображение текущей страницы
- Сохранение параметров поиска при переходе между страницами

### Поиск по турам

```html
<!-- Форма поиска -->
<form method="get" class="mb-4">
    <div class="input-group">
        <input type="text" name="q" class="form-control" 
               placeholder="Поиск по названию, городу, агентству..." 
               value="{{ request.GET.q }}">
        <button class="btn btn-primary" type="submit">🔍 Найти</button>
    </div>
</form>
```

## Docker и автоматизация

### docker-compose.yaml

Был написан базовый докер компоуз с двумя сервисами (приложение и бд)
Для базы данных используется volume для сохранения данных, а для создания бд используются креды, которые прокидываются через .env

### docker-entrypoint.sh - автоматизация сборки при инициализации

Для упрощения деббагинга решил закинуть ентрипоинт который будет сам накатывать миграции и создавать суперпользователя (через менеджмент)

```bash
#!/usr/bin/env bash
set -e

# Ждём, пока Postgres не станет доступен
until pg_isready --host="$POSTGRES_SERVER" --port="$POSTGRES_PORT" \
                 --username="$POSTGRES_USER" --dbname="$POSTGRES_DB"; do
  echo "Waiting for Postgres..."
  sleep 2
done

# Применяем все миграции Django
python manage.py makemigrations 
python manage.py migrate
python manage.py createsu

# Запускаем Django
exec python manage.py runserver 0.0.0.0:8000
```

**Что автоматизировано:**
- Ожидание готовности базы данных PostgreSQL
- Автоматическое создание и применение миграций
- Автоматическое создание суперпользователя
- Запуск сервера разработки

### Dockerfile

Был написан докерфайл с прокидыванием энтрипоинта

```dockerfile
...

# Права на выполнение entrypoint скрипта
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
```

## Реализованный CRUD функционал

### Create (Создание)
- Регистрация пользователя
- Создание тура (для администраторов)
- Создание бронирования
- Создание отзыва

### Read (Чтение)
- Список всех туров с пагинацией и поиском
- Детальная информация о туре
- Список броней пользователя
- Статистика продаж по городам
- Просмотр отзывов

### Update (Обновление)
- Редактирование профиля пользователя
- Редактирование количества гостей в админке
- Подтверждение/отмена подтверждения брони

### Delete (Удаление)
- Отмена бронирования пользователем
- Удаление записей через админ-панель

## Дополнительные возможности

### Фильтры в админ-панели
- По статусу подтверждения брони
- По дате создания
- По городу тура
- По агентству
- По рейтингу отзывов

### Права доступа
- **Анонимные пользователи:** просмотр туров
- **Авторизованные пользователи:** бронирование, отзывы, просмотр своих броней
- **Администраторы:** полный доступ + создание туров + статистика

### Система сообщений (Messages Framework)
```python
messages.success(request, 'Отзыв успешно добавлен!')
messages.error(request, 'Войдите, чтобы оставить отзыв')
```

Отображаются в виде Bootstrap alerts.

## Команды для запуска

```bash
docker-compose up -d --build
```

## Использованный стек

- **Backend:** Python 3.13, Django 5.2.7
- **Database:** PostgreSQL 17
- **Frontend:** HTML5, CSS3, Bootstrap 5 (GPT)
- **Containerization:** Docker, Docker Compose
- **ORM:** Django ORM
- **Forms:** Django Forms with validation
- **Authentication:** Django Auth System

## Выводы

В ходе выполнения лабораторной работы были изучены и реализованы:

1. **Модели Django ORM** - создание связанных моделей с использованием ForeignKey, OneToOneField
2. **Представления** - работа с Class-Based Views (ListView, DetailView, CreateView, DeleteView, TemplateView)
3. **Формы** - создание и валидация форм, кастомные виджеты
4. **CRUD операции** - полный цикл создания, чтения, обновления и удаления данных
5. **Авторизация и аутентификация** - система регистрации, входа, прав доступа
6. **Админ-панель** - расширенная настройка с фильтрами, поиском и массовыми действиями
7. **Пагинация** - разбиение больших списков на страницы
8. **Поиск** - реализация поиска по нескольким полям с использованием Q-объектов
9. **Агрегация данных** - подсчет статистики с использованием Count, Sum
10. **Шаблоны** - наследование, использование тегов и фильтров Django
11. **Bootstrap** - адаптивный дизайн, компоненты (navbar, cards, forms, alerts, badges)
12. **Docker** - контейнеризация приложения, docker-compose, автоматизация развертывания
13. **PostgreSQL** - работа с реляционной базой данных
14. **Миграции** - автоматическое управление схемой базы данных

Приложение полностью функционально, развертывается одной командой и готово к использованию.

