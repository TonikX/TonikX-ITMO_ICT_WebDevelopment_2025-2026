# Лабораторная работа №3.

## Реализация серверной части приложения средствами django и djangorestframework в соответствии с заданием. 

**Цель:** овладеть практическими навыками и умениями реализации web-сервисов средствами Django. 
Программное обеспечение: Python 3.6+, Django 3, Django REST Framework (DRF), PostgreSQL *.

Практическое задание:
Реализовать сайт, используя фреймворк Django 3, Django REST Framework, Djoser и СУБД PostgreSQL *, в соответствии с вариантом задания лабораторной работы.

Свой вариант «Сайт для продвижения личного бренда».
Есть несколько сущностей: администратор, пользователи. У пользователей есть возможность выбрать услугу на сайте (при этом он должен зарегистрироваться и имеет доступ к кабинету с историей покупок), после выбора услуги можно отправить заявку, узнать статус заявки, посмотреть комментарии, которые появятся к заявке. Личный кабинет пользователя должен быть с возможностью отредактировать личные данные.
Комментарии к заявке и изменение ее статуса должны быть доступны администратору через отдельный админский интерфейс. Также администратор должен иметь возможность добавлять, удалять и редактировать услуги.

База данных:
<img width="897" height="775" alt="image" src="https://github.com/user-attachments/assets/b3fc94c5-ee23-4b73-a3e4-66691d4f044a" />

 
## ДОКУМЕНТАЦИЯ ПРОЕКТА
### Сайт для продвижения личного бренда

---

## СОДЕРЖАНИЕ

1. [Описание проекта](#описание-проекта)
2. [Технологический стек](#технологический-стек)
3. [Установка и настройка](#установка-и-настройка)
4. [Структура базы данных](#структура-базы-данных)
5. [Работа с базой данных через Django ORM](#работа-с-базой-данных-через-django-orm)
6. [API (Django REST Framework)](#api-django-rest-framework)
7. [Аутентификация (Djoser)](#аутентификация-djoser)
8. [Примеры запросов](#примеры-запросов)
9. [Справочник по методам](#справочник-по-методам)
10. [Структура проекта](#структура-проекта)
11. [Чек-лист для развёртывания](#чек-лист-для-развёртывания)

---

## Описание проекта

### Цель проекта
Разработка веб-сервиса для продвижения личного бренда, где пользователи могут:
- Просматривать доступные услуги
- Регистрироваться и авторизовываться
- Создавать заявки на услуги
- Отслеживать статус заявок
- Просматривать комментарии к заявкам
- Оставлять отзывы
- Редактировать личные данные в личном кабинете

Администраторы могут:
- Управлять услугами (создавать, редактировать, удалять, деактивировать)
- Просматривать и изменять статус заявок
- Оставлять комментарии к заявкам
- Управлять отзывами (публиковать/скрывать)
- Управлять пользователями

### Основные сущности
- **Пользователь** (обычный пользователь / администратор)
- **Услуга** (предлагаемые услуги)
- **Заявка** (заказ услуги пользователем)
- **Комментарий** (комментарии администратора к заявке)
- **Файл/Изображение** (материалы к услугам)
- **Отзыв** (отзывы пользователей об услугах)

---

## Технологический стек

| Компонент | Версия/Технология |
|-----------|-------------------|
| Backend Framework | Django 3+ |
| REST Framework | Django REST Framework |
| Аутентификация | Djoser (JWT) |
| База данных | PostgreSQL |
| Язык программирования | Python 3.6+ |

---

## Установка и настройка

### 1. Создание виртуального окружения

```bash
# Создание виртуального окружения
python -m venv .venv

# Активация (Windows)
.\.venv\Scripts\activate
```

### 2. Установка зависимостей

```bash
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install djoser
pip install psycopg2-binary  # для PostgreSQL
```

### 3. Создание файла зависимостей

```bash
pip freeze > requirements.txt
```

**Файл `requirements.txt`:**
```txt
asgiref==3.11.0
Django==3.2.25
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
djoser==2.2.0
psycopg2-binary==2.9.9
PyJWT==2.8.0
sqlparse==0.5.5
tzdata==2025.3
```

### 4. Создание проекта и приложения django

```bash
# Создание проекта
django-admin startproject brand_manager
cd brand_manager

# Создание приложения
python manage.py startapp manager_services
```

### Шаг 5: Настройка `settings.py`

```python
# brand_manager/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'djoser',
    
    # Local apps
    'manager_services',
]

# Настройки базы данных (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'personal_brand_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Настройки статических файлов и медиа
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Настройки аутентификации
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Настройки Djoser
DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'SEND_CONFIRMATION_EMAIL': False,
    'SET_USERNAME_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {
        'user_create': 'core.serializers.UserCreateSerializer',
        'user': 'core.serializers.UserSerializer',
        'current_user': 'core.serializers.UserSerializer',
    },
}

# Настройки JWT
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
```

---

## Структура базы данных

### Модель: Пользователь (User)

```python
# core/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Пользователь системы"""
    
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
    )
    
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, max_length=254, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True, verbose_name='Номер телефона')
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Роль'
    )
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    
    # Поле для аутентификации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]
```

### Модель: Услуга (Service)

```python
class Service(models.Model):
    """Услуга для продвижения личного бренда"""
    
    CATEGORY_CHOICES = (
        ('consulting', 'Консультация'),
        ('coaching', 'Коучинг'),
        ('training', 'Тренинг'),
        ('content', 'Контент'),
        ('design', 'Дизайн'),
        ('marketing', 'Маркетинг'),
    )
    
    name = models.CharField(max_length=200, verbose_name='Название услуги')
    description = models.TextField(verbose_name='Описание услуги')
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена'
    )
    duration = models.IntegerField(
        verbose_name='Продолжительность (в минутах)',
        default=60
    )
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        verbose_name='Категория'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_services',
        verbose_name='Кто создал'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['category']),
        ]
    
    @property
    def primary_image(self):
        """Получить главное изображение услуги"""
        primary = self.files.filter(is_primary=True).first()
        if primary:
            return primary.file_url
        return None
```

### Модель: Заявка (Order)

```python
class Order(models.Model):
    """Заявка на услугу"""
    
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Услуга'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    notes = models.TextField(blank=True, verbose_name='Дополнительные заметки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата завершения'
    )
    
    def __str__(self):
        return f"Заявка #{self.id} - {self.user.email} - {self.service.name}"
    
    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['service']),
        ]
```

### Модель: Комментарий (Comment)

```python
class Comment(models.Model):
    """Комментарий к заявке (от администратора)"""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Заявка'
    )
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='admin_comments',
        verbose_name='Администратор'
    )
    content = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_visible_to_user = models.BooleanField(
        default=True,
        verbose_name='Виден пользователю'
    )
    
    def __str__(self):
        return f"Комментарий к заявке #{self.order.id} от {self.admin.email}"
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['admin']),
        ]
```

### Модель: Файл/Изображение (File)

```python
class File(models.Model):
    """Файл/изображение для услуги"""
    
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Услуга'
    )
    file = models.FileField(
        upload_to='service_files/',
        verbose_name='Файл'
    )
    file_name = models.CharField(
        max_length=255,
        verbose_name='Оригинальное имя файла'
    )
    file_path = models.CharField(
        max_length=500,
        verbose_name='Путь к файлу',
        blank=True
    )
    file_size = models.IntegerField(
        verbose_name='Размер файла (в байтах)',
        default=0
    )
    mime_type = models.CharField(
        max_length=100,
        verbose_name='Тип файла',
        blank=True
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name='Главное изображение'
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_files',
        verbose_name='Кто загрузил'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Альтернативный текст'
    )
    
    def __str__(self):
        return self.file_name
    
    @property
    def file_url(self):
        """Получить URL файла"""
        return self.file.url if self.file else None
    
    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
        indexes = [
            models.Index(fields=['service', 'is_primary']),
            models.Index(fields=['display_order']),
        ]
```

### Модель: Отзыв (Review)

```python
class Review(models.Model):
    """Отзыв о услуге"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Услуга'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name='Заявка'
    )
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Оценка'
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст отзыва')
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Подтвержден'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликован'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    def __str__(self):
        return f"{self.title} - {self.user.email} - {self.rating}★"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        indexes = [
            models.Index(fields=['service', 'is_published']),
            models.Index(fields=['user']),
        ]
```

### Модель: История статусов (OrderStatusHistory)

```python
class OrderStatusHistory(models.Model):
    """История изменений статуса заявки"""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='status_history',
        verbose_name='Заявка'
    )
    status = models.CharField(
        max_length=20,
        choices=Order.STATUS_CHOICES,
        verbose_name='Статус'
    )
    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='status_changes',
        verbose_name='Кто изменил'
    )
    comment = models.TextField(blank=True, verbose_name='Комментарий к изменению')
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    
    def __str__(self):
        return f"{self.order.id} - {self.status} - {self.changed_at}"
    
    class Meta:
        verbose_name = "История статуса"
        verbose_name_plural = "История статусов"
        ordering = ['-changed_at']
```

---

## Работа с базой данных через Django ORM

### Шаг 1: Создание и применение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### Шаг 2: Запуск интерактивного режима

```bash
python manage.py shell
```

### Шаг 3: Импорт моделей

```python
from core.models import User, Service, Order, Comment, File, Review, OrderStatusHistory
from django.utils import timezone
from datetime import datetime, timedelta
```

### Шаг 4: Создание объектов

#### Создание пользователей

```python
# Создание администратора
admin = User.objects.create_user(
    username='admin_user',
    email='admin@personalbrand.com',
    password='admin123',
    first_name='Админ',
    last_name='Админов',
    phone='+79001112233',
    role='admin'
)

# Создание обычных пользователей
user1 = User.objects.create_user(
    username='ivan_ivanov',
    email='ivan@example.com',
    password='user123',
    first_name='Иван',
    last_name='Иванов',
    phone='+79001112244',
    role='user'
)

user2 = User.objects.create_user(
    username='anna_smirnova',
    email='anna@example.com',
    password='user123',
    first_name='Анна',
    last_name='Смирнова',
    phone='+79001112255',
    role='user'
)
```

#### Создание услуг

```python
# Создание услуг
service1 = Service.objects.create(
    name='Консультация по личному бренду',
    description='Индивидуальная консультация по развитию личного бренда',
    price=5000,
    duration=60,
    category='consulting',
    is_active=True,
    created_by=admin
)

service2 = Service.objects.create(
    name='Создание контента для соцсетей',
    description='Разработка контент-плана и создание постов',
    price=15000,
    duration=120,
    category='content',
    is_active=True,
    created_by=admin
)

service3 = Service.objects.create(
    name='Фотосессия для профиля',
    description='Профессиональная фотосессия для социальных сетей',
    price=10000,
    duration=90,
    category='design',
    is_active=True,
    created_by=admin
)
```

#### Создание заявок

```python
# Создание заявок
order1 = Order.objects.create(
    user=user1,
    service=service1,
    status='new',
    notes='Хочу обсудить стратегию развития в LinkedIn'
)

order2 = Order.objects.create(
    user=user1,
    service=service2,
    status='in_progress',
    notes='Нужен контент на 2 недели для Instagram'
)

order3 = Order.objects.create(
    user=user2,
    service=service3,
    status='completed',
    notes='Фотосессия для профиля в соцсетях'
)
```

#### Создание комментариев

```python
# Создание комментариев к заявкам
comment1 = Comment.objects.create(
    order=order1,
    admin=admin,
    content='Здравствуйте! Готов обсудить вашу стратегию. Когда вам удобно?',
    is_visible_to_user=True
)

comment2 = Comment.objects.create(
    order=order2,
    admin=admin,
    content='Начинаю работу над контент-планом. Пришлю черновик через 2 дня.',
    is_visible_to_user=True
)
```

#### Создание файлов

```python
# Создание файлов (в реальном проекте файлы загружаются через форму)
file1 = File.objects.create(
    service=service1,
    file_name='consultation.jpg',
    file_size=256000,
    mime_type='image/jpeg',
    is_primary=True,
    display_order=1,
    uploaded_by=admin,
    alt_text='Консультация по личному бренду'
)

file2 = File.objects.create(
    service=service2,
    file_name='content_plan.png',
    file_size=512000,
    mime_type='image/png',
    is_primary=True,
    display_order=1,
    uploaded_by=admin,
    alt_text='Создание контента'
)
```

#### Создание отзывов

```python
# Создание отзывов
review1 = Review.objects.create(
    user=user2,
    service=service3,
    order=order3,
    rating=5,
    title='Отличная фотосессия!',
    content='Очень доволен результатом. Фотографии получились профессиональными.',
    is_verified=True,
    is_published=True
)
```

### Шаг 5: Фильтрация и запросы

#### Базовая фильтрация

```python
# Все активные услуги
active_services = Service.objects.filter(is_active=True)

# Все заявки пользователя
user_orders = Order.objects.filter(user=user1)

# Заявки со статусом "в работе"
in_progress_orders = Order.objects.filter(status='in_progress')

# Отзывы с оценкой 5
five_star_reviews = Review.objects.filter(rating=5)

# Комментарии, видимые пользователю
visible_comments = Comment.objects.filter(is_visible_to_user=True)
```

#### Фильтрация по связанным таблицам

```python
# Заявки для конкретной услуги
service_orders = Order.objects.filter(service=service1)

# Отзывы для конкретной услуги
service_reviews = Review.objects.filter(service=service1)

# Комментарии для конкретной заявки
order_comments = Comment.objects.filter(order=order1)

# Файлы для конкретной услуги
service_files = File.objects.filter(service=service1)
```

#### Комбинированная фильтрация

```python
# Завершенные заявки пользователя за последний месяц
from django.utils import timezone
from datetime import timedelta

one_month_ago = timezone.now() - timedelta(days=30)
completed_orders = Order.objects.filter(
    user=user1,
    status='completed',
    completed_at__gte=one_month_ago
)

# Опубликованные отзывы для активной услуги
published_reviews = Review.objects.filter(
    service__is_active=True,
    is_published=True
)

# Заявки администратора со статусом "новая" или "в работе"
admin_active_orders = Order.objects.filter(
    service__created_by=admin,
    status__in=['new', 'in_progress']
)
```

### Шаг 6: Агрегация и аннотация

#### Агрегация

```python
from django.db.models import Avg, Count, Min, Max, Sum

# Средняя оценка услуги
avg_rating = Review.objects.filter(service=service1).aggregate(Avg('rating'))
# {'rating__avg': 4.5}

# Количество заявок для услуги
order_count = Order.objects.filter(service=service1).aggregate(Count('id'))
# {'id__count': 10}

# Минимальная и максимальная цена услуг
price_stats = Service.objects.aggregate(
    min_price=Min('price'),
    max_price=Max('price'),
    avg_price=Avg('price')
)
# {'min_price': 5000, 'max_price': 15000, 'avg_price': 10000}
```

#### Аннотация

```python
# Количество отзывов для каждой услуги
services_with_reviews = Service.objects.annotate(
    review_count=Count('reviews')
).order_by('-review_count')

for service in services_with_reviews:
    print(f"{service.name}: {service.review_count} отзывов")

# Средняя оценка для каждой услуги
services_with_avg_rating = Service.objects.annotate(
    avg_rating=Avg('reviews__rating')
).filter(avg_rating__isnull=False)

for service in services_with_avg_rating:
    print(f"{service.name}: {service.avg_rating}★")

# Количество заявок для каждого пользователя
users_with_order_count = User.objects.annotate(
    order_count=Count('orders')
).filter(order_count__gt=0)

for user in users_with_order_count:
    print(f"{user.email}: {user.order_count} заявок")
```

#### Группировка с `.values()`

```python
# Статистика по категориям услуг
category_stats = Service.objects.values('category').annotate(
    count=Count('id'),
    avg_price=Avg('price')
).order_by('-count')

for stat in category_stats:
    print(f"{stat['category']}: {stat['count']} услуг, средняя цена: {stat['avg_price']}")

# Статистика по статусам заявок
status_stats = Order.objects.values('status').annotate(
    count=Count('id')
).order_by('status')

for stat in status_stats:
    print(f"{stat['status']}: {stat['count']} заявок")
```

### Шаг 7: Обновление и удаление

```python
# Обновление статуса заявки
order1.status = 'in_progress'
order1.save()

# Обновление через update()
Order.objects.filter(id=order1.id).update(status='completed')

# Удаление услуги
service3.delete()

# Мягкое удаление (деактивация)
service2.is_active = False
service2.save()
```

---

## API (Django REST Framework)

### Шаг 1: Создание сериализаторов

**Файл: `core/serializers.py`**

```python
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Service, Order, Comment, File, Review, OrderStatusHistory


# ==================== СЕРИАЛИЗАТОРЫ ПОЛЬЗОВАТЕЛЕЙ ====================

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'username', 'phone', 'role', 'date_joined'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'role']


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name',
            'last_name', 'phone', 'password', 'password2'
        ]
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone': {'required': False},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Пароли не совпадают."
            })
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


# ==================== СЕРИАЛИЗАТОРЫ УСЛУГ ====================

class ServiceSerializer(serializers.ModelSerializer):
    """Сериализатор для услуг (публичный)"""
    
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'description', 'price',
            'duration', 'category', 'is_active',
            'created_at', 'primary_image'
        ]
        read_only_fields = ['id', 'created_at', 'primary_image']
    
    def get_primary_image(self, obj):
        return obj.primary_image


class ServiceAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для услуг (админ)"""
    
    created_by_email = serializers.EmailField(
        source='created_by.email',
        read_only=True
    )
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'description', 'price',
            'duration', 'category', 'is_active',
            'created_by', 'created_by_email',
            'created_at', 'updated_at', 'primary_image'
        ]
        read_only_fields = ['id', 'created_by', 'created_by_email', 'created_at', 'updated_at']


# ==================== СЕРИАЛИЗАТОРЫ ЗАЯВОК ====================

class OrderCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заявки"""
    
    class Meta:
        model = Order
        fields = ['id', 'service', 'notes']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для заявки (пользователь)"""
    
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_price = serializers.DecimalField(
        source='service.price',
        max_digits=8,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = Order
        fields = [
            'id', 'service', 'service_name', 'service_price',
            'status', 'notes', 'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'service_name', 'service_price',
            'status', 'created_at', 'updated_at', 'completed_at'
        ]


class OrderAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для заявки (админ)"""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_email', 'user_full_name',
            'service', 'service_name', 'status', 'notes',
            'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'user_email', 'user_full_name', 'service_name']
    
    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()


# ==================== СЕРИАЛИЗАТОРЫ КОММЕНТАРИЕВ ====================

class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    
    admin_email = serializers.EmailField(source='admin.email', read_only=True)
    admin_full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'order', 'admin', 'admin_email',
            'admin_full_name', 'content', 'created_at', 'is_visible_to_user'
        ]
        read_only_fields = [
            'id', 'admin', 'admin_email', 'admin_full_name', 'created_at'
        ]
    
    def get_admin_full_name(self, obj):
        return f"{obj.admin.first_name} {obj.admin.last_name}".strip()


# ==================== СЕРИАЛИЗАТОРЫ ФАЙЛОВ ====================

class FileSerializer(serializers.ModelSerializer):
    """Сериализатор для файлов (публичный)"""
    
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = File
        fields = [
            'id', 'service', 'file_name', 'file_url',
            'file_size', 'mime_type', 'is_primary',
            'display_order', 'alt_text'
        ]
        read_only_fields = [
            'id', 'file_url', 'file_size', 'mime_type'
        ]
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class FileUploadSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки файлов"""
    
    class Meta:
        model = File
        fields = [
            'service', 'file', 'alt_text',
            'is_primary', 'display_order'
        ]
        extra_kwargs = {
            'file': {'required': True},
            'service': {'required': True},
        }


class FileAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для файлов (админ)"""
    
    service_name = serializers.CharField(source='service.name', read_only=True)
    uploaded_by_email = serializers.EmailField(
        source='uploaded_by.email',
        read_only=True
    )
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = File
        fields = [
            'id', 'service', 'service_name', 'file_name',
            'file_url', 'file_path', 'file_size', 'mime_type',
            'is_primary', 'display_order', 'uploaded_by',
            'uploaded_by_email', 'uploaded_at', 'alt_text'
        ]
        read_only_fields = [
            'id', 'file_name', 'file_path', 'file_size',
            'mime_type', 'uploaded_by', 'uploaded_by_email', 'uploaded_at'
        ]
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


# ==================== СЕРИАЛИЗАТОРЫ ОТЗЫВОВ ====================

class ReviewCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отзыва"""
    
    class Meta:
        model = Review
        fields = [
            'order', 'service', 'rating',
            'title', 'content'
        ]
        extra_kwargs = {
            'order': {'required': True},
            'service': {'required': True},
            'rating': {'required': True},
            'title': {'required': True},
            'content': {'required': True},
        }


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыва (публичный)"""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_email', 'service',
            'service_name', 'rating', 'title',
            'content', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'user_email', 'service',
            'service_name', 'created_at', 'updated_at'
        ]


class ReviewAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыва (админ)"""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_email', 'service',
            'service_name', 'order_id', 'rating',
            'title', 'content', 'is_verified',
            'is_published', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'user_email', 'service',
            'service_name', 'order_id', 'created_at', 'updated_at'
        ]


# ==================== СЕРИАЛИЗАТОРЫ СТАТУСОВ ====================

class OrderStatusUpdateSerializer(serializers.Serializer):
    """Сериализатор для изменения статуса заявки"""
    
    STATUS_CHOICES = ['new', 'in_progress', 'completed', 'cancelled']
    
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    comment = serializers.CharField(required=False, allow_blank=True)
    
    def validate_status(self, value):
        if value not in self.STATUS_CHOICES:
            raise serializers.ValidationError("Неверный статус")
        return value


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """Сериализатор для истории статусов"""
    
    changed_by_email = serializers.EmailField(
        source='changed_by.email',
        read_only=True
    )
    
    class Meta:
        model = OrderStatusHistory
        fields = [
            'id', 'order', 'status', 'changed_by',
            'changed_by_email', 'comment', 'changed_at'
        ]
        read_only_fields = [
            'id', 'order', 'changed_by', 'changed_by_email', 'changed_at'
        ]
```

---

### Шаг 2: Создание представлений

**Файл: `core/views.py`**

```python
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg, Q
from datetime import datetime
from .models import User, Service, Order, Comment, File, Review, OrderStatusHistory
from .serializers import (
    UserSerializer, ServiceSerializer, ServiceAdminSerializer,
    OrderCreateSerializer, OrderSerializer, OrderAdminSerializer,
    CommentSerializer, FileSerializer, FileUploadSerializer,
    FileAdminSerializer, ReviewCreateSerializer, ReviewSerializer,
    ReviewAdminSerializer, OrderStatusUpdateSerializer,
    OrderStatusHistorySerializer
)


# ==================== ПЕРМИШЕНЫ (РАЗРЕШЕНИЯ) ====================

class IsAdmin(permissions.BasePermission):
    """Разрешение только для администраторов"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsOwnerOrAdmin(permissions.BasePermission):
    """Разрешение для владельца объекта или администратора"""
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.user == request.user


# ==================== ПУБЛИЧНЫЕ ЕНДПОИНТЫ ====================

class ServiceListView(generics.ListAPIView):
    """GET: Список всех активных услуг (публичный)"""
    
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]


class ServiceDetailView(generics.RetrieveAPIView):
    """GET: Детали услуги (публичный)"""
    
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]


class ServiceFilesView(generics.ListAPIView):
    """GET: Получить файлы для конкретной услуги (публичный)"""
    
    serializer_class = FileSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        service_id = self.kwargs.get('service_id')
        return File.objects.filter(
            service_id=service_id,
            service__is_active=True
        ).order_by('display_order')


class ServiceReviewsView(generics.ListAPIView):
    """GET: Список опубликованных отзывов на услугу"""
    
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        service_id = self.kwargs.get('service_id')
        return Review.objects.filter(
            service_id=service_id,
            is_published=True
        ).order_by('-created_at')


class ServiceCategoriesView(APIView):
    """GET: Список всех категорий услуг с количеством услуг в каждой"""
    
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        categories = Service.objects.filter(is_active=True).values(
            'category'
        ).annotate(
            count=Count('id')
        ).order_by('category')
        
        return Response(categories)


# ==================== ЕНДПОИНТЫ ПОЛЬЗОВАТЕЛЯ ====================

class OrderListView(generics.ListCreateAPIView):
    """GET: Список заявок текущего пользователя | POST: Создание новой заявки"""
    
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    """GET: Детали заявки пользователя"""
    
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCancelView(APIView):
    """POST: Отмена заявки (пользователем)"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, id):
        order = get_object_or_404(Order, id=id, user=request.user)
        
        if order.status == 'cancelled':
            return Response(
                {"detail": "Заявка уже отменена"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if order.status == 'completed':
            return Response(
                {"detail": "Нельзя отменить завершенную заявку"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'cancelled'
        order.save()
        
        # Создаем запись в истории
        OrderStatusHistory.objects.create(
            order=order,
            status='cancelled',
            changed_by=request.user,
            comment='Отменено пользователем'
        )
        
        return Response({"detail": "Заявка отменена"})


class OrderCommentsView(generics.ListAPIView):
    """GET: Получить комментарии к заявке (видимые пользователю)"""
    
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id, user=self.request.user)
        return Comment.objects.filter(
            order=order,
            is_visible_to_user=True
        ).order_by('created_at')


class ReviewCreateView(generics.CreateAPIView):
    """POST: Создать отзыв (только для завершенных заказов пользователя)"""
    
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        order = serializer.validated_data.get('order')
        
        # Проверяем, что заявка принадлежит пользователю и завершена
        if order.user != self.request.user:
            raise serializers.ValidationError(
                "Вы не можете оставить отзыв на эту заявку"
            )
        
        if order.status != 'completed':
            raise serializers.ValidationError(
                "Отзыв можно оставить только на завершенную заявку"
            )
        
        # Проверяем, что отзыв еще не оставлен
        if Review.objects.filter(order=order).exists():
            raise serializers.ValidationError(
                "Отзыв на эту заявку уже существует"
            )
        
        serializer.save(user=self.request.user, is_verified=True)


# ==================== АДМИНСКИЕ ЕНДПОИНТЫ - УСЛУГИ ====================

class AdminServiceListView(generics.ListCreateAPIView):
    """GET: Список всех услуг (для админа, с неактивными) | POST: Создание новой услуги"""
    
    serializer_class = ServiceAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        return Service.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AdminServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET: Детали услуги (админ) | PUT: Полное обновление | PATCH: Частичное | DELETE: Удаление"""
    
    serializer_class = ServiceAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        return Service.objects.all()


class AdminServiceDeactivateView(APIView):
    """POST: Деактивация услуги (админ)"""
    
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def post(self, request, id):
        service = get_object_or_404(Service, id=id)
        service.is_active = False
        service.save()
        return Response({"detail": "Услуга деактивирована"})


# ==================== АДМИНСКИЕ ЕНДПОИНТЫ - ЗАЯВКИ ====================

class AdminOrderListView(generics.ListAPIView):
    """GET: Список всех заявок (админ, с фильтрами)"""
    
    serializer_class = OrderAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        queryset = Order.objects.all().order_by('-created_at')
        
        # Фильтрация по статусу
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Фильтрация по пользователю
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Фильтрация по услуге
        service_id = self.request.query_params.get('service_id')
        if service_id:
            queryset = queryset.filter(service_id=service_id)
        
        return queryset


class AdminOrderDetailView(generics.RetrieveAPIView):
    """GET: Детали заявки (админ)"""
    
    serializer_class = OrderAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        return Order.objects.all()


class AdminOrderStatusHistoryView(generics.ListAPIView):
    """GET: История статусов заявки (админ)"""
    
    serializer_class = OrderStatusHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        order_id = self.kwargs.get('id')
        return OrderStatusHistory.objects.filter(
            order_id=order_id
        ).order_by('-changed_at')


class AdminOrderStatusUpdateView(APIView):
    """PATCH: Изменение статуса заявки (админ)"""
    
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def patch(self, request, id):
        order = get_object_or_404(Order, id=id)
        serializer = OrderStatusUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            new_status = serializer.validated_data['status']
            comment_text = serializer.validated_data.get('comment', '')
            
            # Обновляем статус
            order.status = new_status
            
            # Если заявка завершена, устанавливаем дату завершения
            if new_status == 'completed' and not order.completed_at:
                order.completed_at = datetime.now()
            
            order.save()
            
            # Создаем запись в истории
            OrderStatusHistory.objects.create(
                order=order,
                status=new_status,
                changed_by=request.user,
                comment=comment_text
            )
            
            return Response({"detail": "Статус изменен"})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==================== АДМИНСКИЕ ЕНДПОИНТЫ - КОММЕНТАРИИ ====================

class AdminCommentListView(generics.ListCreateAPIView):
    """GET: Список всех комментариев (админ) | POST: Добавить комментарий к заявке"""
    
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-created_at')
        
        # Фильтрация по заявке
        order_id = self.request.query_params.get('order_id')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)


class AdminCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET: Получить комментарий | PUT/PATCH: Обновить | DELETE: Удалить"""
    
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        return Comment.objects.all()


class AdminCommentVisibilityView(APIView):
    """PATCH: Изменить видимость комментария (админ)"""
    
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def patch(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        comment.is_visible_to_user = not comment.is_visible_to_user
        comment.save()
        return Response({
            "detail": f"Видимость изменена на {comment.is_visible_to_user}"
        })


# ==================== АДМИНСКИЕ ЕНДПОИНТЫ - ФАЙЛЫ ====================

class AdminFileUploadView(generics.CreateAPIView):
    """POST: Загрузка файла для услуги (админ)"""
    
    serializer_class = FileUploadSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def perform_create(self, serializer):
        file_obj = serializer.validated_data['file']
        
        # Создаем запись о файле
        file_instance = serializer.save(
            uploaded_by=self.request.user,
            file_name=file_obj.name,
            file_size=file_obj.size,
            mime_type=file_obj.content_type
        )
        
        # Сохраняем путь к файлу
        file_instance.file_path = file_instance.file.name
        file_instance.save()


class AdminFileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET: Получить информацию о файле | PUT/PATCH: Обновить | DELETE: Удалить"""
    
    serializer_class = FileAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        return File.objects.all()


# ==================== АДМИНСКИЕ ЕНДПОИНТЫ - ОТЗЫВЫ ====================

class AdminReviewListView(generics.ListAPIView):
    """GET: Все отзывы (админ)"""
    
    serializer_class = ReviewAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        return Review.objects.all().order_by('-created_at')


class AdminReviewPendingView(generics.ListAPIView):
    """GET: Список отзывов на модерации (админ)"""
    
    serializer_class = ReviewAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        return Review.objects.filter(is_published=False).order_by('-created_at')


class AdminReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET: Детали отзыва | PUT/PATCH: Обновить | DELETE: Удалить"""
    
    serializer_class = ReviewAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        return Review.objects.all()


class AdminReviewPublishView(APIView):
    """PATCH: Опубликовать/скрыть отзыв (админ)"""
    
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def patch(self, request, id):
        review = get_object_or_404(Review, id=id)
        review.is_published = not review.is_published
        review.save()
        return Response({
            "detail": f"Отзыв {'опубликован' if review.is_published else 'скрыт'}"
        })


# ==================== АДМИНСКИЕ ЕНДПОИНТЫ - ПОЛЬЗОВАТЕЛИ ====================

class AdminUserListView(generics.ListAPIView):
    """GET: Список всех пользователей (админ)"""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')


class AdminUserDetailView(generics.RetrieveAPIView):
    """GET: Детали пользователя (админ)"""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        return User.objects.all()


class AdminUserRoleUpdateView(APIView):
    """PATCH: Изменить роль пользователя (админ)"""
    
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def patch(self, request, id):
        user = get_object_or_404(User, id=id)
        
        # Нельзя изменить роль самого себя
        if user == request.user:
            return Response(
                {"detail": "Нельзя изменить свою роль"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        new_role = request.data.get('role')
        if new_role not in ['user', 'admin']:
            return Response(
                {"detail": "Неверная роль"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.role = new_role
        user.save()
        
        return Response({
            "detail": f"Роль пользователя изменена на {new_role}"
        })
```

---

### Шаг 3: Настройка маршрутов

**Файл: `core/urls.py`**

```python
from django.urls import path
from .views import (
    ServiceListView, ServiceDetailView, ServiceFilesView,
    ServiceReviewsView, ServiceCategoriesView,
    OrderListView, OrderDetailView, OrderCancelView,
    OrderCommentsView, ReviewCreateView,
    AdminServiceListView, AdminServiceDetailView,
    AdminServiceDeactivateView, AdminOrderListView,
    AdminOrderDetailView, AdminOrderStatusHistoryView,
    AdminOrderStatusUpdateView, AdminCommentListView,
    AdminCommentDetailView, AdminCommentVisibilityView,
    AdminFileUploadView, AdminFileDetailView,
    AdminReviewListView, AdminReviewPendingView,
    AdminReviewDetailView, AdminReviewPublishView,
    AdminUserListView, AdminUserDetailView,
    AdminUserRoleUpdateView
)

app_name = "core"

urlpatterns = [
    # ==================== ПУБЛИЧНЫЕ ЕНДПОИНТЫ ====================
    
    # Услуги (публичные)
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<int:id>/', ServiceDetailView.as_view(), name='service-detail'),
    path('services/<int:service_id>/files/', ServiceFilesView.as_view(), name='service-files'),
    path('services/<int:service_id>/reviews/', ServiceReviewsView.as_view(), name='service-reviews'),
    path('services/categories/', ServiceCategoriesView.as_view(), name='service-categories'),
    
    # Заявки (пользователь)
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:id>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
    path('orders/<int:order_id>/comments/', OrderCommentsView.as_view(), name='order-comments'),
    
    # Отзывы (публичные)
    path('reviews/', ReviewCreateView.as_view(), name='review-create'),
    
    
    # ==================== АДМИНСКИЕ ЕНДПОИНТЫ ====================
    
    # Админ - Услуги
    path('admin/services/', AdminServiceListView.as_view(), name='admin-service-list'),
    path('admin/services/<int:id>/', AdminServiceDetailView.as_view(), name='admin-service-detail'),
    path('admin/services/<int:id>/deactivate/', AdminServiceDeactivateView.as_view(), name='admin-service-deactivate'),
    
    # Админ - Заявки
    path('admin/orders/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/orders/<int:id>/', AdminOrderDetailView.as_view(), name='admin-order-detail'),
    path('admin/orders/<int:id>/history/', AdminOrderStatusHistoryView.as_view(), name='admin-order-history'),
    path('admin/orders/<int:id>/status/', AdminOrderStatusUpdateView.as_view(), name='admin-order-status'),
    
    # Админ - Комментарии
    path('admin/comments/', AdminCommentListView.as_view(), name='admin-comment-list'),
    path('admin/comments/<int:id>/', AdminCommentDetailView.as_view(), name='admin-comment-detail'),
    path('admin/comments/<int:id>/visibility/', AdminCommentVisibilityView.as_view(), name='admin-comment-visibility'),
    
    # Админ - Файлы
    path('admin/files/upload/', AdminFileUploadView.as_view(), name='admin-file-upload'),
    path('admin/files/<int:id>/', AdminFileDetailView.as_view(), name='admin-file-detail'),
    
    # Админ - Отзывы
    path('admin/reviews/', AdminReviewListView.as_view(), name='admin-review-list'),
    path('admin/reviews/pending/', AdminReviewPendingView.as_view(), name='admin-review-pending'),
    path('admin/reviews/<int:id>/', AdminReviewDetailView.as_view(), name='admin-review-detail'),
    path('admin/reviews/<int:id>/publish/', AdminReviewPublishView.as_view(), name='admin-review-publish'),
    
    # Админ - Пользователи
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:id>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/users/<int:id>/role/', AdminUserRoleUpdateView.as_view(), name='admin-user-role'),
]
```

**Файл: `personal_brand_project/urls.py`**

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Djoser аутентификация
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
    # API приложения
    path('api/', include('core.urls')),
]

# Настройка медиа файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Аутентификация (Djoser)

### Настройка Djoser

Djoser уже настроен в `settings.py` (см. раздел "Установка и настройка").

### Доступные ендпоинты аутентификации

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/auth/users/` | Регистрация нового пользователя |
| POST | `/auth/jwt/create/` | Получение JWT токена |
| POST | `/auth/jwt/refresh/` | Обновление JWT токена |
| POST | `/auth/jwt/verify/` | Проверка валидности токена |
| GET | `/auth/users/me/` | Получение информации о текущем пользователе |
| PUT/PATCH | `/auth/users/me/` | Обновление данных текущего пользователя |
| POST | `/auth/users/set_password/` | Изменение пароля |

---

## Примеры запросов

### 1. Регистрация пользователя

```bash
curl -X POST http://127.0.0.1:8000/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "newuser",
    "password": "securepassword123",
    "password2": "securepassword123",
    "first_name": "Иван",
    "last_name": "Иванов",
    "phone": "+79001234567"
  }'
```

**Ответ:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "newuser",
  "first_name": "Иван",
  "last_name": "Иванов",
  "phone": "+79001234567"
}
```

### 2. Получение JWT токена

```bash
curl -X POST http://127.0.0.1:8000/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Ответ:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Просмотр списка услуг

```bash
curl http://127.0.0.1:8000/api/services/
```

**Ответ:**
```json
[
  {
    "id": 1,
    "name": "Консультация по личному бренду",
    "description": "Индивидуальная консультация...",
    "price": "5000.00",
    "duration": 60,
    "category": "consulting",
    "is_active": true,
    "created_at": "2026-02-16T10:00:00Z",
    "primary_image": "/media/service_files/consultation.jpg"
  }
]
```

### 4. Создание заявки

```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -d '{
    "service": 1,
    "notes": "Хочу обсудить стратегию развития"
  }'
```

**Ответ:**
```json
{
  "id": 1,
  "service": 1,
  "notes": "Хочу обсудить стратегию развития"
}
```

### 5. Просмотр своих заявок

```bash
curl http://127.0.0.1:8000/api/orders/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

**Ответ:**
```json
[
  {
    "id": 1,
    "service": 1,
    "service_name": "Консультация по личному бренду",
    "service_price": "5000.00",
    "status": "new",
    "notes": "Хочу обсудить стратегию развития",
    "created_at": "2026-02-16T11:00:00Z",
    "updated_at": "2026-02-16T11:00:00Z"
  }
]
```

### 6. Создание услуги (админ)

```bash
curl -X POST http://127.0.0.1:8000/api/admin/services/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -d '{
    "name": "Коучинг по карьерному росту",
    "description": "Индивидуальный коучинг...",
    "price": 10000,
    "duration": 90,
    "category": "coaching",
    "is_active": true
  }'
```

### 7. Изменение статуса заявки (админ)

```bash
curl -X PATCH http://127.0.0.1:8000/api/admin/orders/1/status/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -d '{
    "status": "in_progress",
    "comment": "Начинаю работу над заявкой"
  }'
```

### 8. Загрузка файла для услуги (админ)

```bash
curl -X POST http://127.0.0.1:8000/api/admin/files/upload/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -F "service=1" \
  -F "file=@/path/to/image.jpg" \
  -F "alt_text=Изображение услуги" \
  -F "is_primary=true"
```

---

## Справочник по методам

### HTTP методы и их назначение

| Метод | Назначение | Пример использования |
|-------|-----------|---------------------|
| **GET** | Получение данных | Просмотр списка услуг |
| **POST** | Создание данных | Создание заявки |
| **PUT** | Полное обновление | Обновление всех полей услуги |
| **PATCH** | Частичное обновление | Изменение статуса заявки |
| **DELETE** | Удаление | Удаление отзыва |

### Статус-коды ответов

| Код | Описание | Пример |
|-----|----------|--------|
| **200 OK** | Успешный запрос | Получение списка услуг |
| **201 Created** | Ресурс создан | Регистрация пользователя |
| **204 No Content** | Успешное удаление | Удаление комментария |
| **400 Bad Request** | Ошибка валидации | Неверные данные формы |
| **401 Unauthorized** | Не авторизован | Отсутствует токен |
| **403 Forbidden** | Нет прав доступа | Обычный пользователь пытается удалить услугу |
| **404 Not Found** | Ресурс не найден | Запрос несуществующей услуги |
| **500 Internal Server Error** | Ошибка сервера | Внутренняя ошибка приложения |

---

## Структура проекта

```
personal_brand_project/
├── personal_brand_project/          # Основной пакет проекта
│   ├── __init__.py
│   ├── settings.py                  # Настройки проекта
│   ├── urls.py                      # Главные маршруты
│   ├── wsgi.py
│   └── asgi.py
├── core/                            # Приложение
│   ├── __init__.py
│   ├── models.py                    # Модели данных
│   ├── serializers.py               # Сериализаторы
│   ├── views.py                     # Представления
│   ├── urls.py                      # Маршруты приложения
│   ├── admin.py                     # Админ-панель
│   └── apps.py
├── media/                           # Медиа файлы (изображения)
│   └── service_files/
├── .venv/                           # Виртуальное окружение
├── manage.py
├── requirements.txt                 # Зависимости
└── db.sqlite3 (или PostgreSQL)     # База данных
```

---

## Чек-лист для развёртывания

### ✅ Быстрый старт

```bash
# 1. Клонирование репозитория
git clone <repository-url>
cd personal_brand_project

# 2. Создание и активация виртуального окружения
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Установка зависимостей
pip install -r requirements.txt

# 4. Настройка базы данных
# Создайте базу данных в PostgreSQL
# Обновите настройки в settings.py

# 5. Миграции
python manage.py migrate

# 6. Создание суперпользователя
python manage.py createsuperuser

# 7. Запуск сервера
python manage.py runserver
```

### ✅ Проверка работоспособности

- [ ] Сервер запускается без ошибок
- [ ] Доступна админ-панель (`/admin/`)
- [ ] Работает регистрация пользователя (`/auth/users/`)
- [ ] Работает получение токена (`/auth/jwt/create/`)
- [ ] Доступен список услуг (`/api/services/`)
- [ ] Работает создание заявки (с токеном)
- [ ] Админские ендпоинты работают (с ролью `admin`)

---

## Заключение

Документация предоставляет полное руководство по развёртыванию и использованию проекта "Сайт для продвижения личного бренда". Проект реализует все требования лабораторной работы:

✅ Модели базы данных через Django ORM
✅ API через Django REST Framework
✅ Аутентификация через Djoser (JWT)
✅ Разделение прав доступа (пользователь/админ)
✅ Полноценная документация в формате Markdown
