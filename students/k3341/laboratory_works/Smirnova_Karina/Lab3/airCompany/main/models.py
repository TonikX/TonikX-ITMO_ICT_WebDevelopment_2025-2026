from django.db import models

class AirlineCompany(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название компании')

    def __str__(self):
        return self.name

class Plane(models.Model):
    number = models.CharField(max_length=20, verbose_name='Номер самолета')
    plane_type = models.CharField(max_length=50, verbose_name='Тип самолета')
    seats_capacity = models.IntegerField(verbose_name='Число мест')
    flight_speed = models.IntegerField(verbose_name='Скорость полета')
    under_repair = models.BooleanField(default=False, verbose_name='В ремонте')
    airline_company = models.ForeignKey(AirlineCompany, on_delete=models.CASCADE, verbose_name='Компания-авиаперевозчик')

    def __str__(self):
        return self.number

class Crew(models.Model):
    members = models.ManyToManyField('CrewMember', verbose_name='Члены экипажа')

    def __str__(self):
        return f'Crew {self.pk}'
class CrewMember(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    age = models.IntegerField(verbose_name='Возраст')
    education = models.CharField(max_length=255, verbose_name='Образование')
    work_experience = models.IntegerField(verbose_name='Стаж работы')
    passport_info = models.CharField(max_length=255, verbose_name='Паспортные данные')
    flight_authorization = models.BooleanField(default=False, verbose_name='Допуск к рейсу')
    company = models.ManyToManyField(AirlineCompany, verbose_name='Компания, в которой работает')

    def __str__(self):
        return self.full_name

class Route(models.Model):
    flight_number = models.CharField(max_length=20, verbose_name='Номер рейса')
    distance = models.IntegerField(verbose_name='Расстояние до пункта назначения')
    departure_point = models.CharField(max_length=255, verbose_name='Пункт вылета')
    landing_points = models.CharField(max_length=255, blank=True, null=True,  verbose_name='Пункты посадки')
    transit_landings = models.CharField(max_length=255, blank=True, null=True,   verbose_name='Транзитные посадки')
    destination_point = models.CharField(max_length=255, verbose_name='Пункт назначения')

    def __str__(self):
        return self.flight_number

class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='flights', verbose_name='Маршрут')
    departure_datetime = models.DateTimeField(verbose_name='Дата и время вылета')
    arrival_datetime = models.DateTimeField(verbose_name='Дата и время прилета')
    transit_landing_datetime = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время транзитных посадок')
    sold_tickets = models.IntegerField(verbose_name='Количество проданных билетов')
    airplanes = models.ManyToManyField(Plane, verbose_name='Самолеты, обслуживающие рейс')
    crew = models.ManyToManyField(Crew, verbose_name='Экипаж, обслуживающий рейс')

    def __str__(self):
        return f'Flight {self.pk}'






