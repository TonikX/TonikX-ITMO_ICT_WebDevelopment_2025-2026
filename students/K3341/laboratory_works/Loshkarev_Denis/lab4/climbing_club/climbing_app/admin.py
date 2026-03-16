from django.contrib import admin
from .models import Club, Alpinist, Mountain, Route, Climb, Participation

admin.site.register(Club)
admin.site.register(Alpinist)
admin.site.register(Mountain)
admin.site.register(Route)
admin.site.register(Climb)
admin.site.register(Participation)
