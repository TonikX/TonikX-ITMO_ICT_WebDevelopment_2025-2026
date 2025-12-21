# Практическая работа 3.1

## Задание 1:
> Напишите запрос на создание 6-7 новых автовладельцев и 5-6 автомобилей, каждому автовладельцу назначьте удостоверение и от 1 до 3 автомобилей. Задание можете выполнить либо в интерактивном режиме интерпретатора, либо в отдельном python-файле. Результатом должны стать запросы и отображение созданных объектов. 

## Выполнение:

```python
import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_django_web_project.settings')
django.setup()

from project_first_app.models import Owner, Car, DrivingLicense, Ownership

cars = []

def add_owners():
    Owner.objects.all().delete()
    Owner.objects.create(last_name='Amber', first_name='Mike', birthday=datetime(1999, 12, 11))
    Owner.objects.create(last_name='Conner', first_name='Bill', birthday=datetime(2001, 11, 6))
    Owner.objects.create(last_name='Hurley', first_name='Ann', birthday=datetime(1987, 10, 15))
    Owner.objects.create(last_name='Pierce', first_name='Jeff', birthday=datetime(2000, 10, 27))
    Owner.objects.create(last_name='Boyer', first_name='Bob', birthday=datetime(1974, 9, 5))
    Owner.objects.create(last_name='Clayton', first_name='Alex', birthday=datetime(1979, 1, 2))

def add_cars():
    Car.objects.all().delete()
    cars.append(Car.objects.create(license_plate='TZR378', brand='BMW', model="520i", color="black"))
    cars.append(Car.objects.create(license_plate='24724A', brand='Toyota', model="Camry", color="white"))
    cars.append(Car.objects.create(license_plate='11420Y', brand='Toyota', model="Camry", color="black"))
    cars.append(Car.objects.create(license_plate='25394A', brand='Dodge', model="Charger", color="red"))
    cars.append(Car.objects.create(license_plate='26064A', brand='Chevrolet', model="Malibu", color="gray"))
    cars.append(Car.objects.create(license_plate='AH32943', brand='Honda', model="Accord", color="blue"))

def add_driving_licenses():
    DrivingLicense.objects.all().delete()
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Mike").first(), number='451549845', type="B", date_of_issue=datetime(2018, 11, 25))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Bill").first(), number='545800949', type="B", date_of_issue=datetime(2022, 10, 12))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Ann").first(), number='798132657', type="B", date_of_issue=datetime(2012, 11, 23))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Jeff").first(), number='19543250', type="B", date_of_issue=datetime(2023, 2, 19))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Bob").first(), number='465159457', type="B", date_of_issue=datetime(1999, 1, 26))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Alex").first(), number='019798429', type="B", date_of_issue=datetime(2002, 9, 1))

    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Ann").first(), number='789914522', type="B", date_of_issue=datetime(2020, 9, 30))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Bob").first(), number='4519346878', type="B", date_of_issue=datetime(2006, 2, 25))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Bob").first(), number='198732415', type="B", date_of_issue=datetime(2014, 1, 21))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Bob").first(), number='678121634', type="B", date_of_issue=datetime(2023, 1, 2))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Alex").first(), number='975316515', type="B", date_of_issue=datetime(2010, 9, 15))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Alex").first(), number='121578746', type="B", date_of_issue=datetime(2020, 9, 10))

def add_ownership():
    Ownership.objects.all().delete()
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Mike").first(), car=cars[0], start_date=datetime(2015, 6, 8), end_date=None)
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Bill").first(), car=cars[1], start_date=datetime(2022, 11, 3), end_date=None)
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Ann").first(), car=cars[0], start_date=datetime(2012, 12, 2), end_date=datetime(2015, 6, 8))
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Ann").first(), car=cars[2], start_date=datetime(2016, 1, 10), end_date=None)
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Jeff").first(), car=cars[3], start_date=datetime(2024, 2, 18), end_date=None)
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Bob").first(), car=cars[2], start_date=datetime(2000, 11, 2), end_date=datetime(2016, 1, 10))
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Bob").first(), car=cars[3], start_date=datetime(2016, 3, 11), end_date=datetime(2024, 2, 18))
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Bob").first(), car=cars[4], start_date=datetime(2025, 3, 8), end_date=None)
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Alex").first(), car=cars[5], start_date=datetime(2005, 8, 6), end_date=None)

#add_owners()
#add_cars()
#add_driving_licenses()
#add_ownership()

for ownership in Ownership.objects.all():
    print(f"{ownership.owner.first_name} {ownership.owner.last_name}, born in {ownership.owner.birthday}, \
last driver license got issued in {DrivingLicense.objects.filter(owner=ownership.owner).latest("date_of_issue").date_of_issue} has driven this car:")
    print(f"    {ownership.car}")
```
## Задание 2:
> По созданным в пр.1 данным написать следующие запросы на фильтрацию:
Где это необходимо, добавьте related_name к полям модели
Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)
Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)
Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта модели (можно в 2 запроса)
Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)
Найти всех владельцев, чей год владения машиной начинается с 2010 (или любой другой год, который присутствует у вас в базе) 

## Выполнение:

```python
import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_django_web_project.settings')
django.setup()

from project_first_app.models import Owner, Car, DrivingLicense, Ownership

for car in Car.objects.filter(brand="Toyota"):
    print(car)

print("\n")

for owner in Owner.objects.filter(first_name="Bob"):
    print(owner)

print("\n")

person = Owner.objects.all()[2]
print(DrivingLicense.objects.filter(owner=person).latest("date_of_issue")) # последние продлённые права

print("\n")

for owner in Owner.objects.filter(ownership__car__color="red", ownership__end_date=None).distinct():
    print(owner)

print("\n")

for owner in Owner.objects.filter(ownership__start_date__gte=datetime(2010, 1, 1)).distinct():
    print(owner)
```

## Задание 3:
> Необходимо реализовать следующие запросы c применением описанных методов:
Вывод даты выдачи самого старшего водительского удостоверения
Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе
Выведите количество машин для каждого водителя
Подсчитайте количество машин каждой марки
Отсортируйте всех автовладельцев по дате выдачи удостоверения

## Выполнение:

```python
import os
import django
from datetime import datetime
from django.db.models import Count, Max

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_django_web_project.settings')
django.setup()

from project_first_app.models import Owner, Car, DrivingLicense, Ownership

print(DrivingLicense.objects.earliest("date_of_issue").date_of_issue)

print("\n")

print(Ownership.objects.latest("start_date").start_date)

print("\n")

for owner in (Owner.objects.annotate(ownership_count=Count('ownership'))):
    print(f"{owner} had {owner.ownership_count} cars in total")

print("\n")

for brand in Car.objects.values("brand").annotate(count=Count('brand')):
    print(f"{brand["brand"]} - {brand["count"]}")

print("\n")

for owner in Owner.objects.annotate(dl_last_date=Max("drivinglicense__date_of_issue")).order_by("dl_last_date"):
    print(owner, f"{owner.dl_last_date}")

```

# Практическая работа 3.2

## Задание 1:
> Реализовать ендпоинты для добавления и просмотра скилов методом, описанным в пункте выше.

## Выполнение:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from .models import Warrior, Profession, Skill, SkillOfWarrior
from .serializers import (
    WarriorSerializer,
    WarriorUpdateSerializer,
    WarriorCreateSerializer,
    ProfessionCreateSerializer,
    SkillSerializer,
    SkillCreateSerializer,
    WarriorExtendedSerializer,
    WarriorProfessionSerializer,
    WarriorSkillSerializer,
    SkillOfWarriorCreateSerializer,
)

class SkillListAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({"Skills": serializer.data})

class SkillCreateAPIView(APIView):
    def post(self, request):
        skill_data = request.data.get("skill")
        serializer = SkillCreateSerializer(data=skill_data)

        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()

        return Response({"Success": f"Skill '{skill_saved.title}' created succesfully."})
```

## Задание 2:
> Реализовать ендпоинты:
> - Вывод полной информации о всех войнах и их профессиях (в одном запросе).
> - Вывод полной информации о всех войнах и их скилах (в одном запросе).
> - Вывод полной информации о войне (по id), его профессиях и скилах.
> - Удаление война по id.
> - Редактирование информации о войне.


## Выполнение:

```python
class WarriorProfessionListAPIView(generics.ListAPIView):
    serializer_class = WarriorProfessionSerializer
    queryset = Warrior.objects.all()

class WarriorSkillListAPIView(generics.ListAPIView):
    serializer_class = WarriorSkillSerializer
    queryset = Warrior.objects.all()

class WarriorRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = WarriorExtendedSerializer
    queryset = Warrior.objects.all()

class WarriorRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = WarriorUpdateSerializer
    queryset = Warrior.objects.all()

class WarriorCreateAPIView(generics.CreateAPIView):
   serializer_class = WarriorCreateSerializer
   queryset = Warrior.objects.all()

   def perform_create(self, serializer):
       serializer.save() 
```

## serializers.py

```python
from rest_framework import serializers
from .models import Warrior, Profession, Skill, SkillOfWarrior

class WarriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrior
        fields = "__all__"

class WarriorCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Warrior.objects.create(**validated_data)
    
    class Meta:
        model = Warrior
        fields = "__all__"

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["title"]

class SkillCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)

    def create(self, validated_data):
        return Skill.objects.create(**validated_data)
    
class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ["title", "description"]

class ProfessionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()

    def create(self, validated_data):
       profession = Profession(**validated_data)
       profession.save()
       return Profession(**validated_data)

class WarriorSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"

class WarriorProfessionSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"

class WarriorExtendedSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skill = SkillSerializer(many=True)
    race = serializers.CharField(source="get_race_display", read_only=True)

    class Meta:
        model = Warrior
        fields = "__all__"

class WarriorUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Warrior
        fields = "__all__"

class SkillOfWarriorCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return SkillOfWarrior.objects.create(**validated_data)
    
    class Meta:
        model = SkillOfWarrior
        fields = "__all__"
```