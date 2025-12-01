from django.contrib import admin

from .models import CleaningAssignment, Employee


class CleaningAssignmentInline(admin.TabularInline):
    model = CleaningAssignment
    extra = 1


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'status', 'hire_date')
    list_filter = ('status',)
    inlines = [CleaningAssignmentInline]
