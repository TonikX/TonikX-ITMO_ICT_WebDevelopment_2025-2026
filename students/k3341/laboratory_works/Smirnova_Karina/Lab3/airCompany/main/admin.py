from django.contrib import admin
from .models import AirlineCompany, Plane, Crew, CrewMember, Route, Flight, TransitLanding

admin.site.register(AirlineCompany)
admin.site.register(Plane)
admin.site.register(Crew)
admin.site.register(CrewMember)
admin.site.register(Route)
admin.site.register(Flight)
admin.site.register(TransitLanding)
