# Лабораторная работа №3 Реализация серверной части на django rest. Документирование API.

**Студент:** Шукалов Андрей Денисович  
**Университет:** ИТМО  
**Группа:** К3339 

---

* БД: Создать программную систему, предназначенную для администратора гостиницы.


## Модель Room
Модель для хранения информации о номерах в гостинице.

* `number` Номер комнаты
* `price` Стоимость за сутки
* `room_type` Тип номера
* `floor` Этаж, на котором расположен номер
* `phone` Номер телефона для связи с номером

```python
class Room(models.Model):
    TYPES_OF_ROOMS = [('single', 'Одноместный'), ('tuple', 'Двухместный'), ('triple','Трехместный')]

    number = models.PositiveIntegerField(unique=True, verbose_name='Номер комнаты')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость за сутки')
    room_type = models.CharField(max_length=10, choices=TYPES_OF_ROOMS, verbose_name="Тип номера")
    floor = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Этаж')
    phone = models.CharField(max_length=15, verbose_name='Телефон')

    def __str__(self):
        return f"Комната {self.number} ({self.get_room_type_display()})"
```

## Модель Client
Модель для хранения информации о клиентах.

* `passport_number` Номер паспорта клиента
* `first_name` Имя клиента
* `last_name` Фамилия клиента
* `middle_name` Отчество клиента
* `city_of_origin` Город, из которого прибыл клиент
* `check_in_date` Дата заезда клиента в гостиницу
* `check_out_date` Дата выезда клиента из гостиницы.
* `room` Внешний ключ, указывающий на номер, в котором проживает клиент


```python
class Client(models.Model):
    passport_number = models.CharField(max_length=20, verbose_name="Номер паспорта")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Отчество")
    city_of_origin = models.CharField(max_length=100, verbose_name="Город проживания")
    check_in_date = models.DateField(verbose_name="Дата заезда")
    check_out_date = models.DateField(verbose_name='Дата уезда', null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="clients", verbose_name="Номер")

    class Meta:
        unique_together = ('passport_number', 'check_in_date')

    def __str__(self):
        return f"{self.middle_name} {self.first_name} {self.last_name} ({self.passport_number})"
```


## Модель Employee
Модель для хранения информации о сотрудниках гостиницы.

* `first_name` Имя сотрудника
* `last_name` Фамилия сотрудника
* `middle_name` Отчество сотрудника
* `add_date` Дата принятия сотрудника на работу
* `delete_date` Дата увольнения сотрудника
* `dismissed` Флаг, указывающий на то, уволен ли сотрудник

```python
class Employee(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Отчество")
    add_date = models.DateField(verbose_name='Дата приема на работу')
    delete_date = models.DateField(verbose_name='Дата увольнения', null=True, blank=True)
    dismissed = models.BooleanField('Уволен', default=False)
    def __str__(self):
        return f"{self.middle_name} {self.first_name} {self.last_name}"
```

## Модель CleaningSchedule
Модель для расписания уборки номеров.

* `employee` Связь с моделью `Employee`, указывающая на сотрудника
* `day_of_week` День недели
* `floor` Этаж, на котором будет проведена уборка

```python
class CleaningSchedule(models.Model):

DAYS_OF_WEEK = [
    (1, 'Понедельник'),
    (2, 'Вторник'),
    (3, 'Среда'),
    (4, 'Четверг'),
    (5, 'Пятница'),
    (6, 'Суббота'),
    (7, 'Воскресенье'),
]

employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="cleaning_schedules", verbose_name="Работник")
day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, verbose_name='День недели')
floor = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Этаж')

def __str__(self):
    return f"{self.employee} - {self.floor} - {self.day_of_week}"
```

# Endpoints

## Room Endpoints

### **GET|POST api/rooms/**

Возвращает список всех номеров в гостинице и позволяет добавить новый.


### **GET api/rooms/room_history/**

Возвращает информацию о клиентах, проживавших в заданном номере в заданный период времени.

**Параметры:**

* `room_number`: Номер комнаты (обязательный параметр).
* `start`: Начало периода (в формате YYYY-MM-DD).
* `end`: Конец периода (в формате YYYY-MM-DD).


### **GET /rooms/free_rooms/**

Возвращает количество свободных номеров в гостинице на определённый период времени.

**Параметры:**

* `start`: Начало периода (в формате YYYY-MM-DD).
* `end`: Конец периода (в формате YYYY-MM-DD).

Так как используется `ModelViewSet`, то PUT | PATCH | DELETE | GET Обрабатываются на эндпоинте **api/cleaning_schedules/{id}/** 

## Clients Endpoint

### **GET | POST /clients/**

Возвращает список всех клиентов в гостинице, а так же позволяет добавить новых

### **GET /clients/clients_town_count/**

Возвращает количество клиентов, прибывших из заданного города.

**Параметры:**

* `town`: Город происхождения клиента (обязательный параметр).

### **GET /clients/{pk}/same_clients/**

Возвращает список клиентов, которые проживали в те же дни, что и указанный клиент.

Так как используется `ModelViewSet`, то PUT | PATCH | DELETE | GET Обрабатываются на эндпоинте **api/cleaning_schedules/{id}/** 

## Employees Endpoint

### **GET | POST /employees/**

Возвращает список всех сотрудников гостиницы и позволяет добавить новых.

### Так как используется `ModelViewSet`, то PUT|PATCH|DELETE|GET Обрабатываются на эндпоинте **api/employees/{id}/** 

## **Cleaning Schedule Endpoint**

### **GET | POST /cleaning_schedules/**

Возвращает расписание работников, которые бираются на этажах

### **GET /cleaning_schedules/cleaning_schedule/**

Возвращает информацию о том, кто из служащих убирал номер указанного клиента в заданный день недели.

**Параметры:**

* `day`: День недели (обязательный параметр, от 1 до 7).


Так как используется `ModelViewSet`, то PUT | PATCH | DELETE | GET Обрабатываются на эндпоинте **api/cleaning_schedules/{id}/** 

## Auth Endpoints

### **POST /api/auth/users/** 

Регистрация нового пользователя

### **POST /api/auth/users/**

Получение токена пользователем

### **GET /api/auth/users/me/**

Информация о текущем пользователе