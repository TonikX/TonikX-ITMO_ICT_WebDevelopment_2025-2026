from django.contrib import admin

# Register your models here.
from .models import Race, Racer, User, Results, Comments

admin.site.register(Race)
admin.site.register(Racer)
admin.site.register(User)
admin.site.register(Results)
admin.site.register(Comments)