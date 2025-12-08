from django.contrib import admin
from django.contrib import admin
from .models import BusType, Bus, Route, Driver, WorkShift

admin.site.register(BusType)
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Driver)
admin.site.register(WorkShift)