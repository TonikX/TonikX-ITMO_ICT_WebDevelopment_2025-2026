from django.contrib import admin
from .models import Room, Client, Stay, Employee, CleaningSchedule

admin.site.register(Room)
admin.site.register(Client)
admin.site.register(Stay)
admin.site.register(Employee)
admin.site.register(CleaningSchedule)