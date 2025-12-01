from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('passport_number', 'last_name', 'first_name', 'city')
    search_fields = ('passport_number', 'last_name', 'first_name', 'city')
