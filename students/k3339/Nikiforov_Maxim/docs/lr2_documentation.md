# Лабораторная работа 2 — Django Web Framework

Практическое занятие №2.1  
**Тема**: Django Web framework. Установка. Реализация первого приложения.

---

## Задание 1: Установка Django Web Framework

**Цель**: Установить Django и создать проект согласно именованию.

**Что мы сделали**:

Далее мы установили Django в виртуальном окружении:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install django==6.0
```

Создали проект Django с именованием `django_project_nikiforov`:

```powershell
django-admin startproject django_project_nikiforov
cd django_project_nikiforov
```

Создали приложение `project_first_app`:

```powershell
python manage.py startapp project_first_app
```

Зарегистрировали приложение в `settings.py`, добавив `'project_first_app'` в `INSTALLED_APPS`.

---

## Задание 2: Модель данных (Практическое задание 2.1 и 2.2)

**Цель**: Создать модель данных об автовладельцах и автомобилях согласно схеме БД.

**Что мы сделали**:

Далее в файл `project_first_app/models.py` мы добавили четыре модели:

### 1. **Модель User** (расширенный пользователь)

```python
class User(AbstractUser):
    """Кастомная модель пользователя — владелец автомобиля."""
    passport_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер паспорта')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Домашний адрес')
    nationality = models.CharField(max_length=50, blank=True, null=True, verbose_name='Национальность')
    birth_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата рождения')
    cars = models.ManyToManyField('Car', through='Ownership', related_name='owners')
```

Использовали стратегию расширения **AbstractUser** (лучшая практика) — это позволило сохранить встроенную систему аутентификации Django и добавить только необходимые поля.

### 2. **Модель Car** (автомобиль)

```python
class Car(models.Model):
    """Модель автомобиля"""
    id_car = models.AutoField(primary_key=True, verbose_name='ID автомобиля')
    plate_number = models.CharField(max_length=15, verbose_name='Гос. номер')
    brand = models.CharField(max_length=20, verbose_name='Марка')
    model = models.CharField(max_length=20, verbose_name='Модель')
    color = models.CharField(max_length=30, null=True, blank=True, verbose_name='Цвет')

    class Meta:
        db_table = 'car'
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
```

### 3. **Модель DriverLicense** (водительское удостоверение)

```python
class DriverLicense(models.Model):
    """Модель водительского удостоверения. Связь M:1 с User"""
    id_license = models.AutoField(primary_key=True, verbose_name='ID удостоверения')
    id_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='id_owner',
        verbose_name='Владелец',
        null=False
    )
    license_number = models.CharField(max_length=10, verbose_name='Номер удостоверения')
    license_type = models.CharField(max_length=10, verbose_name='Тип удостоверения')
    issue_date = models.DateTimeField(verbose_name='Дата выдачи')

    class Meta:
        db_table = 'driver_license'
        verbose_name = 'Водительское удостоверение'
        verbose_name_plural = 'Водительские удостоверения'
```

### 4. **Модель Ownership** (владение автомобилем)

```python
class Ownership(models.Model):
    """Ассоциативная сущность (связь M:M между User и Car с атрибутами периода владения)"""
    id_ownership = models.AutoField(primary_key=True, verbose_name='ID владения')
    id_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        db_column='id_owner',
        verbose_name='Владелец',
        null=True,
        blank=True
    )
    id_car = models.ForeignKey(
        Car,
        on_delete=models.SET_NULL,
        db_column='id_car',
        verbose_name='Автомобиль',
        null=True,
        blank=True
    )
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата начала владения')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата окончания владения')

    class Meta:
        db_table = 'ownership'
        verbose_name = 'Владение'
        verbose_name_plural = 'Владения'
```

**Конфигурация AUTH_USER_MODEL в settings.py**:

Далее мы указали в `settings.py`:

```python
AUTH_USER_MODEL = 'project_first_app.User'
```

Это сообщает Django использовать кастомную модель вместо встроенной `auth.User`.

**Создание и применение миграций**:

Далее мы создали и применили миграции:

```powershell
python manage.py makemigrations
python manage.py migrate
```

Миграции создают необходимые таблицы в базе данных SQLite (`db.sqlite3`).

---

## Задание 3: Django Admin (Практическое задание 3)
  - `address`: `CharField`.
  - `nationality`: `CharField`.
  - `birth_date`: `DateTimeField`.
  - `cars`: `ManyToManyField('Car', through='Ownership')` — связь многие-ко-многим через промежуточную модель `Ownership`.
- **`Car`**:
  - `id_car`: `AutoField` (PK)
  - `plate_number`, `brand`, `model`, `color` — сведения об автомобиле.
- **`DriverLicense`**:
  - `id_license` (PK), `id_owner` (FK -> `User`), `license_number`, `license_type`, `issue_date`.
- **`Ownership`**:
  - ассоциативная таблица между `User` и `Car`: `id_owner` (FK -> `User`), `id_car` (FK -> `Car`), `start_date`, `end_date`.

**Админка (см. `project_first_app/admin.py`)**
- **Регистрация моделей**: `User`, `Car`, `DriverLicense`, `Ownership` зарегистрированы в админке.
- **UserAdmin** расширяет базовый `UserAdmin`, добавляет поля (`passport_number`, `address`, `nationality`, `birth_date`) в форму создания/редактирования и отображает дополнительные столбцы.

**Представления и маршруты**
- Все маршруты приложения определены в `project_first_app/urls.py` и подключены в `django_project_nikiforov/urls.py` на корневом уровне (`path('', include('project_first_app.urls'))`).
- **Владельцы (функциональные представления)**:
  - `owner_list` — вывод списка владельцев с поддержкой поиска (`q` GET-параметр) и пагинации (5 элементов на страницу). Реализована безопасная обработка несуществующих страниц (`PageNotAnInteger`, `EmptyPage`).
  - `owner_detail` — детальная страница владельца по `owner_id` с обработкой `User.DoesNotExist` (возврат `Http404`).
  - `create_owner` — форма создания владельца (используется `OwnerCreationForm`). При успешном сохранении выполняется `messages.success`, при ошибках — логирование и `messages.error`.
- **Автомобили (CBV)**:
  - `CarListView` — список автомобилей.
  - `CarDetailView` — детальная информация об автомобиле (pk аргумент `car_id`).
  - `CarCreateView` / `CarUpdateView` / `CarDeleteView` — стандартные CRUD-представления на основе классов с `success_url = reverse_lazy('car_list')`.

**URLs (основные)**
- `owner/list/` → `owner_list` (name=`owner_list`)
- `owner/create/` → `create_owner` (name=`owner_create`)
- `owner/<int:owner_id>/` → `owner_detail` (name=`owner_detail`)
- `car/list/` → `CarListView` (name=`car_list`)
- `car/create/` → `CarCreateView` (name=`car_create`)
- `car/<int:car_id>/` → `CarDetailView` (name=`car_detail`)
- `car/<int:car_id>/update/` → `CarUpdateView` (name=`car_update`)
- `car/<int:car_id>/delete/` → `CarDeleteView` (name=`car_delete`)

**Шаблоны**
- Расположение: `templates/` + `templates/project_first_app/`.
- Основные файлы:
  - `templates/base.html` — базовый шаблон (общая верстка, подключение сообщений и навигации).
  - `templates/owner_list.html` — список владельцев (с формой поиска и пагинацией).
  - `templates/owner.html` — детальная страница владельца.
  - `templates/owner_create.html` — страница с формой создания владельца.
  - `templates/car_list.html`, `templates/project_first_app/car_create.html`, `car_detail.html`, `car_update.html`, `car_delete.html` — CRUD-шаблоны для `Car`.

**Формы**
- Основная форма: `OwnerCreationForm` (см. `project_first_app/forms.py`) — форма создания пользователя с валидацией. `create_owner` использует эту форму и показывает сообщения об успехе/ошибках.

**Поведение и особенности реализации**
- **Поиск и пагинация**: `owner_list` использует `GET`-параметр `q` для фильтрации по `first_name`, `last_name`, `username` и `passport_number`. Пагинация реализована через `django.core.paginator.Paginator` с 5 элементами на страницу.
- **Custom User**: использована собственная модель `User`, поэтому во всём проекте надо ссылаться на неё через `get_user_model()` или `settings.AUTH_USER_MODEL`.
- **Ассоциативная таблица `Ownership`**: позволяет хранить периоды владения автомобилем (start/end), что расширяет семантику отношения между `User` и `Car`.
- **Админка**: настроена для удобного управления всеми сущностями; добавлены поисковые поля и фильтры.

**Что было сделано (кратко)**
- Создана кастомная модель пользователя `User` с дополнительными полями.
- Реализована предметная область: `Car`, `DriverLicense`, `Ownership`.
- Реализована полная CRUD-логика для автомобилей (CBV) и форма создания владельца (FBV).
- Добавлен поиск по владельцам и пагинация списка.
- Настроена админка для всех моделей.

**Запуск и проверка**
- После миграций и создания суперпользователя проверьте:
  - `http://127.0.0.1:8000/car/list/` — список автомобилей.
  - `http://127.0.0.1:8000/owner/list/` — список владельцев (поиск & навигация).
  - `http://127.0.0.1:8000/admin/` — админка (управление моделями и создание записей).

**Где смотреть код**
- Модели: `project_first_app/models.py`
- Представления: `project_first_app/views.py`
- Маршруты: `project_first_app/urls.py` и `django_project_nikiforov/urls.py`
- Админка: `project_first_app/admin.py`
- Шаблоны: `templates/` и `templates/project_first_app/`

**Скриншот административной панели**:

![Административная панель Django](lr2_screen/image.png)


Проект


Лабораторная работа 2 — Доска домашних заданий
==============================================

Краткое описание
----------------
Веб-приложение на Django для управления домашними заданиями: преподаватель создает задания и просматривает сдачи, студенты сдают работы и видят оценки. Интерфейс на Bootstrap, база данных PostgreSQL.

![Внешний вид](lr2_screen/image2.png)


Технологии
----------
- Python 3.13, Django 6.0
- PostgreSQL (по умолчанию `homework_db`, пользователь `postgres`, пароль `password`)
- psycopg2-binary, python-decouple

Как запустить локально
----------------------
1. Установить зависимости: `pip install -r requirements.txt`
2. Настроить БД PostgreSQL (или поменять настройки в `laboratory_work_2/settings.py` через переменные окружения: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`).
3. Применить миграции: `python manage.py migrate`
4. Создать суперпользователя: `python manage.py createsuperuser`
5. Запустить сервер: `python manage.py runserver` и открыть `http://127.0.0.1:8000/`

Основные страницы
-----------------
- `/register/`, `/login/`, `/logout/` — регистрация и вход.
- `/homeworks/` — список заданий с поиском и фильтром по предмету.
- `/homeworks/<id>/` — детали задания; студент может сдать работу, преподаватель видит все сдачи.
- `/my-grades/` — оценки студента и статистика по сдачам.
- `/class-grades/` — матрица оценок класса (только для преподавателя).
- `/admin/` — управление предметами, заданиями и оценками.

![Внешний вид](lr2_screen/image3.png)

Что реализовано
---------------
- Модели: `Subject`, `Homework`, `StudentSubmission` (одна сдача на студента, флаг опоздания, оценки 2–5).
- Пагинация списков, поиск по названию/описанию/предмету.
- Подсветка просроченных заданий, отметка опоздавших сдач.
- Статистика по сдачам (всего, проверено, вовремя, с опозданием).
- Кастомные template-фильтры для словаря оценок и подсчета опозданий.

Кратко об архитектуре
---------------------
Стандартный MVT Django: модели в `projects/models.py`, представления в `projects/views.py`, шаблоны в `projects/templates/`, маршруты подключены через `laboratory_work_2/urls.py`. Статика Bootstrap, без дополнительного фронтенд-сборщика.

СЦЕНАРИЙ 1: ОТ АДМИНИСТРАТОРА

1. Открыть http://localhost:8000/admin/
2. Авторизоваться (admin/password123)
3. Перейти в "Предметы" → "Добавить"
4. Заполнить форму:
   Name: Математика
5. Сохранить
6. Перейти в "Домашние задания" → "Добавить"
7. Заполнить:
   Subject: Математика
   Teacher: Admin
   Title: Вычисление интегралов
   Description: Вычислить 10 интегралов
   Due date: 2025-01-20 23:59
   Penalty info: 1 балл за день опоздания
8. Сохранить

СЦЕНАРИЙ 2: ОТ СТУДЕНТА

1. Открыть http://localhost:8000/register/
2. Зарегистрироваться:
   Username: student1
   Email: student@example.com
   Password: pass123456
3. Открыть http://localhost:8000/login/
4. Авторизоваться
5. Открыть http://localhost:8000/homeworks/
6. Кликнуть на задание "Вычисление интегралов"
7. Заполнить поле "Ваше решение"
8. Нажать "Сдать работу"
9. Открыть http://localhost:8000/my-grades/
10. Увидеть свою сданную работу

СЦЕНАРИЙ 3: ОЦЕНИВАНИЕ

1. Открыть http://localhost:8000/admin/
2. Перейти в "Сдачи домашних заданий"
3. Выбрать сданную работу студента
4. Установить Grade: 4
5. Сохранить
6. Студент увидит оценку на /my-grades/

