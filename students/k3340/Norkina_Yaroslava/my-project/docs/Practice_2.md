# **Часть 1.**

## Практическое задание 1: Необходимо установить Django Web framework любым доступным способом.

Установка Django Web framework средствами **командной строки** в
виртуальном окружении Python.

1.  Используя командную строку, создать папку для проекта и перейти в
    нее.

2.  Создать среду окружения (имя среды можно задать произвольно -
    tutorial-env):

<img width="442" height="259" alt="image" src="https://github.com/user-attachments/assets/ed103e90-9fd0-4e79-a5ba-1f6287b5413a" />

В результате создается каталог .venv

3.  Виртуальное окружение активировано:

<img width="974" height="126" alt="image" src="https://github.com/user-attachments/assets/6c2aaff1-9e3e-437e-ac3a-c7e315362e88" />

<img width="974" height="202" alt="image" src="https://github.com/user-attachments/assets/04e3b3a4-2714-4d38-b2aa-475f3534c246" />


4.  Установка Django

<img width="974" height="389" alt="image" src="https://github.com/user-attachments/assets/f1278d2c-ffea-40f9-96e1-6a33efeafe22" />


5.  Создать проект Django:
  -----------------------------------------------------------------------
  django-admin startproject blogfspo
  -----------------------------------------------------------------------

<img width="374" height="339" alt="image" src="https://github.com/user-attachments/assets/996bf1a2-c956-42bc-9402-ab7825660f54" />


6.  Создать приложение project_first_app:

`python manage.py startapp project_first_app`

<img width="382" height="649" alt="image" src="https://github.com/user-attachments/assets/24ccec93-532e-4c82-b4bf-a3c54b443fbd" />

## Практическое задание 2.
**Практическое задание 2.1: В проекте создать модель данных об автовладельцах в соответствии с рисунком 2.**

Указание: Таблицы и атрибуты именовать только на латинице. 

<img width="974" height="323" alt="image" src="https://github.com/user-attachments/assets/8f62238b-23ef-45f9-91db-9c8930aa054e" />


Рисунок 2. Модель данных в проекте

**Работа с моделями (Django 2)**

1.  Для описания моделей необходимо открыть файл models.py приложения и
    создать все модели.

<img width="974" height="498" alt="image" src="https://github.com/user-attachments/assets/ecb99630-cefc-4d09-bd2a-428b15ad59fd" />


2.  В **файл models.py** добавлены модели, соответствующие ER-диаграмме.
    Все модели используют **Django ORM**

<img width="974" height="311" alt="image" src="https://github.com/user-attachments/assets/a8f483d6-5096-4ed1-9f5c-e2e3b1e57033" />


3.  Выполнены миграции

Было добавлено приложение 'project_first_app' в settings.py для
корректной работы миграций в проекте:

<img width="680" height="378" alt="image" src="https://github.com/user-attachments/assets/ba5de74f-bd7c-481b-abd8-6f5925c5e2c5" />


`python manage.py makemigrations`

`python manage.py migrate`

<img width="974" height="181" alt="image" src="https://github.com/user-attachments/assets/36a6d0b6-d5e1-4f8f-b8e4-2ec6d6b9ebc8" />


<img width="974" height="483" alt="image" src="https://github.com/user-attachments/assets/ac143e6c-0ba9-4004-8d2d-c8b9eaedc957" />

Созданные миграции:

<img width="958" height="454" alt="image" src="https://github.com/user-attachments/assets/f5993343-68d4-4a2f-a8d3-489637d5c93c" />


## **Практическое задание 3:** Необходимо заполнить таблицы данными средствами админ-панели.

1.  Зарегистрировать владельца авто в админ-панели.

`from .models import Owner`

`admin.site.register(Owner)`

<img width="974" height="271" alt="image" src="https://github.com/user-attachments/assets/b78a91a8-3280-4842-8c72-d640a60822f9" />


2.  Создать суперпользователя командой:

`python manage.py createsuperuser`

<img width="974" height="329" alt="image" src="https://github.com/user-attachments/assets/630a573a-acdb-4678-9555-0c174e3aa49c" />


3.  Запустить сервер командой:

  -----------------------------------------------------------------------
  python manage.py runserver
  -----------------------------------------------------------------------

<img width="974" height="389" alt="image" src="https://github.com/user-attachments/assets/4749bbbc-a2d4-477d-beb6-66965c67c371" />


4.  Зайти в админ-панель по url-адресу (127.0.0.1:8000/admin/) и
    добавить двух владельцев автомобилей, 4 автомобиля. Далее связать
    каждого владельца минимум с тремя автомобилями, так, чтобы не было
    пересечений по датам владения и продажи.

Админ-панель:

<img width="974" height="297" alt="image" src="https://github.com/user-attachments/assets/9f3fe5d7-78d0-4d8f-b156-3ae5c7e4f5dd" />

<img width="974" height="334" alt="image" src="https://github.com/user-attachments/assets/85699964-d234-472c-a5f3-ef9242280158" />

<img width="868" height="322" alt="image" src="https://github.com/user-attachments/assets/57bd4a01-aa8f-4e47-9c98-3c48b471157e" />

<img width="866" height="392" alt="image" src="https://github.com/user-attachments/assets/9b36b0de-1fa8-4128-b351-84ac644f2bc2" />


## **Практическое задание 4:** 
### Создать в файле views.py (находится в папке приложения) представление (контроллер), который выводит из базы данных данные о владельце автомобиля. 

1.  Код представления

<img width="974" height="447" alt="image" src="https://github.com/user-attachments/assets/46b191cb-c477-4933-b280-905f912fdfef" />

2.  Создать страницу html-шаблона owner.html в папке templates (создать
    папку templates в корне проекта, если ее нигде нет, далее в
    контекстном меню папки создать html-файл). Страница должна содержать
    отображение полей переданных из контроллера. Код страницы:

<img width="974" height="350" alt="image" src="https://github.com/user-attachments/assets/e00cc954-ddbe-493b-8cab-267767f5243a" />

## **Практическое задание 5:** Работа с адресацией

1.  Создать файл адресов urls.py в папке приложения (\*\_app) (пока
    пустой). 

<img width="315" height="373" alt="image" src="https://github.com/user-attachments/assets/cd2e034f-877d-4ce9-b4d4-07e7f73b0974" />


2.  Импортировать файл urls.py приложения в проект (модифицировать файл
    urls.py в той папке, в которой хранится файл setting.py). Файл c
    кодом в приложении:
``` python
from django.urls import path

from . import views



urlpatterns = \[

    path(\'owner/\<int:owner_id\>/\', views.owner_detail,
    name=\'owner_detail\'),

\]
```

В проекте:

<img width="974" height="414" alt="image" src="https://github.com/user-attachments/assets/c5503d1d-37d8-40ee-ba98-1808b94e76c0" />


3.  При переходе по ссылке **"127.0.0.1:8000/owner/1"** получаем данные
    о водителе с id 1:

<img width="974" height="481" alt="image" src="https://github.com/user-attachments/assets/073064a1-54c4-40ad-a139-3f8cd9ed1d40" />


# *Часть 2.*

## **Практическое задание:** Правильно настроить связь между автомобилем, владением и владельцем.

1.  Для правильной настройки используется реализация связи «многие ко
    многим» через класс Ownership

<img width="974" height="619" alt="image" src="https://github.com/user-attachments/assets/f24d4ef8-2b36-44bf-bbee-ea9d46c90c9d" />


## **Практическое задание (по задаче 2): **

1\. Реализовать вывод всех владельцев функционально. Добавить данные
минимум от трех владельцах. Должны быть реализованы контроллер (views) и
шаблоны (temlates).

-   Создадим вывод всех владельцев функционально в файле views.py
``` python
def owner_list(request):

owners = Owner.objects.all()

return render(request, \'owners/owner_list.html\', {\'owners\': owners})
``` 

-   Создадим страницу html с шаблоном для функции

<img width="906" height="342" alt="image" src="https://github.com/user-attachments/assets/3137eed5-aada-4551-be64-607d4cdf0481" />


-   Получим страницу следующего содержания по ссылке
    http://127.0.0.1:8000/owners/

<img width="974" height="207" alt="image" src="https://github.com/user-attachments/assets/0a337846-e2c7-4c26-9627-f333dbbfcdb2" />


-   Добавлены еще водители

<img width="974" height="426" alt="image" src="https://github.com/user-attachments/assets/c3762346-8a98-495a-9738-6a23b10db6b6" />


-   Посмотрим список владельцев

<img width="974" height="217" alt="image" src="https://github.com/user-attachments/assets/cdeccd41-ff23-4efd-a48f-40a3449d19c4" />


2\. Реализовать вывод всех автомобилей, вывод автомобиля по id,
обновления на основе классов. Добавить данные минимум о трех
автомобилях. Должны быть реализованы контроллер (views) и шаблоны
(temlates).

-   Добавим действия с отображением автомобилей, а также обновление
    данных о них. Был изменен файл views.py

<img width="974" height="523" alt="image" src="https://github.com/user-attachments/assets/ec123b87-ab79-46c7-b3cc-1efbf8e6e00f" />

-   Далее созданы шаблоны соответствующих страниц.

/cars/car_list.html

<img width="974" height="523" alt="image" src="https://github.com/user-attachments/assets/eebfc8dd-a4b8-43c4-92c0-2002bed16d26" />


/cars/car_detail.html

<img width="974" height="281" alt="image" src="https://github.com/user-attachments/assets/bd1cd59a-935d-4a0e-90b0-e018e63a7c89" />

/cars/car_form.html

<img width="974" height="257" alt="image" src="https://github.com/user-attachments/assets/98c962a5-25cf-454c-831d-65955d4a21c7" />


-   Получились следующие страницы

<img width="974" height="200" alt="image" src="https://github.com/user-attachments/assets/d6e64769-c247-4987-94a0-bc63ac8ddb8c" />


<img width="974" height="275" alt="image" src="https://github.com/user-attachments/assets/1a46493a-204f-4b36-add7-d24188924367" />


<img width="974" height="188" alt="image" src="https://github.com/user-attachments/assets/f947e91f-92f3-4d9f-a7e0-845414f8facf" />


**Практическое задание (по задаче 3)** 

1\. Реализовать форму ввода всех владельцев функционально. Добавить
данные минимум о **еще** трех владельцах. Должны быть реализованы форма
(Form), контроллер (views) и шаблоны (temlates).

-   Добавлена форма ввода владельца

<img width="974" height="349" alt="image" src="https://github.com/user-attachments/assets/563c8d8e-9b82-45b7-aaf0-a292c5bb670d" />


-   Добавлен контроллер

<img width="974" height="547" alt="image" src="https://github.com/user-attachments/assets/2ab11fd8-9f7b-43af-be15-de730b680cb7" />


-   Создан шаблон /owners/owner_form.html

-   Происходит успешное добавление владельца:

<img width="974" height="395" alt="image" src="https://github.com/user-attachments/assets/802d9536-7b2c-47e1-9b84-65d5bf1956cf" />


<img width="974" height="230" alt="image" src="https://github.com/user-attachments/assets/dbc06516-c0db-4b59-8ac0-27bab2f114ed" />


-   Были добавлены еще 3 владельца автомобилей

<img width="974" height="280" alt="image" src="https://github.com/user-attachments/assets/1fbcef55-dd23-4f43-8e09-3afce18a270b" />


Которые корректно отображаются в режиме администратора:

<img width="974" height="502" alt="image" src="https://github.com/user-attachments/assets/4212effe-8b8f-48b5-829a-4dda665e11ab" />

2\. Реализовать форму ввода, обновления и удаления всех автомобилей на
основе классов. Добавить данные минимум о **еще** трех автомобилях.
Должны быть реализованы форма (Form), контроллер (views) и шаблоны
(temlates).

-   Добавление и удаление авто

<img width="974" height="453" alt="image" src="https://github.com/user-attachments/assets/ebb1a06b-326d-44a3-95e0-751eb2c21027" />

-   Создан шаблон удаления для авто

/cars/car_confirm_delete.html

<img width="974" height="419" alt="image" src="https://github.com/user-attachments/assets/21e227e6-5e2e-4082-9565-bc9611a4772f" />


-   urls.py приложения:
``` python
\# vehicles/urls.py

from django.urls import path

from . import views

urlpatterns = \[

    \# Владельцы --- функциональные представления

    path(\'owners/\', views.owner_list, name=\'owner_list\'),

    path(\'owners/create/\', views.owner_create, name=\'owner_create\'),

    \# Автомобили --- классовые представления

    path(\'cars/\', views.CarListView.as_view(), name=\'car_list\'),

    path(\'cars/\<int:pk\>/\', views.CarDetailView.as_view(),
name=\'car_detail\'),

    path(\'cars/create/\', views.CarCreateView.as_view(),
name=\'car_create\'),

    path(\'cars/\<int:pk\>/update/\', views.CarUpdateView.as_view(),
name=\'car_update\'),

    path(\'cars/\<int:pk\>/delete/\', views.CarDeleteView.as_view(),
name=\'car_delete\'),

\]
```
-   Работоспособность удаления

<img width="974" height="221" alt="image" src="https://github.com/user-attachments/assets/8745f3ef-17a7-407c-9490-e9766ee84567" />


<img width="974" height="200" alt="image" src="https://github.com/user-attachments/assets/33d028e2-8252-42ab-b112-92fdf4f19c5e" />


<img width="974" height="364" alt="image" src="https://github.com/user-attachments/assets/914a0d64-8afd-4e57-9016-e97e065893da" />


# **Часть 3.**

Это стратегия использования новой модели пользователя, которая
отнаследована от AbstractUser. Требует особой осторожности и изменения
настроек в settings.py. В идеале должно быть сделано в начале проекта,
так как будет существенно влиять на схему базы данных.

 

## **Практическое задание:** 
### сделать "Владельца автомобиля" пользователем и расширить модель пользователя его атрибутами, так, чтобы о нем хранилась следующая информация: 

-   номер паспорта;

-   домашний адрес;

-   национальность. 

Отобразить новые поля пользователя в Django Admin. Отредактировать код
из предыдущих работ, так, чтобы выводилась информация о пользователях.

Реализовать интерфейс создания пользователя с новыми атрибутами.

-   В ходе выполнения практического задания применяется расширение
    AbstractUser, которое используется для класса Owner, чтобы сделать
    владельца автомобиля пользователем и позволить хранение
    дополнительной информации о нем. Для начала создается расширенная
    модель пользователя c новыми полями по заданию.

<img width="974" height="470" alt="image" src="https://github.com/user-attachments/assets/5f941ab5-eb7f-4ac4-a915-14affa5db0af" />


-   Затем необходимо добавить переменную в файл settings.py
``` python
\# AbstractUser class User

AUTH_USER_MODEL = \'project_first_app.User\'
```

-   Далее добавляем соответствующие изменения в models.py, где
    необходимо сделать импорт настроек из settings.py и заменить
    использование класса Owner на переменную settings.AUTH_USER_MODEL
    (класс Owner удаляется)

-   Также необходимо настроить администрирование нового класса:
    admin.py. Кроме добавления класса из .models, создается специальный
    класс CustomUserAdmin. Он нужен, чтобы новые поля отображались в
    роли администратора, можно было создавать и редактировать
    пользователей с этими полями, а также сохранялась вся стандартная
    функциональность (UserAdmin),
``` python
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import User

from .models import DriverLicense

from .models import Car

from .models import Ownership

admin.site.register(DriverLicense)

admin.site.register(Car)

admin.site.register(Ownership)

\@admin.register(User)

class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (

        (\'Личные данные\', {\'fields\': (\'birth_date\',)}),

        (\'Паспортные данные\', {\'fields\': (\'passport_number\',
\'home_address\', \'nationality\')}),

    )

    add_fieldsets = UserAdmin.add_fieldsets + (

        (\'Личные данные\', {\'fields\': (\'first_name\', \'last_name\',
\'birth_date\')}),

        (\'Паспортные данные\', {\'fields\': (\'passport_number\',
\'home_address\', \'nationality\')}),

    )

    list_display = (\'username\', \'first_name\', \'last_name\',
\'birth_date\', \'passport_number\')
```

-   Следующим изменением в старом проекте будет удаление файла миграций,
    базы данных и создание новых миграций.

`python manage.py makemigrations`

<img width="974" height="119" alt="image" src="https://github.com/user-attachments/assets/1de85d2c-cb0f-4790-92ce-f6e96180b63e" />


`python manage.py migrate`

<img width="974" height="405" alt="image" src="https://github.com/user-attachments/assets/c1222e92-9549-4469-b624-abdbcf54a21f" />


Также заново создается суперпользователь

`python manage.py createsuperuser`

<img width="974" height="217" alt="image" src="https://github.com/user-attachments/assets/558628a6-af27-44dc-9f49-058ea527d624" />


-   Получилось запустить сервер и зайти как администратор:

<img width="974" height="317" alt="image" src="https://github.com/user-attachments/assets/6fcf38bc-5c73-45b8-a4d3-4cb695d7a2ab" />


Необходимо добавить данные в базу, чтобы протестировать формы ввода и
посмотра данных.

<img width="974" height="225" alt="image" src="https://github.com/user-attachments/assets/70fa1ba0-2143-4faa-807e-8a08ae28f567" />


-   Последними шагами было отредактировать страницы вывода информации о
    владельце (теперь пользователе), файла views.py и urls.py для
    корректного отображения информации из нового класса базы данных. Был
    получен следующий вывод информации о владельце автомобиля по его ID:
<img width="974" height="386" alt="image" src="https://github.com/user-attachments/assets/d7a0114a-05f0-4391-8ecd-b6b41a62e834" />

