from django.contrib import admin
from .models import Author, Book, BookAuthor, ReadingHall, Reader, BookCopy, Loan, STATUS_AVAILABLE
from django.db.models import Q
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils import timezone

class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1
    verbose_name = "Автор"
    verbose_name_plural = "Авторы книги"



# авторы

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("author_id", "full_name")
    search_fields = ("full_name",)


# книги

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("book_id", "title", "publisher", "publication_year", "cipher", "is_active")
    search_fields = ("title", "cipher")
    list_filter = ("publisher", "publication_year", "section", "is_active")
    inlines = [BookAuthorInline]


@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ("book_author_id", "book", "author")
    list_filter = ("author", "book")


# залы

@admin.register(ReadingHall)
class ReadingHallAdmin(admin.ModelAdmin):
    list_display = ("hall_id", "number", "name", "capacity")
    search_fields = ("name", "number")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "monthly-report/",
                self.admin_site.admin_view(self.monthly_report_view),
                name="library_app_monthly_report",
            ),
        ]
        return custom_urls + urls

    def monthly_report_view(self, request):
        today = timezone.now().date()
        year = request.GET.get("year", today.year)
        month = request.GET.get("month", today.month)

        api_url = reverse("monthly-report") + f"?year={year}&month={month}"
        return redirect(api_url)

# Читатели


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = (
        "reader_id",
        "full_name",
        "card_number",
        "education_level",
        "has_academic_degree",
        "hall",
        "is_active",
    )
    search_fields = ("full_name", "card_number", "passport_number")
    list_filter = ("hall", "education_level", "has_academic_degree", "is_active")
    readonly_fields = ("registered_at",)


# Экземпляр книги


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ("copy_id", "book", "hall", "status", "date_received", "date_written_off")
    list_filter = ("hall", "status", "book")
    search_fields = ("copy_id", "book__title", "book__cipher")


# Выдача книги


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("loan_id", "reader", "copy", "assigned_at", "returned_at")
    list_filter = ("assigned_at", "returned_at")
    search_fields = ("reader__full_name", "reader__card_number", "copy__book__title")
    autocomplete_fields = ("reader",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("reader", "copy", "copy__book")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Для поля 'copy' при создании выдачи отображаем только экземпляры со статусом 'available';
        """
        if db_field.name == "copy":
            # по умолчанию - только доступные экземпляры
            qs = BookCopy.objects.filter(status=STATUS_AVAILABLE)

            object_id = request.resolver_match.kwargs.get("object_id")
            if object_id:
                try:
                    current_loan = Loan.objects.get(pk=object_id)
                    qs = BookCopy.objects.filter(
                        Q(pk=current_loan.copy_id) | Q(status=STATUS_AVAILABLE)
                    )
                except Loan.DoesNotExist:
                    pass

            kwargs["queryset"] = qs

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
