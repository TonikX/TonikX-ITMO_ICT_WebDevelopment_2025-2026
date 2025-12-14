# Лабораторная работа 2. Реализация простого сайта средствами Django

## Вариант 6: Табло победителей автогонок

Реализован веб-сервис для управления автогонками с использованием Django 3.2 и SQLite (с возможностью использования PostgreSQL).

## Модели данных

### Race (Автогонка)
Модель для хранения информации об автогонках.

```python
class Race(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название гонки')
    date = models.DateField(verbose_name='Дата проведения')
    location = models.CharField(max_length=200, verbose_name='Место проведения')
    description = models.TextField(verbose_name='Описание гонки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
```

**Поля:**
- `name` - название гонки
- `date` - дата проведения
- `location` - место проведения
- `description` - описание гонки
- `created_at` - дата создания записи

### Racer (Гонщик)
Модель для хранения информации о гонщиках.

```python
class Racer(models.Model):
    EXPERIENCE_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
        ('professional', 'Профессионал'),
    ]
    
    CLASS_CHOICES = [
        ('formula1', 'Формула-1'),
        ('formula2', 'Формула-2'),
        ('formula3', 'Формула-3'),
        ('rally', 'Ралли'),
        ('endurance', 'Выносливость'),
        ('other', 'Другое'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    team_name = models.CharField(max_length=200, verbose_name='Название команды')
    car_description = models.TextField(verbose_name='Описание автомобиля')
    racer_description = models.TextField(verbose_name='Описание участника')
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    racer_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
```

**Поля:**
- `user` - связь с пользователем (OneToOne)
- `full_name` - ФИО гонщика
- `team_name` - название команды
- `car_description` - описание автомобиля
- `racer_description` - описание участника
- `experience` - уровень опыта (выбор из списка)
- `racer_class` - класс участника (выбор из списка)

### Registration (Регистрация)
Модель для регистрации гонщиков на гонки.

```python
class Registration(models.Model):
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    race_time = models.TimeField(null=True, blank=True, verbose_name='Время заезда')
    result = models.CharField(max_length=100, blank=True, verbose_name='Результат')
    position = models.IntegerField(null=True, blank=True, verbose_name='Позиция')
    
    class Meta:
        unique_together = ['racer', 'race']
```

**Поля:**
- `racer` - гонщик (ForeignKey)
- `race` - гонка (ForeignKey)
- `registration_date` - дата регистрации
- `race_time` - время заезда (заполняется админом)
- `result` - результат (заполняется админом)
- `position` - позиция (заполняется админом)

**Особенности:**
- Уникальная связка гонщик-гонка (один гонщик не может зарегистрироваться дважды на одну гонку)
- Поля `race_time`, `result`, `position` заполняются только администратором через Django-admin

### Comment (Комментарий)
Модель для комментариев к гонкам.

```python
class Comment(models.Model):
    COMMENT_TYPE_CHOICES = [
        ('cooperation', 'Вопрос о сотрудничестве'),
        ('race_question', 'Вопрос о гонках'),
        ('other', 'Иное'),
    ]
    
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    race_date = models.DateField(verbose_name='Дата заезда')
    text = models.TextField(verbose_name='Текст комментария')
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPE_CHOICES)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг (1-10)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
```

**Поля:**
- `race` - гонка (ForeignKey)
- `author` - автор комментария (ForeignKey к User)
- `race_date` - дата заезда, о котором идет речь
- `text` - текст комментария
- `comment_type` - тип комментария (выбор из списка)
- `rating` - рейтинг от 1 до 10
- `created_at` - дата создания

## Функционал

### 1. Регистрация новых пользователей
- Реализована страница регистрации (`/register/`)
- После регистрации пользователь автоматически авторизуется
- Используется стандартная форма Django `UserCreationForm` с расширением для email

### 2. Просмотр автогонок и регистрация гонщиков
- **Главная страница** (`/`) - список всех гонок с пагинацией и поиском
- **Детальная страница гонки** (`/race/<id>/`) - подробная информация о гонке
- **Регистрация на гонку** (`/race/<id>/register/`) - регистрация гонщика на гонку
- Пользователь может редактировать и удалять свои регистрации:
  - `/registration/<id>/edit/` - редактирование регистрации
  - `/registration/<id>/delete/` - удаление регистрации

### 3. Написание отзывов и комментариев
- **Добавление комментария** (`/race/<id>/comment/`) - форма для добавления комментария
- При добавлении комментария сохраняются:
  - Дата заезда
  - Текст комментария
  - Тип комментария (вопрос о сотрудничестве, вопрос о гонках, иное)
  - Рейтинг (1-10)
  - Информация о комментаторе (автор)

### 4. Административные функции
- **Django-admin** - администратор может:
  - Указывать время заезда (`race_time`)
  - Указывать результат (`result`)
  - Указывать позицию (`position`)
- **Таблица результатов** (`/race/<id>/results/`) - доступна только администраторам, отображает всех участников гонки с результатами

### 5. Профиль гонщика
- **Создание профиля** (`/create-racer-profile/`) - после регистрации пользователь создает профиль гонщика
- **Просмотр профиля** (`/racer-profile/`) - просмотр информации о гонщике и всех его регистрациях

## Интерфейс

### Дизайн
- Использован **Bootstrap 5.3** для современного и адаптивного дизайна
- Градиентное меню навигации
- Карточки с эффектом hover
- Иконки Bootstrap Icons
- Адаптивная верстка для мобильных устройств

### Навигация
- Главная страница
- Мой профиль (для авторизованных пользователей)
- Панель администратора (для администраторов)
- Вход/Выход
- Регистрация

### Пагинация
- Реализована на главной странице (список гонок) - 6 гонок на страницу
- Реализована для комментариев на странице гонки - 5 комментариев на страницу
- Используется стандартный Django Paginator

### Поиск и фильтрация
- Поиск по названию гонки
- Поиск по месту проведения
- Поиск по описанию
- Поиск работает в сочетании с пагинацией

## Структура проекта

```
lab2/
├── racing_project/          # Основной проект Django
│   ├── settings.py          # Настройки проекта
│   ├── urls.py              # Главный файл URL-маршрутов
│   └── ...
├── racing/                   # Приложение racing
│   ├── models.py            # Модели данных
│   ├── views.py             # Представления (views)
│   ├── forms.py             # Формы
│   ├── admin.py             # Настройка админки
│   ├── urls.py              # URL-маршруты приложения
│   └── migrations/          # Миграции БД
├── templates/               # Шаблоны
│   └── racing/
│       ├── base.html        # Базовый шаблон
│       ├── index.html      # Главная страница
│       ├── race_detail.html # Детальная страница гонки
│       └── ...
├── static/                  # Статические файлы
├── manage.py               # Управляющий скрипт Django
├── requirements.txt        # Зависимости проекта
└── .gitignore             # Игнорируемые файлы
```

## Важные файлы

### settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'racing',  # Наше приложение
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

### urls.py (racing_project)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('racing.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='racing/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
```

### urls.py (racing)
```python
urlpatterns = [
    path('', views.index, name='index'),
    path('race/<int:race_id>/', views.race_detail, name='race_detail'),
    path('register/', views.register_user, name='register'),
    path('create-racer-profile/', views.create_racer_profile, name='create_racer_profile'),
    path('racer-profile/', views.racer_profile, name='racer_profile'),
    path('race/<int:race_id>/register/', views.register_for_race, name='register_for_race'),
    path('registration/<int:registration_id>/edit/', views.edit_registration, name='edit_registration'),
    path('registration/<int:registration_id>/delete/', views.delete_registration, name='delete_registration'),
    path('race/<int:race_id>/comment/', views.add_comment, name='add_comment'),
    path('race/<int:race_id>/results/', views.race_results, name='race_results'),
]
```

## Django Admin

Настроена административная панель для всех моделей:

- **RaceAdmin** - управление гонками с фильтрацией по дате и месту
- **RacerAdmin** - управление гонщиками с фильтрацией по опыту и классу
- **RegistrationAdmin** - управление регистрациями с возможностью указания времени заезда, результата и позиции
- **CommentAdmin** - управление комментариями с фильтрацией по типу и рейтингу

## Разделение прав

### Обычные пользователи
- Просмотр гонок
- Регистрация на гонки
- Редактирование и удаление своих регистраций
- Добавление комментариев
- Просмотр своего профиля

### Администраторы
- Все права обычных пользователей
- Доступ к Django-admin
- Просмотр таблицы результатов гонок
- Управление временем заезда, результатами и позициями через админку

## Установка и запуск

1. Установить зависимости:
```bash
pip install -r requirements.txt
```

2. Выполнить миграции:
```bash
python manage.py migrate
```

3. Создать суперпользователя:
```bash
python manage.py createsuperuser
```

4. Запустить сервер разработки:
```bash
python manage.py runserver
```

5. Открыть в браузере:
- Главная страница: http://127.0.0.1:8000/
- Админка: http://127.0.0.1:8000/admin/


