# Практическая работа №2.1

## Практическое задание 1

Необходимо установить Django Web framework любым доступным способом.

**Формат именований файлов:**

- Формат имени Django-проекта: “django_project_фамилия”.
- Формат имени Django-приложения: “project_first_app”.

### Выполнение задания 1

В первую очередь создадим venv-окружение для работы с Python и запустим его. Для этого выполним в терминале следующие команды:

```
python3 -m venv .venv
source .venv/bin/activate
```

Теперь установим Django:

```
pip install django
```

Создадим новый django-проект:

```
django-admin startproject django_project_klimenkov
```

А внутри этого проекта создадим новое приложение:

```
python3 manage.py startapp project_first_app
```

В результате нами был успешно установлен Django Web framework и создан базовый проект с приложением внутри. Теперь наш проект имеет следующую структуру файлов:

![1](../img/lab_2/pw_1/1.png)

Можно также проверить что проект создан корректно, запустив его на localhost с помощью команды:

```
python3 manage.py runserver
```

![2](../img/lab_2/pw_1/2.png)

И увидеть, что в браузере по адресу `http://127.0.0.1:8000/` находится приветственная страница Django:

![3](../img/lab_2/pw_1/3.png)

## Практическое задание 2.1

В проекте создать модель данных об автовладельцах в соответствии с рисунком:

![4](../img/lab_2/pw_1/4.png)

Указание: Таблицы и атрибуты именовать только на латинице.

Важно! Не забывайте о внешних ключах, полях выбора, правильном оформлении ассоциативной сущности в модели.

### Выполнение задания 2.1

В Django модели хранятся в файле `models.py`. Создадим в этом файле необходимые модели в соответствии с рисунком:

```python title="django_project_klimenkov/project_first_app/models.py"
from django.db import models
from django.contrib.auth.models import AbstractUser


class Owner(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    license_plate = models.CharField(max_length=15)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.model} ({self.license_plate})"


class DrivingLicense(models.Model):
    LICENSE_TYPES = [
        ('A', 'Категория A'),
        ('B', 'Категория B'),
        ('C', 'Категория C'),
        ('D', 'Категория D'),
        ('BE', 'Категория BE'),
        ('CE', 'Категория CE'),
        ('DE', 'Категория DE'),
        ('Tm', 'Категория Tm'),
        ('Tb', 'Категория Tb'),
        ('M', 'Категория M'),
        ('A1', 'Подкатегория A1'),
        ('B1', 'Подкатегория B1'),
        ('C1', 'Подкатегория C1'),
        ('D1', 'Подкатегория D1'),
        ('C1E', 'Подкатегория C1E'),
        ('D1E', 'Подкатегория D1E'),
    ]

    license_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10, choices=LICENSE_TYPES)
    issue_date = models.DateField()

    def __str__(self):
        return f"{self.license_number} ({self.license_type})"


class Ownership(models.Model):
    ownership_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} - {self.car} ({self.start_date} - {self.end_date})"
```

Для создания модели автовладельца воспользуемся `AbstractUser`, который уже содержит в себе поля `first_name`, `last_name` и `id`, а значит можно в классе модели их не указывать.

Для создания всех остальных моделей воспользуемся более общей `Model`, для которой ID указывать нужно.

Типы данных задаём с помощью `django.db.models` (`AutoField` - для ID, `DateField` - для дат, `CharField` - для строковых значений, `ForeignKey` - для внешних ключей).

Связь "многие ко многим" между автовладельцами и автомобилями реализуем с помощью отдельной модели `Ownership`.

Делаем поле `license_type` для `DrivingLicense` выборным с помощью параметра `choices=LICENSE_TYPES`, где `LICENSE_TYPES` - список с допустимыми значениями.

Для полей, которые могут быть необязательными, указываем параметры `null=True, blank=True`.

## Практическое задание 2.2

Создать миграции и применить их к базе данных.

### Выполнение задания 2.2

Для того чтобы сделать миграцию, нам нужно сначала зарегистрировать приложение `project_first_app`. Для этого перейдём в файл общих настроек проекта `django_project_klimenkov/django_project_klimenkov/settings.py` и добавим название нашего приложения в `INSTALLED_APPS`:

```python title="django_project_klimenkov/django_project_klimenkov/settings.py"
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'project_first_app', # Регистрируем наше приложение
]
```

Также, так как мы использовали `AbstractUser` для создания модели `Owner`, то нам нужно указать в настройках, что теперь `Owner` будет использоваться вместо базовой модели пользователя:

```python title="django_project_klimenkov/django_project_klimenkov/settings.py"
# Добавим эту строку
AUTH_USER_MODEL = 'project_first_app.Owner'
```

Теперь создадим миграцию с помощью команды:

```
python3 manage.py makemigrations project_first_app
```

Видим, что в папке `django_project_klimenkov/project_first_app/migrations` появился файл `0001_initial.py`, который содержит информацию о созданной нами миграции:

![5](../img/lab_2/pw_1/5.png)

Применим миграцию к базе данных с помощью команды:

```
python3 manage.py migrate
```

Теперь если посмотреть структуру файла `db.sqlite3`, в котором хранится база данных всего проекта, то можно увидеть следующие таблицы:

![6](../img/lab_2/pw_1/6.png)

Как можно заметить, база данных содержит как таблицы для созданных нами моделей, так и служебные таблицы. Тем не менее, наличие всех этих таблиц говорит о том, что миграция прошла успешно.

## Практическое задание 3

Необходимо заполнить таблицы данными средствами админ-панели:

- Зарегистрировать автовладельца и остальные модели данных в админ-панели.
- Создать суперпользователя.
- Через админ-панель добавить двух владельцев автомобилей, четыре автомобиля. Далее связать каждого владельца минимум с тремя автомобилями, так, чтобы не было пересечений по датам владения и продажи.

### Выполнение задания 3

Для начала зарегистрируем все созданные модели данных, чтобы к ним можно было бы получить доступ из админ-панели. Для этого перейдём в файл `django_project_klimenkov/project_first_app/admin.py` и укажем там все регистрируемые модели, а также те их поля, которые будут отображаться в общем списке:

```python title="django_project_klimenkov/project_first_app/admin.py"
from django.contrib import admin
from .models import Owner, Car, DrivingLicense, Ownership


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'birth_date']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['car_id', 'license_plate', 'model', 'color']


@admin.register(DrivingLicense)
class DrivingLicenseAdmin(admin.ModelAdmin):
    list_display = ['license_id', 'owner', 'license_number', 'license_type', 'issue_date']


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ['ownership_id', 'owner', 'car', 'start_date', 'end_date']
```

Также для получения доступа к админ-панели требуется создать суперпользователя, указав для него имя пользователя и пароль. Сделаем это можно с помощью следующей команды:

```
python3 manage.py createsuperuser
```

После создания суперпользователя запустим сервер и перейдём по адресу `http://127.0.0.1:8000/admin/`, где в появившемся окне нужно будет ввести username и пароль суперпользователя, после чего мы сможем получить доступ к админ-панели:

![7](../img/lab_2/pw_1/7.png)

![8](../img/lab_2/pw_1/8.png)

Теперь через админ-панель добавим необходимые данные.

В случае с `Owner` мы использовали `AbstractUser`, а значит полей доступных для ввода в админ-панели будет больше, чем мы напрямую указывали, но чтобы успешно добавить автовладельца будет достаточно задать значения лишь нужным нам полям `first_name`, `last_name` и `birth_date`, а также полям `username` и `password`, которые являются обязательными для `AbstractUser` (так как мы не будем использовать эти поля, то им можно задать произвольные значения, но так, чтобы `username` у всех пользователей был уникальным):

![9](../img/lab_2/pw_1/9.png)

Создадим таким образом двух автовладельцев:

![10](../img/lab_2/pw_1/10.png)

(Пользователь с ID 1 является суперпользователем, которого мы создали ранее.)

Аналогичным образом добавим четыре автомобиля и свяжем каждого владельца минимум с тремя автомобилями, избегая пересечения по датам:

![11](../img/lab_2/pw_1/11.png)

![12](../img/lab_2/pw_1/12.png)

![13](../img/lab_2/pw_1/13.png)

![14](../img/lab_2/pw_1/14.png)

## Практическое задание 4

Создать в файле views.py (находится в папке приложения) представление (контроллер), который выводит из базы данных данные о владельце автомобиля.

Создать страницу html-шаблона owner.html в папке templates (создать папку templates в корне проекта, если её нигде нет, далее в контекстном меню папки создать html-файл). Страница должна содержать отображение полей переданных из контроллера.

### Выполнение задания 4

Для начала перейдём в файл `django_project_klimenkov/project_first_app/views.py` и создадим там контроллер, который будет выводить данные о владельце автомобиля:

```python title="django_project_klimenkov/project_first_app/views.py"
from django.shortcuts import render
from django.http import Http404
from .models import Owner


def owner_detail(request, id):
    """
    Представление для отображения детальной информации об автовладельце.
    """
    try:
        owner = Owner.objects.get(pk=id)
    except Owner.DoesNotExist:
        raise Http404("Автовладелец не найден")
    
    return render(request, 'owners/owner_detail.html', {'owner': owner})
```

Чтобы контроллер работал корректно, нужно также создать html-шаблон, с помощью которого контроллер сможет отображать информацию об автовладельце. Создадим данный шаблон в папке `templates` (данной папки по-умолчанию нет, так что первоначально создадим её):

```html title="django_project_klimenkov/templates/owners/owner_detail.html"
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Информация об автовладельце</title>
</head>
<body>
    <h1>Информация об автовладельце</h1> 
    <div>
        <p><strong>ID:</strong> {{ owner.id }}</p>
        <p><strong>Фамилия:</strong> {{ owner.last_name }}</p>
        <p><strong>Имя:</strong> {{ owner.first_name }}</p>
        <p><strong>Дата рождения:</strong> {{ owner.birth_date }}</p>
    </div>
</body>
</html>
```

Чтобы папка `templates` воспринималась проектом как папка для html-шаблонов нужно добавить её в `settings.TEMPLATES`:

```python title="django_project_klimenkov/django_project_klimenkov/settings.py"
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Регистрируем созданную нами папку как папку для шаблонов
        'DIRS': [BASE_DIR / 'templates'],

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

## Практическое задание 5

Создать файл адресов `urls.py` в папке приложения.

Импортировать файл `urls.py` приложения в проект (модифицировать файл `urls.py` в той папке, в которой хранится файл `setting.py`).

Описать в файле `urls.py` приложения, созданном ранее, такой url-адрес, который сможет обратиться к контроллеру и вывести страницу, которая должна быть отрендерена контроллером.

Результат: по url-адресу `127.0.0.1:8000/owner/1` возможно получить страницу с информацией о первом автовладельце.

### Выполнение задания 5

Создадим файл адресов `django_project_klimenkov/project_first_app/urls.py` в папке приложения. Чтобы адреса, добавленные в этот файл, работали корректно, требуется зарегистрировать созданный файл в файле адресов `django_project_klimenkov/django_project_klimenkov/urls.py` в папке проекта. Сделаем это:

```python title="django_project_klimenkov/django_project_klimenkov/urls.py"
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # Адрес для доступа к админ-панели
    path('', include('project_first_app.urls')), # Регистрируем адреса приложения
]
```

Теперь в `django_project_klimenkov/project_first_app/urls.py` укажем url-адрес, по которому можно будет получить информацию о конкретном автовладельце:

```python title="django_project_klimenkov/project_first_app/urls.py"
from django.urls import path
from . import views


urlpatterns = [
    # При переходе по этому адресу в контроллер owner_detail будут переданы
    # request (сам запрос) и id (ID автовладельца)
    path('owner/<int:id>/', views.owner_detail, name='owner_detail'),
]
```

Теперь при переходе по адресу `127.0.0.1:8000/owner/<id>` будет выведена информация об автовладельце с идентификатором `id`.

Для проверки запустим сервер и перейдём по адресу `127.0.0.1:8000/owner/2/`:

![15](../img/lab_2/pw_1/15.png)

Видим, что действительно отобразилась информация об автовладельце с ID 2 согласно созданному нами шаблону.

## Добавление CSS-стилей

На данный момент страница с информацией об автовладельце использует только "голый" HTML, а потому её оформление может быть не самым привлекательным. Чтобы это исправить, попробуем подключить к приложению CSS-стили.

Для этого создадим папки `django_project_klimenkov/static/css` и поместим туда файл `styles.css`, в который в дальнейшем можно будет добавлять CSS-стили для веб-приложения.

Зарегистрируем папку `static` как папку для статических файлов (CSS, JavaScript, изображения) в `settings.py`:

```python title="django_project_klimenkov/django_project_klimenkov/settings.py"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Регистрируем папку "static" как папку для статических файлов
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

Теперь подключим к шаблону `owner_detail.html` CSS-стили из файла `styles.css`:

```html title="django_project_klimenkov/templates/owners/owner_detail.html"
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Информация об автовладельце</title>
    <link rel="stylesheet" href="{% static 'css/styles.css'%}" type="text/css">
</head>
<body>
    <h1>Информация об автовладельце</h1>
    <div class="detail-card">
        <p><strong>ID:</strong> {{ owner.id }}</p>
        <p><strong>Фамилия:</strong> {{ owner.last_name }}</p>
        <p><strong>Имя:</strong> {{ owner.first_name }}</p>
        <p><strong>Дата рождения:</strong> {{ owner.birth_date }}</p>
    </div>
</body>
</html>
```

Для подключения CSS-стилей добавили следующие строки:

- `{% load static %}`: Подгрузка статических файлов к HTML-шаблону.
- `<link rel="stylesheet" href="{% static 'css/styles.css'%}" type="text/css">`: Подключение CSS-стилей из `styles.css`.

Теперь обновим страницу и увидим, что CSS-стили действительно применились:

![16](../img/lab_2/pw_1/16.png)
