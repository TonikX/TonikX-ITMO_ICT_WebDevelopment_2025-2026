Практическое задание №3.1
---

## Цель работы
1) Научиться создавать объекты в БД через Django ORM (не через админку).  
2) Освоить выполнение запросов фильтрации (`filter`, `exclude`, `get`) и работу со связями.  
3) Освоить агрегирование/аннотацию (`aggregate`, `annotate`, `values`, `order_by`, `distinct`).

---

## Ход работы

### Запуск Django shell

#### Команда

```bash
python manage.py shell
```

![Скриншот manage.py shell](images/shell.jpg)

---

### Создание объектов

**Задача:** Создать 6–7 автовладельцев и 5–6 автомобилей. Каждому владельцу назначить удостоверение и 1–3 автомобиля.
**Примечание:** Если авто добавляются владельцу, должна заполняться ассоциативная сущность владения (`Ownership`).

```python
from datetime import date
from autos.models import Owner, Car, DriverLicense, Ownership

car1 = Car.objects.create(brand="Toyota", model="Camry", color="Red")
car2 = Car.objects.create(brand="Toyota", model="Corolla", color="Black")
car3 = Car.objects.create(brand="BMW", model="X5", color="White")
car4 = Car.objects.create(brand="Audi", model="A4", color="Red")
car5 = Car.objects.create(brand="Kia", model="Rio", color="Blue")
car6 = Car.objects.create(brand="Lada", model="Vesta", color="Gray")
```

![Скриншот 8 — create Car](images/create_cars.jpg)

---

### Создание удостоверений и создание владельцев

```python
lic1 = DriverLicense.objects.create(number="77-11-123456", issue_date=date(2011, 5, 10))
lic2 = DriverLicense.objects.create(number="77-11-223456", issue_date=date(2013, 7, 21))
lic3 = DriverLicense.objects.create(number="77-11-323456", issue_date=date(2009, 3, 2))
lic4 = DriverLicense.objects.create(number="77-11-423456", issue_date=date(2018, 11, 30))
lic5 = DriverLicense.objects.create(number="77-11-523456", issue_date=date(2010, 1, 15))
lic6 = DriverLicense.objects.create(number="77-11-623456", issue_date=date(2016, 6, 6))
lic7 = DriverLicense.objects.create(number="77-11-723456", issue_date=date(2012, 9, 9))
```
```python
own1 = Owner.objects.create(first_name="Олег", last_name="Иванов", license=lic1)
own2 = Owner.objects.create(first_name="Ирина", last_name="Петрова", license=lic2)
own3 = Owner.objects.create(first_name="Олег", last_name="Сидоров", license=lic3)
own4 = Owner.objects.create(first_name="Анна", last_name="Кузнецова", license=lic4)
own5 = Owner.objects.create(first_name="Максим", last_name="Смирнов", license=lic5)
own6 = Owner.objects.create(first_name="Денис", last_name="Орлов", license=lic6)
own7 = Owner.objects.create(first_name="Елена", last_name="Волкова", license=lic7)
```

![Скриншот 10 — create DriverLicense](images/create_licenses.jpg)

---

### Заполнение ассоциативной сущности владения

```python
Ownership.objects.create(owner=own1, car=car1, start_date=date(2015, 6, 1))
Ownership.objects.create(owner=own1, car=car5, start_date=date(2019, 4, 12))

Ownership.objects.create(owner=own2, car=car2, start_date=date(2017, 1, 20))
Ownership.objects.create(owner=own2, car=car4, start_date=date(2020, 2, 2))

Ownership.objects.create(owner=own3, car=car3, start_date=date(2010, 8, 8))

Ownership.objects.create(owner=own4, car=car6, start_date=date(2012, 12, 12))
Ownership.objects.create(owner=own4, car=car1, start_date=date(2021, 7, 7))

Ownership.objects.create(owner=own5, car=car4, start_date=date(2010, 5, 5))
Ownership.objects.create(owner=own6, car=car5, start_date=date(2014, 3, 3))
Ownership.objects.create(owner=own7, car=car2, start_date=date(2018, 8, 18))
```

![Скриншот 12 — create Owner](images/owners.jpg)

---

### Вывести все машины марки “Toyota”

```python
Car.objects.filter(brand="Toyota")
```

![Скриншот 16 — filter Toyota](images/filter1.jpg)

---

### Найти всех водителей с именем “Олег”

```python
Owner.objects.filter(first_name="Олег")
```

![Скриншот 17 — filter Owner first\_name=Олег](images/oleg.jpg)

---

### Взять случайного владельца → получить его id → по id получить удостоверение (2 запроса)

```python
rnd = Owner.objects.order_by("?").first()
rnd.id
```
```python
lic = DriverLicense.objects.get(id=rnd.license_id)
lic
```

![Скриншот 18 — random owner + id](images/18_random_owner_id.jpg)

---

### Вывести всех владельцев красных машин

```python
Owner.objects.filter(cars__color="Red").distinct()
```

![Скриншот 20 — owners of red cars](images/20_red_car_owners.jpg)

---

### Найти всех владельцев, чей год владения машиной начинается с 2010

```python
Owner.objects.filter(ownerships__start_date__year=2010).distinct()
```

![Скриншот 21 — owners start\_date year 2010](images/21_owners_year_2010.jpg)

---

### Вывод даты выдачи самого старшего водительского удостоверения

```python
DriverLicense.objects.aggregate(oldest_issue_date=Min("issue_date"))
```

![Скриншот 23 — Min(issue\_date)](screenshots/23_min_issue_date.png)

---

### Самая поздняя дата владения машиной (по существующим записям владения)

```python
Ownership.objects.aggregate(latest_ownership_date=Max("start_date"))
```

![Скриншот 24 — Max(start\_date)](images/24_max_ownership_date.jpg)

---

### Количество машин для каждого водителя

```python
Owner.objects.annotate(cars_count=Count("cars", distinct=True))\
    .values("id", "first_name", "last_name", "cars_count")
```

![Скриншот 25 — annotate Count cars per owner](images/25_cars_count_per_owner.jpg)

---

### Подсчитать количество машин каждой марки

```python
Car.objects.values("brand").annotate(cnt=Count("id")).order_by("brand")
```

![Скриншот 26 — group by brand + Count](images/26_cars_per_brand.jpg)

---

### Отсортировать всех автовладельцев по дате выдачи удостоверения (+ distinct)

```python
Owner.objects.order_by("license__issue_date").distinct()
```

![Скриншот 27 — order\_by license\_\_issue\_date + distinct](images/27_order_by_issue_date.jpg)

---

## Вывод

В ходе работы были:

* созданы модели и применены миграции;
* заполнена база данными через Django ORM в интерактивном режиме;
* выполнены запросы фильтрации по полям и по связям;
* выполнены запросы агрегации, аннотации и группировки, а также сортировка с устранением дублей через `distinct()`.