from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Reader, Loan, BookStock

@extend_schema(tags=["Analytics"])
class ReaderBooksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reader_id: int):
        qs = (
            Loan.objects
            .filter(reader_id=reader_id, returned_at__isnull=True)
            .select_related("book", "hall", "reader")
            .prefetch_related("book__authors")
        )

        data = []
        for loan in qs:
            data.append({
                "loan_id": loan.id,
                "assigned_at": loan.assigned_at,
                "qty": loan.qty,
                "hall": {"id": loan.hall_id, "name": loan.hall.name},
                "book": {
                    "id": loan.book_id,
                    "title": loan.book.title,
                    "authors": [{"id": a.id, "full_name": a.full_name} for a in loan.book.authors.all()],
                }
            })

        return Response({
            "reader_id": reader_id,
            "active_loans": data
        })

@extend_schema(tags=["Analytics"])
class OverdueLoansAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get("days", 30))
        cutoff = timezone.now().date() - timedelta(days=days)

        qs = (
            Loan.objects
            .filter(returned_at__isnull=True, assigned_at__lte=cutoff)
            .select_related("reader", "book", "hall")
            .order_by("assigned_at")
        )

        data = [{
            "loan_id": l.id,
            "assigned_at": l.assigned_at,
            "days": days,
            "reader": {"id": l.reader_id, "full_name": l.reader.full_name},
            "book": {"id": l.book_id, "title": l.book.title},
            "hall": {"id": l.hall_id, "name": l.hall.name},
            "qty": l.qty,
        } for l in qs]

        return Response({"cutoff": cutoff, "results": data})

@extend_schema(tags=["Analytics"])
class RareBooksLoansAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # книги, у которых суммарно по всем залам <= 2
        rare_book_ids = (
            BookStock.objects
            .values("book_id")
            .annotate(total=Sum("copies"))
            .filter(total__lte=2)
            .values_list("book_id", flat=True)
        )

        qs = (
            Loan.objects
            .filter(returned_at__isnull=True, book_id__in=rare_book_ids)
            .select_related("reader", "book", "hall")
            .order_by("reader_id", "book_id")
        )

        data = [{
            "loan_id": l.id,
            "reader": {"id": l.reader_id, "full_name": l.reader.full_name},
            "book": {"id": l.book_id, "title": l.book.title},
            "hall": {"id": l.hall_id, "name": l.hall.name},
            "assigned_at": l.assigned_at,
            "qty": l.qty,
        } for l in qs]

        return Response({"results": data})

@extend_schema(tags=["Analytics"])
class ReadersUnder20APIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cutoff = timezone.now().date() - timedelta(days=20 * 365)
        count = Reader.objects.filter(birth_date__gt=cutoff).count()
        return Response({"under_20_count": count, "cutoff_birth_date": cutoff})

@extend_schema(tags=["Analytics"])
class ReaderEducationStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total = Reader.objects.count()
        if total == 0:
            return Response({"total": 0, "education": {}, "education_percent": {}, "degree_percent": 0.0})

        edu_counts = (
            Reader.objects
            .values("education_lvl")
            .annotate(cnt=Count("id"))
            .order_by()
        )

        education = {}
        education_percent = {}
        for row in edu_counts:
            lvl = row["education_lvl"] or "unknown"
            c = row["cnt"]
            education[lvl] = c
            education_percent[lvl] = round(c / total * 100, 2)

        degree_count = Reader.objects.filter(degree=True).count()
        degree_percent = round(degree_count / total * 100, 2)

        return Response({
            "total": total,
            "education": education,
            "education_percent": education_percent,
            "degree_count": degree_count,
            "degree_percent": degree_percent,
        })
