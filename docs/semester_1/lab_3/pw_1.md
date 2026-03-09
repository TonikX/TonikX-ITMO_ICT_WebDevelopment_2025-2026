# Практическая работа №3.1

## Практическое задание 1

### Описание задания

Воспользуйтесь проектом из практики 2.1:

![](../img/lab_3/pw/6.png)

Напишите запрос на создание 6-7 новых автовладельцев и 5-6 автомобилей, каждому автовладельцу назначьте удостоверение и от 1 до 3 автомобилей. Задание можете выполнить либо в интерактивном режиме интерпретатора, либо в отдельном python-файле. Результатом должны стать запросы и отображение созданных объектов.

> Если вы добавляете автомобили владельцу через метод .add(), не забудьте заполнить также ассоциативную сущность “владение”

### Выполнение задания

Для создания требуемых объектов будем использовать следующий код:

```python
import random
from datetime import date, timedelta
from project_first_app.models import Owner, Car, DrivingLicense, Ownership

owners_data = [
    {
        'username': 'frolov',
        'password': '12345',
        'first_name': 'Иван',
        'last_name': 'Фролов',
        'birth_date': date(1990, 5, 15),
        'passport_number': '2847591036',
        'address': 'г. Самара, ул. Матросова, 10, кв. 2',
        'nationality': 'Русский'
    },
    {
        'username': 'zaitsev',
        'password': '12345',
        'first_name': 'Тимофей',
        'last_name': 'Зайцев',
        'birth_date': date(1985, 8, 22),
        'passport_number': '7392048165',
        'address': 'г. Казань, ул. Трактовая, 50, кв. 1',
        'nationality': 'Русский'
    },
    {
        'username': 'utkin',
        'password': '12345',
        'first_name': 'Никита',
        'last_name': 'Уткин',
        'birth_date': date(1992, 3, 10),
        'passport_number': '1503847291',
        'address': 'г. Москва, ул. Овражная, 43, кв. 1',
        'nationality': 'Татарин'
    },
    {
        'username': 'orlov',
        'password': '12345',
        'first_name': 'Леонид',
        'last_name': 'Орлов',
        'birth_date': date(1988, 11, 5),
        'passport_number': '9462173580',
        'address': 'г. Казань, ул. Октябрьская, 43, кв. 24',
        'nationality': 'Русский'
    },
    {
        'username': 'karpov',
        'password': '12345',
        'first_name': 'Степан',
        'last_name': 'Карпов',
        'birth_date': date(1995, 7, 30),
        'passport_number': '3728461059',
        'address': 'г. Тольятти, ул. Родниковая, 7, кв. 97',
        'nationality': 'Чуваш'
    },
    {
        'username': 'gorbunov',
        'password': '12345',
        'first_name': 'Иван',
        'last_name': 'Горбунов',
        'birth_date': date(1991, 12, 18),
        'passport_number': '6059138427',
        'address': 'г. Воронеж, ул. Клубная, 45, кв. 40',
        'nationality': 'Русский'
    },
    {
        'username': 'ivanov',
        'password': '12345',
        'first_name': 'Никита',
        'last_name': 'Иванов',
        'birth_date': date(1989, 2, 15),
        'passport_number': '8812345678',
        'address': 'г. Нижний Новгород, ул. Железнодорожная, 17, кв. 39',
        'nationality': 'Армянин'
    }
]

cars_data = [
    {
        'license_plate': 'А777ВС78',
        'model': 'Lada Vesta SW Cross',
        'color': 'Красный'
    },
    {
        'license_plate': 'М001АА99',
        'model': 'Haval Dargo',
        'color': 'Синий'
    },
    {
        'license_plate': 'К999ОР178',
        'model': 'BMW M240i xDrive',
        'color': 'Жёлтый'
    },
    {
        'license_plate': 'Т255НУ50',
        'model': 'Kia Stinger',
        'color': 'Красный'
    },
    {
        'license_plate': 'Е123АВ77',
        'model': 'Mazda CX-50',
        'color': 'Зелёный'
    },
    {
        'license_plate': 'В444ММ161',
        'model': 'Jeep Avenger',
        'color': 'Белый'
    },
]

driving_licenses_data = [
    {
        "license_number": "1234567890",
        "license_type": "B",
        "issue_date": date(2018, 5, 12),
    },
    {
        "license_number": "0987654321",
        "license_type": "C",
        "issue_date": date(2016, 8, 23),
    },
    {
        "license_number": "1122334455",
        "license_type": "D",
        "issue_date": date(2020, 1, 15),
    },
    {
        "license_number": "6677889900",
        "license_type": "BE",
        "issue_date": date(2019, 11, 30),
    },
    {
        "license_number": "2244668800",
        "license_type": "A",
        "issue_date": date(2022, 3, 7),
    },
    {
        "license_number": "1357924680",
        "license_type": "CE",
        "issue_date": date(2017, 9, 14),
    },
    {
        "license_number": "9876501234",
        "license_type": "M",
        "issue_date": date(2023, 6, 21),
    }
]

owners = []
for owner_data in owners_data:
    owner = Owner.objects.create_user(
        username=owner_data['username'],
        password=owner_data['password'],
        first_name=owner_data['first_name'],
        last_name=owner_data['last_name'],
        birth_date=owner_data['birth_date'],
        passport_number=owner_data['passport_number'],
        address=owner_data['address'],
        nationality=owner_data['nationality']
    )
    owners.append(owner)

cars = []
for car_data in cars_data:
    car = Car.objects.create(
        license_plate=car_data['license_plate'],
        model=car_data['model'],
        color=car_data['color']
    )
    cars.append(car)

for i, license_data in enumerate(driving_licenses_data):
    DrivingLicense.objects.create(
        owner=owners[i],
        license_number=license_data['license_number'],
        license_type=license_data['license_type'],
        issue_date=license_data['issue_date']
    )

# (<индекс_владельца> [<индексы_автомобилей>])
ownerships_plan = [
    (0, [0, 1]),
    (1, [2, 3, 4]),
    (2, [5]),
    (3, [0, 2]),
    (4, [1, 3, 4]),
    (5, [2, 5]),
    (6, [0])
]

for owner_idx, car_indices in ownerships_plan:
    owner = owners[owner_idx]
    for car_idx in car_indices:
        start_date = date.today() - timedelta(days=random.randint(1, 3650))
        days_after_start = random.randint(1, 1825)
        end_date = start_date + timedelta(days=days_after_start)
        Ownership.objects.create(
            owner=owner,
            car=cars[car_idx],
            start_date=start_date,
            end_date=end_date
        )
```

Запустим интерактивный режим:

```
python3 manage.py shell
```

Вставим написанный выше код в терминал:

![](../img/lab_3/pw/1.png)

Проверим в админ-панели, что требуемые объекты создались:

![](../img/lab_3/pw/2.png)

![](../img/lab_3/pw/3.png)

![](../img/lab_3/pw/4.png)

![](../img/lab_3/pw/5.png)

Видим, что все требуемые объекты были успешно добавлены в базу данных.

## Практическое задание 2

### Описание задания

По созданным в пр.1 данным написать следующие запросы на фильтрацию:

1. Где это необходимо, добавьте `related_name`к полям модели
2. Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)
3. Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)
4. Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)
5. Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)
6. Найти всех владельцев, чей [год владения машиной](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#year) начинается с 2010 (или любой другой год, который присутствует у вас в базе)

### Выполнение задания

#### Пункт 1

> Где это необходимо, добавьте `related_name` к полям модели

Учитывая целесообразность добавим `related_name` к следующим полям моделей:

```python
class DrivingLicense(models.Model):
    # ...
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='driving_licenses')
    # ...

class Ownership(models.Model):
    # ...
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ownerships')
    # ...

class Owner(AbstractUser):
    # ...
    cars = models.ManyToManyField('Car', through='Ownership', related_name='owners')
    # ...
```

Применим сделанные изменения к базе данных:

```
python3 manage.py makemigrations project_first_app
python3 manage.py migrate
```

![](../img/lab_3/pw/7.png)

Теперь обратную связь от целевой модели к исходной можно получить по заданным `related_name`:

```python
owner = Owner.objects.get(id=1)
licenses = owner.driving_licenses.all()

owner = Owner.objects.get(id=1)
ownerships = owner.ownerships.all()

car = Car.objects.get(car_id=1)
car_ownerships = car.ownerships.all()

car = Car.objects.get(car_id=1)
owners = car.owners.all()
```

#### Пункт 2

> Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)

Напишем соответствующий запрос:

```python
toyota_cars = Car.objects.filter(model__icontains='toyota')
print(toyota_cars)
```

Запустим этот код в shell и получим все автомобили Toyota из базы данных:

![](../img/lab_3/pw/8.png)

#### Пункт 3

> Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)

Напишем соответствующий запрос:

```python
owners = Owner.objects.filter(first_name='Олег')
print(owners)
```

Выполним его в shell:

![](../img/lab_3/pw/9.png)

#### Пункт 4

> Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)

Напишем соответствующий запрос:

```python
owner = Owner.objects.order_by('?').first()
owner_id = owner.id
driving_license = DrivingLicense.objects.filter(owner_id=owner_id)
print(driving_license)
```

Выполним его в shell:

![](../img/lab_3/pw/10.png)

#### Пункт 5

> Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)

Напишем соответствующий запрос:

```python
owners = Owner.objects.filter(cars__color='Красный').distinct()
print(owners)
```

Выполним его в shell:

![](../img/lab_3/pw/11.png)

#### Пункт 6

> Найти всех владельцев, чей [год владения машиной](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#year) начинается с 2010 (или любой другой год, который присутствует у вас в базе)

Напишем соответствующий запрос:

```python
owners = Owner.objects.filter(ownerships__start_date__year=2020).distinct()
print(owners)
```

Выполним его в shell:

![](../img/lab_3/pw/12.png)

## Практическое задание 3

### Описание задания

Необходимо реализовать следующие запросы c применением методов агрегации (`.aggregate()`), аннотации (`.annotate()`), группировки (`.values()`) и упорядочивания (`.order_by()`):

1. Вывод даты выдачи самого старшего водительского удостоверения
2. Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе
3. Выведите количество машин для каждого водителя
4. Подсчитайте количество машин каждой марки
5. Отсортируйте всех автовладельцев по дате выдачи удостоверения (Примечание: чтобы не выводить несколько раз одни и те же записи воспользуйтесь методом `.distinct()`)

### Выполнение задания

#### Пункт 1

> Вывод даты выдачи самого старшего водительского удостоверения

Напишем соответствующий запрос:

```python
from django.db.models import Min
oldest_issue = DrivingLicense.objects.aggregate(oldest_issue_date=Min('issue_date'))
oldest_issue_date = oldest_issue['oldest_issue_date']
print(oldest_issue_date)
```

Выполним его в shell:

![](../img/lab_3/pw/13.png)

#### Пункт 2

> Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе

Напишем соответствующий запрос:

```python
from django.db.models import Max
latest_end = Ownership.objects.aggregate(latest_end=Max('end_date'))['latest_end']
print(latest_end)
```

Выполним его в shell:

![](../img/lab_3/pw/14.png)

#### Пункт 3

> Выведите количество машин для каждого водителя

Напишем соответствующий запрос:

```python
from django.db.models import Count
owners_with_counts = (
    Owner.objects
    .annotate(car_count=Count('cars'))
    .values('last_name', 'first_name', 'car_count')
    .order_by('-car_count', 'last_name')
)
for row in owners_with_counts:
    print(f"{row['last_name']} {row['first_name']}: {row['car_count']}")
```

Выполним его в shell:

![](../img/lab_3/pw/15.png)

#### Пункт 4

> Подсчитайте количество машин каждой марки

Напишем соответствующий запрос:

```python
from django.db.models import Count
cars_per_model = (
    Car.objects
    .values('model')
    .annotate(count=Count('model'))
    .order_by('-count', 'model')
)
for row in cars_per_model:
    print(f"{row['model']}: {row['count']}")
```

Выполним его в shell:

![](../img/lab_3/pw/16.png)

#### Пункт 5

> Отсортируйте всех автовладельцев по дате выдачи удостоверения (Примечание: чтобы не выводить несколько раз одни и те же записи воспользуйтесь методом .distinct())

Напишем соответствующий запрос:

```python
owners_ordered = (
    Owner.objects
    .filter(driving_licenses__isnull=False)
    .order_by('driving_licenses__issue_date')
    .distinct())
print(owners_ordered)
```

Выполним его в shell:

![](../img/lab_3/pw/17.png)
