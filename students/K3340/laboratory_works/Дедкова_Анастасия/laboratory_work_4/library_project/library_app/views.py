from datetime import timedelta, date
from calendar import monthrange

from django.utils import timezone
from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Author,
    Book,
    ReadingHall,
    Reader,
    BookCopy,
    Loan,
    STATUS_ON_LOAN,
    STATUS_WRITTEN_OFF,
)
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    ReadingHallSerializer,
    ReaderSerializer,
    BookCopySerializer,
    LoanSerializer,
)


# Авторы

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by("full_name")
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]


# Книги

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("title")
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

# Экземпляры книг

class BookCopyViewSet(viewsets.ModelViewSet):
    queryset = BookCopy.objects.select_related("book", "hall").all()
    serializer_class = BookCopySerializer
    permission_classes = [AllowAny]

    # GET /api/copies/on-loan/
    @action(detail=False, methods=["get"], url_path="on-loan")
    def on_loan(self, request):
        """
        Возвращает все экземпляры книг, которые сейчас на руках.
        """
        qs = (
            BookCopy.objects
            .filter(status=STATUS_ON_LOAN)
            .select_related("book", "hall")
            .order_by("book__title")
        )
        serializer = self.get_serializer(qs, many=True, context={"request": request})
        return Response(serializer.data)


# Залы

class ReadingHallViewSet(viewsets.ModelViewSet):
    queryset = ReadingHall.objects.all().order_by("number")
    serializer_class = ReadingHallSerializer
    permission_classes = [AllowAny]


# Читатели

class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all().order_by("full_name")
    serializer_class = ReaderSerializer
    permission_classes = [AllowAny]

    # Какие книги закреплены за заданным читателем?
    #
    # GET /api/readers/<id>/books/
    @action(detail=True, methods=["get"], url_path="books")
    def books(self, request, pk=None):
        reader = self.get_object()
        loans_qs = (
            Loan.objects
            .filter(reader=reader, returned_at__isnull=True)
            .select_related("copy", "copy__book", "copy__hall")
        )
        copies = [loan.copy for loan in loans_qs]
        serializer = BookCopySerializer(copies, many=True, context={"request": request})
        return Response(serializer.data)

    # Кто из читателей взял книгу более месяца тому назад?
    #
    # GET /api/readers/with-old-loans/
    @action(detail=False, methods=["get"], url_path="with-old-loans")
    def with_old_loans(self, request):
        today = timezone.now()
        cutoff = today - timedelta(days=30)

        readers_qs = (
            Reader.objects
            .filter(
                loans__assigned_at__lt=cutoff,
                loans__returned_at__isnull=True,
            )
            .distinct()
            .order_by("full_name")
        )

        serializer = ReaderSerializer(readers_qs, many=True, context={"request": request})
        return Response(serializer.data)

    # За кем из читателей закреплены книги, количество экземпляров которых в библиотеке не превышает 2?
    #
    # GET /api/readers/with-rare-books/
    @action(detail=False, methods=["get"], url_path="with-rare-books")
    def with_rare_books(self, request):
        # считаем количество экземпляров по каждой книге
        # в библиотеке все книги, кроме списанных
        books_with_few_copies = (
            BookCopy.objects
            .exclude(status=STATUS_WRITTEN_OFF)
            .values("book_id")
            .annotate(total=Count("copy_id"))
            .filter(total__lte=2)
            .values_list("book_id", flat=True)
        )

        # находим активные выдачи таких редких книг
        rare_loans = (
            Loan.objects
            .filter(
                returned_at__isnull=True,
                copy__book_id__in=books_with_few_copies,
            )
        )

        # читатели, за которыми такие книги числятся
        readers_qs = (
            Reader.objects
            .filter(loans__in=rare_loans)
            .distinct()
            .order_by("full_name")
        )

        serializer = ReaderSerializer(readers_qs, many=True, context={"request": request})
        return Response(serializer.data)

    # Сколько в библиотеке читателей младше 20 лет?
    #
    # GET /api/readers/younger-than-20/
    @action(detail=False, methods=["get"], url_path="younger-than-20")
    def younger_than_20(self, request):
        today = timezone.now().date()

        try:
            twenty_years_ago = today.replace(year=today.year - 20)
        except ValueError:
            # на случай 29 февраля
            twenty_years_ago = today.replace(month=2, day=28, year=today.year - 20)

        # младше 20
        qs = Reader.objects.filter(birth_date__gt=twenty_years_ago)
        count = qs.count()

        return Response({
            "younger_than_20": count,
        })

    # Статистика по образованию и учёной степени
    #
    # GET /api/readers/education-stats/
    @action(detail=False, methods=["get"], url_path="education-stats")
    def education_stats(self, request):
        """
        Возвращает статистику по уровню образования и наличию учёной степени
        в процентах от общего числа читателей.
        """
        total = Reader.objects.count()
        if total == 0:
            return Response({
                "total_readers": 0,
                "by_education": {},
                "academic_degree": {
                    "with_degree_percent": 0.0,
                    "without_degree_percent": 0.0,
                },
            })

        # Группируем по уровню образования
        education_counts = (
            Reader.objects
            .values("education_level")
            .annotate(count=Count("reader_id"))
        )

        by_education = {}
        for item in education_counts:
            level = item["education_level"] or "не указано"
            count = item["count"]
            percent = round(count * 100.0 / total, 2)
            by_education[level] = {
                "count": count,
                "percent": percent,
            }

        # Статистика по учёной степени
        with_degree = Reader.objects.filter(has_academic_degree=True).count()
        without_degree = total - with_degree

        with_degree_percent = round(with_degree * 100.0 / total, 2)
        without_degree_percent = round(without_degree * 100.0 / total, 2)

        data = {
            "total_readers": total,
            "by_education": by_education,
            "academic_degree": {
                "with_degree": with_degree,
                "with_degree_percent": with_degree_percent,
                "without_degree": without_degree,
                "without_degree_percent": without_degree_percent,
            },
        }

        return Response(data)

    @action(detail=False, methods=["get"])
    def older_than_20(self, request):
        """
        Возвращает количество читателей, которым больше 20 лет.
        """
        today = timezone.now().date()
        cutoff_date = today.replace(year=today.year - 20)

        count = Reader.objects.filter(
            birth_date__lt=cutoff_date
        ).count()

        return Response({"older_than_20": count})


    @action(detail=False, methods=["get"], url_path="find-by-card")
    def find_by_card(self, request):
        """
        Поиск читателя по номеру билета и паспорту.
        Возвращает данные читателя + его активные не возвращённые выдачи.
        """
        card = request.query_params.get("card_number")
        passport = request.query_params.get("passport_number")

        if not card or not passport:
            return Response(
                {"detail": "Нужно передать параметры card_number и passport_number."},
                status=400,
            )

        try:
            reader = Reader.objects.get(
                card_number=card,
                passport_number=passport,
            )
        except Reader.DoesNotExist:
            return Response(
                {"detail": "Читатель с такими данными не найден."},
                status=404,
            )

        today = timezone.now().date()

        # активные не возвращённые выдачи этого читателя
        loans_qs = (
            Loan.objects
            .filter(reader=reader, returned_at__isnull=True)
            .select_related("copy", "copy__book")
            .order_by("assigned_at")
        )

        active_loans = []
        for loan in loans_qs:
            assigned_date = loan.assigned_at.date()
            days_on_loan = (today - assigned_date).days

            active_loans.append({
                "loan_id": loan.loan_id,
                "book_id": loan.copy.book.book_id,
                "book_title": loan.copy.book.title,
                "assigned_at": assigned_date.isoformat(),
                "days_on_loan": days_on_loan,
                "is_overdue": days_on_loan > 10,  # > 10 дней — будем красить
            })

        reader_data = {
            "id": reader.reader_id,
            "full_name": reader.full_name,
            "card_number": reader.card_number,
            "passport_number": reader.passport_number,
            "hall": reader.hall.name if reader.hall else None,
            "education_level": reader.education_level,
            "has_academic_degree": reader.has_academic_degree,
        }

        return Response({
            "reader": reader_data,
            "active_loans": active_loans,
        })

    # Все выдачи конкретного читателя.
    #
    # GET /api/readers/1/loans/
    @action(detail=True, methods=["get"], url_path="loans")
    def loans(self, request, pk=None):
        reader = self.get_object()           # Reader
        loans = reader.loans.select_related("copy", "copy__book")
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)


# Выдачи

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.select_related("reader", "copy", "copy__book").all()
    serializer_class = LoanSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request):
        """
        Возвращает все книги, которые сейчас на руках.
        """
        active_loans = (
            Loan.objects
            .filter(returned_at__isnull=True)
            .select_related("copy", "copy__book", "reader")
        )

        data = []
        now = timezone.now()

        for loan in active_loans:
            book = loan.copy.book

            authors = Author.objects.filter(bookauthor__book=book)

            data.append({
                "loan_id": loan.loan_id,
                "copy_id": loan.copy.copy_id,
                "assigned_at": loan.assigned_at,
                "days_on_loan": (now - loan.assigned_at).days,

                "book": {
                    "id": book.book_id,
                    "title": book.title,
                    "publisher": book.publisher,
                    "year": book.publication_year,
                    "section": book.section,
                    "authors": [a.full_name for a in authors],
                },

                "reader": {
                    "id": loan.reader.reader_id,
                    "full_name": loan.reader.full_name,
                },

                "hall": loan.copy.hall.name,
                "status": loan.copy.status,
            })

        return Response(data)


# Отчёт за месяц

class MonthlyReportView(APIView):

    def get(self, request):
        # Определяем месяц и год (если не переданы - берём текущие)
        today = timezone.now().date()
        year = int(request.query_params.get("year", today.year))
        month = int(request.query_params.get("month", today.month))

        # 1 число месяца
        start_date = date(year, month, 1)
        # последний день месяца
        last_day = monthrange(year, month)[1]
        end_date = date(year, month, last_day)

        halls = list(ReadingHall.objects.all())

        report = {
            "year": year,
            "month": month,
            "per_day": [],
            "new_readers": {
                "total": 0,
                "by_hall": []
            }
        }

        # Для каждого дня считаем книги/читателей по залам
        current = start_date
        while current <= end_date:
            day_entry = {
                "date": current.isoformat(),
                "halls": [],
                "total_books": 0,
                "total_readers": 0,
            }

            for hall in halls:
                books_count = BookCopy.objects.filter(
                    hall=hall,
                    date_received__lte=current
                ).filter(
                    Q(date_written_off__isnull=True) |
                    Q(date_written_off__gt=current)
                ).count()

                readers_count = Reader.objects.filter(
                    hall=hall,
                    registered_at__lte=current,
                    is_active=True,
                ).count()

                day_entry["halls"].append({
                    "hall_id": hall.hall_id,
                    "hall_name": hall.name,
                    "books": books_count,
                    "readers": readers_count,
                })

                day_entry["total_books"] += books_count
                day_entry["total_readers"] += readers_count

            report["per_day"].append(day_entry)
            current += timedelta(days=1)

        # Сколько читателей записалось за этот месяц
        new_readers_qs = Reader.objects.filter(
            registered_at__gte=start_date,
            registered_at__lte=end_date,
        ).select_related("hall")

        total_new = new_readers_qs.count()
        report["new_readers"]["total"] = total_new

        by_hall = {}
        for hall in halls:
            by_hall[hall.hall_id] = {
                "hall_id": hall.hall_id,
                "hall_name": hall.name,
                "count": 0,
            }

        for r in new_readers_qs:
            if r.hall_id is not None:
                by_hall[r.hall_id]["count"] += 1

        report["new_readers"]["by_hall"] = list(by_hall.values())

        return Response(report)
