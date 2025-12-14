from django.contrib import admin
from .models import Airport, Company, Plane, Flight, Seat, Passenger, Ticket, CrewMember, Crew

# Register your models here.
admin.site.register(Airport)
admin.site.register(Company)
admin.site.register(Plane)
admin.site.register(Flight)
admin.site.register(Seat)
admin.site.register(Passenger)
admin.site.register(Ticket)
admin.site.register(CrewMember)
admin.site.register(Crew)
