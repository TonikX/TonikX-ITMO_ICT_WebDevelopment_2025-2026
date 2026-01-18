# Лабораторная 3

### Задание:
Реализовать модель базы данных средствами DjangoORM (согласовать с преподавателем на консультации).
1. Реализовать логику работу API средствами Django REST Framework (используя  методы сериализации).

2. Подключить регистрацию / авторизацию по токенам / вывод информации о текущем пользователе средствами Djoser.

3. Выполнить практическую работу 3.1 по оформлению документации (в процессе разработки)

4. Реализовать документацию, описывающую работу всех используемых endpoint-ов из пункта 3 и 4 средствами Read the Docs или MkDocs.

### Задание варианта: 
- Создать программную систему, предназначенную для администратора гостиницы.

Работа с системой предполагает получение следующей информации:
- о клиентах, проживавших в заданном номере, в заданный период времени
- о количестве клиентов, прибывших из заданного города
- о том, кто из служащих убирал номер указанного клиента в заданный день недели
- сколько в гостинице свободных номеров
- список клиентов с указанием места жительства, которые проживали в те же дни, что и заданный клиент, в определенный период времени

Администратор должен иметь возможность выполнить следующие операции:
- принять на работу или уволить служащего гостиницы
- изменить расписание работы служащего
- поселить или выселить клиента

Необходимо предусмотреть также возможность автоматической выдачи отчета о работе гостиницы за указанный квартал текущего года. Такой отчет должен содержать следующие сведения:
- число клиентов за указанный период в каждом номере
- количество номеров на каждом этаже
- общая сумма дохода за каждый номер
- суммарный доход по всей гостинице

### Выполнение работы 


Модель базы данных средствами DjangoORM
![](1.png)
`models.py`
```python
from django.db import models


class RoomType(models.Model):
    """
    Тип номера
    """
    room_types = (
       ('1', '1-местный'),
       ('2', '2-местный'),
       ('3', '3-местный'),
    )
    room_type = models.CharField(max_length=1, choices=room_types, verbose_name='Тип номера')
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
       return f'мест: {self.room_type}, цена {self.price}'


class Rooms(models.Model):
    """
    Номера в отеле
    """
    id_room_type = models.ForeignKey('RoomType',  verbose_name='Номер отеля', on_delete=models.CASCADE, related_name='rooms')
    room_number = models.IntegerField(verbose_name='Номер комнаты')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона', unique=True)
    floor = models.IntegerField(verbose_name='Этаж')

    def __str__(self):
        return f'комната: {self.room_number}, телефон: {self.phone_number}, этаж: {self.floor}'


class Residents(models.Model):
    """
    Проживающие гостиницы
    """

    passport_number = models.CharField(max_length=30, verbose_name='Номер паспорта')
    name = models.CharField(max_length=30, verbose_name='Имя')
    surname = models.CharField(max_length=30, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=30, verbose_name='Отчество')
    city = models.CharField(max_length=40, verbose_name='Город')

    def __str__(self):
       return f'Проживающий: {self.name} {self.surname} {self.patronymic}'


class Reservation(models.Model):
    """
    Бронирование номера
    """

    residents = models.ManyToManyField('Residents', related_name='reservations')
    rooms = models.ManyToManyField('Rooms', related_name='reservations')
    start_date = models.DateField(verbose_name='Дата заезда', null=True, blank=True)
    end_date = models.DateField(verbose_name='Дата выезда', null=True, blank=True)

    def __str__(self):
        return f"Бронирование {self.id} c {self.start_date} по {self.end_date}"


class Workers(models.Model):
    """
    Работники гостиницы
    """

    name = models.CharField(max_length=30, verbose_name='Имя')
    surname = models.CharField(max_length=30, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=30, verbose_name='Отчество')
    is_employed = models.BooleanField(verbose_name="Трудоустроен", null=True, blank=True)

    def __str__(self):
       return f'Работник: {self.name} {self.surname} {self.patronymic}'


class CleaningInformation(models.Model):
    """
    Информация об уборке номеров
    """

    week_days = (('mon', 'monday'),
                 ('tue', 'tuesday'),
                 ('wed', 'wednesday'),
                 ('thu', 'thursday'),
                 ('fri', 'friday'),
                 ('sat', 'saturday'),
                 ('sun', 'sunday'))
    id_worker = models.ForeignKey('Workers', related_name='cleaning_information', on_delete=models.CASCADE)
    week_day = models.CharField(max_length=3, choices=week_days, verbose_name='День недели')
    floor = models.IntegerField(verbose_name='Этаж')

    def __str__(self):
        return f'{self.id_worker} {self.week_day} {self.floor}'


class Cleaning(models.Model):
    """
    Фактическая уборка номера
    """

    worker = models.ForeignKey('Workers', on_delete=models.CASCADE, related_name='cleanings')
    room = models.ForeignKey('Rooms', on_delete=models.CASCADE, related_name='cleanings')
    cleaning_date = models.DateTimeField(verbose_name='Дата уборки')


    def __str__(self):
        return f"Уборка комнаты {self.room.room_number} работником {self.worker} в {self.cleaning_date}"

```


Созданы APIViews для классов: 

![](swagger_1.png)

![](swagger_2.png)

Запросы: 
![](reservations_get.png)
![](reservations_patch.png)
![](reservations_post.png)
![](reservations_del.png)

![](residents_get.png)
![](residents_post.png)
![](residents_patch.png)
![](residents_delete.png)

![](rooms_post.png)
![](rooms_get.png)
![](rooms_put.png)
![](rooms_del.png)

![](room_types_get.png)
![](room_types_get1.png)
![](room_types_patch.png)

![](workers_get.png)
![](workers_patch.png)
![](workers_post.png)

![](cleaning_get.png)
![](cleaning_del.png)
![](cleaning_post.png)

![](cleaning_info_get.png)
![](cleaning_info_del.png)
![](cleaning_info_post.png)
![](cleaning_info_put.png)



### Запросы

![](swagger_3.png)

**О клиентах, проживавших в заданном номере, в заданный период времени**

Запрос: http://127.0.0.1:8000/clients/?room_number=104&start_date=2020-01-01&end_date=2025-12-12

Ответ:
![](2.png)

**О количестве клиентов, прибывших из заданного города**

Запрос: http://127.0.0.1:8000/from_city/?city=vdk

Ответ:
![](3.png)


**О том, кто из служащих убирал номер указанного клиента в заданный день недели**

Запрос: http://127.0.0.1:8000/cleaing_staff/?id_client=3&week_day=wed

Ответ:
![](4.png)

**Сколько в гостинице свободных номеров**

Запрос: http://127.0.0.1:8000/available_rooms/

Ответ:
![](5.png)

**Список клиентов с указанием места жительства, которые проживали в те же дни, что и заданный клиент, в определенный период времени**

Запрос: http://127.0.0.1:8000/clients_with_city/?id_client=3&start_date=2010-01-01&end_date=2027-01-01

Ответ:
![](6.png)

**Выдача отчета**

Запрос: http://127.0.0.1:8000/report/?year=2025&quarter=1

Ответ:
![](7.png)

### Djoser

Добавляем в `urls.py` 
```python
path('auth/', include('djoser.urls')),
path('auth/', include('djoser.urls.authtoken')),
```

И в `settings.py`

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken', 
    'djoser',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication', 
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
```

![](11.png)
![](12.png)
![](13.png)
