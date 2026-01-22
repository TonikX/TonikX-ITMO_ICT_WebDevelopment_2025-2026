from django.contrib import admin
from .models import CarOwner
from .models import Car
from .models import Ownership
from .models import DriversLicense

admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(Ownership)
admin.site.register(DriversLicense)

# Register your models here.
