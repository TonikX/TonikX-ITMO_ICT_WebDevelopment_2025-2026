from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Author, Customer, Book, Contract, Order, BookAuthor, BookEditor, OrderItem

admin.site.register(User, UserAdmin)
admin.site.register(Author)
admin.site.register(Customer)
admin.site.register(Contract)


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1  # Количество пустых строк для добавления


class BookEditorInline(admin.TabularInline):
    model = BookEditor
    extra = 1


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'pages_count')
    inlines = [BookAuthorInline, BookEditorInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at')
    inlines = [OrderItemInline]
