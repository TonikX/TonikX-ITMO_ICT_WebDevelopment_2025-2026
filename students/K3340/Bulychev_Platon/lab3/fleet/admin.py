from django.contrib import admin
from .models import BusType, Bus, Route, Driver, Schedule, Absence

admin.site.register(BusType)
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Driver)
admin.site.register(Schedule)
admin.site.register(Absence)
