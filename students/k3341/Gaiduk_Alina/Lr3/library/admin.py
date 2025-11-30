"""
Django admin configuration for library models.
"""
from django.contrib import admin
from .models import (
    Author, Publisher, BookSection, Book, BookAuthor,
    Hall, Reader, BookCopy, BookIssue, HallBookStock, Staff
)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['author_id', 'full_name', 'created_at']
    search_fields = ['full_name']
    list_filter = ['created_at']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['publisher_id', 'name', 'created_at']
    search_fields = ['name']


@admin.register(BookSection)
class BookSectionAdmin(admin.ModelAdmin):
    list_display = ['section_id', 'name', 'created_at']
    search_fields = ['name']


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['book_id', 'title', 'publisher', 'publish_year', 'section', 'cipher']
    search_fields = ['title', 'cipher']
    list_filter = ['publisher', 'section', 'publish_year']
    inlines = [BookAuthorInline]


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['hall_id', 'hall_number', 'name', 'capacity']
    search_fields = ['name']
    list_filter = ['capacity']


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = [
        'reader_id', 'card_number', 'full_name', 'birth_date',
        'education_level', 'has_academic_degree', 'hall', 'is_active'
    ]
    search_fields = ['card_number', 'full_name', 'passport_number']
    list_filter = ['education_level', 'has_academic_degree', 'is_active', 'hall', 'registration_date']
    readonly_fields = ['registration_date', 'last_reregistration_date']


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ['copy_id', 'book', 'hall', 'inventory_number', 'registration_date', 'is_written_off']
    search_fields = ['inventory_number', 'book__title']
    list_filter = ['hall', 'is_written_off', 'registration_date']


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['issue_id', 'reader', 'copy', 'hall', 'issue_date', 'return_date']
    search_fields = ['reader__full_name', 'copy__book__title']
    list_filter = ['hall', 'issue_date', 'return_date']
    readonly_fields = ['issue_date']


@admin.register(HallBookStock)
class HallBookStockAdmin(admin.ModelAdmin):
    list_display = ['hall', 'book', 'copies_total']
    list_filter = ['hall']
    search_fields = ['book__title']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['staff_id', 'login', 'email', 'created_at']
    search_fields = ['login', 'email']
    readonly_fields = ['password_hash']

