from django.contrib import admin

from .models import Hotel, HotelUser, RoomType, Facility, Reservation, Review

admin.site.register(Hotel)
admin.site.register(HotelUser)
admin.site.register(RoomType)
admin.site.register(Facility)
admin.site.register(Reservation)
admin.site.register(Review)