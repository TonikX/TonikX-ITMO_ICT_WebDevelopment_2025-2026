from django.contrib import admin
from .models import Reader, Book, Borrowing

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year', 'available')
    list_filter = ('available', 'year')
    search_fields = ('title', 'author')

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('reader', 'book', 'date_from', 'date_to')
    list_filter = ('date_from', 'date_to')
