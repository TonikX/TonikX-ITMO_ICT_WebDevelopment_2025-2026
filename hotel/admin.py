from django.contrib import admin
from .models import Floor, Room, Client, StayRecord, Employee, CleaningSchedule, CleaningRecord

# Регистрация моделей
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Client)
admin.site.register(StayRecord)
admin.site.register(Employee)
admin.site.register(CleaningSchedule)
admin.site.register(CleaningRecord)
