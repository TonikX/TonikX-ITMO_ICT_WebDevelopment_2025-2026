from django.contrib import admin
from .models import Hotel, RoomType, Room, Reservation, Review

admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Review)
