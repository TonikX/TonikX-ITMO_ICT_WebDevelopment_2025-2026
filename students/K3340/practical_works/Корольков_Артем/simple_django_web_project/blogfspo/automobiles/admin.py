# automobiles/admin.py

from django.contrib import admin
from django.utils import timezone
from .models import Owner, Car, Ownership, DriverLicense


class OwnershipInline(admin.TabularInline):
    """Встроенное отображение владений в админке владельца и автомобиля"""
    model = Ownership
    extra = 1
    fields = ['car', 'start_date', 'end_date']
    autocomplete_fields = ['car']


class DriverLicenseInline(admin.TabularInline):
    """Встроенное отображение водительских удостоверений"""
    model = DriverLicense
    extra = 1
    fields = ['license_number', 'license_type', 'issue_date', 'expiry_date']


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_full_name', 'phone', 'passport_number', 'nationality', 'get_short_address']
    list_filter = ['birth_date', 'nationality']
    search_fields = ['first_name', 'last_name', 'phone', 'passport_number', 'address']
    list_editable = ['phone', 'nationality']
    inlines = [OwnershipInline, DriverLicenseInline]
    # Поля для формы редактирования
    fieldsets = [
        ('Основная информация', {
            'fields': [
                'first_name',
                'last_name',
                'birth_date',
                'phone'
            ]
        }),
        ('Паспортные данные', {
            'fields': [
                'passport_number',
            ]
        }),
        ('Адрес и гражданство', {
            'fields': [
                'address',
                'nationality'
            ]
        }),
    ]
    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = 'ФИО'

    def get_phone(self, obj):
        return obj.phone if obj.phone else "Не указан"

    get_phone.short_description = 'Телефон'

    def get_short_address(self, obj):
        return obj.get_short_address() if obj.address else "Не указан"

    get_short_address.short_description = 'Адрес'


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'state_number', 'color', 'get_current_owner']
    list_filter = ['brand', 'color']
    search_fields = ['brand', 'model', 'state_number']
    inlines = [OwnershipInline]

    def get_current_owner(self, obj):
        owner = obj.get_current_owner()
        return owner.get_full_name() if owner else "Нет владельца"

    get_current_owner.short_description = 'Текущий владелец'


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ['owner', 'car', 'start_date', 'end_date', 'get_is_current']
    list_filter = ['start_date', 'end_date']
    search_fields = ['owner__first_name', 'owner__last_name', 'car__brand', 'car__model']
    date_hierarchy = 'start_date'
    autocomplete_fields = ['owner', 'car']

    def get_is_current(self, obj):
        return obj.is_current()

    get_is_current.short_description = 'Текущее владение'
    get_is_current.boolean = True


@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ['license_number', 'owner', 'license_type', 'issue_date', 'get_expiry_date', 'get_is_valid']
    list_filter = ['license_type', 'issue_date']
    search_fields = ['license_number', 'owner__first_name', 'owner__last_name']
    autocomplete_fields = ['owner']

    def get_expiry_date(self, obj):
        return obj.expiry_date if obj.expiry_date else "Не указана"

    get_expiry_date.short_description = 'Срок действия'

    def get_is_valid(self, obj):
        return obj.is_valid()

    get_is_valid.short_description = 'Действителен'
    get_is_valid.boolean = True