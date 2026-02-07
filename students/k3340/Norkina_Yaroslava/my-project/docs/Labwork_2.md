# Отчет

## Лабораторная работа №2 «Реализация простого сайта средствами Django»

Цель: овладеть практическими навыками и умениями реализации web-сервисов

средствами Django 2.2.

Программное обеспечение: Python 3.6+, Django 3, PostgreSQL \*.

**Практическое задание:**

Реализовать сайт используя фреймворк Django 3 и СУБД PostgreSQL \*, в

соответствии с вариантом задания лабораторной работы.

7\. Свой вариант

Приложение каршеринга, страница отображения поездок. Поездка должна
иметь следующие данные: водитель, длительность, время начала, точка
начала и окончания, данные об автомобиле, тариф.

Необходимо реализовать следующий функционал:

-   Регистрация новых пользователей.

-   Пользователь должен просматривать прошедшие поездки и иметь
    возможность создавать и завершать новые поездки.

-   После завершения поездки администратор должен иметь возможность
    добавить к поездке комментарий о состоянии машины и о ремонте, если
    он требуется, средствами Django-admin.

-   Написание отзыва к поездке. При добавлении комментариев должны
    сохраняться даты поездки, текст комментария, рейтинг (1-10),
    информация о комментаторе.

-   В клиентской части должна формироваться таблица всех поездок за
    последний месяц и информации о поездке, водителе и автомобиле.

Ход работы.

1 Этап. Создание базы данных

<img width="974" height="434" alt="image" src="https://github.com/user-attachments/assets/a6151543-a799-429d-8529-dfa8ca88adc8" />

Models.py

``` python
\# carshering/models.py

from django.db import models

from django.contrib.auth.models import AbstractUser

from django.core.validators import MinValueValidator, RegexValidator

\# ========================

\# 1. Расширенный пользователь (Users → User)

\# ========================

class User(AbstractUser):

\# Поле user_name из SQL заменяется на first_name + last_name или
username

\# Но если нужно именно user_name --- добавим его

user_name = models.CharField(\"Имя пользователя\", max_length=50)

def \_\_str\_\_(self):

return self.user_name or self.username

\# ========================

\# 2. Models → Model

\# ========================

class Model(models.Model):

brand = models.CharField(

\"Марка\",

max_length=50,

validators=\[MinValueValidator(1, message=\"Марка не может быть
пустой\")\]

)

model_name = models.CharField(

\"Модель\",

max_length=50,

validators=\[MinValueValidator(1, message=\"Модель не может быть
пустой\")\]

)

power = models.PositiveIntegerField(\"Мощность (л.с.)\")

class Meta:

verbose_name = \"Модель автомобиля\"

verbose_name_plural = \"Модели автомобилей\"

def \_\_str\_\_(self):

return f\"{self.brand} {self.model_name}\"

\# ========================

\# 3. Cars → Car

\# ========================

class Car(models.Model):

mileage = models.PositiveIntegerField(\"Пробег\", default=0)

licence = models.CharField(

\"Гос. номер\",

max_length=9,

unique=True,

validators=\[RegexValidator(r\'\^\[A-Z0-9\]{1,9}\$\', \'Номер должен
содержать до 9 латинских букв и цифр\')\]

)

serial_number = models.CharField(\"VIN\", max_length=17, blank=True)

buying_date = models.DateField(\"Дата покупки\")

city = models.CharField(\"Город\", max_length=50, blank=True)

coordinates = models.FloatField(\"Координаты\")

malfunctions = models.TextField(\"Неисправности\", blank=True)

model = models.ForeignKey(

Model,

on_delete=models.CASCADE,

verbose_name=\"Модель\",

related_name=\'cars\'

)

class Meta:

verbose_name = \"Автомобиль\"

verbose_name_plural = \"Автомобили\"

def \_\_str\_\_(self):

return f\"{self.licence} ({self.model})\"

\# ========================

\# 4. Passport

\# ========================

class Passport(models.Model):

passport_number = models.CharField(

\"Номер паспорта\",

max_length=6,

unique=True,

validators=\[RegexValidator(r\'\^\\d{6}\$\', \'Номер паспорта --- 6
цифр\')\]

)

serial_number = models.CharField(

\"Серия паспорта\",

max_length=4,

validators=\[RegexValidator(r\'\^\\d{4}\$\', \'Серия паспорта --- 4
цифры\')\]

)

birth_date = models.DateField(\"Дата рождения\")

user = models.OneToOneField(

User,

on_delete=models.CASCADE,

verbose_name=\"Пользователь\",

related_name=\'passport\'

)

class Meta:

verbose_name = \"Паспорт\"

verbose_name_plural = \"Паспорта\"

def \_\_str\_\_(self):

return f\"Паспорт {self.serial_number} {self.passport_number}\"

\# ========================

\# 5. DriverLicense

\# ========================

class DriverLicense(models.Model):

date_of_issue = models.DateField(\"Дата выдачи\")

expiration_date = models.DateField(\"Срок действия\")

user = models.OneToOneField(

User,

on_delete=models.CASCADE,

verbose_name=\"Водитель\",

related_name=\'driver_license\'

)

class Meta:

verbose_name = \"Водительское удостоверение\"

verbose_name_plural = \"Водительские удостоверения\"

def \_\_str\_\_(self):

return f\"ВУ {self.user.user_name} (до {self.expiration_date})\"

def clean(self):

from django.core.exceptions import ValidationError

if self.expiration_date \<= self.date_of_issue:

raise ValidationError(\"Срок действия должен быть позже даты выдачи.\")

def save(self, \*args, \*\*kwargs):

self.full_clean()

super().save(\*args, \*\*kwargs)

\# ========================

\# 6. Repairs

\# ========================

class Repair(models.Model):

description = models.TextField(\"Описание\", blank=True)

datetime = models.DateTimeField(\"Дата и время ремонта\")

car = models.ForeignKey(

Car,

on_delete=models.CASCADE,

verbose_name=\"Автомобиль\",

related_name=\'repairs\'

)

class Meta:

verbose_name = \"Ремонт\"

verbose_name_plural = \"Ремонты\"

def \_\_str\_\_(self):

return f\"Ремонт {self.car.licence} от {self.datetime.date()}\"

\# ========================

\# 7. Payment

\# ========================

class Payment(models.Model):

description = models.TextField(\"Описание\")

value = models.FloatField(

\"Сумма\",

validators=\[MinValueValidator(0.01, \"Сумма должна быть
положительной\")\]

)

date = models.DateField(\"Дата платежа\")

deadline = models.DateField(\"Срок оплаты\")

type = models.CharField(\"Тип платежа\", max_length=50, blank=True)

user = models.ForeignKey(

User,

on_delete=models.CASCADE,

verbose_name=\"Пользователь\",

related_name=\'payments\'

)

class Meta:

verbose_name = \"Платёж\"

verbose_name_plural = \"Платежи\"

def \_\_str\_\_(self):

return f\"Платёж {self.user.user_name}: {self.value} руб.\"

def clean(self):

from django.core.exceptions import ValidationError

if self.deadline \<= self.date:

raise ValidationError(\"Срок оплаты должен быть позже даты платежа.\")

def save(self, \*args, \*\*kwargs):

self.full_clean()

super().save(\*args, \*\*kwargs)

\# ========================

\# 8. Tariffs

\# ========================

class Tariff(models.Model):

price_per_minute = models.PositiveIntegerField(\"Цена за минуту\",
null=True, blank=True)

start_time = models.DateTimeField(\"Начало действия\")

end_time = models.DateTimeField(\"Окончание действия\")

model = models.ForeignKey(

Model,

on_delete=models.CASCADE,

verbose_name=\"Модель\",

related_name=\'tariffs\'

)

class Meta:

verbose_name = \"Тариф\"

verbose_name_plural = \"Тарифы\"

def \_\_str\_\_(self):

return f\"Тариф для {self.model} ({self.start_time} --
{self.end_time})\"

def clean(self):

from django.core.exceptions import ValidationError

if self.end_time \<= self.start_time:

raise ValidationError(\"Окончание должно быть позже начала.\")

def save(self, \*args, \*\*kwargs):

self.full_clean()

super().save(\*args, \*\*kwargs)

\# ========================

\# 9. Trip

\# ========================

class Trip(models.Model):

start_time = models.DateTimeField(\"Начало поездки\")

end_time = models.DateTimeField(\"Окончание поездки\")

problems = models.TextField(\"Проблемы\", blank=True)

comments = models.TextField(\"Комментарии\", blank=True)

car = models.ForeignKey(

Car,

on_delete=models.CASCADE,

verbose_name=\"Автомобиль\",

related_name=\'trips\'

)

user = models.ForeignKey(

User,

on_delete=models.CASCADE,

verbose_name=\"Пользователь\",

related_name=\'trips\'

)

class Meta:

verbose_name = \"Поездка\"

verbose_name_plural = \"Поездки\"

def \_\_str\_\_(self):

return f\"Поездка {self.user.user_name} на {self.car.licence}\"

def clean(self):

from django.core.exceptions import ValidationError

if self.end_time \<= self.start_time:

raise ValidationError(\"Окончание поездки должно быть позже начала.\")

def save(self, \*args, \*\*kwargs):

self.full_clean()

super().save(\*args, \*\*kwargs)
```

**2 Этап. Реализация проекта средствами Django-фрэймворка**

2.1 Перенос базы данных в проект

Создаем новый проект: `django-admin startproject django_project_norkina_2`

<img width="252" height="338" alt="image" src="https://github.com/user-attachments/assets/2a180e58-395c-4ae9-ac20-b7d54b156b83" />

Дальше в новом проекте создаем приложение: `python manage.py startapp`
`project2_first_app`

<img width="265" height="273" alt="image" src="https://github.com/user-attachments/assets/2e236811-9f7c-4046-805a-d9ca1d4af3aa" />

`python manage.py makemigrations`

<img width="974" height="230" alt="image" src="https://github.com/user-attachments/assets/45d76de9-9276-4cdc-b2a0-7355116f0245" />

`python manage.py migrate`

<img width="974" height="428" alt="image" src="https://github.com/user-attachments/assets/14842b25-5cba-4a1b-a92d-3305039b35a2" />

Зарегистрируем модели в файле admin.py и добавим суперпользователя:

<img width="974" height="173" alt="image" src="https://github.com/user-attachments/assets/64943f87-44cb-4943-b3fd-52f9ebcaaa81" />


Теперь сервер с базой данных готов и его можно запустить.

<img width="974" height="467" alt="image" src="https://github.com/user-attachments/assets/0a0f38f2-5ad3-484c-9ba9-258b234ab4db" />

2.2 Реализация CRUD (Create, read, update and delete) интерфейсов 

\- Первоначально создана страница просмотра таблицы всех поездок

trip_list.html:

``` python
\<!DOCTYPE html\>

\<html lang=\"ru\"\>

\<head\>

    \<meta charset=\"UTF-8\"\>

    \<title\>Поездки за последний месяц\</title\>

    \<style\>

        table { border-collapse: collapse; width: 100%; }

        th, td { border: 1px solid #ccc; padding: 8px; text-align: left;
}

        th { background-color: #f4f4f4; }

        tr:nth-child(even) { background-color: #f9f9f9; }

    \</style\>

\</head\>

\<body\>

    \<h1\>Поездки за последний месяц\</h1\>

    \<p\>Период: с {{ one_month_ago\|date:\"d.m.Y H:i\" }} по {{
now\|date:\"d.m.Y H:i\" }}\</p\>

    {% if trips %}

        \<table\>

            \<thead\>

                \<tr\>

                    \<th\>ФИО водителя\</th\>

                    \<th\>Начало\</th\>

                    \<th\>Окончание\</th\>

                    \<th\>Гос. номер\</th\>

                    \<th\>Марка и модель\</th\>

                    \<th\>Проблемы\</th\>

                    \<th\>Комментарии\</th\>

                \</tr\>

            \</thead\>

            \<tbody\>

                {% for trip in trips %}

                \<tr\>

                    \<td\>{{ trip.user.first_name }} {{
trip.user.last_name }}\</td\>

                    \<td\>{{ trip.start_time\|date:\"d.m.Y H:i\"
}}\</td\>

                    \<td\>{{ trip.end_time\|date:\"d.m.Y H:i\" }}\</td\>

                    \<td\>{{ trip.car.licence }}\</td\>

                    \<td\>{{ trip.car.model.brand }} {{
trip.car.model.model_name }}\</td\>

                    \<td\>{{ trip.problems\|default:\"---\" }}\</td\>

                    \<td\>{{ trip.comments\|default:\"---\" }}\</td\>

                \</tr\>

                {% endfor %}

            \</tbody\>

        \</table\>

    {% else %}

        \<p\>За последний месяц поездок не совершено.\</p\>

    {% endif %}

    \<br\>

    \<a href=\"{% url \'trip_list_last_month\' %}\"\>Обновить\</a\>

\</body\>

\</html\>
```

views.py:

``` python
from django.shortcuts import render, redirect

from django.utils import timezone

from datetime import timedelta

from .models import Trip

def trip_list_last_month(request):

    \"\"\"

    Отображает все поездки за последний месяц.

    \"\"\"

    now = timezone.now()

    one_month_ago = now - timedelta(days=30)

    trips = Trip.objects.filter(

        start_time\_\_gte=one_month_ago

    ).select_related(\'user\', \'car\',
\'car\_\_model\').order_by(\'-start_time\')

    context = {

        \'trips\': trips,

        \'now\': now,

        \'one_month_ago\': one_month_ago,

    }

    return render(request, \'trip_list.html\', context)
```

urls.py:

``` python
path(\'trips/\', views.trip_list_last_month,
name=\'trip_list_last_month\'),
```

При этом в settings.py обязательно должны быть указаны проект и
приложение перед запуском сервера:

``` python
WSGI_APPLICATION = \'django_project_norkina_2.wsgi.application\'

AUTH_USER_MODEL = \'project2_first_app.User\'
```
<img width="974" height="349" alt="image" src="https://github.com/user-attachments/assets/19903e90-79e8-4c1d-ab18-a1fa592f1f58" />

\- Добавлены страница и форма регистрации пользователя

register.html:

``` python
\<!DOCTYPE html\>

\<html lang=\"ru\"\>

\<head\>

    \<meta charset=\"UTF-8\"\>

    \<title\>Регистрация\</title\>

    \<style\>

        .form-group { margin-bottom: 15px; }

        label { display: block; font-weight: bold; }

        input { width: 100%; padding: 8px; box-sizing: border-box; }

        button { padding: 10px 20px; background: #28a745; color: white;
border: none; cursor: pointer; }

        button:hover { background: #218838; }

        .error { color: red; font-size: 0.9em; }

    \</style\>

\</head\>

\<body\>

    \<h2\>Регистрация нового пользователя\</h2\>

    \<form method=\"post\"\>

        {% csrf_token %}

        \<div class=\"form-group\"\>

            \<label for=\"{{ form.username.id_for_label
}}\"\>Логин:\</label\>

            {{ form.username }}

            {% if form.username.errors %}\<div class=\"error\"\>{{
form.username.errors }}\</div\>{% endif %}

        \</div\>

        \<div class=\"form-group\"\>

            \<label for=\"{{ form.user_name.id_for_label }}\"\>Имя
пользователя:\</label\>

            {{ form.user_name }}

            {% if form.user_name.errors %}\<div class=\"error\"\>{{
form.user_name.errors }}\</div\>{% endif %}

        \</div\>

        \<div class=\"form-group\"\>

            \<label for=\"{{ form.first_name.id_for_label }}\"\>Имя
(необязательно):\</label\>

            {{ form.first_name }}

        \</div\>

        \<div class=\"form-group\"\>

            \<label for=\"{{ form.last_name.id_for_label }}\"\>Фамилия
(необязательно):\</label\>

            {{ form.last_name }}

        \</div\>

        \<div class=\"form-group\"\>

            \<label for=\"{{ form.email.id_for_label
}}\"\>Email:\</label\>

            {{ form.email }}

            {% if form.email.errors %}\<div class=\"error\"\>{{
form.email.errors }}\</div\>{% endif %}

        \</div\>

        \<div class=\"form-group\"\>

            \<label for=\"{{ form.password1.id_for_label
}}\"\>Пароль:\</label\>

            {{ form.password1 }}

            {% if form.password1.errors %}\<div class=\"error\"\>{{
form.password1.errors }}\</div\>{% endif %}

        \</div\>

        \<div class=\"form-group\"\>

            \<label for=\"{{ form.password2.id_for_label
}}\"\>Подтверждение пароля:\</label\>

            {{ form.password2 }}

            {% if form.password2.errors %}\<div class=\"error\"\>{{
form.password2.errors }}\</div\>{% endif %}

        \</div\>

        \<button type=\"submit\"\>Зарегистрироваться\</button\>

    \</form\>

    \<br\>

    \<a href=\"{% url \'trip_list_last_month\' %}\"\>← Назад\</a\>

\</body\>

\</html\>

forms.py:

from django import forms

from django.contrib.auth.forms import UserCreationForm

from .models import User, Trip

class CustomUserRegistrationForm(UserCreationForm):

    user_name = forms.CharField(

        max_length=50,

        label=\"Имя пользователя\",

        help_text=\"Обязательное поле. До 50 символов.\"

    )

    first_name = forms.CharField(max_length=30, required=False)

    last_name = forms.CharField(max_length=30, required=False)

    email = forms.EmailField(required=True)

    class Meta:

        model = User

        fields = (

            \'username\',

            \'user_name\',

            \'first_name\',

            \'last_name\',

            \'email\',

            \'password1\',

            \'password2\'

        )

    def save(self, commit=True):

        user = super().save(commit=False)

        user.user_name = self.cleaned_data\[\'user_name\'\]

        user.first_name = self.cleaned_data.get(\'first_name\', \'\')

        user.last_name = self.cleaned_data.get(\'last_name\', \'\')

        user.email = self.cleaned_data\[\'email\'\]

        if commit:

            user.save()

        return user
```

views.py:

``` python
from django.contrib.auth import login

from django.urls import reverse_lazy

from .forms import CustomUserRegistrationForm

def register(request):

    if request.method == \'POST\':

        form = CustomUserRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)  # автоматический вход после
регистрации

            return redirect(reverse_lazy(\'trip_list_last_month\'))  #
или любой другой маршрут

    else:

        form = CustomUserRegistrationForm()

    return render(request, \'users/register.html\', {\'form\': form})
```

urls.py:

`path(\'register/\', views.register, name=\'register\'),`

<img width="974" height="489" alt="image" src="https://github.com/user-attachments/assets/6f497fde-39fc-4d09-ad84-c025c78ea657" />

\- Затем добавлена страница профиля

``` python
user_profile.html:

\<!DOCTYPE html\>

\<html lang=\"ru\"\>

\<head\>

    \<meta charset=\"UTF-8\"\>

    \<title\>Мой профиль\</title\>

    \<style\>

        body { font-family: Arial, sans-serif; max-width: 800px; margin:
40px auto; padding: 20px; }

        table { width: 100%; border-collapse: collapse; margin-top:
15px; }

        th, td { border: 1px solid #ccc; padding: 10px; text-align:
left; }

        th { background-color: #f4f4f4; }

        .header { display: flex; justify-content: space-between;
align-items: center; margin-bottom: 20px; }

        .btn { padding: 8px 16px; background: #dc3545; color: white;
border: none; cursor: pointer; text-decoration: none; display:
inline-block; }

        .btn:hover { background: #c82333; }

    \</style\>

\</head\>

\<body\>

    \<div class=\"header\"\>

        \<h1\>Мой профиль\</h1\>

        \<!\-- Кнопка выхода \--\>

        \<form method=\"post\" action=\"{% url \'logout\' %}\"
style=\"display:inline;\"\>

            {% csrf_token %}

            \<button type=\"submit\" class=\"btn\"\>Выйти\</button\>

        \</form\>

    \</div\>

    \<p\>\<strong\>Логин:\</strong\> {{ user.username }}\</p\>

    \<p\>\<strong\>Имя пользователя:\</strong\> {{ user.user_name
}}\</p\>

    \<p\>\<strong\>Email:\</strong\> {{ user.email }}\</p\>

    {% if user.first_name or user.last_name %}

        \<p\>\<strong\>ФИО:\</strong\> {{ user.first_name }} {{
user.last_name }}\</p\>

    {% endif %}

    \<a href=\"{% url \'add_trip\' %}\"\>Добавить новую поездку\</a\>

    \<!\-- Для отзывов \--\>

    {% for trip in trips %}

      \<p\>{{ trip.car.licence }} --- {{ trip.start_time\|date:\"d.m.Y\"
}}

        \<a href=\"{% url \'add_comment\' trip.id %}\"\>Оставить
отзыв\</a\>

      \</p\>

    {% endfor %}

    \<h2\>Мои поездки\</h2\>

    {% if trips %}

        \<table\>

            \<thead\>

                \<tr\>

                    \<th\>Гос. номер\</th\>

                    \<th\>Марка/Модель\</th\>

                    \<th\>Начало\</th\>

                    \<th\>Окончание\</th\>

                \</tr\>

            \</thead\>

            \<tbody\>

                {% for trip in trips %}

                \<tr\>

                    \<td\>{{ trip.car.licence }}\</td\>

                    \<td\>{{ trip.car.model.brand }} {{
trip.car.model.model_name }}\</td\>

                    \<td\>{{ trip.start_time\|date:\"d.m.Y H:i\"
}}\</td\>

                    \<td\>{{ trip.end_time\|date:\"d.m.Y H:i\" }}\</td\>

                \</tr\>

                {% endfor %}

            \</tbody\>

        \</table\>

    {% else %}

        \<p\>У вас пока нет поездок.\</p\>

    {% endif %}

    \<br\>

    \<a href=\"{% url \'trip_list_last_month\' %}\"\>← Все поездки\</a\>

\</body\>

\</html\>

views.py:

from django.contrib.auth.decorators import login_required

from .models import Trip

\@login_required

def user_profile(request):

    \"\"\"

    Отображает профиль текущего пользователя и его поездки.

    \"\"\"

    trips =
Trip.objects.filter(user=request.user).select_related(\'car\',
\'car\_\_model\').order_by(\'-start_time\')

    return render(request, \'users/user_profile.html\', {

        \'user\': request.user,

        \'trips\': trips

    })
```

urls.py:

`path(\'profile/\', views.user_profile, name=\'user_profile\'),`

<img width="974" height="422" alt="image" src="https://github.com/user-attachments/assets/61144c5d-9eea-4e15-b912-da36a32e838b" />

\- Страница входа в аккаунт. Используется стандартный контроллер Jango
для входа в аккаунт, поэтому прописывать функции в views.py не нужно.

login.html:

``` python
\<!DOCTYPE html\>

\<html lang=\"ru\"\>

\<head\>

    \<meta charset=\"UTF-8\"\>

    \<title\>Вход\</title\>

    \<style\>

        body { font-family: Arial, sans-serif; max-width: 500px; margin:
40px auto; padding: 20px; }

        .form-group { margin-bottom: 15px; }

        label { display: block; font-weight: bold; margin-bottom: 5px; }

        input { width: 100%; padding: 8px; box-sizing: border-box; }

        button { padding: 10px 20px; background: #007bff; color: white;
border: none; cursor: pointer; }

        button:hover { background: #0056b3; }

        .error { color: red; font-size: 0.9em; }

        .links { margin-top: 15px; }

        .links a { color: #007bff; text-decoration: none; margin-right:
15px; }

    \</style\>

\</head\>

\<body\>

    \<h2\>Вход в аккаунт\</h2\>

    {% if form.errors %}

        \<p class=\"error\"\>Неверное имя пользователя или пароль.\</p\>

    {% endif %}

    \<form method=\"post\"\>

        {% csrf_token %}

        \<div class=\"form-group\"\>

            \<label for=\"{{ form.username.id_for_label
}}\"\>Логин:\</label\>

            {{ form.username }}

        \</div\>

        \<div class=\"form-group\"\>

            \<label for=\"{{ form.password.id_for_label
}}\"\>Пароль:\</label\>

            {{ form.password }}

        \</div\>

        \<button type=\"submit\"\>Войти\</button\>

    \</form\>

    \<div class=\"links\"\>

        \<a href=\"{% url \'register\' %}\"\>Регистрация\</a\>

        \<a href=\"{% url \'trip_list_last_month\' %}\"\>Главная\</a\>

    \</div\>

\</body\>

\</html\>
```

В файле urls.py прописывается стандартный метод и указывается страница
входа:

``` python
path(\'login/\',
auth_views.LoginView.as_view(template_name=\'users/login.html\'),
name=\'login\'),
```

settings.py:

`LOGIN_REDIRECT_URL = \'/profile/\'`

<img width="974" height="410" alt="image" src="https://github.com/user-attachments/assets/e636bb55-6f9a-4910-92fb-6c75f6431959" />

\- Страница выхода из аккаунта

logout.html:

``` python
\<!DOCTYPE html\>

\<html lang=\"ru\"\>

\<head\>

    \<meta charset=\"UTF-8\"\>

    \<title\>Выход\</title\>

\</head\>

\<body\>

    \<h2\>Вы действительно хотите выйти?\</h2\>

    \<form method=\"post\" action=\"{% url \'logout\' %}\"\>

        {% csrf_token %}

        \<button type=\"submit\"\>Да, выйти\</button\>

    \</form\>

    \<p\>\<a href=\"{% url \'trip_list_last_month\'
%}\"\>Отмена\</a\>\</p\>

\</body\>

\</html\>
```

urls.py:
``` python
path(\'logout/\',
auth_views.LogoutView.as_view(template_name=\'users/login.html\'),
name=\'logout\'),
```

settings.py:

`LOGOUT_REDIRECT_URL = \'trip_list_last_month\'`

После основных страниц с регистрацией добавлены поездки.

\- Форма добавления поездки

add_trip.html:

``` python
\<h2\>Добавить новую поездку\</h2\>

\<form method=\"post\"\>

  {% csrf_token %}

  {{ form.as_p }}

  \<button type=\"submit\"\>Сохранить поездку\</button\>

\</form\>

\<a href=\"{% url \'user_profile\' %}\"\>← Назад\</a\>

forms.py:

class TripForm(forms.ModelForm):

    class Meta:

        model = Trip

        fields = \[\'car\', \'start_time\', \'end_time\'\]

        widgets = {

            \'start_time\': forms.DateTimeInput(attrs={\'type\':
\'datetime-local\'}),

            \'end_time\': forms.DateTimeInput(attrs={\'type\':
\'datetime-local\'}),

        }

    def \_\_init\_\_(self, \*args, \*\*kwargs):

        self.user = kwargs.pop(\'user\', None)

        super().\_\_init\_\_(\*args, \*\*kwargs)

        if self.user:

            self.instance.user = self.user

    def save(self, commit=True):

        trip = super().save(commit=False)

        if self.user:

            trip.user = self.user

        if commit:

            trip.save()

        return trip
```

views.py:

``` python
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from .forms import TripForm

from .models import Trip

\@login_required

def add_trip(request):

    \"\"\"Добавить новую поездку\"\"\"

    if request.method == \'POST\':

        form = TripForm(request.POST, user=request.user)

        if form.is_valid():

            form.save()

            return redirect(\'user_profile\')

    else:

        form = TripForm(user=request.user)

    return render(request, \'users/add_trip.html\', {\'form\': form})
```

urls.py:

`path(\'trip/add/\', views.add_trip, name=\'add_trip\'),`

<img width="974" height="221" alt="image" src="https://github.com/user-attachments/assets/09b070d1-9b5f-4e57-b8b0-93019c303175" />

\- Написание комментария к поездке

add_comment.html:

``` python
\<h2\>Отзыв о поездке\</h2\>

\<p\>Автомобиль: {{ trip.car.licence }}\</p\>

\<form method=\"post\"\>

  {% csrf_token %}

  \<label\>Проблемы:\</label\>

  \<textarea name=\"problems\" rows=\"3\"\>{{ trip.problems
}}\</textarea\>\<br\>

  \<label\>Комментарий:\</label\>

  \<textarea name=\"comments\" rows=\"4\"\>{{ trip.comments
}}\</textarea\>\<br\>

  \<button type=\"submit\"\>Сохранить\</button\>

\</form\>

\<a href=\"{% url \'user_profile\' %}\"\>← Назад\</a\>

views.py:

\@login_required

def add_comment(request, trip_id):

    \"\"\"Добавить комментарий к завершённой поездке\"\"\"

    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)

    if request.method == \'POST\':

        trip.comments = request.POST.get(\'comments\', \'\').strip()

        trip.problems = request.POST.get(\'problems\', \'\').strip()

        trip.save()

        return redirect(\'user_profile\')

    return render(request, \'users/add_comment.html\', {\'trip\': trip})
```

urls.py:

``` python
path(\'trip/\<int:trip_id\>/comment/\', views.add_comment,
name=\'add_comment\'),
```
<img width="974" height="257" alt="image" src="https://github.com/user-attachments/assets/75610d85-05da-4d0a-b94c-c271bf2e5c8f" />


**3 Этап. Настройка оставшихся страниц по варианту**

3.1 Добавление меню и пагинации страниц

\- Установим бутстрап: pip install django-bootstrap3

\- Реализовано меню с бутсрап

Создан файл с описанием шаблона страницы с меню навигации:

``` python
base.html:

\<!DOCTYPE html\>

\<html lang=\"ru\"\>

\<head\>

    \<meta charset=\"UTF-8\"\>

    \<meta name=\"viewport\" content=\"width=device-width,
initial-scale=1.0\"\>

    \<title\>{% block title %}Carshering{% endblock %}\</title\>

    \<!\-- Bootstrap CSS \--\>

    \<link
href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css\"
rel=\"stylesheet\"\>

    \<style\>

        body { padding-top: 56px; } /\* Отступ под фиксированную
навигацию \*/

    \</style\>

\</head\>

\<body\>

\<!\-- Навигационная панель \--\>

\<nav class=\"navbar navbar-expand-lg navbar-dark bg-primary
fixed-top\"\>

    \<div class=\"container\"\>

        \<a class=\"navbar-brand\" href=\"{% url
\'trip_list_last_month\' %}\"\>🚗 Carshering\</a\>

        \<button class=\"navbar-toggler\" type=\"button\"
data-bs-toggle=\"collapse\" data-bs-target=\"#navbarNav\"\>

            \<span class=\"navbar-toggler-icon\"\>\</span\>

        \</button\>

        \<div class=\"collapse navbar-collapse\" id=\"navbarNav\"\>

            \<ul class=\"navbar-nav me-auto\"\>

                \<li class=\"nav-item\"\>

                    \<a class=\"nav-link\" href=\"{% url
\'trip_list_last_month\' %}\"\>Все поездки\</a\>

                \</li\>

                {% if user.is_authenticated %}

                    \<li class=\"nav-item\"\>

                        \<a class=\"nav-link\" href=\"{% url
\'user_profile\' %}\"\>Мой профиль\</a\>

                    \</li\>

                    \<li class=\"nav-item\"\>

                        \<a class=\"nav-link\" href=\"{% url
\'add_trip\' %}\"\>Новая поездка\</a\>

                    \</li\>

                {% endif %}

            \</ul\>

            \<!\-- Правая часть: вход/выход \--\>

            \<ul class=\"navbar-nav\"\>

                {% if user.is_authenticated %}

                    \<li class=\"nav-item dropdown\"\>

                        \<a class=\"nav-link dropdown-toggle\"
href=\"#\" id=\"userMenu\" role=\"button\" data-bs-toggle=\"dropdown\"\>

                            {{ user.user_name\|default:user.username }}

                        \</a\>

                        \<ul class=\"dropdown-menu dropdown-menu-end\"\>

                            \<li\>\<a class=\"dropdown-item\" href=\"{%
url \'user_profile\' %}\"\>Профиль\</a\>\</li\>

                            \<li\>\<hr
class=\"dropdown-divider\"\>\</li\>

                            \<li\>

                                \<form method=\"post\" action=\"{% url
\'logout\' %}\" class=\"d-inline\"\>

                                    {% csrf_token %}

                                    \<button type=\"submit\"
class=\"dropdown-item\"\>Выйти\</button\>

                                \</form\>

                            \</li\>

                        \</ul\>

                    \</li\>

                {% else %}

                    \<li class=\"nav-item\"\>

                        \<a class=\"nav-link\" href=\"{% url \'login\'
%}\"\>Вход\</a\>

                    \</li\>

                    \<li class=\"nav-item\"\>

                        \<a class=\"nav-link\" href=\"{% url
\'register\' %}\"\>Регистрация\</a\>

                    \</li\>

                {% endif %}

            \</ul\>

        \</div\>

    \</div\>

\</nav\>

\<!\-- Основной контент \--\>

\<main class=\"container mt-4\"\>

    {% block content %}

    {% endblock %}

\</main\>

\<!\-- Bootstrap JS \--\>

\<script
src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js\"\>\</script\>

\</body\>

\</html\>
```

Затем все созданные ранее страницы были отредактированы с добавлением
данного шаблона:

``` python
{% extends \'base.html\' %}

{% block content %}

\<!\-- Основной контент \--\>

{% endblock %}
```

В результате получилась удобная навигация по сайту и дополнительный
дизайн страниц:

<img width="921" height="430" alt="image" src="https://github.com/user-attachments/assets/a2d20c2a-af10-47a5-a017-2a46d2a8da42" />

<img width="931" height="387" alt="image" src="https://github.com/user-attachments/assets/49a344eb-e5ba-45b6-a682-568699520c9b" />

<img width="974" height="382" alt="image" src="https://github.com/user-attachments/assets/468dd815-0d2c-423f-bf72-af55164c8b65" />


\- Осталось отредактировать форму ввода отзыва так, чтобы пользователь
не мог добавлять проблему, а это действие выполнял администратор в
случае, если пользователю необходимо будет оплатить штраф или ремонт
автомобиля.

<img width="974" height="414" alt="image" src="https://github.com/user-attachments/assets/4231cd48-d023-4b02-89e5-e4803569d419" />


\- Добавим bootstrap3 в INSTALLED_APPS (settings.py)

\- Используем класс TripListView для добавления функциональности главной
странице:

views.py:

```python
from django.utils import timezone

from datetime import timedelta

from .models import Trip

from django.views.generic import ListView

class TripListView(ListView):

    model = Trip

    template_name = \'carshering/trip_list.html\'

    context_object_name = \'trips\'  # имя переменной в шаблоне

    paginate_by = 10  # по 10 поездок на страницу

    def get_queryset(self):

        now = timezone.now()

        one_month_ago = now - timedelta(days=30)

        return Trip.objects.filter(

            start_time\_\_gte=one_month_ago

        ).select_related(\'user\', \'car\',
\'car\_\_model\').order_by(\'-start_time\')
```

urls.py:

```python
path(\'trips/\', views.TripListView.as_view(),
name=\'trip_list_last_month\'),

trip_list.html:

{% extends \'base.html\' %}

{% load bootstrap3 %}

{% block title %}Поездки за последний месяц{% endblock %}

{% block content %}

\<h1\>Поездки за последний месяц\</h1\>

{% if trips %}

  \<table class=\"table table-striped\"\>

    \<thead\>

      \<tr\>

        \<th\>ФИО водителя\</th\>

        \<th\>Начало\</th\>

        \<th\>Окончание\</th\>

        \<th\>Гос. номер\</th\>

        \<th\>Марка и модель\</th\>

        \<th\>Проблемы\</th\>

      \</tr\>

    \</thead\>

    \<tbody\>

      {% for trip in trips %}

      \<tr\>

        \<td\>

          {% if trip.user.first_name or trip.user.last_name %}

            {{ trip.user.first_name }} {{ trip.user.last_name }}

          {% elif trip.user.user_name %}

            {{ trip.user.user_name }}

          {% else %}

            {{ trip.user.username }}

          {% endif %}

        \</td\>

        \<td\>{{ trip.start_time\|date:\"d.m.Y H:i\" }}\</td\>

        \<td\>{{ trip.end_time\|date:\"d.m.Y H:i\" }}\</td\>

        \<td\>{{ trip.car.licence }}\</td\>

        \<td\>{{ trip.car.model.brand }} {{ trip.car.model.model_name
}}\</td\>

        \<td\>

          {% if trip.problems %}

            \<span class=\"badge bg-warning text-dark\"\>Есть\</span\>

          {% else %}

            \<span class=\"text-success\"\>Нет\</span\>

          {% endif %}

        \</td\>

      \</tr\>

      {% endfor %}

    \</tbody\>

  \</table\>

  \<!\-- Пагинация через django-bootstrap3 \--\>

  {% bootstrap_pagination page_obj %}

{% else %}

  \<p\>За последний месяц поездок не совершено.\</p\>

{% endif %}

{% endblock %}
```

Результат:

<img width="974" height="468" alt="image" src="https://github.com/user-attachments/assets/15fd8196-a75e-4869-b779-3d46c263febd" />

