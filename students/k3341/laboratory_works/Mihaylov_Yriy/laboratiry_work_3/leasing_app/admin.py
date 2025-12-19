from django.contrib import admin
from .models import (
    AdminUser,
    Car,
    Client,
    LeaseApplication,
    Lease,
    MaintenanceCompany,
    Maintenance,
)

admin.site.register(AdminUser)
admin.site.register(Car)
admin.site.register(Client)
admin.site.register(LeaseApplication)
admin.site.register(Lease)
admin.site.register(MaintenanceCompany)
admin.site.register(Maintenance)