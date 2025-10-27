from django.contrib import admin
from .models import Reader, Book, Borrowing, Review

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'user', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year', 'available')
    list_filter = ('available', 'year')
    search_fields = ('title', 'author')
    list_editable = ('available',)

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('reader', 'book', 'date_from', 'date_to', 'is_returned')
    list_filter = ('date_from', 'date_to', 'is_returned')
    list_editable = ('is_returned',)
    search_fields = ('reader__first_name', 'reader__last_name', 'book__title')
    
    def save_model(self, request, obj, form, change):
        # При возврате книги делаем её доступной
        if obj.is_returned:
            obj.book.available = True
            obj.book.save()
        else:
            obj.book.available = False
            obj.book.save()
        super().save_model(request, obj, form, change)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reader', 'book', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('reader__first_name', 'reader__last_name', 'book__title', 'comment')
    readonly_fields = ('created_at',)
