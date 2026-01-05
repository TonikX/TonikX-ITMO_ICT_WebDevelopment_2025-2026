# carApp/admin.py
from django.contrib import admin
from .models import (
    Owner, OwnerContact, DriverLicense,
    VehicleModel, Car, Ownership,
    InsurancePolicy, ServiceRecord, Registration,
)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_model_display', 'vin', 'registration_number', 'year')
    search_fields = ('vin', 'registration_number', 'vehicle_model__manufacturer', 'vehicle_model__model')
    list_filter = ('vehicle_model__manufacturer', 'year')

    def vehicle_model_display(self, obj):
        if obj.vehicle_model:
            return f"{obj.vehicle_model.manufacturer} {obj.vehicle_model.model}"
        return "-"
    vehicle_model_display.short_description = 'Model'

# Register other models simply (adjust as you need)
admin.site.register(Owner)
admin.site.register(OwnerContact)
admin.site.register(DriverLicense)
admin.site.register(VehicleModel)
admin.site.register(Ownership)
admin.site.register(InsurancePolicy)
admin.site.register(ServiceRecord)
admin.site.register(Registration)