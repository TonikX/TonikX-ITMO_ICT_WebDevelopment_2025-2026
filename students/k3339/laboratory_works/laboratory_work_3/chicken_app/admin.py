from django.contrib import admin

from chicken_app.models import Chicken, Employee, Breed, Diet, ResponsibleEmployee, LaborContract, Workshop, Cell

admin.site.register(Chicken)
admin.site.register(Breed)
admin.site.register(Employee)
admin.site.register(Diet)
admin.site.register(ResponsibleEmployee)
admin.site.register(LaborContract)
admin.site.register(Cell)
admin.site.register(Workshop)
