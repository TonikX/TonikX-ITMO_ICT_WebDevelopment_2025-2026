from django.contrib import admin
from .models import Employee, Author, Book, FinancialStatus, Report


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'department', 'hire_date', 'salary']
    list_filter = ['position', 'department', 'hire_date']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'position']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'middle_name', 'email', 'birth_date']
    list_filter = ['birth_date']
    search_fields = ['first_name', 'last_name', 'middle_name', 'email']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'status', 'publication_date', 'print_run', 'price', 'cost']
    list_filter = ['status', 'publication_date', 'print_date']
    search_fields = ['title', 'isbn']
    filter_horizontal = ['authors']


@admin.register(FinancialStatus)
class FinancialStatusAdmin(admin.ModelAdmin):
    list_display = ['date', 'transaction_type', 'category', 'amount', 'book']
    list_filter = ['transaction_type', 'category', 'date']
    search_fields = ['description']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'created_by', 'created_at']
    list_filter = ['report_type', 'created_at']
    search_fields = ['title']
