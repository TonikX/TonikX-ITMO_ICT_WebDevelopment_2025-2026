from django.contrib import admin
from .models import Author, Book, BookAuthor, ReadingHall, Reader, CopyOfBook, LoanRecord


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['author_id', 'full_name', 'birth_date']
    search_fields = ['full_name']
    list_per_page = 20


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['book_id', 'title', 'publisher', 'publication_year', 'section', 'inventory_code', 'is_in_catalog']
    list_filter = ['publication_year', 'section', 'is_in_catalog']
    search_fields = ['title', 'inventory_code', 'publisher']
    list_per_page = 20


@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ['book_author_id', 'book_id', 'author_id', 'author_order']
    list_filter = ['author_id']
    list_per_page = 20


@admin.register(ReadingHall)
class ReadingHallAdmin(admin.ModelAdmin):
    list_display = ['hall_id', 'name', 'hall_number', 'capacity']
    search_fields = ['name']
    list_per_page = 20


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ['reader_id', 'full_name', 'library_card_id', 'birth_date', 'education_level', 'hall_id', 'is_active_member']
    list_filter = ['education_level', 'is_active_member', 'hall_id']
    search_fields = ['full_name', 'library_card_id', 'passport']
    list_per_page = 20


@admin.register(CopyOfBook)
class CopyOfBookAdmin(admin.ModelAdmin):
    list_display = ['copy_book_id', 'book_id', 'hall_id', 'availability_status', 'copy_condition', 'received_date']
    list_filter = ['availability_status', 'copy_condition', 'hall_id']
    search_fields = ['book_id__title']
    list_per_page = 20


@admin.register(LoanRecord)
class LoanRecordAdmin(admin.ModelAdmin):
    list_display = ['loan_id', 'reader_id', 'copy_book_id', 'issued_at', 'due_date', 'returned_at']
    list_filter = ['issued_at', 'returned_at']
    search_fields = ['reader_id__full_name', 'copy_book_id__book_id__title']
    list_per_page = 20