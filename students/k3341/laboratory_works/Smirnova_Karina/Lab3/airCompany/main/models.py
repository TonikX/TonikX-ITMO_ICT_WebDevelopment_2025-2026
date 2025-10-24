from django.db import models

class AirlineCompany(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название компании')

    def __str__(self):
        return self.name

class Plane(models.Model):
    number = models.CharField(max_length=20, verbose_name='Номер самолета')
    type = models.CharField(max_length=50, verbose_name='Тип самолета')
    seats_capacity = models.IntegerField(verbose_name='Число мест')
    flight_speed = models.IntegerField(verbose_name='Скорость полета')
    airline_company = models.ForeignKey(AirlineCompany, on_delete=models.CASCADE, verbose_name='Компания-авиаперевозчик')
    in_repair = models.BooleanField(default=False, verbose_name='В ремонте')

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
    position = models.CharField(max_length=50,
                                verbose_name='Должность (командир, второй пилот, штурман, стюардесса/стюард)')

    def __str__(self):
        return self.full_name

class Route(models.Model):
    distance = models.IntegerField(verbose_name='Расстояние до пункта назначения')
    departure_point = models.CharField(max_length=255, verbose_name='Пункт вылета')
    destination_point = models.CharField(max_length=255, verbose_name='Пункт назначения')
    landing_points = models.CharField(max_length=255, blank=True, null=True,  verbose_name='Пункты посадки')
    transit_landings = models.CharField(max_length=255, blank=True, null=True,   verbose_name='Транзитные посадки')

    def __str__(self):
        return f'{self.departure_point} - {self.destination_point}'

class Flight(models.Model):
    flight_number = models.IntegerField(verbose_name='Номер рейса')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='flights', verbose_name='Маршрут')
    departure_datetime = models.DateTimeField(verbose_name='Дата и время вылета')
    arrival_datetime = models.DateTimeField(verbose_name='Дата и время прилета')
    sold_tickets = models.IntegerField(verbose_name='Количество проданных билетов')
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, verbose_name='Самолет, обслуживающий рейс')
    crew = models.ManyToManyField(Crew, verbose_name='Экипаж, обслуживающий рейс')

    def __str__(self):
        return f'Flight {self.pk}'

class TransitLanding(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, verbose_name='Рейс')
    landing_point = models.CharField(max_length=255, verbose_name='Пункт транзитной посадки')
    landing_datetime = models.DateTimeField(verbose_name='Дата и время транзитной посадки')
    takeoff_datetime = models.DateTimeField(verbose_name='Дата и время вылета (после транзитной посадки)')

    def __str__(self):
        return f'{self.landing_point} для рейса {self.flight.flight_number}'




