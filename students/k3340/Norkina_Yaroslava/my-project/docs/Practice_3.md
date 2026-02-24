Практическая работа №3.

**Реализация серверной части на django rest. Документирование API.**

Часть 1.

Цель работы: получить представление о работе с запросами в Django ORM.

**Практическое задание 1:** 

Воспользуйтесь проектом из практики 2.1: <img width="866" height="285" alt="image" src="https://github.com/user-attachments/assets/b832ba84-39cc-4f45-8544-1a40ba0d0ae5" />


Напишите запрос на создание 6-7 новых автовладельцев и 5-6 автомобилей, каждому автовладельцу назначьте удостоверение и от 1 до 3 автомобилей. Задание можете выполнить либо в интерактивном режиме интерпретатора, либо в отдельном python-файле. Результатом должны стать запросы и отображение созданных объектов. 

_Если вы добавляете автомобили владельцу через метод .add(), не забудьте заполнить также ассоциативную сущность “владение”_

Реализация:

1.  Создадим новый проект Django и скопируем в него файлы практической работы №2.

django-admin startproject django\_project\_norkina

<img width="493" height="254" alt="image" src="https://github.com/user-attachments/assets/de6583e1-b12f-44f5-aa10-e44ce004f0ea" />


1.  Перейдем в интерактивный режим

python manage.py shell

<img width="950" height="168" alt="image" src="https://github.com/user-attachments/assets/922e7cfc-8e13-43be-b0af-158f34731fb1" />

1.  Сделаем импорт необходимых по задания моделей

from project\_first\_app.models import User, DriverLicense, Car, Ownership

from django.utils import timezone

from datetime import datetime, timedelta

<img width="974" height="199" alt="image" src="https://github.com/user-attachments/assets/d91cd663-9e10-47ea-9a5e-26d7f6cf4d66" />

1.  Создаем пользователей через менеджер create\_user (для корректного хранения пароля)

users = \[\]

user1 = User.objects.create\_user(

username='ivanov',

email='ivanov@example.com',

password='password123',

first\_name='Иван',

last\_name='Иванов',

birth\_date=datetime(1990, 5, 15)

)

users.append(user1)

user2 = User.objects.create\_user(

username='petrov',

email='petrov@example.com',

password='password123',

first\_name='Петр',

last\_name='Петров',

birth\_date=datetime(1985, 8, 22)

)

users.append(user2)

user3 = User.objects.create\_user(

username='sidorov',

email='sidorov@example.com',

password='password123',

first\_name='Олег',

last\_name='Сидоров',

birth\_date=datetime(1992, 3, 10)

)

users.append(user3)

user4 = User.objects.create\_user(

username='smirnov',

email='smirnov@example.com',

password='password123',

first\_name='Анна',

last\_name='Смирнова',

birth\_date=datetime(1988, 11, 5)

)

users.append(user4)

user5 = User.objects.create\_user(

username='kuznetsov',

email='kuznetsov@example.com',

password='password123',

first\_name='Дмитрий',

last\_name='Кузнецов',

birth\_date=datetime(1995, 7, 18)

)

users.append(user5)

user6 = User.objects.create\_user(

username='vasilieva',

email='vasilieva@example.com',

password='password123',

first\_name='Елена',

last\_name='Васильева',

birth\_date=datetime(1991, 12, 30)

)

users.append(user6)

user7 = User.objects.create\_user(

username='morozov',

email='morozov@example.com',

password='password123',

first\_name='Сергей',

last\_name='Морозов',

birth\_date=datetime(1987, 4, 25)

)

users.append(user7)

print("Создано пользователей:", len(users))

<img width="974" height="501" alt="image" src="https://github.com/user-attachments/assets/5f2f4e58-d3e2-421d-af04-5394c527587c" />


1.  Создаем автомобили через менеджер create\_user

cars = \[\]

car1 = Car.objects.create(

plate\_number='А123ВС77',

brand='Toyota',

model='Camry',

color='Красный'

)

cars.append(car1)

car2 = Car.objects.create(

plate\_number='В456ДЕ77',

brand='Toyota',

model='Corolla',

color='Синий'

)

cars.append(car2)

car3 = Car.objects.create(

plate\_number='К789ЕМ77',

brand='BMW',

model='X5',

color='Черный'

)

cars.append(car3)

car4 = Car.objects.create(

plate\_number='М101ОР77',

brand='Audi',

model='A4',

color='Белый'

)

cars.append(car4)

car5 = Car.objects.create(

plate\_number='О202СТ77',

brand='Lada',

model='Vesta',

color='Серый'

)

cars.append(car5)

car6 = Car.objects.create(

plate\_number='Р303УК77',

brand='Honda',

model='Civic',

color='Зеленый'

)

cars.append(car6)

print("Создано автомобилей:", len(cars))

<img width="617" height="453" alt="image" src="https://github.com/user-attachments/assets/75789496-2b50-4ec6-90fb-a96a238cb136" />


1.  Создание водительских удостоверений для каждого пользователя

licenses = \[\]

license1 = DriverLicense.objects.create(

owner=user1,

license\_number='1234567890',

license\_type='B',

issue\_date=datetime(2015, 6, 10)

)

licenses.append(license1)

license2 = DriverLicense.objects.create(

owner=user2,

license\_number='2345678901',

license\_type='B',

issue\_date=datetime(2016, 8, 15)

)

licenses.append(license2)

license3 = DriverLicense.objects.create(

owner=user3,

license\_number='3456789012',

license\_type='B',

issue\_date=datetime(2017, 3, 20)

)

licenses.append(license3)

license4 = DriverLicense.objects.create(

owner=user4,

license\_number='4567890123',

license\_type='B',

issue\_date=datetime(2018, 11, 25)

)

licenses.append(license4)

license5 = DriverLicense.objects.create(

owner=user5,

license\_number='5678901234',

license\_type='B',

issue\_date=datetime(2019, 7, 5)

)

licenses.append(license5)

license6 = DriverLicense.objects.create(

owner=user6,

license\_number='6789012345',

license\_type='B',

issue\_date=datetime(2020, 12, 15)

)

licenses.append(license6)

license7 = DriverLicense.objects.create(

owner=user7,

license\_number='7890123456',

license\_type='B',

issue\_date=datetime(2021, 4, 30)

)

licenses.append(license7)

print("Создано удостоверений:", len(licenses))

<img width="974" height="401" alt="image" src="https://github.com/user-attachments/assets/9dc0510e-37fb-4563-94cc-b00dd0aa34b1" />


1.  Создание владений автомобилями для всех пользователей

\# Владения для пользователя 1 (2 автомобиля)

ownership1\_1 = Ownership.objects.create(

owner=user1,

car=car1,

start\_date=datetime(2020, 1, 15),

end\_date=datetime(2023, 1, 15)

)

ownership1\_2 = Ownership.objects.create(

owner=user1,

car=car2,

start\_date=datetime(2021, 3, 20),

end\_date=None # Текущее владение

)

\# Владение для пользователя 2 (1 автомобиль)

ownership2\_1 = Ownership.objects.create(

owner=user2,

car=car3,

start\_date=datetime(2019, 5, 10),

end\_date=None

)

\# Владения для пользователя 3 (3 автомобиля)

ownership3\_1 = Ownership.objects.create(

owner=user3,

car=car4,

start\_date=datetime(2018, 8, 12),

end\_date=datetime(2022, 8, 12)

)

ownership3\_2 = Ownership.objects.create(

owner=user3,

car=car5,

start\_date=datetime(2020, 9, 5),

end\_date=None

)

ownership3\_3 = Ownership.objects.create(

owner=user3,

car=car1,

start\_date=datetime(2022, 11, 20),

end\_date=None

)

\# Владения для пользователя 4 (2 автомобиля)

ownership4\_1 = Ownership.objects.create(

owner=user4,

car=car6,

start\_date=datetime(2021, 2, 14),

end\_date=None

)

ownership4\_2 = Ownership.objects.create(

owner=user4,

car=car2,

start\_date=datetime(2019, 6, 30),

end\_date=datetime(2021, 6, 30)

)

\# Владение для пользователя 5 (1 автомобиль)

ownership5\_1 = Ownership.objects.create(

owner=user5,

car=car3,

start\_date=datetime(2022, 4, 18),

end\_date=None

)

\# Владения для пользователя 6 (2 автомобиля)

ownership6\_1 = Ownership.objects.create(

owner=user6,

car=car4,

start\_date=datetime(2020, 11, 5),

end\_date=None

)

ownership6\_2 = Ownership.objects.create(

owner=user6,

car=car5,

start\_date=datetime(2018, 12, 20),

end\_date=datetime(2020, 12, 20)

)

\# Владения для пользователя 7 (3 автомобиля)

ownership7\_1 = Ownership.objects.create(

owner=user7,

car=car6,

start\_date=datetime(2019, 3, 10),

end\_date=None

)

ownership7\_2 = Ownership.objects.create(

owner=user7,

car=car1,

start\_date=datetime(2021, 7, 22),

end\_date=None

)

ownership7\_3 = Ownership.objects.create(

owner=user7,

car=car2,

start\_date=datetime(2017, 9, 15),

end\_date=datetime(2019, 9, 15)

)

print("Создано владений:", Ownership.objects.count())

<img width="974" height="371" alt="image" src="https://github.com/user-attachments/assets/5bd931df-8f45-452d-96f2-d2898a178529" />


1.  Проверим корректность добавленных объектов:

Проверка пользователей.

print("\\n=== Пользователи ===")

for user in User.objects.all()\[:11\]:

print(f"{user.last\_name} {user.first\_name} - {user.username}")

<img width="824" height="387" alt="image" src="https://github.com/user-attachments/assets/d7418e4f-3846-4db8-b235-df60c7a2322c" />


Проверка автомобилей.

print("\\n=== Автомобили ===")

for car in Car.objects.all():

    print(f"{car.brand} {car.model} ({car.color}) - {car.plate\_number}")

<img width="835" height="373" alt="image" src="https://github.com/user-attachments/assets/629e6351-9e4b-446a-ab20-b7eb6dca5330" />


Проверка удостоверений.

print("\\n=== Водительские удостоверения ===")

for license in DriverLicense.objects.all():

    print(f"{license.owner.last\_name} {license.owner.first\_name} - {license.license\_number} ({license.license\_type})")

<img width="924" height="256" alt="image" src="https://github.com/user-attachments/assets/3f47440a-77ac-4663-b707-6db62a58e37b" />


Проверка владений.

print("\\n=== Владения автомобилями ===")

for ownership in Ownership.objects.all()\[:10\]:  _\# Только первые 10_

    end\_date = ownership.end\_date.date() if ownership.end\_date else "Сейчас"

    print(f"{ownership.owner.last\_name} владеет {ownership.car.brand} {ownership.car.model} с {ownership.start\_date.date()} по {end\_date}")

<img width="578" height="258" alt="image" src="https://github.com/user-attachments/assets/5de3a0ea-7b19-4737-aae6-290697932ba2" />


**Практическое задание 2:** 

По созданным в пр.1 данным написать следующие запросы на фильтрацию:

Выполнение задания:

Для начала в интерактивном режиме shell сделаем импорт необходимых по задания моделей.

from project\_first\_app.models import User, DriverLicense, Car, Ownership

from django.utils import timezone

from datetime import datetime

*   Были добавлены related\_name к полям модели
*   Вывод всех машин марки “Toyota”

toyota\_cars = Car.objects.filter(brand='Toyota')

print("\\n Все автомобили Toyota")

for car in toyota\_cars:

    print(f"{car.brand} {car.model} ({car.color}) - {car.plate\_number}")

Результат:

<img width="974" height="295" alt="image" src="https://github.com/user-attachments/assets/ccdd378b-a369-40ec-93fb-5cb7cd784771" />


*   Найдем всех водителей с именем “Олег”

oleg\_drivers = User.objects.filter(first\_name='Олег')

print("\\n Все водители с именем Олег ")

for driver in oleg\_drivers:

    print(f"{driver.last\_name} {driver.first\_name} - {driver.username}")

Результат применения фильтрации:

<img width="974" height="261" alt="image" src="https://github.com/user-attachments/assets/ca0b597a-a22c-422b-af96-00afbffac197" />


*   Взяв любого случайного владельца, получим его id:

first\_owner = User.objects.first()

owner\_id = first\_owner.id

print(f"\\n Владелец: { first\_owner.last\_name} { first\_owner.first\_name} (ID: {owner\_id}) ")

Вывод:

<img width="974" height="165" alt="image" src="https://github.com/user-attachments/assets/c8e08622-7579-4fa5-9672-3d9160356663" />


Предварительно создадим объект «водительские права» для данного пользователя, если они еще не были добавлены в бд:

license8 = DriverLicense.objects.create(

owner= User.objects.first(),

license\_number='7890000456',

license\_type='B',

issue\_date=datetime(2021, 4, 30)

)

Далее по id получим экземпляр удостоверения в виде объекта модели.

license = DriverLicense.objects.filter(owner\_id=owner\_id).first()

print(f"Удостоверение через фильтрацию: {license.license\_number}")

Результат:

<img width="974" height="219" alt="image" src="https://github.com/user-attachments/assets/549ba738-21a5-438c-962e-2496d6b9a562" />


*   Выведем всех владельцев красных машин

Используем связь через атрибут «цвет» объекта автомобиль для фильтрации по цвету:

red\_car\_owners = Ownership.objects.filter(car\_\_color\_\_icontains='Красный')

print("\\n Владельцы красных авто")

for ownership in red\_car\_owners:

    print(f"{ownership.owner.last\_name} {ownership.owner.first\_name} владеет {ownership.car.brand} {ownership.car.model}")

Вывод:

<img width="974" height="254" alt="image" src="https://github.com/user-attachments/assets/8e3806f0-9aaa-47b3-9069-f8aee47fd581" />


*   Найти всех владельцев, чей [год владения машиной](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#year) начинается с 2010 (или любой другой год, который присутствует у вас в базе)

Фильтрация по году начала владения:

owners\_from\_2010 = Ownership.objects.filter(

start\_date\_\_year\_\_gte=2010

).select\_related('owner', 'car')

for ownership in owners\_from\_2010:

print(f"{ownership.owner.last\_name} {ownership.owner.first\_name} - {ownership.car.brand} {ownership.car.model} (с {ownership.start\_date.date()})")

<img width="974" height="488" alt="image" src="https://github.com/user-attachments/assets/65971b78-3078-4440-84e3-57d1fa03959d" />



**Практическое задание 3:** 

Перед началом импортируем дополнительные модули в shell, которые потребуются для применения функционала более сложных запросов.

from django.db.models import Min, Max, Count, Avg

Реализованы следующие запросы c применением методов агрегации и аннотации:

*   Вывод даты выдачи самого старшего водительского удостоверения: через агрегацию и применение функции Min.

oldest\_license = DriverLicense.objects.aggregate(

oldest\_issue\_date=Min('issue\_date')

)

print(f"Самая ранняя дата выдачи: {oldest\_license\['oldest\_issue\_date'\].date()}")

Результат:

<img width="974" height="239" alt="image" src="https://github.com/user-attachments/assets/7ee993ef-45fc-4c8d-a0fa-4bc2761b9aad" />


*   Укажем самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе

Найдем последнюю дату владения для модели "Camry":

camry\_latest = Ownership.objects.filter(

car\_\_model='Camry'

).aggregate(

latest\_date=Max('start\_date')

)

if camry\_latest\['latest\_date'\]:

print(f"\\nДля модели Camry самая поздняя дата владения: {camry\_latest\['latest\_date'\].date()}")

Результат:

<img width="974" height="285" alt="image" src="https://github.com/user-attachments/assets/21acb1ac-4d7d-4de7-b922-48d2619ff11a" />


*   Выведем количество машин для каждого водителя: метод аннотации.

Используем related\_name из модели Ownership:

<img width="516" height="211" alt="image" src="https://github.com/user-attachments/assets/a0fd5ae2-279d-4d33-8f57-ed55a5108421" />


Код самой функции:

all\_drivers = User.objects.annotate(

car\_count=Count('ownerships')

).order\_by('-car\_count')

print("\\n Все водители владеют:")

for driver in all\_drivers:

cars\_str = f"{driver.car\_count} авто" if driver.car\_count > 0 else "нет авто"

print(f"{driver.last\_name} {driver.first\_name}: {cars\_str}")

<img width="974" height="579" alt="image" src="https://github.com/user-attachments/assets/f273161a-fd53-450c-be33-e4aefd6bae7d" />



*   Найдем количество машин каждой марки: аннотация с подсчетом по признаку объекта.

brand\_counts = Car.objects.values('brand').annotate(

count=Count('id')

).order\_by('-count')

print("\\n Количество автомобилей каждой марки")

for brand\_data in brand\_counts:

print(f"{brand\_data\['brand'\]}: {brand\_data\['count'\]} автомобилей")

Результат:

<img width="974" height="578" alt="image" src="https://github.com/user-attachments/assets/1a08b738-1a15-4486-9110-192eb87f7638" />



*   Отсортируем и выведем всех автовладельцев по дате выдачи удостоверения

Группируем по владельцу с использованием .values() и получаем минимальную дату выдачи для каждого.

print("\\n Список владельцев с датой выдачи прав")

owners\_grouped = DriverLicense.objects.values(

'owner\_\_id',

'owner\_\_first\_name',

'owner\_\_last\_name'

).annotate(

first\_license\_date=Min('issue\_date')

).order\_by('first\_license\_date')

for owner\_data in owners\_grouped:

full\_name = f"{owner\_data\['owner\_\_last\_name'\]} {owner\_data\['owner\_\_first\_name'\]}"

issue\_date = owner\_data\['first\_license\_date'\].date()

print(f"ФИО:{ full\_name } Дата выдачи: { issue\_date }")

Результат:

<img width="605" height="260" alt="image" src="https://github.com/user-attachments/assets/2c0eb183-311b-4346-8901-6369a88b129d" />


Часть 2.

Тема: Django REST Framework. Создание API.

**Цель работы:** изучить основы построения RESTful API с использованием библиотеки Django REST Framework (DRF). Освоить работу с сериализаторами, создать API-представления вручную и с помощью Generics, а также реализовать полный набор CRUD-операций для моделей.

**Практическое задание 1:** 

Реализовать ендпоинты для добавления и просмотра скилов методом, описанным в пункте выше.

Выполнение работы.

Активируем виртуальное окружение:

.venv\\Scripts\\activate

.\\.venv\\Scripts\\activate

Для начала необходимо создать новый проект и установить все необходимые библиотеки.

pip install djangorestframework

<img width="974" height="441" alt="image" src="https://github.com/user-attachments/assets/5dd20bcf-d688-4180-98b9-e42e948e3271" />


Создание проекта

django-admin startproject warriors\_project

cd warriors\_project

python manage.py startapp warriors\_app

Получился новый проект Django и приложение warriors\_app в нем

<img width="423" height="264" alt="image" src="https://github.com/user-attachments/assets/f1c68af9-435f-4153-867a-7a2b536c73ed" />


Подключение приложения и Django Rest Framework

<img width="726" height="309" alt="image" src="https://github.com/user-attachments/assets/725346be-8fc5-4758-8a35-e33b5b2b8a90" />


Создаем модели данных в файле «warriors\_app/models.py»:

Профессия (Profession) - Описание профессии

Скилл (Skill) - Описание умений

Воин (Warrior) - Описание война

Скиллы воина (SkillOfWarrior) - Описание умений война

**Применяем миграции**

python manage.py makemigrations

python manage.py migrate

После создания суперпользователя удалось запустить сервер:

<img width="773" height="251" alt="image" src="https://github.com/user-attachments/assets/d854195b-5873-4f23-a784-efa7bdf93d0e" />


Необходимо настроить сериализацию данных из django к формату JSON.

**Сериализатор**: преобразует информацию, хранящуюся в базе данных и определенную с помощью моделей Django, в формат, который легко и эффективно передается через API. Сериализаторы позволяют преобразовывать сложные данные, такие как наборы запросов и экземпляры моделей, в собственные типы данных Python, которые затем могут быть легко преобразованы в JSON, XML или другие типы содержимого.

**Вид (ViewSet)**: определяет функции (чтение, создание, обновление, удаление), которые будут доступны через API.

**Маршрутизатор**: определяет URL-адреса, которые будут предоставлять доступ к каждому виду.

**Сериализаторы в Django REST Framework (DRF)** – это классы, которые преобразуют сложные данные (экземпляры моделей, наборы запросов) в форматы, удобные для передачи по сети (например, JSON или XML). Также сериализаторы выполняют другие задачи: 

*   проверяют предоставленные пользователем данные;
*   создают и обновляют экземпляры моделей баз данных.

Для этого необходимо создать файл serializers.py и настроить в нем работу сериализаторов.

**Создание сериализаторов.** При создании используется класс модельных сериалайзеров. Общие принципы работы модельного сериалайзера как на чтение, так и на запись идентичны тому, как работает базовый класс Serializer. Он отличается тем, что у него есть несколько инструментов, позволяющих сократить код сериалайзера:

*   автоматическое создание полей сериалайзера на основе данных о корреспондирующих полях модели;
*   автоматическое включение в поля сериалайзера тех же валидаторов, которые есть в полях модели, а также при определённых условиях метавалидаторов;
*   заранее определённые методы create и update.

ProfessionSerializer – Сериализатор для профессии

SkillSerializer – Сериализатор для умений

SkillOfWarriorSerializer – Сериализатор для умений воина с уровнем

WarriorSerializer – Базовый сериализатор для воина

WarriorProfessionSerializer – Сериализатор для воина с профессией

WarriorSkillsSerializer – Сериализатор для воина с умениями

WarriorFullSerializer – Полный сериализатор для воина с профессией и умениями

WarriorCreateSerializer – Сериализатор для создания воина

ProfessionCreateSerializer – Сериализатор для создания профессии

SkillCreateSerializer – Сериализатор для создания умения

SkillOfWarriorCreateSerializer – Сериализатор для создания умения воина

Файл serializers.py:

from rest\_framework import serializers

from .models import Warrior, Profession, Skill, SkillOfWarrior

class ProfessionSerializer(serializers.ModelSerializer):

    class Meta:

        model = Profession

        fields = '\_\_all\_\_'

class SkillSerializer(serializers.ModelSerializer):

    class Meta:

        model = Skill

        fields = '\_\_all\_\_'

class SkillOfWarriorSerializer(serializers.ModelSerializer):

    skill = SkillSerializer(read\_only=True)

    class Meta:

        model = SkillOfWarrior

        fields = \['id', 'skill', 'level'\]

class WarriorSerializer(serializers.ModelSerializer):

    class Meta:

        model = Warrior

        fields = '\_\_all\_\_'

class WarriorProfessionSerializer(serializers.ModelSerializer):

    profession = ProfessionSerializer(read\_only=True)

    race = serializers.CharField(source='get\_race\_display', read\_only=True)

    class Meta:

        model = Warrior

        fields = '\_\_all\_\_'

class WarriorSkillsSerializer(serializers.ModelSerializer):

    skill = SkillOfWarriorSerializer(source='skills', many=True, read\_only=True)

    race = serializers.CharField(source='get\_race\_display', read\_only=True)

    class Meta:

        model = Warrior

        fields = '\_\_all\_\_'

class WarriorFullSerializer(serializers.ModelSerializer):

    profession = ProfessionSerializer(read\_only=True)

    skill = SkillOfWarriorSerializer(source='skills', many=True, read\_only=True)

    race = serializers.CharField(source='get\_race\_display', read\_only=True)

    class Meta:

        model = Warrior

        fields = '\_\_all\_\_'

class WarriorCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Warrior

        fields = '\_\_all\_\_'

class ProfessionCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Profession

        fields = '\_\_all\_\_'

class SkillCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Skill

        fields = '\_\_all\_\_'

class SkillOfWarriorCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = SkillOfWarrior

        fields = '\_\_all\_\_'

Используемые в файле контроллеров сериализаторы необходимо импортировать в файл views.py. SkillSerializer(skills, many=True): теперь родителем выступает не CapitalSerializer, а класс DRF для обработки наборов записей restframework.serializers.ListSerializer.

Созданный экземпляр сериалайзера наделяется атрибутом child. В него включается дочерний сериалайзер – экземпляр класса CapitalSerializer. Задача основного сериалайзера (он относится к классу ListSerializer) – запустить цикл, в ходе которого дочерний обработает каждую запись и превратит ее в словарь.

После создания основного сериалайзера мы обращаемся к его атрибуту data.

В словарь заносится пара «ключ-значение»:

*   ключ – название поля сериалайзера;
*   значение – данные, возвращённые методом to\_representation поля сериалайзера.

Итог: список из OrderedDict в количестве, равном числу переданных и сериализованных записей из модели.

Просмотр всех умений:

class SkillAPIView(APIView):

    def get(self, request):

        skills = Skill.objects.all()

        serializer = SkillSerializer(skills, many=True)

        return Response({"Skills": serializer.data})

Далее необходимо создать URL-адрес, с которого пользователь сможет получить доступ к этому методу: в файл warriors\_app/urls.py вставить следующий код:

from django.urls import path

from .views import (

    SkillAPIView, SkillCreateView

)

app\_name = "warriors\_app"

urlpatterns = \[

    # Скилы через APIView

    path('skills/', SkillAPIView.as\_view(), name='skill-list'),

\]

Также необходимо настроить адресацию на приложение и импортировать его url-файл в проект. В папке проекта изменить файл urls.py:

from django.contrib import admin

from django.urls import path, include

urlpatterns = \[

path('admin/', admin.site.urls),

path('api/', include('warriors\_app.urls')),

\]

Browsable API – удобный инструмент для тестирования API на DRF.

Django Rest Framework позволяет посмотреть в браузере, какую информацию будет отдавать API при обращении к конкретному маршруту (эндпоинту). Достаточно ввести маршрут в адресную строку, и откроется страница с данными о запросе и результате его выполнения. За такое отображение отвечает [BrowsableAPIRenderer](https://www.django-rest-framework.org/api-guide/renderers/#browsableapirenderer).

В итоге по объявленному адресу на сайте становится доступна следующая страница:

<img width="974" height="388" alt="image" src="https://github.com/user-attachments/assets/d13a3c82-c81f-4fa1-b079-30afe98c03cb" />


**Далее рассмотрен метод POST, позволяющий отправить данные на сервер.**

DRF-класс Serializer наследует от класса BaseSerializer, у которого есть [метод \`save](https://github.com/encode/django-rest-framework/blob/master/rest_framework/serializers.py#L179)\`. Но вызвать его напрямую мы пока не можем. Чтобы метод заработал, внутри класса нашего сериалайзера нужно описать два метода:

*   [create](https://github.com/encode/django-rest-framework/blob/master/rest_framework/serializers.py#L212) с логикой сохранения в БД новой записи;
*   [update](https://github.com/encode/django-rest-framework/blob/master/rest_framework/serializers.py#L207) с логикой обновления в БД существующей записи.

Код файла warriors\_app/views.py для создания нового умения:

class SkillCreateView(APIView):

    def post(self, request):

        skill\_data = request.data.get("skill")

        serializer = SkillCreateSerializer(data=skill\_data)

        if serializer.is\_valid(raise\_exception=True):

            skill\_saved = serializer.save()

        return Response({

            "Success": "Skill '{}' created successfully.".format(skill\_saved.title)

        })

Код файла urls.py:

from django.urls import path

from .views import (

    SkillAPIView, SkillCreateView

)

app\_name = "warriors\_app"

urlpatterns = \[

    # Скилы через APIView

    path('skills/', SkillAPIView.as\_view(), name='skill-list'),

    path('skills/create/', SkillCreateView.as\_view(), name='skill-create'),

\]

Работоспособность можно проверить в браузере по указанному выше адресу:

<img width="974" height="482" alt="image" src="https://github.com/user-attachments/assets/6e282406-c84d-4ca4-866c-bce65dd22afd" />


**Практическое задание 2:**

Generic классы скрывают от разработчика часть бизнес-логики представления, позволяя писать меньше кода. Можно сказать, что Generic API View позволяют быстро создавать Rest API. 

С помощью Generic API View можно написать более короткий сценарий с функциональностью CRUD-системы.

ListAPIView используется для ендпоинтов, доступных только для чтения, - представления коллекции экземпляров модели.

CreateAPIView используется для ендпоинтов на создание объектов.

Реализованы ендпоинты:

*   Вывод полной информации обо всех войнах и их профессиях (в одном запросе).

**Сериализатор**:  вывод всех воинов и вывод полной информации о всех войнах и их профессиях.

class WarriorProfessionSerializer(serializers.ModelSerializer):

    profession = ProfessionSerializer(read\_only=True)

    race = serializers.CharField(source='get\_race\_display', read\_only=True)

    class Meta:

        model = Warrior

        fields = '\_\_all\_\_'

**Вид (ViewSet)**: наследуется от ListAPIView - generic метод, используется для ендпоинтов, доступных только для чтения, для представления коллекции экземпляров модели. Предоставляет get обработчик метода.

class WarriorListAPIView(ListAPIView):

    serializer\_class = WarriorSerializer

    queryset = Warrior.objects.all()

class WarriorProfessionListAPIView(ListAPIView):

    serializer\_class = WarriorProfessionSerializer

    queryset = Warrior.objects.all()

**Маршрутизатор**:

urlpatterns = \[

    # Скилы через APIView Прописываем сам маршрут в приложении warriors\_app и

    # связываем маршрут с контроллером:

    path('skills/', SkillAPIView.as\_view(), name='skill-list'),

    path('skills/create/', SkillCreateView.as\_view(), name='skill-create'),

    # Воины через Generic

    path('warriors/', WarriorListAPIView.as\_view(), name='warrior-list'),

    path('warriors/professions/', WarriorProfessionListAPIView.as\_view(), name='warrior-professions'),

\]

*   Вывод полной информации обо всех войнах и их скилах (в одном запросе).

**Сериализатор**:  Сериализатор для воина с умениями

class WarriorSkillsSerializer(serializers.ModelSerializer):

    skill = SkillOfWarriorSerializer(source='skills', many=True, read\_only=True)

    race = serializers.CharField(source='get\_race\_display', read\_only=True)

    class Meta:

        model = Warrior

        fields = '\_\_all\_\_'

**Вид (ViewSet)**: Вывод полной информации обо всех войнах и их скилах

class WarriorSkillsListAPIView(ListAPIView):

    serializer\_class = WarriorSkillsSerializer

    queryset = Warrior.objects.all()

**Маршрутизатор**:

urlpatterns = \[

    # Скилы через APIView Прописываем сам маршрут в приложении warriors\_app и

    # связываем маршрут с контроллером:

    path('skills/', SkillAPIView.as\_view(), name='skill-list'),

    path('skills/create/', SkillCreateView.as\_view(), name='skill-create'),

    # Воины через Generic

    path('warriors/', WarriorListAPIView.as\_view(), name='warrior-list'),

    path('warriors/professions/', WarriorProfessionListAPIView.as\_view(), name='warrior-professions'),

    path('warriors/skills/', WarriorSkillsListAPIView.as\_view(), name='warrior-skills'),

\]

*   Вывод полной информации о войне (по id), его профессиях и скилах.

**Сериализатор**: полный сериализатор для воина с профессией и умениями.

class WarriorFullSerializer(serializers.ModelSerializer):

    profession = ProfessionSerializer(read\_only=True)

    skill = SkillOfWarriorSerializer(source='skills', many=True, read\_only=True)

    race = serializers.CharField(source='get\_race\_display', read\_only=True)

    class Meta:

        model = Warrior

        fields = '\_\_all\_\_'

**Вид (ViewSet)**: Вывод полной информации о войне (по id), его профессиях и скилах

class WarriorDetailAPIView(RetrieveAPIView):

    serializer\_class = WarriorFullSerializer

    queryset = Warrior.objects.all()

    lookup\_field = 'pk'

**Маршрутизатор**:

urlpatterns = \[

    # Скилы через APIView Прописываем сам маршрут в приложении warriors\_app и

    # связываем маршрут с контроллером:

    path('skills/', SkillAPIView.as\_view(), name='skill-list'),

    path('skills/create/', SkillCreateView.as\_view(), name='skill-create'),

    # Воины через Generic

    path('warriors/', WarriorListAPIView.as\_view(), name='warrior-list'),

    path('warriors/professions/', WarriorProfessionListAPIView.as\_view(), name='warrior-professions'),

    path('warriors/skills/', WarriorSkillsListAPIView.as\_view(), name='warrior-skills'),

    path('warriors/<int:pk>/', WarriorDetailAPIView.as\_view(), name='warrior-detail'),

\]

*   Удаление война по id.

**Сериализатор**: базовый

**Вид (ViewSet)**:

class WarriorDeleteAPIView(DestroyAPIView):

    queryset = Warrior.objects.all()

    lookup\_field = 'pk'

**Маршрутизатор**:

urlpatterns = \[

    # Скилы через APIView Прописываем сам маршрут в приложении warriors\_app и

    # связываем маршрут с контроллером:

    path('skills/', SkillAPIView.as\_view(), name='skill-list'),

    path('skills/create/', SkillCreateView.as\_view(), name='skill-create'),

    # Воины через Generic

    path('warriors/', WarriorListAPIView.as\_view(), name='warrior-list'),

    path('warriors/professions/', WarriorProfessionListAPIView.as\_view(), name='warrior-professions'),

    path('warriors/skills/', WarriorSkillsListAPIView.as\_view(), name='warrior-skills'),

    path('warriors/<int:pk>/', WarriorDetailAPIView.as\_view(), name='warrior-detail'),

    path('warriors/<int:pk>/delete/', WarriorDeleteAPIView.as\_view(), name='warrior-delete'),

\]

*   Редактирование информации о войне.

**Сериализатор**: базовый

**Вид (ViewSet)**: Редактирование информации о войне

class WarriorUpdateAPIView(UpdateAPIView):

    serializer\_class = WarriorCreateSerializer

    queryset = Warrior.objects.all()

    lookup\_field = 'pk'

**Маршрутизатор**:

urlpatterns = \[

    # Скилы через APIView Прописываем сам маршрут в приложении warriors\_app и

    # связываем маршрут с контроллером:

    path('skills/', SkillAPIView.as\_view(), name='skill-list'),

    path('skills/create/', SkillCreateView.as\_view(), name='skill-create'),

    # Воины через Generic

    path('warriors/', WarriorListAPIView.as\_view(), name='warrior-list'),

    path('warriors/professions/', WarriorProfessionListAPIView.as\_view(), name='warrior-professions'),

    path('warriors/skills/', WarriorSkillsListAPIView.as\_view(), name='warrior-skills'),

    path('warriors/<int:pk>/', WarriorDetailAPIView.as\_view(), name='warrior-detail'),

    path('warriors/<int:pk>/delete/', WarriorDeleteAPIView.as\_view(), name='warrior-delete'),

    path('warriors/<int:pk>/update/', WarriorUpdateAPIView.as\_view(), name='warrior-update'),

\]

**Тестовые данные и запросы.**

Покажем главное: как мы научили веб-приложение отдавать информацию из базы данных в ответ на запрос, который поступает не от человека через браузер, а от другого приложения. И далее – как это приложение использует полученную информацию.

Создадим тестовые данные и протестируем работу запросов через интерактивный режим. В файле seed\_data.py добавлена функция заполнения данными бд. Запустим и протестируем:

python manage.py shell

from warriors\_app.seed\_data import create\_initial\_data

create\_initial\_data()

<img width="974" height="258" alt="image" src="https://github.com/user-attachments/assets/3d46e5fa-c632-456c-8445-6c8cce64e408" />


Теперь при запуске сервера по GET-запросу отображаются данные о навыках:

<img width="974" height="492" alt="image" src="https://github.com/user-attachments/assets/4ab9e0e5-7904-45af-a01c-9db638d95243" />


{

"Skills": \[

{

"id": 1,

"title": "Python"

},

{

"id": 2,

"title": "JavaScript"

},

{

"id": 3,

"title": "SQL"

},

{

"id": 4,

"title": "React"

},

{

"id": 5,

"title": "Django"

}

\]

}

Для тестирования POST-запроса заполним форму: {"skill": {"title": "TypeScript"}}
<img width="974" height="672" alt="image" src="https://github.com/user-attachments/assets/a6e8920e-8838-465b-ae05-f9935e6c6e2d" />


Результат:

<img width="974" height="287" alt="image" src="https://github.com/user-attachments/assets/39abb499-3348-4279-a6e6-d19b2c4f8fff" />


{

"Success": "Skill 'TypeScript' created successfully."

}

Просмотр всех воинов (GET): http://127.0.0.1:8000/api/warriors/

<img width="974" height="646" alt="image" src="https://github.com/user-attachments/assets/607bc126-3d01-4cf6-9edd-ccc5c93843d8" />


Просмотр воинов с профессиями (GET)

<img width="974" height="502" alt="image" src="https://github.com/user-attachments/assets/e486f915-4559-4954-beaa-3ad6cc36e831" />


Просмотр воинов с умениями (GET)

<img width="974" height="621" alt="image" src="https://github.com/user-attachments/assets/bd17fb14-6e1d-497a-b0ba-f8a6d2da7278" />
)

Редактирование воина (PUT/PATCH) через заполнение формы

<img width="974" height="624" alt="image" src="https://github.com/user-attachments/assets/64567383-f732-4ac2-b59b-79c9bbe82ac3" />


Результат:

<img width="974" height="434" alt="image" src="https://github.com/user-attachments/assets/d447de70-3bc1-4cee-9366-9b2608e7387e" />


Удаление воина (DELETE) – выбираем удалить по id 1

<img width="974" height="371" alt="image" src="https://github.com/user-attachments/assets/0eab16fc-4b27-4959-b966-5fa5cacfd6ab" />


<img width="974" height="200" alt="image" src="https://github.com/user-attachments/assets/c967c151-cc89-44b8-b4c1-9a5402b1837d" />


Удаление выполнено:

<img width="974" height="558" alt="image" src="https://github.com/user-attachments/assets/bef96c39-f32e-46d5-9ac8-93ee6f3eae6b" />


Выводы:

Итак, мы рассмотрели, как сделать API на базе DRF, чтобы получить по GET-запросу набор записей из Django-модели.
