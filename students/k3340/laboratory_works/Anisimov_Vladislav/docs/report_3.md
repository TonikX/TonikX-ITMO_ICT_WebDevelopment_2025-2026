# Лабораторная работа 3

## Схема базы данных

![db_scheme](assets/db_scheme.jpg)

## models.py

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class FuelType(models.IntegerChoices):
    GASOLINE_1 = 1, 'АИ-92'
    GASOLINE_2 = 2, 'АИ-95'
    GASOLINE_3 = 3, 'АИ-98'
    GASOLINE_4 = 4, 'АИ-100'
    DIESEL = 5, 'ДТ'
    ELECTRIC = 6, 'Электрический'
    HYBRID = 7, 'Гибрид'

class TransmissionType(models.TextChoices):
    AUTO = 'A', 'Автоматическая'
    MANUAL = 'M', 'Механическая'

class User(AbstractUser):
    #full_name = models.CharField('Полное имя', max_length=128)
    passport = models.CharField('Паспортные данные', max_length=32)
    phone = models.CharField('Телефон', max_length=16)
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'password', 'phone', 'passport']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Client(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='client',
    )
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Worker(models.Model):
    salary = models.IntegerField('Зарплата')
    position = models.CharField('Должность', max_length=64)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='worker',
    )
    
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
    
    def __str__(self):
        return f"{self.position}: {self.user.first_name + " " + self.user.last_name}"

class CarInfo(models.Model):
    brand = models.CharField('Марка', max_length=32)
    model = models.CharField('Модель', max_length=32)
    description = models.TextField('Описание', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Информация об автомобиле'
        verbose_name_plural = 'Информация об автомобилях'
    
    def __str__(self):
        return f"{self.brand} {self.model}"

class Car(models.Model):
    capacity = models.IntegerField('Количество мест')
    engine_volume = models.FloatField('Объём двигателя')
    horsepower = models.IntegerField('Мощность двигателя')
    fuel_type = models.IntegerField(
        'Тип топлива',
        choices=FuelType.choices
    )
    transmission = models.CharField(
        'Тип КПП',
        max_length=20,
        choices=TransmissionType.choices
    )
    clearance = models.FloatField('Дорожный просвет')
    trunk_volume = models.IntegerField('Объем багажника')
    tank_volume = models.IntegerField('Объём топливного бака')
    fuel_consumption = models.FloatField('Расход топлива')
    gen = models.CharField('Поколение', max_length=32,)
    car_info = models.ForeignKey(
        CarInfo,
        on_delete=models.CASCADE,
        related_name='cars',
    )
    
    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
    
    def __str__(self):
        return f"{self.car_info} {self.transmission}"

class CarInstance(models.Model):
    license_plate = models.CharField('Госномер', max_length=20)
    vincode = models.CharField('VIN-код', max_length=50)
    price = models.IntegerField('Цена проката')
    color = models.CharField('Цвет', max_length=32)
    year = models.IntegerField('Год')
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='instances',
    )
    
    class Meta:
        verbose_name = 'Экземпляр автомобиля'
        verbose_name_plural = 'Экземпляры автомобилей'
    
    def __str__(self):
        return f"{self.license_plate} - {self.car.car_info.brand} {self.car.car_info.model}"

class RentContract(models.Model):
    start_date = models.DateTimeField('Дата начала аренды')
    return_date = models.DateTimeField('Планируемая дата возврата')
    real_return_date = models.DateTimeField(
        'Фактическая дата возврата',
        blank=True,
        null=True
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='contracts',
    )
    car_instance = models.ForeignKey(
        CarInstance,
        on_delete=models.CASCADE,
        related_name='contracts',
    )
    worker = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        related_name='contracts',
    )
    
    class Meta:
        verbose_name = 'Договор аренды'
        verbose_name_plural = 'Договоры аренды'
    
    def __str__(self):
        return f"Договор {self.id} - {self.client}"

class Fine(models.Model):
    date = models.DateTimeField('Дата штрафа')
    cost = models.FloatField('Сумма штрафа')
    description = models.TextField('Описание')
    car_instance = models.ForeignKey(
        CarInstance,
        on_delete=models.CASCADE,
        related_name='fines',
        verbose_name='Экземпляр автомобиля'
    )
    
    class Meta:
        verbose_name = 'Штраф'
        verbose_name_plural = 'Штрафы'
    
    def __str__(self):
        return f"Штраф {self.date.strftime('%Y-%m-%d')} - {self.cost} руб."

class CarCrash(models.Model):
    date = models.DateTimeField('Дата аварии')
    damage = models.FloatField('Ущерб')
    info = models.TextField('Информация об аварии')
    car_instance = models.ForeignKey(
        CarInstance,
        on_delete=models.CASCADE,
        related_name='crashes',
    )
    
    class Meta:
        verbose_name = 'Авария'
        verbose_name_plural = 'Аварии'
    
    def __str__(self):
        return f"Авария {self.date.strftime('%Y-%m-%d')}  на сумму {self.damage}"

```

## serializers.py

```python
from rest_framework import serializers
from .models import *

class CarInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarInfo
        fields = "__all__"

class CarSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['car_info'] = CarInfoSerializer(instance.car_info).data
        return representation

    class Meta:
        model = Car
        fields = "__all__"

class FineSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['car_instance'] = instance.car_instance.__str__()
        return representation
    
    class Meta:
        model = Fine
        fields = "__all__"

class CarCrashSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['car_instance'] = instance.car_instance.__str__()
        return representation
    
    class Meta:
        model = CarCrash
        fields = "__all__"

class CarInstanceSerializer(serializers.ModelSerializer):
    fines = FineSerializer(many=True, read_only=True)
    crashes = CarCrashSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['car'] = CarSerializer(instance.car).data
        representation['fines'] = list(map(lambda el: el["description"], representation['fines']))
        representation['crashes'] = list(map(lambda el: el["info"], representation['crashes']))
        return representation
    
    class Meta:
        model = CarInstance
        fields = "__all__"

class ClientSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = User.objects.get(id=representation['user'])
        representation['user'] = f"{user.first_name} {user.last_name}"
        return representation
        
    class Meta:
        model = Client
        fields = "__all__"

class WorkerSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = User.objects.get(id=representation['user'])
        representation['user'] = f"{user.first_name} {user.last_name}"
        return representation
    
    class Meta:
        model = Worker
        fields = "__all__"

class RentContractSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['worker'] = WorkerSerializer(instance.worker).data['user']
        representation['client'] = ClientSerializer(instance.client).data['user']
        representation['car_instance'] = instance.car_instance.__str__()
        return representation
    
    class Meta:
        model = RentContract
        fields = "__all__"
```

## views.py 

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets
from django.db.models import Count, Max, Sum, F, Q
from django.db.models.functions import Concat
from .models import *
from .serializers import *

class CarInfoAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CarInfoSerializer
    queryset = CarInfo.objects.all()

class CarAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()

class CarInstanceAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CarInstanceSerializer
    queryset = CarInstance.objects.all()

class FineAPIViewSet(viewsets.ModelViewSet):
    serializer_class = FineSerializer
    queryset = Fine.objects.all()

class CarCrashAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CarCrashSerializer
    queryset = CarCrash.objects.all()

class ClientAPIViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

class WorkerAPIViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()

class RentContractAPIViewSet(viewsets.ModelViewSet):
    serializer_class = RentContractSerializer
    queryset = RentContract.objects.all()

class TimesRentedAPIView(APIView):
    def get(self, request):
        annotated = CarInstance.objects.annotate(count=Count('contracts'))
        return Response(dict([(car_instance.__str__(), car_instance.count) for car_instance in annotated]))

class DaysRentedAPIView(APIView):
    def get(self, request):
        annotated = CarInstance.objects.annotate(date=Sum(F('contracts__return_date') - F('contracts__start_date')))
        return Response(dict([(car_instance.__str__(), car_instance.date.days) for car_instance in annotated]))

class ProfitByCarAPIView(APIView):
    def get(self, request):
        annotated = CarInstance.objects.annotate(date=Sum(F('contracts__return_date') - F('contracts__start_date')))
        return Response(dict([(car_instance.__str__(), car_instance.date.days * car_instance.price) for car_instance in annotated]))

class FinesByClientAPIView(APIView):
    def get(self, request):
        annotated = Fine.objects.annotate(client=F("car_instance__contracts__client"),
                                          name=Concat("car_instance__contracts__client__user__first_name",  
                                                      models.Value(' '), 
                                                      "car_instance__contracts__client__user__last_name"),
                                          start=F("car_instance__contracts__start_date"), 
                                          end=F("car_instance__contracts__return_date")).filter(start__lt=F('date'), end__gt=F('date'))

        return Response(dict([(client['name'], client['count']) for client in annotated.values("client").annotate(count=Count('client'), name=F('name'))]))
```

## urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "core"

router = DefaultRouter()
router.register(r'car_infos', CarInfoAPIViewSet)
router.register(r'cars', CarAPIViewSet)
router.register(r'car_instances', CarInstanceAPIViewSet)
router.register(r'fines', FineAPIViewSet)
router.register(r'car_crashes', CarCrashAPIViewSet)
router.register(r'clients', ClientAPIViewSet)
router.register(r'workers', WorkerAPIViewSet)
router.register(r'rent_contracts', RentContractAPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('times_rented', TimesRentedAPIView.as_view()),
    path('days_rented', DaysRentedAPIView.as_view()),
    path('profit_by_car', ProfitByCarAPIView.as_view()),
    path('штрафby_client', FinesByClientAPIView.as_view()),
]
```
## Документация по endpoint-ам

### car_infos

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/core/car_infos/` | Получить список информации об авто
| POST | `/core/car_infos/` | Создать информацию об авто
| GET | `/core/car_infos/<id>/` | Получить информацию об авто
| PUT | `/core/car_infos/<id>/` | Обновить информацию об авто
| PATCH | `/core/car_infos/<id>/` | Частично обновить информацию об авто
| DELETE | `/core/car_infos/<id>/` | Удалить информацию об авто

### cars

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/core/cars/` | Получить список автомобилей
| POST | `/core/cars/` | Создать автомобиль
| GET | `/core/cars/<id>/` | Получить конкретный автомобиль
| PUT | `/core/cars/<id>/` | Обновить автомобиль
| PATCH | `/core/cars/<id>/` | Частично обновить автомобиль
| DELETE | `/core/cars/<id>/` | Удалить автомобиль

### car_instances

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/core/car_instances/` | Получить список всех экземпляров автомобилей
| POST | `/core/car_instances/car_instances/` | Создать экземпляр автомобиля
| GET | `/core/car_instances/<id>/` | Получить конкретный экземпляр автомобиля
| PUT | `/core/car_instances/<id>/` | Обновить экземпляр автомобиля
| PATCH | `/core/car_instances/<id>/` | Частично обновить экземпляр автомобиля
| DELETE | `/core/car_instances/<id>/` | Удалить экземпляр автомобиля

### fines

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/core/fines/` | Получить список всех штрафов
| POST | `/core/fines/` | Создать штраф
| GET | `/core/fines/<id>/` | Получить конкретный штраф
| PUT | `/core/fines/<id>/` | Обновить штраф
| PATCH | `/core/fines/<id>/` | Частично обновить штраф
| DELETE | `/core/fines/<id>/` | Удалить штраф

### car_crashes

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/core/car_crashes/` | Получить список ДТП
| POST | `/core/car_crashes/` | Создать ДТП
| GET | `/core/car_crashes/<id>/` | Получить конкретный ДТП
| PUT | `/core/car_crashes/<id>/` | Обновить ДТП
| PATCH | `/core/car_crashes/<id>/` | Частично обновить ДТП
| DELETE | `/core/car_crashes/<id>/` | Удалить ДТП

### clients

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/core/clients/` | Получить список клиентов
| POST | `/core/clients/` | Создать клиента
| GET | `/core/clients/<id>/` | Получить конкретного клиента
| PUT | `/core/clients/<id>/` | Обновить клиент
| PATCH | `/core/clients/<id>/` | Частично обновить клиент
| DELETE | `/core/clients/<id>/` | Удалить клиент

### workers

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/core/workers/` | Получить список работников
| POST | `/core/workers/` | Создать работника
| GET | `/core/workers/<id>/` | Получить конкретного работник
| PUT | `/core/workers/<id>/` | Обновить работник
| PATCH | `/core/workers/<id>/` | Частично обновить работник
| DELETE | `/core/workers/<id>/` | Удалить работника

### rent_contracts

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/core/rent_contracts/` | Получить список договоров аренды
| POST | `/core/rent_contracts/` | Создать договор аренды
| GET | `/core/rent_contracts/<id>/` | Получить конкретный договор аренды
| PUT | `/core/rent_contracts/<id>/` | Обновить договор аренды
| PATCH | `/core/rent_contracts/<id>/` | Частично обновить договор аренды
| DELETE | `/core/rent_contracts/<id>/` | Удалить договор аренды

### Доп. запросы

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/core/days_rented/` | Суммарное количество дней, на которое был арендован каждый автомобиль
| GET | `/core/times_rented/` | Сколько раз был арендован каждый автомобиль
| GET | `/core/fines_by_client/` | Сколько штрафов собрал клиент
| GET | `/core/profit_by_car/` | Сколько денег принёс каждый авто в бюджет