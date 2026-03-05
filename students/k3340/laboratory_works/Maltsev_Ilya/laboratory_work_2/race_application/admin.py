from django.contrib import admin

from race_application.models import User, Racer, Race, RaceConnection, Review

admin.site.register(User)
admin.site.register(Racer)
admin.site.register(Race)
admin.site.register(RaceConnection)
admin.site.register(Review)
