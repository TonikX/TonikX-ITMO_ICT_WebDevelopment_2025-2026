from django.utils import timezone

from django.db import models
from django.db.models import ForeignKey


# Create your models here.
class PersonAbstract(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['last_name', 'first_name']

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return ' '.join(parts).strip()

    @property
    def short_name(self):
        first = f"{self.first_name[0].upper()}."
        middle = f"{self.middle_name[0].upper()}." if self.middle_name else ""
        return f"{first}{middle} {self.last_name}".strip()


class Enterprise(models.Model):
    name = models.CharField(max_length=200)
    legal_address = models.CharField(max_length=200)
    ogrn = models.CharField(max_length=200)
    services = models.ManyToManyField('Services', related_name='enterprises')


class Services(models.Model):
    name = models.CharField(max_length=200, unique=True)

class Object(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    decorators = models.ManyToManyField('Decorator', related_name='serviced_objects', blank=True)

    @property
    def is_serviced(self):
        return self.contracts.filter(is_active=True).exists()


class Contract(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='contracts')
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='contracts')
    contract_number = models.CharField(max_length=200)
    contract_date = models.DateField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)


class Decorator(PersonAbstract):
    category_types = (
        (0, 'Highest'),
        (1, 'First'),
        (2, 'No Category'),
    )

    phone_number = models.CharField(max_length=200)
    education = models.CharField(max_length=200)
    graduated_from = models.CharField(max_length=200)
    category = models.IntegerField(choices=category_types, default=2)


class ObjectZone(models.Model):
    object_id = ForeignKey(Object, on_delete=models.CASCADE, related_name='zones')
    number = models.CharField(max_length=200)


class Plant(models.Model):
    initial_age = models.IntegerField()  # возраст на момент первой высадки
    description = models.TextField()
    species = models.ForeignKey('Species', on_delete=models.CASCADE, related_name='plant')

    @property
    def current_age(self):
        first_placement = self.placements.order_by('planted_date').first()
        if not first_placement:
            return self.initial_age
        today = timezone.now().year
        return self.initial_age + (today - first_placement.planted_date.year)


class PlantPlacement(models.Model):
    plant = models.ForeignKey('Plant', on_delete=models.CASCADE, related_name='placements')
    zone = models.ForeignKey('ObjectZone', on_delete=models.CASCADE, related_name='placements')
    unique_number = models.IntegerField()
    planted_date = models.DateField()

    class Meta:
        unique_together = (('zone', 'unique_number'),)


class LifeForm(models.Model):
    name = models.CharField(max_length=200)


class Species(models.Model):
    name = models.CharField(max_length=200)
    life_form = ForeignKey(LifeForm, on_delete=models.CASCADE, related_name='species')
    possible_planting_period_from = models.DateField()
    possible_planting_period_to = models.DateField()
    flowering_period_from = models.DateField()
    flowering_period_to = models.DateField()
    special_characteristics = models.TextField()

    @property
    def possible_planting_period(self):
        return f"{self.possible_planting_period_from} to {self.possible_planting_period_to}"

    @property
    def flowering_period(self):
        return f"{self.flowering_period_from} to {self.flowering_period_to}"


class PlantWateringSchedule(models.Model):
    plant = models.ForeignKey('Plant', on_delete=models.CASCADE, related_name='schedule')
    frequency = models.CharField(max_length=200)
    time_watering_start = models.TimeField()
    time_watering_end = models.TimeField()
    water_norm_liters_winter = models.IntegerField()
    water_norm_liters_summer = models.IntegerField()
    water_norm_liters_fall = models.IntegerField()
    water_norm_liters_spring = models.IntegerField()

    @property
    def current_water_norm_liters(self):
        seasons = {
            'winter': (12, 1, 2),
            'spring': (3, 4, 5),
            'summer': (6, 7, 8),
            'fall': (9, 10, 11)
        }

        month_now = timezone.now().month

        for season, months in seasons.items():
            if month_now in months:
                field_name = f"water_norm_liters_{season}"
                return getattr(self, field_name, 0)  # Возвращаем значение поля

        return 0

    @property
    def watering_time_period(self):
        return f"{self.time_watering_start} to {self.time_watering_end}"


class Worker(PersonAbstract):
    phone_number = models.CharField(max_length=200)
    address = models.CharField(max_length=200)


class PlantWorkerAssignment(models.Model):
    plant = models.ForeignKey('Plant', on_delete=models.CASCADE, related_name='worker_assignments')
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='worker_assignments')
    date = models.DateField()

    class Meta:
        unique_together = (('plant', 'date'),)

class ObjectWorkerAssignment(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='worker_assignments')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='object_assignments')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

