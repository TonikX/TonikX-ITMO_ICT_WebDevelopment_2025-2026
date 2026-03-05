from django.contrib import admin

from project_tour_app.models import Tour, Agency, Reservation, Review

# Register your models here.
admin.site.register(Tour)
admin.site.register(Agency)
admin.site.register(Reservation)
admin.site.register(Review)