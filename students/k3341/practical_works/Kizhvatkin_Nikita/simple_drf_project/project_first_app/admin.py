from django.contrib import admin
from .models import Car, License, Ownership, Owner


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    pass


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    pass


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    pass
