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

 
### Сайт для продвижения личного бренда

---

## Описание проекта

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

### 5. Настройка `settings.py`

В проекте используется Djoser — это простая библиотека для аутентификации в Django. Она используется для генерации токенов для аутентификации. Для этого нужно указать три поля: имя пользователя, адрес электронной почты и пароль. Библиотека работает только с POST-запросами. 

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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Настройки Djoser
DJOSER = {
    "HIDE_USERS": True,
    "USER_ID_FIELD": "id",

    "USER_CREATE_PASSWORD_RETYPE": False,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": False,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": False,
    "SEND_ACTIVATION_EMAIL": False,
    "SEND_CONFIRMATION_EMAIL": False,

    "SERIALIZERS": {
        "user_create": "manager_services.serializers.UserCreateSerializer",
        "user": "manager_services.serializers.UserSerializer",
        "current_user": "manager_services.serializers.UserSerializer",
    },
}

# Настройки JWT
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(hours=3),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=5),
}
```
Настройка JWT (JSON Web Token) при использовании Djoser нужна для реализации аутентификации с помощью токенов. Djoser предоставляет набор представлений Django Rest Framework (DRF) для обработки базовых действий: регистрации, входа, выхода, сброса пароля и активации учётной записи. JWT позволяет: 
- Генерировать токены для идентификации пользователей. Например, сервер может сгенерировать токен с флагом «логин как администратор» и предоставить его клиенту. Клиент использует токен, чтобы доказать, что он вошёл в систему как администратор. 
- Обновлять токены — JWT-токены истекают через выбранный период, и их нужно обновлять. 
- Проверять токены — есть конечные точки Djoser, которые позволяют проверять JWT. 
Для настройки JWT при использовании Djoser используется пакет djangorestframework-simplejwt. 


---

## Структура базы данных

### Модель: Пользователь (User)

```python
# core/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Пользователь системы"""

    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(verbose_name='username', max_length=20, unique=True)
    email = models.EmailField('Электронная почта', unique=True)
    phone = models.CharField('Номер телефона', max_length=20, blank=True)
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=Role.choices,
        default=Role.USER
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
```

### Модель: Услуга (Service)

```python
class Service(models.Model):
    """Услуга"""

    name = models.CharField('Название услуги', max_length=200)
    description = models.TextField('Описание услуги')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField('Продолжительность (в минутах)')
    category = models.CharField('Категория', max_length=100)
    is_active = models.BooleanField('Активна', default=True)
    created_by = models.ForeignKey(
        User,
        verbose_name='Кто создал',
        on_delete=models.PROTECT,
        related_name='created_services',
        limit_choices_to={'role': User.Role.ADMIN}
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
```

### Модель: Заявка (Order)

```python
class Order(models.Model):
    """Заявка на услугу"""

    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_PROGRESS = 'in_progress', 'В работе'
        COMPLETED = 'completed', 'Завершена'
        CANCELLED = 'cancelled', 'Отменена'

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        related_name='orders'
    )
    service = models.ForeignKey(
        Service,
        verbose_name='Услуга',
        on_delete=models.PROTECT,
        related_name='orders'
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    notes = models.TextField('Дополнительные заметки', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    completed_at = models.DateTimeField('Дата завершения', null=True, blank=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заявка #{self.id} - {self.user.email}'

    def save(self, *args, **kwargs):
        # Автоматически устанавливаем completed_at при завершении заявки
        if self.status == self.Status.COMPLETED and not self.completed_at:
            from django.utils import timezone
            self.completed_at = timezone.now()
        elif self.status != self.Status.COMPLETED:
            self.completed_at = None
        super().save(*args, **kwargs)
```

### Модель: Комментарий (Comment)

```python
class Comment(models.Model):
    """Комментарий к заявке"""

    order = models.ForeignKey(
        Order,
        verbose_name='Заявка',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    admin = models.ForeignKey(
        User,
        verbose_name='Администратор',
        on_delete=models.PROTECT,
        related_name='comments',
        limit_choices_to={'role': User.Role.ADMIN}
    )
    content = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_visible_to_user = models.BooleanField('Виден пользователю', default=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий к заявке #{self.order.id}'
```

### Модель: Файл/Изображение (File)

```python
class File(models.Model):
    """Файл/Изображение для услуги"""

    service = models.ForeignKey(
        Service,
        verbose_name='Услуга',
        on_delete=models.CASCADE,
        related_name='files'
    )
    file_name = models.CharField('Оригинальное имя файла', max_length=255)
    file_path = models.CharField('Путь к файлу', max_length=500)
    file_size = models.PositiveIntegerField('Размер файла (в байтах)')
    mime_type = models.CharField('Тип файла', max_length=100)
    is_primary = models.BooleanField('Главное изображение', default=False)
    display_order = models.PositiveIntegerField('Порядок отображения', default=0)
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)
    uploaded_by = models.ForeignKey(
        User,
        verbose_name='Кто загрузил',
        on_delete=models.PROTECT,
        related_name='uploaded_files',
        limit_choices_to={'role': User.Role.ADMIN}
    )
    alt_text = models.CharField('Альтернативный текст', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['display_order', 'uploaded_at']

    def __str__(self):
        return self.file_name
```

### Модель: Отзыв (Review)

```python
class Review(models.Model):
    """Отзыв на услугу"""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    service = models.ForeignKey(
        Service,
        verbose_name='Услуга',
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    order = models.ForeignKey(
        Order,
        verbose_name='Заявка',
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Текст отзыва')
    is_verified = models.BooleanField('Подтвержден', default=True)
    is_published = models.BooleanField('Опубликован', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['order'],
                name='unique_review_per_order'
            )
        ]

    def __str__(self):
        return f'Отзыв от {self.user.email} на {self.service.name}'
```

### Модель: История статусов (OrderStatusHistory)

```python
class OrderStatusHistory(models.Model):
    """История изменения статусов заявки"""

    order = models.ForeignKey(
        Order,
        verbose_name='Заявка',
        on_delete=models.CASCADE,
        related_name='status_history'
    )
    old_status = models.CharField('Старый статус', max_length=20, choices=Order.Status.choices)
    new_status = models.CharField('Новый статус', max_length=20, choices=Order.Status.choices)
    changed_by = models.ForeignKey(
        User,
        verbose_name='Кто изменил',
        on_delete=models.PROTECT,
        related_name='changed_statuses',
        limit_choices_to={'role': User.Role.ADMIN}
    )
    changed_at = models.DateTimeField('Дата изменения', auto_now_add=True)
    comment = models.TextField('Комментарий к изменению', blank=True)

    class Meta:
        verbose_name = 'История статуса'
        verbose_name_plural = 'История статусов'
        ordering = ['-changed_at']

    def __str__(self):
        return f'{self.order} - {self.old_status} → {self.new_status}'
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
from manager_services.models import User, Service, Order, Comment, File, Review, OrderStatusHistory
from django.utils import timezone
from datetime import datetime, timedelta
```

---

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
    role=User.Role.ADMIN,
    is_staff=True
)
admin1 = User.objects.create_user(
    username='superadmin',
    email='admin@example.com',
    password='admin123',
    first_name='Супер',
    last_name='Админ',
    role=User.Role.ADMIN,
    is_staff=True
)


# Создание обычных пользователей
user1 = User.objects.create_user(
    username='ivan_ivanov',
    email='ivan@example.com',
    password='user123',
    first_name='Иван',
    last_name='Иванов',
    phone='+79001112244',
    role=User.Role.USER
)

user2 = User.objects.create_user(
    username='anna_smirnova',
    email='anna@example.com',
    password='user123',
    first_name='Анна',
    last_name='Смирнова',
    phone='+79001112255',
    role=User.Role.USER
)

user3 = User.objects.create_user(
    username='petr_petrov',
    email='petr@example.com',
    password='user123',
    first_name='Петр',
    last_name='Петров',
    phone='+79001112266',
    role=User.Role.USER
)
```

#### Создание услуг

```python
# Создание услуг администратором
service1 = Service.objects.create(
    name='Консультация по личному бренду',
    description='Индивидуальная консультация по развитию личного бренда с анализом текущей ситуации и разработкой стратегии',
    price=5000,
    duration=60,
    category='consulting',
    is_active=True,
    created_by=admin
)

service2 = Service.objects.create(
    name='Создание контента для соцсетей',
    description='Разработка контент-плана и создание постов для социальных сетей на 2 недели',
    price=15000,
    duration=120,
    category='content',
    is_active=True,
    created_by=admin
)

service3 = Service.objects.create(
    name='Фотосессия для профиля',
    description='Профессиональная фотосессия для социальных сетей и профессионального профиля',
    price=10000,
    duration=90,
    category='design',
    is_active=True,
    created_by=admin
)

service4 = Service.objects.create(
    name='Коучинг по карьерному росту',
    description='Индивидуальный коучинг для достижения карьерных целей и профессионального развития',
    price=12000,
    duration=90,
    category='coaching',
    is_active=True,
    created_by=admin
)

service5 = Service.objects.create(
    name='Анализ конкурентов',
    description='Глубокий анализ конкурентов в вашей нише с выявлением сильных и слабых сторон',
    price=8000,
    duration=60,
    category='marketing',
    is_active=True,
    created_by=admin
)
```

#### Создание заявок

```python
# Создание заявок пользователями
order1 = Order.objects.create(
    user=user1,
    service=service1,
    status=Order.Status.NEW,
    notes='Хочу обсудить стратегию развития в LinkedIn и профессиональном сообществе'
)

order2 = Order.objects.create(
    user=user1,
    service=service2,
    status=Order.Status.IN_PROGRESS,
    notes='Нужен контент на 2 недели для Instagram с акцентом на экспертность'
)

order3 = Order.objects.create(
    user=user2,
    service=service3,
    status=Order.Status.COMPLETED,
    notes='Фотосессия для профиля в соцсетях и LinkedIn'
)

order4 = Order.objects.create(
    user=user3,
    service=service4,
    status=Order.Status.NEW,
    notes='Хочу проработать карьерные цели на следующие 2 года'
)

order5 = Order.objects.create(
    user=user2,
    service=service5,
    status=Order.Status.IN_PROGRESS,
    notes='Анализ конкурентов в сфере консалтинга'
)
```

#### Создание комментариев

```python
# Создание комментариев администратором к заявкам
comment1 = Comment.objects.create(
    order=order1,
    admin=admin,
    content='Здравствуйте, Иван! Готов обсудить вашу стратегию. Предлагаю назначить встречу на следующей неделе. Какие у вас предпочтения по времени?',
    is_visible_to_user=True
)

comment2 = Comment.objects.create(
    order=order2,
    admin=admin,
    content='Начинаю работу над контент-планом. Пришлю черновик через 2 дня для вашего согласования.',
    is_visible_to_user=True
)

comment3 = Comment.objects.create(
    order=order3,
    admin=admin,
    content='Фотосессия успешно завершена! Отправляю вам отобранные фотографии для выбора финальных вариантов.',
    is_visible_to_user=True
)

comment4 = Comment.objects.create(
    order=order4,
    admin=admin,
    content='Петр, давайте начнем с анализа вашей текущей ситуации и определим приоритетные цели.',
    is_visible_to_user=True
)
```

#### Создание файлов/изображений

```python
# Создание файлов для услуг (в реальном проекте файлы загружаются через форму)
file1 = File.objects.create(
    service=service1,
    file_name='consultation_main.jpg',
    file_path='/media/service_files/consultation_main.jpg',
    file_size=256000,
    mime_type='image/jpeg',
    is_primary=True,
    display_order=1,
    uploaded_by=admin,
    alt_text='Консультация по личному бренду'
)

file2 = File.objects.create(
    service=service1,
    file_name='consultation_process.png',
    file_path='/media/service_files/consultation_process.png',
    file_size=512000,
    mime_type='image/png',
    is_primary=False,
    display_order=2,
    uploaded_by=admin,
    alt_text='Процесс консультации'
)

file3 = File.objects.create(
    service=service2,
    file_name='content_plan_example.jpg',
    file_path='/media/service_files/content_plan_example.jpg',
    file_size=384000,
    mime_type='image/jpeg',
    is_primary=True,
    display_order=1,
    uploaded_by=admin,
    alt_text='Пример контент-плана'
)

file4 = File.objects.create(
    service=service3,
    file_name='photo_session_samples.jpg',
    file_path='/media/service_files/photo_session_samples.jpg',
    file_size=768000,
    mime_type='image/jpeg',
    is_primary=True,
    display_order=1,
    uploaded_by=admin,
    alt_text='Примеры фотосессий'
)
```

#### Создание отзывов

```python
# Создание отзывов (только для завершенных заявок)
review1 = Review.objects.create(
    user=user2,
    service=service3,
    order=order3,
    rating=5,
    title='Отличная фотосессия!',
    content='Очень доволен результатом! Фотографии получились профессиональными и естественными. Рекомендую!',
    is_verified=True,
    is_published=True
)

```

#### Создание истории статусов

```python
# История изменений статусов (создается автоматически при изменении статуса)
# Пример ручного создания для демонстрации:

history1 = OrderStatusHistory.objects.create(
    order=order1,
    old_status=Order.Status.NEW,
    new_status=Order.Status.IN_PROGRESS,
    changed_by=admin,
    comment='Начал работу над заявкой'
)

history2 = OrderStatusHistory.objects.create(
    order=order3,
    old_status=Order.Status.IN_PROGRESS,
    new_status=Order.Status.COMPLETED,
    changed_by=admin,
    comment='Услуга оказана, фотографии переданы клиенту'
)

history3 = OrderStatusHistory.objects.create(
    order=order2,
    old_status=Order.Status.NEW,
    new_status=Order.Status.IN_PROGRESS,
    changed_by=admin,
    comment='Начал разработку контент-плана'
)
```

---

### Шаг 5: Фильтрация и запросы

#### Базовая фильтрация

```python
# Все активные услуги
active_services = Service.objects.filter(is_active=True)
print(f"Активных услуг: {active_services.count()}")

# Все заявки пользователя
user_orders = Order.objects.filter(user=user1)
print(f"Заявок у {user1.username}: {user_orders.count()}")

# Заявки со статусом "в работе"
in_progress_orders = Order.objects.filter(status=Order.Status.IN_PROGRESS)
print(f"Заявок в работе: {in_progress_orders.count()}")

# Отзывы с оценкой 5
five_star_reviews = Review.objects.filter(rating=5)
print(f"Отзывов на 5 звезд: {five_star_reviews.count()}")

# Комментарии, видимые пользователю
visible_comments = Comment.objects.filter(is_visible_to_user=True)
print(f"Видимых комментариев: {visible_comments.count()}")

# Администраторы
admins = User.objects.filter(role=User.Role.ADMIN)
print(f"Администраторов: {admins.count()}")
```

Результат:

<img width="1289" height="697" alt="image" src="https://github.com/user-attachments/assets/c366d192-3be4-47be-93a6-b0d3d9ee107e" />


#### Фильтрация по связанным таблицам

```python
# Заявки для конкретной услуги
service_orders = Order.objects.filter(service=service1)
print(f"Заявок на услугу '{service1.name}': {service_orders.count()}")

# Отзывы для конкретной услуги
service_reviews = Review.objects.filter(service=service3)
print(f"Отзывов на услугу '{service3.name}': {service_reviews.count()}")

# Комментарии для конкретной заявки
order_comments = Comment.objects.filter(order=order1)
print(f"Комментариев к заявке #{order1.id}: {order_comments.count()}")

```
Результат:

<img width="1120" height="504" alt="image" src="https://github.com/user-attachments/assets/2ca58d55-7efd-4f77-b2ec-df2a941b75ce" />

#### Комбинированная фильтрация

```python
# Завершенные заявки пользователя за последний месяц
from django.utils import timezone
from datetime import timedelta

one_month_ago = timezone.now() - timedelta(days=30)
completed_orders = Order.objects.filter(
    user=user1,
    status=Order.Status.COMPLETED,
    completed_at__gte=one_month_ago
)
print(f"Завершенных заявок за месяц: {completed_orders.count()}")

# Опубликованные отзывы для активной услуги
published_reviews = Review.objects.filter(
    service__is_active=True,
    is_published=True
)
print(f"Опубликованных отзывов: {published_reviews.count()}")

# Заявки администратора со статусом "новая" или "в работе"
admin_active_orders = Order.objects.filter(
    service__created_by=admin,
    status__in=[Order.Status.NEW, Order.Status.IN_PROGRESS]
)
print(f"Активных заявок администратора: {admin_active_orders.count()}")

# Пользователи с ролью "пользователь" и не пустым телефоном
active_users = User.objects.filter(
    role=User.Role.USER,
    phone__isnull=False
)
print(f"Активных пользователей с телефоном: {active_users.count()}")

# Заявки, созданные за последние 7 дней
week_ago = timezone.now() - timedelta(days=7)
recent_orders = Order.objects.filter(created_at__gte=week_ago)
print(f"Заявок за неделю: {recent_orders.count()}")
```
Результат:

<img width="1272" height="735" alt="image" src="https://github.com/user-attachments/assets/75d859f7-2396-4766-be84-04fff9bf4b8c" />

<img width="1197" height="409" alt="image" src="https://github.com/user-attachments/assets/f389ed87-7161-42a6-b44e-270a8dd242c2" />



#### Фильтрация по тексту

```python
# Услуги, название которых содержит "консультация"
consulting_services = Service.objects.filter(
    name__icontains='консультация'
)
print(f"Услуг с 'консультация': {consulting_services.count()}")

# Услуги категории "коучинг" или "консалтинг"
coaching_services = Service.objects.filter(
    category__in=['coaching', 'consulting']
)
print(f"Коучинговых услуг: {coaching_services.count()}")

# Отзывы с заголовком, начинающимся на "Отлично"
excellent_reviews = Review.objects.filter(
    title__istartswith='отлично'
)
print(f"Отзывов 'Отлично': {excellent_reviews.count()}")
```

Результат:

<img width="1005" height="607" alt="image" src="https://github.com/user-attachments/assets/6766a8a1-20a6-4415-9669-ea1b6f6f178e" />


#### Фильтрация через историю статусов

```python
# Заявки, которые были переведены в статус "завершена" администратором
completed_by_admin = OrderStatusHistory.objects.filter(
    new_status=Order.Status.COMPLETED,
    changed_by=admin
)
print(f"Завершенных администратором: {completed_by_admin.count()}")

# Заявки, которые были отменены
cancelled_orders = Order.objects.filter(status=Order.Status.CANCELLED)
print(f"Отмененных заявок: {cancelled_orders.count()}")
```
Вывод:

<img width="1101" height="343" alt="image" src="https://github.com/user-attachments/assets/cef0d159-867f-488d-8ec0-79b421729912" />


---

### Шаг 6: Агрегация и аннотация

#### Агрегация

```python
from django.db.models import Avg, Count, Min, Max, Sum, Q

# Средняя оценка всех отзывов
avg_rating = Review.objects.aggregate(Avg('rating'))
print(f"Средняя оценка: {avg_rating['rating__avg']}")

# Количество заявок для конкретной услуги
order_count = Order.objects.filter(service=service1).aggregate(Count('id'))
print(f"Заявок на услугу '{service1.name}': {order_count['id__count']}")

# Минимальная и максимальная цена услуг
price_stats = Service.objects.aggregate(
    min_price=Min('price'),
    max_price=Max('price'),
    avg_price=Avg('price')
)
print(f"Цены: мин {price_stats['min_price']}, макс {price_stats['max_price']}, сред {price_stats['avg_price']}")

# Общее количество отзывов
total_reviews = Review.objects.aggregate(Count('id'))
print(f"Всего отзывов: {total_reviews['id__count']}")

# Количество опубликованных отзывов
published_count = Review.objects.filter(is_published=True).aggregate(Count('id'))
print(f"Опубликованных отзывов: {published_count['id__count']}")

# Статистика по статусам заявок
status_stats = Order.objects.values('status').annotate(
    count=Count('id')
).order_by('status')
for stat in status_stats:
    print(f"Статус {stat['status']}: {stat['count']} заявок")
```

Результат агрегации:
<img width="1218" height="181" alt="image" src="https://github.com/user-attachments/assets/3f0c6783-86b5-41d3-aa07-8ad425f072b9" />

<img width="1305" height="836" alt="image" src="https://github.com/user-attachments/assets/805127b7-f2f0-4c2a-a0cc-6b87a650a6d6" />


#### Аннотация

```python
# Количество отзывов для каждой услуги
services_with_reviews = Service.objects.annotate(
    review_count=Count('reviews')
).order_by('-review_count')

print("\nУслуги по количеству отзывов:")
for service in services_with_reviews:
    print(f"  {service.name}: {service.review_count} отзывов")

# Средняя оценка для каждой услуги
services_with_avg_rating = Service.objects.annotate(
    avg_rating=Avg('reviews__rating')
).filter(avg_rating__isnull=False).order_by('-avg_rating')

print("\nУслуги по средней оценке:")
for service in services_with_avg_rating:
    print(f"  {service.name}: {service.avg_rating:.1f}★")

# Количество заявок для каждого пользователя
users_with_order_count = User.objects.filter(
    role=User.Role.USER
).annotate(
    order_count=Count('orders')
).filter(order_count__gt=0).order_by('-order_count')

print("\nПользователи по количеству заявок:")
for user in users_with_order_count:
    print(f"  {user.username}: {user.order_count} заявок")

# Количество комментариев для каждой заявки
orders_with_comments = Order.objects.annotate(
    comment_count=Count('comments')
).filter(comment_count__gt=0).order_by('-comment_count')

print("\nЗаявки по количеству комментариев:")
for order in orders_with_comments:
    print(f"  Заявка #{order.id}: {order.comment_count} комментариев")

# Количество файлов для каждой услуги
services_with_files = Service.objects.annotate(
    file_count=Count('files')
).order_by('-file_count')

print("\nУслуги по количеству файлов:")
for service in services_with_files:
    print(f"  {service.name}: {service.file_count} файлов")
```

#### Группировка с `.values()`

```python
# Статистика по категориям услуг
category_stats = Service.objects.values('category').annotate(
    count=Count('id'),
    avg_price=Avg('price'),
    min_price=Min('price'),
    max_price=Max('price')
).order_by('-count')

print("\nСтатистика по категориям:")
for stat in category_stats:
    print(f"  {stat['category']}: {stat['count']} услуг, "
          f"сред. цена: {stat['avg_price']:.0f}, "
          f"диапазон: {stat['min_price']} - {stat['max_price']}")

# Статистика по статусам заявок с группировкой по пользователю
user_status_stats = Order.objects.values(
    'user__username',
    'status'
).annotate(
    count=Count('id')
).order_by('user__username', 'status')

print("\nСтатистика заявок по пользователям и статусам:")
current_user = None
for stat in user_status_stats:
    if stat['user__username'] != current_user:
        current_user = stat['user__username']
        print(f"\n  {current_user}:")
    print(f"    {stat['status']}: {stat['count']}")

# Статистика отзывов по оценкам
rating_distribution = Review.objects.values('rating').annotate(
    count=Count('id')
).order_by('rating')

print("\nРаспределение оценок:")
for stat in rating_distribution:
    print(f"  {stat['rating']}★: {stat['count']} отзывов")

# Статистика по администраторам (кто сколько комментариев оставил)
admin_comment_stats = Comment.objects.values(
    'admin__username'
).annotate(
    comment_count=Count('id')
).order_by('-comment_count')

print("\nСтатистика комментариев по администраторам:")
for stat in admin_comment_stats:
    print(f"  {stat['admin__username']}: {stat['comment_count']} комментариев")
```

---

### Шаг 7: Обновление и удаление

#### Обновление объектов

```python
# Обновление статуса заявки (автоматически создается запись в истории)
order1.status = Order.Status.IN_PROGRESS
order1.save()
print(f"Статус заявки #{order1.id} изменен на: {order1.get_status_display()}")

# Проверка автоматического создания истории
history = OrderStatusHistory.objects.filter(
    order=order1,
    new_status=Order.Status.IN_PROGRESS
).first()
if history:
    print(f"Создана запись в истории: {history.old_status} → {history.new_status}")

# Обновление через update() (не вызывает сигналы и не создает историю)
Order.objects.filter(id=order2.id).update(
    status=Order.Status.COMPLETED
)
print(f"Заявка #{order2.id} завершена через update()")

# Обновление нескольких полей
service1.name = 'Премиум консультация по личному бренду'
service1.price = 7000
service1.save()
print(f"Услуга обновлена: {service1.name}, новая цена: {service1.price}")

# Частичное обновление через словарь
Service.objects.filter(id=service2.id).update(
    price=18000,
    duration=150
)
print(f"Услуга '{service2.name}' обновлена: цена {service2.price}, длительность {service2.duration}")

# Обновление видимости комментария
comment1.is_visible_to_user = False
comment1.save()
print(f"Комментарий #{comment1.id} скрыт от пользователя")

# Публикация отзыва
review1.is_published = True
review1.save()
print(f"Отзыв опубликован: {review1.title}")
```

#### Удаление объектов

```python
# Удаление отзыва
review_to_delete = Review.objects.filter(
    user=user2,
    service=service3
).first()
if review_to_delete:
    review_id = review_to_delete.id
    review_to_delete.delete()
    print(f"Отзыв #{review_id} удален")

# Мягкое удаление (деактивация услуги)
service_to_deactivate = Service.objects.get(id=service5.id)
service_to_deactivate.is_active = False
service_to_deactivate.save()
print(f"Услуга '{service_to_deactivate.name}' деактивирована")

# Проверка, что деактивированная услуга не показывается в публичном списке
active_count = Service.objects.filter(is_active=True).count()
print(f"Активных услуг после деактивации: {active_count}")

# Удаление комментария
comment_to_delete = Comment.objects.filter(
    order=order4
).first()
if comment_to_delete:
    comment_id = comment_to_delete.id
    comment_to_delete.delete()
    print(f"Комментарий #{comment_id} удален")

# Внимание: удаление пользователя с заявками вызовет ошибку из-за on_delete=PROTECT
# Сначала нужно удалить или переназначить связанные объекты
```

---

## API (Django REST Framework)

### Создание сериализаторов

**Файл: `manager_services/serializers.py`**

```python
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import User

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'phone', 'password')

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'phone', 'role', 'date_joined')


from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Service, File, Order, OrderStatusHistory, Comment, Review
from django.utils import timezone

User = get_user_model()


class ServiceListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка услуг (публичный)"""
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration',
                  'category', 'primary_image', 'created_at']
        read_only_fields = ['created_at']

    def get_primary_image(self, obj):
        """Получить главное изображение услуги"""
        primary_file = obj.files.filter(is_primary=True).first()
        if primary_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_file.file_path)
            return primary_file.file_path
        return None


class ServiceDetailSerializer(ServiceListSerializer):
    """Сериализатор для деталей услуги (публичный)"""
    images = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta(ServiceListSerializer.Meta):
        fields = ServiceListSerializer.Meta.fields + [
            'images', 'review_count', 'average_rating'
        ]

    def get_images(self, obj):
        """Получить все изображения услуги"""
        files = obj.files.all().order_by('display_order')
        request = self.context.get('request')
        return [
            {
                'id': file.id,
                'url': request.build_absolute_uri(file.file_path) if request else file.file_path,
                'alt_text': file.alt_text,
                'is_primary': file.is_primary
            }
            for file in files
        ]

    def get_review_count(self, obj):
        """Количество опубликованных отзывов"""
        return obj.reviews.filter(is_published=True).count()

    def get_average_rating(self, obj):
        """Средний рейтинг опубликованных отзывов"""
        published_reviews = obj.reviews.filter(is_published=True)
        if published_reviews.exists():
            return round(
                sum(review.rating for review in published_reviews) / published_reviews.count(),
                1
            )
        return None


class ServiceAdminSerializer(ServiceListSerializer):  # Изменено: наследуемся от ServiceListSerializer
    """Сериализатор для админской работы с услугами"""
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)

    class Meta(ServiceListSerializer.Meta):
        fields = ServiceListSerializer.Meta.fields + ['is_active', 'created_by', 'created_by_email',
                  'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        """При создании услуги автоматически устанавливаем создателя"""
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class FileSerializer(serializers.ModelSerializer):
    """Сериализатор для файлов (админ)"""
    uploaded_by_email = serializers.EmailField(source='uploaded_by.email', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'service', 'service_name', 'file_name', 'file_url',
                  'file_path', 'file_size', 'mime_type', 'is_primary',
                  'display_order', 'uploaded_by', 'uploaded_by_email',
                  'uploaded_at', 'alt_text']
        read_only_fields = ['uploaded_by', 'uploaded_at', 'file_path',
                            'file_size', 'mime_type']

    def get_file_url(self, obj):
        """Полный URL к файлу"""
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file_path)
        return obj.file_path

    def validate(self, data):
        """Проверка, что только один файл может быть главным"""
        if data.get('is_primary', False):
            service = data.get('service') or self.instance.service
            # Если это обновление, исключаем текущий файл из проверки
            if self.instance:
                other_primary = File.objects.filter(
                    service=service,
                    is_primary=True
                ).exclude(id=self.instance.id).exists()
            else:
                other_primary = File.objects.filter(
                    service=service,
                    is_primary=True
                ).exists()

            if other_primary:
                raise serializers.ValidationError({
                    'is_primary': 'У услуги уже есть главное изображение'
                })
        return data

    def create(self, validated_data):
        """При создании файла автоматически устанавливаем загрузившего"""
        user = self.context['request'].user
        validated_data['uploaded_by'] = user
        return super().create(validated_data)


class FileUploadSerializer(serializers.Serializer):
    """Сериализатор для загрузки файлов"""
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    file = serializers.FileField()
    alt_text = serializers.CharField(max_length=255, required=False, allow_blank=True)
    is_primary = serializers.BooleanField(default=False)
    display_order = serializers.IntegerField(default=0, min_value=0)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    admin_email = serializers.EmailField(source='admin.email', read_only=True)
    admin_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'order', 'admin', 'admin_email', 'admin_full_name',
                  'content', 'created_at', 'is_visible_to_user']
        read_only_fields = ['admin', 'created_at']

    def get_admin_full_name(self, obj):
        return obj.admin.get_full_name()

    def create(self, validated_data):
        """При создании комментария автоматически устанавливаем администратора"""
        user = self.context['request'].user
        validated_data['admin'] = user
        return super().create(validated_data)


class CommentVisibilitySerializer(serializers.ModelSerializer):
    """Сериализатор для изменения видимости комментария"""

    class Meta:
        model = Comment
        fields = ['is_visible_to_user']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отзыва"""

    class Meta:
        model = Review
        fields = ['order', 'service', 'rating', 'title', 'content']
        read_only_fields = ['user', 'is_verified', 'is_published']

    def validate(self, data):
        """Проверка возможности оставить отзыв"""
        user = self.context['request'].user
        order = data['order']
        service = data['service']

        # Проверка, что заявка принадлежит пользователю
        if order.user != user:
            raise serializers.ValidationError({
                'order': 'Эта заявка не принадлежит вам'
            })

        # Проверка, что заявка завершена
        if order.status != Order.Status.COMPLETED:
            raise serializers.ValidationError({
                'order': 'Отзыв можно оставить только к завершенной заявке'
            })

        # Проверка, что услуга в заявке соответствует выбранной услуге
        if order.service != service:
            raise serializers.ValidationError({
                'service': 'Услуга в заявке не соответствует выбранной услуге'
            })

        # Проверка, что отзыв еще не оставляли
        if Review.objects.filter(order=order).exists():
            raise serializers.ValidationError({
                'order': 'Вы уже оставляли отзыв к этой заявке'
            })

        return data

    def create(self, validated_data):
        """При создании отзыва автоматически устанавливаем пользователя"""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class ReviewListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка отзывов (публичный)"""
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user_full_name', 'rating', 'title', 'content',
                  'created_at', 'is_verified']
        read_only_fields = ['created_at']

    def get_user_full_name(self, obj):
        # Показываем только инициалы для приватности
        full_name = obj.user.get_full_name()
        if full_name:
            parts = full_name.split()
            if len(parts) >= 2:
                return f"{parts[0]} {parts[1][0]}."
        return full_name


class ReviewDetailSerializer(ReviewListSerializer):
    """Сериализатор для деталей отзыва"""
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta(ReviewListSerializer.Meta):
        fields = ReviewListSerializer.Meta.fields + ['service_name', 'updated_at']


class ReviewAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для админской работы с отзывами"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    order_id = serializers.IntegerField(source='order.id', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_email',
                  'service', 'service_name', 'order_id', 'rating',
                  'title', 'content', 'is_verified', 'is_published',
                  'created_at', 'updated_at']
        read_only_fields = ['user', 'service', 'order', 'created_at', 'updated_at']


class UserAdminListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка пользователей (админ)"""
    order_count = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone',
                  'role', 'date_joined', 'order_count', 'review_count']

    def get_order_count(self, obj):
        return obj.orders.count()

    def get_review_count(self, obj):
        return obj.reviews.count()


class UserAdminDetailSerializer(UserAdminListSerializer):
    """Сериализатор для деталей пользователя (админ)"""

    class Meta(UserAdminListSerializer.Meta):
        fields = UserAdminListSerializer.Meta.fields + ['last_login']


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения роли пользователя"""

    class Meta:
        model = User
        fields = ['role']


class CategorySerializer(serializers.Serializer):
    """Сериализатор для категорий услуг"""
    name = serializers.CharField()
    service_count = serializers.IntegerField()


class OrderCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заявки"""

    class Meta:
        model = Order
        fields = ['service', 'notes']

    def validate_service(self, value):
        """Проверка, что услуга активна"""
        if not value.is_active:
            raise serializers.ValidationError("Эта услуга временно недоступна")
        return value

    def create(self, validated_data):
        """При создании заявки автоматически устанавливаем пользователя"""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class OrderListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка заявок пользователя"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_price = serializers.DecimalField(
        source='service.price',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'service', 'service_name', 'service_price',
                  'status', 'created_at', 'completed_at', 'comment_count']
        read_only_fields = ['status', 'created_at', 'completed_at']

    def get_comment_count(self, obj):
        """Количество видимых комментариев"""
        return obj.comments.filter(is_visible_to_user=True).count()


class OrderDetailSerializer(OrderListSerializer):
    """Сериализатор для деталей заявки"""
    service_details = ServiceListSerializer(source='service', read_only=True)
    visible_comments = serializers.SerializerMethodField()

    class Meta(OrderListSerializer.Meta):
        fields = OrderListSerializer.Meta.fields + [
            'notes', 'service_details', 'visible_comments'
        ]

    def get_visible_comments(self, obj):
        """Только видимые пользователю комментарии"""
        comments = obj.comments.filter(is_visible_to_user=True)
        return CommentSerializer(comments, many=True, context=self.context).data


class OrderAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для админской работы с заявками"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    service_name = serializers.CharField(source='service.name', read_only=True)
    all_comments = CommentSerializer(source='comments', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_email', 'user_full_name',
                  'service', 'service_name', 'status', 'notes',
                  'created_at', 'completed_at', 'all_comments']
        read_only_fields = ['user', 'service', 'created_at']

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()


class OrderStatusUpdateSerializer(serializers.Serializer):
    """Сериализатор для изменения статуса заявки"""
    status = serializers.ChoiceField(choices=Order.Status.choices)
    comment = serializers.CharField(required=False, allow_blank=True)

    def validate_status(self, value):
        """Проверка валидности статуса"""
        order = self.context.get('order')
        if order and order.status == Order.Status.COMPLETED and value != Order.Status.COMPLETED:
            raise serializers.ValidationError(
                "Нельзя изменить статус завершенной заявки"
            )
        return value


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """Сериализатор для истории статусов"""
    changed_by_email = serializers.EmailField(source='changed_by.email', read_only=True)

    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'old_status', 'new_status', 'changed_by',
                  'changed_by_email', 'changed_at', 'comment']
        read_only_fields = ['changed_by', 'changed_at']

class ReviewPublishSerializer(serializers.Serializer):
    """Сериализатор для публикации отзыва"""
    is_published = serializers.BooleanField(required=True)

class ReviewVerifySerializer(serializers.Serializer):
    """Сериализатор для подтверждения отзыва"""
    is_verified = serializers.BooleanField(required=True)
```

---

### Создание представлений

**Файл: `manager_services/views.py`**

```python
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count, Q, Avg
from .models import *
from .serializers import *
import os
from django.conf import settings
from django.core.files.storage import default_storage


class ServiceListAPIView(APIView):
    """
    GET: Список всех активных услуг (публичный)
    """

    def get(self, request):
        services = Service.objects.filter(is_active=True).order_by('-created_at')

        # Фильтрация по категории, если указана
        category = request.query_params.get('category')
        if category:
            services = services.filter(category=category)

        # Поиск по названию, если указан
        search = request.query_params.get('search')
        if search:
            services = services.filter(name__icontains=search)

        serializer = ServiceListSerializer(services, many=True, context={'request': request})
        return Response(serializer.data)


class ServiceDetailAPIView(APIView):
    """
    GET: Детали услуги (публичный)
    """

    def get(self, request, pk):
        try:
            service = Service.objects.get(id=pk, is_active=True)
        except Service.DoesNotExist:
            return Response(
                {"error": "Услуга не найдена или неактивна"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ServiceDetailSerializer(service, context={'request': request})
        return Response(serializer.data)


class ServiceCategoriesAPIView(APIView):
    """
    GET: Список всех категорий услуг с количеством услуг в каждой
    """

    def get(self, request):
        # Получаем все категории из активных услуг
        categories = Service.objects.filter(is_active=True) \
            .values('category') \
            .annotate(service_count=Count('id')) \
            .order_by('category')

        # Преобразуем QuerySet в список словарей для сериализации
        categories_list = [
            {'name': cat['category'], 'service_count': cat['service_count']}
            for cat in categories
        ]

        serializer = CategorySerializer(categories_list, many=True)
        return Response(serializer.data)


class AdminServiceListAPIView(APIView):
    """
    GET: Список всех услуг (для админа, с неактивными)
    POST: Создание новой услуги (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ServiceAdminSerializer

    def get(self, request):
        services = Service.objects.all().order_by('-created_at')

        # Фильтрация по активности, если указана
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            services = services.filter(is_active=is_active.lower() == 'true')

        # Фильтрация по категории, если указана
        category = request.query_params.get('category')
        if category:
            services = services.filter(category=category)

        # Поиск по названию, если указан
        search = request.query_params.get('search')
        if search:
            services = services.filter(name__icontains=search)

        serializer = ServiceAdminSerializer(services, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceAdminSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminServiceDetailAPIView(APIView):
    """
    GET: Детали услуги (админ)
    PUT: Полное обновление услуги (админ)
    PATCH: Частичное обновление (админ)
    DELETE: Удаление услуги из БД (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ServiceAdminSerializer

    def get_object(self, pk):
        try:
            return Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return None

    def get(self, request, pk):
        service = self.get_object(pk)
        if not service:
            return Response(
                {"error": "Услуга не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ServiceAdminSerializer(service, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        service = self.get_object(pk)
        if not service:
            return Response(
                {"error": "Услуга не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ServiceAdminSerializer(service, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        service = self.get_object(pk)
        if not service:
            return Response(
                {"error": "Услуга не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ServiceAdminSerializer(service, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        service = self.get_object(pk)
        if not service:
            return Response(
                {"error": "Услуга не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, есть ли связанные заявки
        if service.orders.exists():
            return Response(
                {
                    "error": "Невозможно удалить услугу, так как существуют связанные заявки",
                    "order_count": service.orders.count()
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Удаляем файлы, связанные с услугой
        if service.files.exists():
            for file in service.files.all():

                file_path = os.path.join(settings.MEDIA_ROOT, file.file_path)


                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except OSError as e:
                        # Логируем ошибку
                        print(f"Ошибка при удалении файла {file_path}: {e}")

                # Удаляем запись из БД
                file.delete()

        # Удаляем саму услугу
        service.delete()

        return Response(
            {"message": "Услуга успешно удалена"},
            status=status.HTTP_200_OK
        )


class AdminServiceDeactivateAPIView(APIView):
    """
    POST: Деактивация услуги (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, pk):
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response(
                {"error": "Услуга не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Деактивируем услугу
        service.is_active = False
        service.save()

        serializer = ServiceAdminSerializer(service, context={'request': request})
        return Response({
            "message": "Услуга успешно деактивирована",
            "service": serializer.data
        })


class AdminFileUploadAPIView(APIView):
    """
    POST: Загрузка файла для услуги (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = FileUploadSerializer

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Получаем валидированные данные
        service = serializer.validated_data['service']
        uploaded_file = request.FILES['file']
        alt_text = serializer.validated_data.get('alt_text', '')
        is_primary = serializer.validated_data.get('is_primary', False)
        display_order = serializer.validated_data.get('display_order', 0)

        # Проверяем, что только один файл может быть главным
        if is_primary:
            existing_primary = File.objects.filter(service=service, is_primary=True).exists()
            if existing_primary:
                return Response(
                    {"error": "У услуги уже есть главное изображение"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Генерируем уникальное имя файла
        original_filename = uploaded_file.name
        file_extension = os.path.splitext(original_filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # Определяем путь для сохранения
        upload_path = f"services/{service.id}/{unique_filename}"

        # Сохраняем файл на диск
        file_path = default_storage.save(upload_path, uploaded_file)

        try:
            # Получаем информацию о файле
            file_size = uploaded_file.size
            mime_type = uploaded_file.content_type

            # Создаем запись в БД
            file_obj = File.objects.create(
                service=service,
                file_name=original_filename,
                file_path=file_path,
                file_size=file_size,
                mime_type=mime_type,
                is_primary=is_primary,
                display_order=display_order,
                uploaded_by=request.user,
                alt_text=alt_text
            )

            # Сериализуем и возвращаем результат
            serializer = FileSerializer(file_obj, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Если что-то пошло не так, удаляем загруженный файл
            if default_storage.exists(file_path):
                default_storage.delete(file_path)

            return Response(
                {"error": f"Ошибка при сохранении файла: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminFileDetailAPIView(APIView):
    """
    GET: Получить информацию о файле (админ)
    PUT: Обновить информацию о файле (админ)
    PATCH: Частичное обновление информации о файле (админ)
    DELETE: Удалить файл (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = FileSerializer

    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            return None

    def get(self, request, pk):
        file_obj = self.get_object(pk)
        if not file_obj:
            return Response(
                {"error": "Файл не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = FileSerializer(file_obj, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        file_obj = self.get_object(pk)
        if not file_obj:
            return Response(
                {"error": "Файл не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = FileSerializer(file_obj, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        file_obj = self.get_object(pk)
        if not file_obj:
            return Response(
                {"error": "Файл не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, что устанавливается is_primary
        if 'is_primary' in request.data and request.data['is_primary']:
            # Проверяем, есть ли уже главное изображение у этой услуги
            existing_primary = File.objects.filter(
                service=file_obj.service,
                is_primary=True
            ).exclude(id=file_obj.id).exists()

            if existing_primary:
                return Response(
                    {"error": "У услуги уже есть главное изображение"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = FileSerializer(file_obj, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        file_obj = self.get_object(pk)
        if not file_obj:
            return Response(
                {"error": "Файл не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Сохраняем путь к файлу перед удалением
        file_path = file_obj.file_path

        # Удаляем запись из БД
        file_obj.delete()

        # Удаляем физический файл с диска
        if default_storage.exists(file_path):
            try:
                default_storage.delete(file_path)
            except Exception as e:
                # Логируем ошибку, но не возвращаем ошибку пользователю
                print(f"Ошибка при удалении файла {file_path}: {e}")

        return Response(
            {"message": "Файл успешно удален"},
            status=status.HTTP_200_OK
        )


class ServiceFilesAPIView(APIView):
    """
    GET: Получить файлы для конкретной услуги (публичный)
    """

    def get(self, request, service_id):
        try:
            service = Service.objects.get(id=service_id, is_active=True)
        except Service.DoesNotExist:
            return Response(
                {"error": "Услуга не найдена или неактивна"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем файлы услуги, отсортированные по порядку отображения
        files = service.files.all().order_by('display_order', 'uploaded_at')

        file_type = request.query_params.get('type')
        if file_type == 'images':
            files = files.filter(mime_type__startswith='image/')
        elif file_type == 'documents':
            files = files.exclude(mime_type__startswith='image/')

        serializer = FileSerializer(files, many=True, context={'request': request})
        return Response(serializer.data)


class OrderListCreateAPIView(APIView):
    """
    GET: Список заявок текущего пользователя
    POST: Создание новой заявки
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def get(self, request):
        # Получаем заявки текущего пользователя
        orders = Order.objects.filter(user=request.user).order_by('-created_at')

        # Фильтрация по статусу, если указана
        status_filter = request.query_params.get('status')
        if status_filter:
            orders = orders.filter(status=status_filter)

        # Фильтрация по услуге, если указана
        service_id = request.query_params.get('service_id')
        if service_id:
            orders = orders.filter(service_id=service_id)

        serializer = OrderListSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Создаем заявку
        order = serializer.save()

        # Создаем запись в истории статусов
        OrderStatusHistory.objects.create(
            order=order,
            old_status='',  # Первый статус, поэтому старого нет
            new_status=order.status,
            changed_by=request.user,
            comment='Создание заявки'
        )

        # Возвращаем детали созданной заявки
        detail_serializer = OrderDetailSerializer(order, context={'request': request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailAPIView(APIView):
    """
    GET: Детали заявки пользователя
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Order.objects.get(pk=pk, user=user)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk, request.user)
        if not order:
            return Response(
                {"error": "Заявка не найдена или у вас нет к ней доступа"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderDetailSerializer(order, context={'request': request})
        return Response(serializer.data)


class OrderCancelAPIView(APIView):
    """
    POST: Отмена заявки (пользователем)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена или у вас нет к ней доступа"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, можно ли отменить заявку
        if order.status == Order.Status.COMPLETED:
            return Response(
                {"error": "Нельзя отменить завершенную заявку"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if order.status == Order.Status.CANCELLED:
            return Response(
                {"error": "Заявка уже отменена"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Сохраняем старый статус
        old_status = order.status

        # Меняем статус на отменен
        order.status = Order.Status.CANCELLED
        order.save()

        # Создаем запись в истории статусов
        OrderStatusHistory.objects.create(
            order=order,
            old_status=old_status,
            new_status=order.status,
            changed_by=request.user,
            comment='Отмена пользователем'
        )

        serializer = OrderDetailSerializer(order, context={'request': request})
        return Response({
            "message": "Заявка успешно отменена",
            "order": serializer.data
        })


class AdminOrderListAPIView(APIView):
    """
    GET: Список всех заявок (админ, с фильтрами)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')

        # Фильтрация по статусу
        status_filter = request.query_params.get('status')
        if status_filter:
            orders = orders.filter(status=status_filter)

        # Фильтрация по пользователю
        user_id = request.query_params.get('user_id')
        if user_id:
            orders = orders.filter(user_id=user_id)

        # Фильтрация по услуге
        service_id = request.query_params.get('service_id')
        if service_id:
            orders = orders.filter(service_id=service_id)

        # Фильтрация по дате создания (от)
        date_from = request.query_params.get('date_from')
        if date_from:
            orders = orders.filter(created_at__date__gte=date_from)

        # Фильтрация по дате создания (до)
        date_to = request.query_params.get('date_to')
        if date_to:
            orders = orders.filter(created_at__date__lte=date_to)

        # Поиск по email пользователя
        search = request.query_params.get('search')
        if search:
            orders = orders.filter(
                Q(user__email__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(notes__icontains=search)
            )

        serializer = OrderAdminSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)


class AdminOrderDetailAPIView(APIView):
    """
    GET: Детали заявки (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderAdminSerializer(order, context={'request': request})
        return Response(serializer.data)


class AdminOrderStatusUpdateAPIView(APIView):
    """
    PATCH: Изменение статуса заявки (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = OrderStatusUpdateSerializer

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Сохраняем старый статус
        old_status = order.status
        new_status = serializer.validated_data['status']
        comment = serializer.validated_data.get('comment', '')

        # Проверяем, что статус изменился
        if old_status == new_status:
            return Response(
                {"error": "Новый статус совпадает со старым"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, что нельзя изменить статус завершенной заявки
        if old_status == Order.Status.COMPLETED:
            return Response(
                {"error": "Нельзя изменить статус завершенной заявки"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Меняем статус
        order.status = new_status
        order.save()

        # Создаем запись в истории статусов
        OrderStatusHistory.objects.create(
            order=order,
            old_status=old_status,
            new_status=new_status,
            changed_by=request.user,
            comment=comment or f'Изменение статуса администратором'
        )

        # Возвращаем обновленную заявку
        order_serializer = OrderAdminSerializer(order, context={'request': request})
        return Response({
            "message": "Статус заявки успешно обновлен",
            "order": order_serializer.data
        })


class AdminOrderHistoryAPIView(APIView):
    """
    GET: История статусов заявки (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем историю статусов для этой заявки
        history = order.status_history.all().order_by('-changed_at')

        serializer = OrderStatusHistorySerializer(history, many=True)
        return Response(serializer.data)


class OrderCommentsAPIView(APIView):
    """
    GET: Получить комментарии к заявке (видимые пользователю)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            # Проверяем, что заявка принадлежит пользователю или пользователь - админ
            if request.user.is_admin:
                order = Order.objects.get(pk=order_id)
            else:
                order = Order.objects.get(pk=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена или у вас нет к ней доступа"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем только видимые комментарии
        comments = order.comments.filter(is_visible_to_user=True).order_by('created_at')

        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)


class AdminCommentListAPIView(APIView):
    """
    GET: Список всех комментариев (админ, с фильтрами)
    POST: Добавить комментарий к заявке (админ)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get(self, request):
        comments = Comment.objects.all().order_by('-created_at')

        # Фильтрация по заявке
        order_id = request.query_params.get('order_id')
        if order_id:
            comments = comments.filter(order_id=order_id)

        # Фильтрация по администратору
        admin_id = request.query_params.get('admin_id')
        if admin_id:
            comments = comments.filter(admin_id=admin_id)

        # Фильтрация по видимости
        is_visible = request.query_params.get('is_visible')
        if is_visible is not None:
            comments = comments.filter(is_visible_to_user=is_visible.lower() == 'true')

        # Поиск по содержимому
        search = request.query_params.get('search')
        if search:
            comments = comments.filter(content__icontains=search)

        # Фильтрация по дате создания (от)
        date_from = request.query_params.get('date_from')
        if date_from:
            comments = comments.filter(created_at__date__gte=date_from)

        # Фильтрация по дате создания (до)
        date_to = request.query_params.get('date_to')
        if date_to:
            comments = comments.filter(created_at__date__lte=date_to)

        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        # Проверяем, что заявка существует
        order_id = request.data.get('order')
        if not order_id:
            return Response(
                {"error": "Не указана заявка"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Заявка не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Создаем комментарий
        serializer = CommentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminCommentDetailAPIView(APIView):
    """
    GET: Получить комментарий (админ)
    PUT: Обновить комментарий (админ)
    PATCH: Частичное обновление комментария (админ)
    DELETE: Удалить комментарий (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CommentSerializer

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return None

    def get(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response(
                {"error": "Комментарий не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response(
                {"error": "Комментарий не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, что можно редактировать только свои комментарии
        if comment.admin != request.user:
            return Response(
                {"error": "Вы можете редактировать только свои комментарии"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentSerializer(comment, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response(
                {"error": "Комментарий не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Для изменения видимости - доступно всем админам
        # Для изменения контента - только автору
        if 'content' in request.data and comment.admin != request.user:
            return Response(
                {"error": "Вы можете редактировать только свои комментарии"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response(
                {"error": "Комментарий не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, что можно удалять только свои комментарии
        if comment.admin != request.user:
            return Response(
                {"error": "Вы можете удалять только свои комментарии"},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()
        return Response(
            {"message": "Комментарий успешно удален"},
            status=status.HTTP_200_OK
        )


class AdminCommentVisibilityAPIView(APIView):
    """
    PATCH: Изменить видимость комментария (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(
                {"error": "Комментарий не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommentVisibilitySerializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Видимость комментария успешно изменена",
            "comment": CommentSerializer(comment, context={'request': request}).data
        })


class ServiceReviewsAPIView(APIView):
    """
    GET: Список опубликованных отзывов на услугу
    """

    def get(self, request, service_id):
        try:
            service = Service.objects.get(id=service_id, is_active=True)
        except Service.DoesNotExist:
            return Response(
                {"error": "Услуга не найдена или неактивна"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем только опубликованные отзывы
        reviews = service.reviews.filter(is_published=True).order_by('-created_at')

        # Фильтрация по рейтингу, если указан
        rating = request.query_params.get('rating')
        if rating:
            reviews = reviews.filter(rating=rating)

        # Фильтрация по подтвержденным отзывам
        verified_only = request.query_params.get('verified_only')
        if verified_only and verified_only.lower() == 'true':
            reviews = reviews.filter(is_verified=True)

        # Пагинация (базовая)
        limit = request.query_params.get('limit')
        if limit and limit.isdigit():
            reviews = reviews[:int(limit)]

        # Статистика по отзывам
        total_reviews = reviews.count()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        rating_distribution = reviews.values('rating').annotate(count=Count('id')).order_by('-rating')

        serializer = ReviewListSerializer(reviews, many=True, context={'request': request})

        return Response({
            "service_id": service_id,
            "service_name": service.name,
            "statistics": {
                "total_reviews": total_reviews,
                "average_rating": round(average_rating, 1),
                "rating_distribution": list(rating_distribution)
            },
            "reviews": serializer.data
        })


class UserReviewCreateAPIView(APIView):
    """
    POST: Создать отзыв (только для завершенных заказов пользователя)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewCreateSerializer

    def post(self, request):
        serializer = ReviewCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        review = serializer.save()

        # Возвращаем детали созданного отзыва
        detail_serializer = ReviewDetailSerializer(review, context={'request': request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class ReviewDetailAPIView(APIView):
    """
    GET: Детали отзыва (публичный)
    """

    def get(self, request, pk):
        try:
            review = Review.objects.get(pk=pk, is_published=True)
        except Review.DoesNotExist:
            return Response(
                {"error": "Отзыв не найден или не опубликован"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReviewDetailSerializer(review, context={'request': request})
        return Response(serializer.data)


class AdminReviewListAPIView(APIView):
    """
    GET: Все отзывы (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        reviews = Review.objects.all().order_by('-created_at')

        # Фильтрация по услуге
        service_id = request.query_params.get('service_id')
        if service_id:
            reviews = reviews.filter(service_id=service_id)

        # Фильтрация по пользователю
        user_id = request.query_params.get('user_id')
        if user_id:
            reviews = reviews.filter(user_id=user_id)

        # Фильтрация по статусу публикации
        is_published = request.query_params.get('is_published')
        if is_published is not None:
            reviews = reviews.filter(is_published=is_published.lower() == 'true')

        # Фильтрация по подтверждению
        is_verified = request.query_params.get('is_verified')
        if is_verified is not None:
            reviews = reviews.filter(is_verified=is_verified.lower() == 'true')

        # Фильтрация по рейтингу
        rating = request.query_params.get('rating')
        if rating:
            reviews = reviews.filter(rating=rating)


        # Фильтрация по дате создания (от)
        date_from = request.query_params.get('date_from')
        if date_from:
            reviews = reviews.filter(created_at__date__gte=date_from)

        # Фильтрация по дате создания (до)
        date_to = request.query_params.get('date_to')
        if date_to:
            reviews = reviews.filter(created_at__date__lte=date_to)

        serializer = ReviewAdminSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)


class AdminPendingReviewsAPIView(APIView):
    """
    GET: Список отзывов на модерации (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Отзывы, ожидающие модерации (не опубликованные)
        pending_reviews = Review.objects.filter(is_published=False).order_by('created_at')

        # Фильтрация по услуге, если указана
        service_id = request.query_params.get('service_id')
        if service_id:
            pending_reviews = pending_reviews.filter(service_id=service_id)

        # Фильтрация по дате создания (от)
        date_from = request.query_params.get('date_from')
        if date_from:
            pending_reviews = pending_reviews.filter(created_at__date__gte=date_from)

        serializer = ReviewAdminSerializer(pending_reviews, many=True, context={'request': request})

        # Статистика
        total_pending = pending_reviews.count()

        return Response({
            "statistics": {
                "total_pending": total_pending,
                "pending_by_service": pending_reviews.values('service__name').annotate(count=Count('id'))
            },
            "reviews": serializer.data
        })


class AdminReviewDetailAPIView(APIView):
    """
    GET: Детали отзыва (админ)
    PUT: Полное обновление отзыва (админ)
    PATCH: Частичное обновление отзыва (админ)
    DELETE: Удалить отзыв (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ReviewAdminSerializer

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return None

    def get(self, request, pk):
        review = self.get_object(pk)
        if not review:
            return Response(
                {"error": "Отзыв не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReviewAdminSerializer(review, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        review = self.get_object(pk)
        if not review:
            return Response(
                {"error": "Отзыв не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReviewAdminSerializer(review, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        review = self.get_object(pk)
        if not review:
            return Response(
                {"error": "Отзыв не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReviewAdminSerializer(review, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        review = self.get_object(pk)
        if not review:
            return Response(
                {"error": "Отзыв не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        review.delete()
        return Response(
            {"message": "Отзыв успешно удален"},
            status=status.HTTP_200_OK
        )


class AdminReviewPublishAPIView(APIView):
    """
    PATCH: Опубликовать/скрыть отзыв (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ReviewPublishSerializer

    def patch(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response(
                {"error": "Отзыв не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, что указан статус публикации
        is_published = request.data.get('is_published')
        if is_published is None:
            return Response(
                {"error": "Не указан статус публикации (is_published)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Меняем статус публикации
        review.is_published = is_published
        review.save()

        action = "опубликован" if is_published else "скрыт"
        serializer = ReviewAdminSerializer(review, context={'request': request})

        return Response({
            "message": f"Отзыв успешно {action}",
            "review": serializer.data
        })


class AdminUserListAPIView(APIView):
    """
    GET: Список всех пользователей (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = User.objects.all().order_by('-date_joined')

        # Фильтрация по роли
        role = request.query_params.get('role')
        if role:
            users = users.filter(role=role)

        # Фильтрация по активности
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            users = users.filter(is_active=is_active.lower() == 'true')

        # Поиск по email, имени, фамилии
        search = request.query_params.get('search')
        if search:
            users = users.filter(
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone__icontains=search)
            )

        # Фильтрация по дате регистрации (от)
        date_from = request.query_params.get('date_from')
        if date_from:
            users = users.filter(date_joined__date__gte=date_from)

        # Фильтрация по дате регистрации (до)
        date_to = request.query_params.get('date_to')
        if date_to:
            users = users.filter(date_joined__date__lte=date_to)

        # Аннотация с количеством заявок и отзывов
        users = users.annotate(
            order_count=Count('orders', distinct=True),
            review_count=Count('reviews', distinct=True)
        )

        serializer = UserAdminListSerializer(users, many=True)
        return Response(serializer.data)


class AdminUserDetailAPIView(APIView):
    """
    GET: Детали пользователя (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем статистику пользователя
        user_data = UserAdminDetailSerializer(user).data

        # Дополнительная статистика
        orders = user.orders.all()
        reviews = user.reviews.all()

        # Статистика по заявкам
        order_stats = {
            "total": orders.count(),
            "by_status": orders.values('status').annotate(count=Count('id')),
            "recent_orders": orders.order_by('-created_at')[:5].values('id', 'service__name', 'status', 'created_at')
        }

        # Статистика по отзывам
        review_stats = {
            "total": reviews.count(),
            "published": reviews.filter(is_published=True).count(),
            "average_rating": reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] if reviews.exists() else None,
            "recent_reviews": reviews.order_by('-created_at')[:5].values('id', 'service__name', 'rating', 'created_at')
        }

        return Response({
            "user": user_data,
            "statistics": {
                "orders": order_stats,
                "reviews": review_stats
            }
        })


class AdminUserRoleUpdateAPIView(APIView):
    """
    PATCH: Изменить роль пользователя (админ)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, что пользователь не меняет свою собственную роль
        if user == request.user:
            return Response(
                {"error": "Вы не можете изменить свою собственную роль"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, что указана новая роль
        serializer = UserRoleUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Сохраняем новую роль
        old_role = user.role
        serializer.save()

        return Response({
            "message": f"Роль пользователя успешно изменена с '{old_role}' на '{user.role}'",
            "user": UserAdminDetailSerializer(user).data
        })
```

---

### Настройка маршрутов

**Файл: `manager_services/urls.py`**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('api/services/', views.ServiceListAPIView.as_view(), name='service-list'),
    path('api/services/<int:pk>/', views.ServiceDetailAPIView.as_view(), name='service-detail'),
    path('api/services/categories/', views.ServiceCategoriesAPIView.as_view(), name='service-categories'),

    path('api/admin/services/', views.AdminServiceListAPIView.as_view(), name='admin-service-list'),
    path('api/admin/services/<int:pk>/', views.AdminServiceDetailAPIView.as_view(), name='admin-service-detail'),
    path('api/admin/services/<int:pk>/deactivate/', views.AdminServiceDeactivateAPIView.as_view(),
         name='admin-service-deactivate'),

    path('api/admin/files/upload/', views.AdminFileUploadAPIView.as_view(), name='admin-file-upload'),
    path('api/admin/files/<int:pk>/', views.AdminFileDetailAPIView.as_view(), name='admin-file-detail'),
    path('api/services/<int:service_id>/files/', views.ServiceFilesAPIView.as_view(), name='service-files'),

    path('api/orders/', views.OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('api/orders/<int:pk>/', views.OrderDetailAPIView.as_view(), name='order-detail'),
    path('api/orders/<int:pk>/cancel/', views.OrderCancelAPIView.as_view(), name='order-cancel'),

    path('api/admin/orders/', views.AdminOrderListAPIView.as_view(), name='admin-order-list'),
    path('api/admin/orders/<int:pk>/', views.AdminOrderDetailAPIView.as_view(), name='admin-order-detail'),
    path('api/admin/orders/<int:pk>/status/', views.AdminOrderStatusUpdateAPIView.as_view(), name='admin-order-status'),
    path('api/admin/orders/<int:pk>/history/', views.AdminOrderHistoryAPIView.as_view(), name='admin-order-history'),

    path('api/orders/<int:order_id>/comments/', views.OrderCommentsAPIView.as_view(), name='order-comments'),

    path('api/admin/comments/', views.AdminCommentListAPIView.as_view(), name='admin-comment-list'),
    path('api/admin/comments/<int:pk>/', views.AdminCommentDetailAPIView.as_view(), name='admin-comment-detail'),
    path('api/admin/comments/<int:pk>/visibility/', views.AdminCommentVisibilityAPIView.as_view(),
         name='admin-comment-visibility'),

    path('api/services/<int:service_id>/reviews/', views.ServiceReviewsAPIView.as_view(), name='service-reviews'),
    path('api/reviews/', views.UserReviewCreateAPIView.as_view(), name='review-create'),
    path('api/reviews/<int:pk>/', views.ReviewDetailAPIView.as_view(), name='review-detail'),

    path('api/admin/reviews/', views.AdminReviewListAPIView.as_view(), name='admin-review-list'),
    path('api/admin/reviews/pending/', views.AdminPendingReviewsAPIView.as_view(), name='admin-pending-reviews'),
    path('api/admin/reviews/<int:pk>/', views.AdminReviewDetailAPIView.as_view(), name='admin-review-detail'),
    path('api/admin/reviews/<int:pk>/publish/', views.AdminReviewPublishAPIView.as_view(), name='admin-review-publish'),

    path('api/admin/users/', views.AdminUserListAPIView.as_view(), name='admin-user-list'),
    path('api/admin/users/<int:pk>/', views.AdminUserDetailAPIView.as_view(), name='admin-user-detail'),
    path('api/admin/users/<int:pk>/role/', views.AdminUserRoleUpdateAPIView.as_view(), name='admin-user-role'),
]
```

**Файл: `brand_manager/urls.py`**

```python
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include('manager_services.urls')),
    # maybe not 
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
]
```

---

## Аутентификация (Djoser)

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
| POST | `/auth/users/set_username/` | Изменение имени пользователя |
| POST | `/auth/users/activate/` | Активация учётной записи пользователя через электронную почту |

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
lab34/
├── brand_manager/          # Основной пакет проекта
│   ├── __init__.py
│   ├── settings.py                  # Настройки проекта
│   ├── urls.py                      # Главные маршруты
│   ├── wsgi.py
│   └── asgi.py
├── services_manager/                            # Приложение
│   ├── __init__.py
│   ├── models.py                    # Модели данных
│   ├── serializers.py               # Сериализаторы
│   ├── views.py                     # Представления
│   ├── urls.py                      # Маршруты приложения
│   ├── admin.py                     # Админ-панель
│   └── apps.py
├── media/                           # Медиа файлы (изображения)
│   └── service_files/
├── manage.py
├── requirements.txt                 # Зависимости
└── db.sqlite3                       # База данных
```

---

## Чек-лист для развёртывания

### Быстрый старт

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

### Проверка работоспособности

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

- Модели базы данных через Django ORM
- API через Django REST Framework
- Аутентификация через Djoser (JWT)
- Разделение прав доступа (пользователь/админ)
- Полноценная документация в формате Markdown
