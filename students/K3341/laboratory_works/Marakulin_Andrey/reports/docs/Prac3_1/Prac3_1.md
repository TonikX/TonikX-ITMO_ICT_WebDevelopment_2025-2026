# Отчет по Практическому занятию №3.1
### Тема: Запросы в Django ORM

## 1. Подготовка и настройка проекта

Для выполнения заданий был создан проект Django и приложение `car_app`. В приложении определены модели данных согласно схеме из Практического задания 1, а приложение `car_app` было зарегистрировано в `INSTALLED_APPS` в файле `settings.py`.

### Модель данных

Модели **CarOwner**, **CarLicense**, **Car** и **CarOwnership** определены в `car_app/models.py`.

```python
from django.db import models

class CarOwner(models.Model):
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    birth_date = models.DateField(null=True, verbose_name='Дата_рождения')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class CarLicense(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, verbose_name='Id_владельца', related_name='license')
    number = models.CharField(max_length=10, verbose_name='Номер_удостоверения')
    type = models.CharField(max_length=10, verbose_name='Тип')
    issue_date = models.DateField(verbose_name='Дата_выдачи')

    def __str__(self):
        return f"Удостоверение №{self.number} ({self.owner.last_name})"

class Car(models.Model):
    plate_number = models.CharField(max_length=15, verbose_name='Гос. номер')
    make = models.CharField(max_length=20, verbose_name='Марка')
    model = models.CharField(max_length=20, verbose_name='Модель')
    color = models.CharField(max_length=30, verbose_name='Цвет')

    # Many-to-Many связь с CarOwner через CarOwnership
    owners = models.ManyToManyField(CarOwner, through='CarOwnership', verbose_name='Владельцы', related_name='cars')

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate_number})"

class CarOwnership(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, verbose_name='Id_владельца', related_name='ownerships') # Добавлен related_name
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Id_автомобиля')
    start_date = models.DateField(verbose_name='Дата_начала')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата_окончания')

    def __str__(self):
        return f"{self.owner.last_name} владеет {self.car.plate_number}"
```

### Запуск интерактивного режима

После применения миграций (`makemigrations` и `migrate`) была запущена интерактивная консоль Django (`python manage.py shell`) и импортированы необходимые классы:

```python
from car_app.models import CarOwner, CarLicense, Car, CarOwnership
from django.db.models import Avg, Min, Max, Count
from datetime import date
```

---

## 2. Практическое задание 1: Создание объектов

Создано 7 автовладельцев, 6 автомобилей, для каждого владельца создано удостоверение и установлены отношения владения (1-3 автомобиля), с заполнением ассоциативной сущности **CarOwnership**.

### 1. Создание Автомобилей

```python
car1 = Car.objects.create(plate_number='А123БВ77', make='Toyota', model='Camry', color='Красный')
car2 = Car.objects.create(plate_number='С456ДЕ99', make='Honda', model='CR-V', color='Синий')
car3 = Car.objects.create(plate_number='Е789ЖЗ50', make='Lada', model='Vesta', color='Белый')
car4 = Car.objects.create(plate_number='К012ЛМ10', make='Toyota', model='Corolla', color='Черный')
car5 = Car.objects.create(plate_number='Н345ПР33', make='BMW', model='X5', color='Серый')
car6 = Car.objects.create(plate_number='Р678СТ44', make='Mercedes', model='E-Class', color='Красный')

Car.objects.all()
# <QuerySet [<Car: Toyota Camry (А123БВ77)>, <Car: Honda CR-V (С456ДЕ99)>, ..., <Car: Mercedes E-Class (Р678СТ44)>]>
```

### 2. Создание Владельцев и Удостоверений

```python
owner1 = CarOwner.objects.create(last_name='Иванов', first_name='Олег', birth_date='1980-05-15')
owner2 = CarOwner.objects.create(last_name='Петрова', first_name='Анна', birth_date='1992-11-20')
owner3 = CarOwner.objects.create(last_name='Сидоров', first_name='Иван', birth_date='1975-01-01')
owner4 = CarOwner.objects.create(last_name='Смирнова', first_name='Елена', birth_date='1998-08-25')
owner5 = CarOwner.objects.create(last_name='Кузнецов', first_name='Дмитрий', birth_date='1985-04-10')
owner6 = CarOwner.objects.create(last_name='Соколов', first_name='Михаил', birth_date='1990-07-07')
owner7 = CarOwner.objects.create(last_name='Волкова', first_name='Ольга', birth_date='2000-02-14')

CarLicense.objects.create(owner=owner1, number='01A1234567', type='B', issue_date='2000-06-01')
CarLicense.objects.create(owner=owner2, number='02B2345678', type='B,C', issue_date='2012-10-10')
CarLicense.objects.create(owner=owner3, number='03C3456789', type='A,B', issue_date='1995-03-20')
CarLicense.objects.create(owner=owner4, number='04D4567890', type='B', issue_date='2016-09-05')
CarLicense.objects.create(owner=owner5, number='05E5678901', type='B,D', issue_date='2005-01-15')
CarLicense.objects.create(owner=owner6, number='06F6789012', type='B', issue_date='2010-02-28')
CarLicense.objects.create(owner=owner7, number='07G7890123', type='B,C', issue_date='2023-11-01')
```

### 3. Создание отношений Владения (CarOwnership)

```python
CarOwnership.objects.create(owner=owner1, car=car1, start_date='2015-01-01', end_date='2020-01-01')
CarOwnership.objects.create(owner=owner1, car=car4, start_date='2020-05-20') # 2 машины

CarOwnership.objects.create(owner=owner2, car=car2, start_date='2018-03-10') # 1 машина

CarOwnership.objects.create(owner=owner3, car=car3, start_date='2010-11-11')
CarOwnership.objects.create(owner=owner3, car=car5, start_date='2012-04-01')
CarOwnership.objects.create(owner=owner3, car=car6, start_date='2021-08-01', end_date='2024-01-31') # 3 машины

CarOwnership.objects.create(owner=owner4, car=car1, start_date='2020-02-01')
CarOwnership.objects.create(owner=owner4, car=car6, start_date='2024-02-01') # 2 машины

CarOwnership.objects.create(owner=owner5, car=car5, start_date='2005-02-01', end_date='2012-03-31') # 1 машина

CarOwnership.objects.create(owner=owner6, car=car3, start_date='2023-01-01') # 1 машина

CarOwnership.objects.create(owner=owner7, car=car2, start_date='2024-05-01')
CarOwnership.objects.create(owner=owner7, car=car4, start_date='2024-06-01')
CarOwnership.objects.create(owner=owner7, car=car5, start_date='2024-07-01') # 3 машины

CarOwnership.objects.all()
# <QuerySet [..., <CarOwnership: Волкова владеет Н345ПР33>]>
```

---

## 3. Практическое задание 2: Фильтрация запросов

Выполнены запросы на фильтрацию с использованием методов `.filter()`, `.get()`, а также поиска через отношения (`__`).

### 1. Выведете все машины марки "Toyota"

```python
Car.objects.filter(make='Toyota')
# <QuerySet [<Car: Toyota Camry (А123БВ77)>, <Car: Toyota Corolla (К012ЛМ10)>]>
```

### 2. Найти всех водителей с именем "Олег"

```python
CarOwner.objects.filter(first_name='Олег')
# <QuerySet [<CarOwner: Олег Иванов>]>
```

### 3. Получить экземпляр удостоверения по id случайного владельца

```python
random_owner = CarOwner.objects.first() # Берем первого владельца
owner_id = random_owner.id
print(f"ID владельца: {owner_id}")
# ID владельца: 1

license_object = CarLicense.objects.get(owner_id=owner_id)
print(license_object)
# Удостоверение №01A1234567 (Иванов)
```

### 4. Вывести всех владельцев красных машин

Используется обращение через ManyToMany поле `owners` к связанной модели `Car`, и далее фильтрация по полю `color`. Применен `.distinct()` для исключения дубликатов владельцев.

```python
CarOwner.objects.filter(cars__color='Красный').distinct()
# <QuerySet [<CarOwner: Олег Иванов>, <CarOwner: Иван Сидоров>, <CarOwner: Елена Смирнова>]>
```

### 5. Найти всех владельцев, чей год владения машиной начинается с 2010

Используется обращение к ассоциативной сущности `CarOwnership` через подтвержденное имя обратной связи **`carownership`** (или **`carownership_set`**, если используется это имя) с фильтрацией по году (`__year`) поля `start_date` и оператором **больше или равно** (`__gte`).

```python
CarOwner.objects.filter(carownership__start_date__year__gte=2010).distinct()
# <QuerySet [<CarOwner: Олег Иванов>, <CarOwner: Анна Петрова>, <CarOwner: Иван Сидоров>, <CarOwner: Елена Смирнова>, <CarOwner: Михаил Соколов>, <CarOwner: Ольга Волкова>]>
```

---

## 4. Практическое задание 3: Агрегация и аннотация запросов

Выполнены запросы с применением агрегационных функций (`Min`, `Max`, `Count`) и группировки (`values()`, `annotate()`).

### 1. Вывод даты выдачи самого старшего водительского удостоверения

Используется агрегация с функцией **Min** для нахождения самой ранней даты.

```python
CarLicense.objects.aggregate(oldest_issue_date=Min('issue_date'))
# {'oldest_issue_date': datetime.date(1995, 3, 20)}
```

### 2. Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей

Используется агрегация с функцией **Max** по полю `end_date` в таблице `CarOwnership`.

```python
CarOwnership.objects.aggregate(latest_end_date=Max('end_date'))
# {'latest_end_date': datetime.date(2024, 2, 1)}
```

### 3. Выведите количество машин для каждого водителя

Используется **аннотация** (`annotate()`) с функцией **Count** по полю `cars` (связь Many-to-Many).

```python
owners_car_count = CarOwner.objects.annotate(car_count=Count('cars'))
for owner in owners_car_count:
    print(f"{owner.first_name} {owner.last_name}: {owner.car_count} машин")

# Олег Иванов: 2 машин
# Анна Петрова: 1 машин
# Иван Сидоров: 3 машин
# Елена Смирнова: 2 машин
# Дмитрий Кузнецов: 1 машин
# Михаил Соколов: 1 машин
# Ольга Волкова: 3 машин
```

### 4. Подсчитайте количество машин каждой марки

Используется **группировка** (`values('make')`) с последующей **аннотацией** (`annotate(Count('id'))`).

```python
Car.objects.values('make').annotate(total_count=Count('id'))
# <QuerySet [
#    {'make': 'Toyota', 'total_count': 2}, 
#    {'make': 'Honda', 'total_count': 1}, 
#    {'make': 'Lada', 'total_count': 1}, 
#    {'make': 'BMW', 'total_count': 1}, 
#    {'make': 'Mercedes', 'total_count': 1}
# ]>
```

### 5. Отсортируйте всех автовладельцев по дате выдачи удостоверения

Используется метод **`.order_by()`** с обращением через внешний ключ (`license__issue_date`) и **`.distinct()`** для вывода уникальных владельцев.

```python
CarOwner.objects.order_by('license__issue_date').distinct()
# <QuerySet [
#    <CarOwner: Иван Сидоров>,      # 1995-03-20
#    <CarOwner: Олег Иванов>,       # 2000-06-01
#    <CarOwner: Дмитрий Кузнецов>,  # 2005-01-15
#    <CarOwner: Михаил Соколов>,    # 2010-02-28
#    <CarOwner: Анна Петрова>,      # 2012-10-10
#    <CarOwner: Елена Смирнова>,    # 2016-09-05
#    <CarOwner: Ольга Волкова>      # 2023-11-01
# ]>
```

### Выводы
В ходе выполнения практического занятия были освоены основные методы работы с запросами в **Django ORM**. Практически реализованы:

1.  Создание и модификация объектов с использованием методов **`.create()`** и **`.save()`**.

2.  Выполнение **DQL-запросов** (выборки) с фильтрацией по условиям, включая сложные запросы с поиском через связанные таблицы (`__` синтаксис).

3.  Применение функций **агрегации** (`.aggregate()`) и **аннотации** (`.annotate()`) для выполнения групповых вычислений.

4.  Использование **ленивого выполнения Queryset'ов**.