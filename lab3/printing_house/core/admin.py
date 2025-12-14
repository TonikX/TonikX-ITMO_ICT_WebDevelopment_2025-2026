from django.contrib import admin
from .models import (
    Employee, Manager, Editor, Author, Book, Contract, ContractAuthor,
    BookEditor, Customer, Order, OrderItem, FinancialRecord,
    Newspaper, PrintingHouse, PostOffice, PrintingRun, Distribution
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'hire_date', 'salary']
    list_filter = ['position', 'hire_date']
    search_fields = ['user__first_name', 'user__last_name', 'position']


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'hire_date', 'salary']
    list_filter = ['department', 'hire_date']
    search_fields = ['user__first_name', 'user__last_name', 'department']


@admin.register(Editor)
class EditorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'experience_years', 'hire_date']
    list_filter = ['specialization', 'experience_years']
    search_fields = ['user__first_name', 'user__last_name', 'specialization']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'birth_date', 'contact_email']
    list_filter = ['birth_date']
    search_fields = ['first_name', 'last_name', 'middle_name', 'contact_email']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'publication_date', 'price', 'genre']
    list_filter = ['genre', 'publication_date']
    search_fields = ['title', 'isbn', 'description']


class ContractAuthorInline(admin.TabularInline):
    model = ContractAuthor
    extra = 1


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['contract_number', 'book', 'manager', 'signing_date', 'status', 'total_amount']
    list_filter = ['status', 'signing_date', 'manager']
    search_fields = ['contract_number', 'book__title', 'manager__user__first_name']
    inlines = [ContractAuthorInline]


@admin.register(ContractAuthor)
class ContractAuthorAdmin(admin.ModelAdmin):
    list_display = ['contract', 'author', 'order_on_cover', 'royalty_percentage', 'royalty_amount']
    list_filter = ['order_on_cover']


class BookEditorInline(admin.TabularInline):
    model = BookEditor
    extra = 1


@admin.register(BookEditor)
class BookEditorAdmin(admin.ModelAdmin):
    list_display = ['book', 'editor', 'is_lead_editor', 'start_date', 'end_date']
    list_filter = ['is_lead_editor', 'start_date']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'customer_type', 'email']
    list_filter = ['customer_type']
    search_fields = ['name', 'contact_person', 'email']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'order_date', 'status', 'total_amount']
    list_filter = ['status', 'order_date']
    search_fields = ['order_number', 'customer__name']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity', 'unit_price', 'total_price']
    list_filter = ['order__order_date']


@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = ['date', 'record_type', 'amount', 'description', 'related_contract', 'related_order']
    list_filter = ['record_type', 'date']
    search_fields = ['description']


# Админка для моделей газетной системы

@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'publication_index', 'editor_full_name', 'price_per_copy']
    list_filter = ['price_per_copy']
    search_fields = ['title', 'publication_index', 'editor_last_name', 'editor_first_name']
    
    def editor_full_name(self, obj):
        return obj.editor_full_name
    editor_full_name.short_description = 'Редактор'


@admin.register(PrintingHouse)
class PrintingHouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'address']


@admin.register(PostOffice)
class PostOfficeAdmin(admin.ModelAdmin):
    list_display = ['number', 'address']
    search_fields = ['number', 'address']


@admin.register(PrintingRun)
class PrintingRunAdmin(admin.ModelAdmin):
    list_display = ['printing_house', 'newspaper', 'circulation']
    list_filter = ['printing_house', 'circulation']
    search_fields = ['printing_house__name', 'newspaper__title']


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ['post_office', 'newspaper', 'printing_house', 'quantity']
    list_filter = ['post_office', 'printing_house']
    search_fields = ['post_office__number', 'newspaper__title', 'printing_house__name']