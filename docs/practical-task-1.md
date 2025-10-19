# Документация: Веб-приложение Django для управления данными об автовладельцах

---

## Описание проекта

Веб-приложение на Django для управления данными об автовладельцах, их автомобилях и водительских удостоверениях.

**Технологии:**
- Python 3.13
- Django 5.2.7
- SQLite (база данных)

---

## Создание моделей данных

### Шаг 1: Определение структуры данных

Для реализации системы управления автовладельцами необходимы следующие сущности:

**Основные сущности:**
- **Автовладелец** (CarOwner) - информация о владельцах автомобилей
- **Автомобиль** (Car) - данные об автомобилях
- **Водительское удостоверение** (DriverLicense) - информация о водительских правах
- **Владение** (Ownership) - связь между владельцами и автомобилями (ассоциативная сущность)

### Шаг 2: Реализация моделей

Создан файл `task1/models.py` с описанием всех моделей данных:

```python
from django.db import models


class CarOwner(models.Model):
    """Автовладелец"""
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Автовладелец"
        verbose_name_plural = "Автовладельцы"
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Car(models.Model):
    """Автомобиль"""
    license_plate = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"


class DriverLicense(models.Model):
    """Водительское удостоверение"""
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='licenses')
    license_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    issue_date = models.DateField()
    
    class Meta:
        verbose_name = "Водительское удостоверение"
        verbose_name_plural = "Водительские удостоверения"
    
    def __str__(self):
        return f"{self.license_number} ({self.owner})"


class Ownership(models.Model):
    """Владение (ассоциативная сущность)"""
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ownerships')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Владение"
        verbose_name_plural = "Владения"
    
    def __str__(self):
        return f"{self.owner} -> {self.car}"
```

### Описание полей моделей

#### CarOwner (Автовладелец)
| Поле | Тип | Описание |
|------|-----|----------|
| id | AutoField | Первичный ключ (создается автоматически) |
| last_name | CharField(30) | Фамилия |
| first_name | CharField(30) | Имя |
| birth_date | DateField | Дата рождения (может быть NULL) |

#### Car (Автомобиль)
| Поле | Тип | Описание |
|------|-----|----------|
| id | AutoField | Первичный ключ |
| license_plate | CharField(15) | Государственный номер |
| brand | CharField(20) | Марка |
| model | CharField(20) | Модель |
| color | CharField(30) | Цвет (может быть NULL) |

#### DriverLicense (Водительское удостоверение)
| Поле | Тип | Описание |
|------|-----|----------|
| id | AutoField | Первичный ключ |
| owner_id | ForeignKey | Внешний ключ на CarOwner |
| license_number | CharField(10) | Номер удостоверения |
| type | CharField(10) | Тип удостоверения |
| issue_date | DateField | Дата выдачи |

#### Ownership (Владение)
| Поле | Тип | Описание |
|------|-----|----------|
| id | AutoField | Первичный ключ |
| owner_id | ForeignKey | Внешний ключ на CarOwner |
| car_id | ForeignKey | Внешний ключ на Car |
| start_date | DateField | Дата начала владения |
| end_date | DateField | Дата окончания владения (может быть NULL) |

### Шаг 3: Конфигурация приложения

Создан файл `task1/apps.py` для настройки приложения:

```python
from django.apps import AppConfig


class Task1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task1'
```

**Назначение:**
- Определяет конфигурацию Django-приложения
- Указывает тип первичного ключа по умолчанию (BigAutoField)
- Задает имя модуля приложения

### Шаг 4: Инициализация приложения

В файл `task1/__init__.py` добавлена ссылка на конфигурацию:

```python
default_app_config = 'task1.apps.Task1Config'
```

**Назначение:**
- Связывает приложение с его конфигурацией
- Позволяет Django автоматически находить настройки приложения

### Шаг 5: Регистрация приложения

В файле `task1/settings.py` добавлено приложение в список установленных:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'task1',  # Добавлено наше приложение
]
```

### Шаг 6: Создание и применение миграций

Выполнены команды для создания таблиц в базе данных:

```bash
# Создание файлов миграций
python manage.py makemigrations task1

# Применение миграций к базе данных
python manage.py migrate
```

**Результат:**
- Создан файл миграции `task1/migrations/0001_initial.py`
- В базе данных SQLite созданы таблицы:
  - `task1_carowner` - таблица автовладельцев
  - `task1_car` - таблица автомобилей
  - `task1_driverlicense` - таблица водительских удостоверений
  - `task1_ownership` - таблица владений
- Установлены все связи между таблицами (Foreign Keys)
- Созданы индексы для оптимизации запросов

---

## Настройка административной панели

### Шаг 7: Регистрация моделей в админке

Создан файл `task1/admin.py` для регистрации моделей в административной панели Django:

```python
from django.contrib import admin
from .models import CarOwner, Car, DriverLicense, Ownership


@admin.register(CarOwner)
class CarOwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'birth_date')
    search_fields = ('last_name', 'first_name')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'license_plate', 'brand', 'model', 'color')
    search_fields = ('license_plate', 'brand', 'model')
    list_filter = ('brand',)


@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'license_number', 'type', 'issue_date')
    search_fields = ('license_number', 'owner__last_name')
    list_filter = ('type',)


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'car', 'start_date', 'end_date')
    search_fields = ('owner__last_name', 'car__license_plate')
    list_filter = ('start_date',)
```

**Возможности каждой модели в админке:**
- **list_display** - список полей, отображаемых в таблице
- **search_fields** - поля, по которым можно искать
- **list_filter** - фильтры в боковой панели

**Результат:**
- Все модели доступны в административной панели
- Возможность создавать, редактировать и удалять записи
- Удобный поиск и фильтрация данных

### Шаг 8: Создание суперпользователя

Выполнены команды для создания администратора:

```bash
# Создание администратора
python manage.py createsuperuser --username admin --email admin@example.com --no-input

# Установка пароля через Django shell
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); u = User.objects.get(username='admin'); u.set_password('admin'); u.save()"
```

**Результат:**
- Создан суперпользователь с учетными данными:
  - Логин: `admin`
  - Пароль: `admin`
- Доступ к административной панели по адресу: `/admin/`

---

## Создание представлений и шаблонов

### Шаг 9: Создание контроллера (View)

Создан файл `task1/views.py` с функцией для отображения информации о владельце:

```python
from django.http import Http404
from django.shortcuts import render
from .models import CarOwner


def owner_detail(request, owner_id):
    """Контроллер для отображения информации о владельце автомобиля"""
    try:
        owner = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("CarOwner does not exist")
    
    return render(request, 'owner.html', {'owner': owner})
```

**Как работает контроллер:**
1. Принимает HTTP-запрос и параметр `owner_id` из URL
2. Выполняет запрос к базе данных для получения объекта `CarOwner` с указанным ID
3. Если владелец не найден, возвращает ошибку 404
4. Если найден, передает объект `owner` в HTML-шаблон
5. Рендерит страницу с данными владельца

### Шаг 10: Создание папки для шаблонов

Создана директория для HTML-шаблонов:

```bash
mkdir -p templates
```

### Шаг 11: Создание HTML-шаблона

Создан файл `templates/owner.html` для отображения информации:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Информация о владельце</title>
</head>
<body>
    <h1>Информация о владельце автомобиля</h1>
    <p><strong>Имя:</strong> {{owner.first_name}}</p>
    <p><strong>Фамилия:</strong> {{owner.last_name}}</p>
    <p><strong>Дата рождения:</strong> {{owner.birth_date}}</p>
</body>
</html>
```

**Синтаксис шаблонов Django:**
- `{{owner.first_name}}` - выводит значение поля `first_name` объекта `owner`
- `{{owner.last_name}}` - выводит значение поля `last_name`
- `{{owner.birth_date}}` - выводит дату рождения в формате даты

### Шаг 12: Настройка путей к шаблонам

В файле `task1/settings.py` обновлена конфигурация шаблонов:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Добавлен путь к папке templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**Результат:**
- Django теперь ищет шаблоны в папке `templates/` в корне проекта
- Возможность использовать шаблоны во всех представлениях

### Шаг 13: Настройка маршрутизации URL

В файле `task1/urls.py` добавлен маршрут для нового представления:

```python
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
]
```

**Описание маршрута:**
- `owner/<int:owner_id>/` - шаблон URL-адреса
- `<int:owner_id>` - динамический параметр типа integer, автоматически передается в функцию
- `views.owner_detail` - функция-обработчик запроса
- `name='owner_detail'` - имя маршрута для использования в коде и шаблонах

**Примеры URL:**
- `/owner/1/` - отобразить информацию о владельце с ID=1
- `/owner/5/` - отобразить информацию о владельце с ID=5

**Результат:**
- Настроена полная цепочка: URL → View → Template
- При переходе по адресу `/owner/<ID>/` отображается информация о владельце

---

## Запуск и использование приложения

### Запуск сервера разработки

Для запуска приложения используется встроенный сервер разработки Django:

```bash
# Активация виртуального окружения
source project-env/bin/activate

# Запуск сервера
python manage.py runserver
```

**Результат:**
- Сервер запускается на адресе: **http://127.0.0.1:8000/**
- Приложение доступно для работы в браузере
- Автоматическая перезагрузка при изменении кода

### Использование административной панели

**URL:** http://127.0.0.1:8000/admin/

**Вход в систему:**
- Логин: `admin`
- Пароль: `admin`

**Доступный функционал:**
- Просмотр всех записей в таблицах
- Добавление новых записей (автовладельцы, автомобили, удостоверения, владения)
- Редактирование существующих записей
- Удаление записей
- Поиск по указанным полям
- Фильтрация данных

### Просмотр информации о владельце

**URL-адрес:** http://127.0.0.1:8000/owner/`<ID>`/

**Примеры использования:**
- http://127.0.0.1:8000/owner/1/ - информация о владельце с ID=1
- http://127.0.0.1:8000/owner/2/ - информация о владельце с ID=2

**Процесс работы:**
1. Открыть административную панель (`/admin/`)
2. Войти под учетными данными администратора
3. Создать запись автовладельца в разделе "Автовладельцы"
4. Запомнить ID созданной записи (отображается в списке)
5. Перейти по адресу `/owner/<ID>/`
6. На странице отобразится информация о владельце: имя, фамилия, дата рождения

---

## Структура базы данных

### Диаграмма связей

```
┌─────────────────┐         ┌──────────────────────┐
│   CarOwner      │         │   DriverLicense      │
├─────────────────┤         ├──────────────────────┤
│ id (PK)         │◄───────┤│ id (PK)              │
│ last_name       │      1:N│ owner_id (FK)        │
│ first_name      │         │ license_number       │
│ birth_date      │         │ type                 │
└─────────────────┘         │ issue_date           │
        │                   └──────────────────────┘
        │ 1:N
        │
        ▼
┌─────────────────┐
│   Ownership     │
├─────────────────┤
│ id (PK)         │
│ owner_id (FK)   │
│ car_id (FK)     │
│ start_date      │
│ end_date        │
└─────────────────┘
        │ N:1
        │
        ▼
┌─────────────────┐
│      Car        │
├─────────────────┤
│ id (PK)         │
│ license_plate   │
│ brand           │
│ model           │
│ color           │
└─────────────────┘
```

### Описание связей

1. **CarOwner ↔ DriverLicense** (один ко многим)
   - У одного владельца может быть несколько водительских удостоверений
   - Каждое удостоверение принадлежит только одному владельцу
   - При удалении владельца удаляются все его удостоверения (CASCADE)

2. **CarOwner ↔ Car** (многие ко многим через Ownership)
   - Один владелец может владеть несколькими автомобилями
   - Один автомобиль может иметь несколько владельцев (в разное время или одновременно)
   - Связь реализована через промежуточную таблицу `Ownership`

3. **Ownership** (ассоциативная сущность)
   - Хранит историю владения автомобилями
   - `start_date` - дата начала владения
   - `end_date` - дата окончания владения (NULL если владение активно)
   - Позволяет отслеживать временные периоды владения

---

## Полезные команды Django

### Работа с миграциями

```bash
# Создать миграции на основе изменений в моделях
python manage.py makemigrations

# Применить миграции к базе данных
python manage.py migrate

# Показать список всех миграций и их статус
python manage.py showmigrations

# Откатить миграции приложения к начальному состоянию
python manage.py migrate task1 zero

# Показать SQL-код миграции
python manage.py sqlmigrate task1 0001
```

### Работа с данными

```bash
# Открыть интерактивную оболочку Django с доступом к моделям
python manage.py shell

# Создать суперпользователя интерактивно
python manage.py createsuperuser

# Загрузить данные из JSON-файла
python manage.py loaddata fixture.json

# Выгрузить данные приложения в JSON
python manage.py dumpdata task1 > fixture.json

# Выгрузить данные конкретной модели
python manage.py dumpdata task1.CarOwner > owners.json
```

### Разработка

```bash
# Запустить сервер разработки
python manage.py runserver

# Запустить сервер на другом порту
python manage.py runserver 8080

# Запустить сервер на всех интерфейсах
python manage.py runserver 0.0.0.0:8000

# Проверить проект на ошибки конфигурации
python manage.py check

# Собрать статические файлы в одну папку
python manage.py collectstatic
```

---

## Примеры работы с моделями

### Создание объектов

```python
from task1.models import CarOwner, Car, DriverLicense, Ownership
from datetime import date

# Создание автовладельца
owner = CarOwner.objects.create(
    first_name="Иван",
    last_name="Иванов",
    birth_date=date(1990, 5, 15)
)

# Создание автомобиля
car = Car.objects.create(
    license_plate="А123БВ777",
    brand="Toyota",
    model="Camry",
    color="Черный"
)

# Создание водительского удостоверения
license = DriverLicense.objects.create(
    owner=owner,
    license_number="1234567890",
    type="B",
    issue_date=date(2015, 6, 10)
)

# Создание записи о владении
ownership = Ownership.objects.create(
    owner=owner,
    car=car,
    start_date=date(2020, 1, 1)
)
```

### Запросы к базе данных

```python
# Получить всех владельцев
all_owners = CarOwner.objects.all()

# Получить владельца по ID
owner = CarOwner.objects.get(id=1)

# Фильтрация по фамилии
ivanovs = CarOwner.objects.filter(last_name="Иванов")

# Поиск автомобилей по марке
toyotas = Car.objects.filter(brand="Toyota")

# Получить все автомобили конкретного владельца через связь
owner_cars = Car.objects.filter(ownerships__owner=owner)

# Получить все удостоверения владельца через related_name
owner_licenses = owner.licenses.all()

# Получить текущие активные владения (без даты окончания)
active_ownerships = Ownership.objects.filter(end_date__isnull=True)

# Получить владельцев, родившихся после определенной даты
young_owners = CarOwner.objects.filter(birth_date__gte=date(1990, 1, 1))

# Подсчет количества автомобилей каждой марки
from django.db.models import Count
car_counts = Car.objects.values('brand').annotate(count=Count('id'))
```

---

## Итоги реализации

В результате выполнения работы создано полнофункциональное веб-приложение на Django со следующими компонентами:

### Реализованный функционал

1. **Модели данных**
   - Четыре связанные таблицы с правильными отношениями
   - Поддержка NULL-значений для необязательных полей
   - Русские названия в административной панели
   - Реализация метода `__str__` для удобного отображения объектов

2. **Административная панель**
   - Регистрация всех моделей
   - Настроенные списки полей для отображения
   - Поиск и фильтрация данных
   - Возможность полного управления данными через веб-интерфейс

3. **Представления и шаблоны**
   - Контроллер для отображения информации о владельце
   - HTML-шаблон с использованием синтаксиса Django
   - Обработка ошибок (404 для несуществующих записей)
   - Настроенная маршрутизация URL

4. **База данных**
   - SQLite база данных с четырьмя таблицами
   - Правильно настроенные внешние ключи
   - Каскадное удаление связанных данных
   - Индексы для оптимизации запросов
