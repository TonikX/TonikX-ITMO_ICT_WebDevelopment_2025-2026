from django.contrib import admin
from .models import ReadingRoom, Reader, Book, BookCopy, BookAssignment


@admin.register(ReadingRoom)
class ReadingRoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'capacity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['number', 'name']
    ordering = ['number']


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'full_name', 'education', 'has_degree', 'reading_room', 'is_active', 'registration_date']
    list_filter = ['education', 'has_degree', 'is_active', 'reading_room', 'registration_date']
    search_fields = ['ticket_number', 'full_name', 'passport_number', 'phone_number']
    ordering = ['ticket_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'authors', 'publisher', 'publication_year', 'section', 'is_active']
    list_filter = ['is_active', 'publication_year', 'section']
    search_fields = ['title', 'authors', 'code', 'section']
    ordering = ['title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ['book', 'reading_room', 'quantity', 'created_at']
    list_filter = ['reading_room', 'created_at']
    search_fields = ['book__title', 'reading_room__name']
    ordering = ['book', 'reading_room']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(BookAssignment)
class BookAssignmentAdmin(admin.ModelAdmin):
    list_display = ['book', 'reader', 'assignment_date', 'return_date', 'is_returned']
    list_filter = ['is_returned', 'assignment_date', 'return_date']
    search_fields = ['book__title', 'reader__full_name', 'reader__ticket_number']
    ordering = ['-assignment_date']
    readonly_fields = ['created_at']
