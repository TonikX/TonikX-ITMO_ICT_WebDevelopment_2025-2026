from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CarOwner, Car, DriverLicense, Ownership


@admin.register(CarOwner)
class CarOwnerAdmin(UserAdmin):
    """Админка для владельцев автомобилей (расширенная модель User)"""

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "passport_number",
        "nationality",
        "is_staff",
    )
    search_fields = ("username", "first_name", "last_name", "email", "passport_number")
    list_filter = ("is_staff", "is_superuser", "is_active", "nationality")

    # Добавляем наши кастомные поля в fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (
            "Дополнительная информация",
            {
                "fields": (
                    "birth_date",
                    "passport_number",
                    "home_address",
                    "nationality",
                )
            },
        ),
    )

    # Добавляем кастомные поля при создании пользователя
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Дополнительная информация",
            {
                "fields": (
                    "birth_date",
                    "passport_number",
                    "home_address",
                    "nationality",
                )
            },
        ),
    )


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "license_plate", "brand", "model", "color")
    search_fields = ("license_plate", "brand", "model")
    list_filter = ("brand",)


@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "license_number", "type", "issue_date")
    search_fields = ("license_number", "owner__last_name")
    list_filter = ("type",)


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "car", "start_date", "end_date")
    search_fields = ("owner__last_name", "car__license_plate")
    list_filter = ("start_date",)
