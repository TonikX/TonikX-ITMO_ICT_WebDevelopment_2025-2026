from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    passport_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Passport Number")
    home_address = models.TextField(blank=True, null=True, verbose_name="Home Address")
    nationality = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nationality")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    
    # Racing-specific fields
    racing_experience = models.IntegerField(default=0, verbose_name="Racing Experience (years)")
    racing_class = models.CharField(max_length=50, blank=True, null=True, verbose_name="Racing Class")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Team Name")
    description = models.TextField(blank=True, null=True, verbose_name="Team Description")
    founded_date = models.DateField(null=True, blank=True, verbose_name="Founded Date")
    
    def __str__(self):
        return self.name

class Car(models.Model):
    license_plate = models.CharField(max_length=10, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=30, blank=True)
    
    # Racing-specific fields
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Racing Team")
    car_description = models.TextField(blank=True, null=True, verbose_name="Car Description")
    max_speed = models.IntegerField(null=True, blank=True, verbose_name="Max Speed (km/h)")
    engine_power = models.IntegerField(null=True, blank=True, verbose_name="Engine Power (HP)")
    
    def __str__(self):
        return f"{self.brand} {self.model} - {self.license_plate}"

class Race(models.Model):
    RACE_TYPES = [
        ('FORMULA', 'Formula Racing'),
        ('RALLY', 'Rally'),
        ('ENDURANCE', 'Endurance'),
        ('DRAG', 'Drag Racing'),
        ('DRIFT', 'Drifting'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Race Name")
    race_type = models.CharField(max_length=20, choices=RACE_TYPES, verbose_name="Race Type")
    location = models.CharField(max_length=200, verbose_name="Race Location")
    date = models.DateField(verbose_name="Race Date")
    description = models.TextField(blank=True, null=True, verbose_name="Race Description")
    
    def __str__(self):
        return f"{self.name} - {self.get_race_type_display()}"

class RaceRegistration(models.Model):
    racer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Racer")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Race Car")
    race = models.ForeignKey(Race, on_delete=models.CASCADE, verbose_name="Race Event")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Registration Date")
    
    # Race results (filled by admin)
    lap_time = models.DurationField(null=True, blank=True, verbose_name="Best Lap Time")
    final_position = models.IntegerField(null=True, blank=True, verbose_name="Final Position")
    completed_laps = models.IntegerField(default=0, verbose_name="Completed Laps")
    dnf = models.BooleanField(default=False, verbose_name="Did Not Finish")
    
    class Meta:
        unique_together = ['racer', 'race']
    
    def __str__(self):
        return f"{self.racer} - {self.race}"

class RaceComment(models.Model):
    COMMENT_TYPES = [
        ('COLLABORATION', 'Question about collaboration'),
        ('RACE_INFO', 'Question about races'),
        ('OTHER', 'Other'),
    ]
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Comment Author")
    race = models.ForeignKey(Race, on_delete=models.CASCADE, verbose_name="Race")
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPES, verbose_name="Comment Type")
    text = models.TextField(verbose_name="Comment Text")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)], verbose_name="Rating (1-10)")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    
    def __str__(self):
        return f"Comment by {self.author} on {self.race}"