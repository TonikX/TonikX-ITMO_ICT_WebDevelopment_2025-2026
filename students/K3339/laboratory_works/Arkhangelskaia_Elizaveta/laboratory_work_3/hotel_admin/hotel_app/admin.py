from django.contrib import admin
from .models import *

admin.site.register(RoomType)
admin.site.register(Rooms)
admin.site.register(Residents)
admin.site.register(Reservation)
admin.site.register(Workers)
admin.site.register(CleaningInformation)
admin.site.register(Cleaning)