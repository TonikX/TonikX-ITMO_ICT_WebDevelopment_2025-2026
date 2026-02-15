from rest_framework import generics, permissions, filters, status, viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
import calendar
from rest_framework.exceptions import ValidationError
from datetime import timedelta, date
from django.db.models import Sum, Q, OuterRef, Subquery, DateField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import *
from .serializers import *



@extend_schema_view(
    get=extend_schema(tags=["Halls"]),
    post=extend_schema(tags=["Halls"]),
)
class HallListCreateAPIView(generics.ListCreateAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    get=extend_schema(tags=["Halls"]),
    patch=extend_schema(tags=["Halls"]),
    delete=extend_schema(tags=["Halls"]),
)
class HallRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    get=extend_schema(tags=["Authors"]),
    post=extend_schema(tags=["Authors"]),
)
class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    get=extend_schema(tags=["Authors"]),
    patch=extend_schema(tags=["Authors"]),
    delete=extend_schema(tags=["Authors"]),
)
class AuthorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    get=extend_schema(tags=["Books"]),
    post=extend_schema(tags=["Books"]),
)
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all().prefetch_related("authors")
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookCreateUpdateSerializer
        return BookSerializer


@extend_schema_view(
    get=extend_schema(tags=["Books"]),
    patch=extend_schema(tags=["Books"]),
    delete=extend_schema(tags=["Books"]),
)
class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    queryset = Book.objects.all().prefetch_related("authors")
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return BookCreateUpdateSerializer
        return BookSerializer


@extend_schema_view(
    get=extend_schema(tags=["Readers"]),
    post=extend_schema(tags=["Readers"]),
)
class ReaderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReaderSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    # поиск: по ФИО и по номеру билета (через связь)
    search_fields = ["full_name", "ticket_history__ticket_number"]

    # сортировка: по ФИО и по аннотированному "активному билету"
    ordering_fields = ["full_name", "active_ticket_number"]
    ordering = ["full_name"]

    def get_queryset(self):
        today = timezone.localdate()

        active_ticket_sq = ReaderTicketHistory.objects.filter(
            reader_id=OuterRef("pk"),
            valid_from__lte=today,
        ).filter(
            # active: valid_to is null OR valid_to >= today
            Q(valid_to__isnull=True) | Q(valid_to__gte=today)
        ).order_by("-valid_from", "-id").values("ticket_number")[:1]

        return (
            Reader.objects.all()
            .annotate(active_ticket_number=Subquery(active_ticket_sq))
        )

class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        with transaction.atomic():
            # 1) create reader
            reader_ser = ReaderSerializer(data=request.data["reader"])
            reader_ser.is_valid(raise_exception=True)
            reader = reader_ser.save()

            # 2) create ticket
            ReaderTicketHistory.objects.create(
                reader=reader,
                ticket_number=request.data["ticket_number"],
                valid_from=request.data.get("valid_from"),
                valid_to=None
            )

            # 3) create hall (optional)
            hall_id = request.data.get("hall")
            if hall_id:
                ReaderHallHistory.objects.create(
                    reader=reader, hall_id=hall_id,
                    valid_from=request.data.get("valid_from"),
                    valid_to=None
                )

            return Response({"id": reader.id}, status=status.HTTP_201_CREATED)
        
@extend_schema_view(
    get=extend_schema(tags=["Readers"]),
    patch=extend_schema(tags=["Readers"]),
    delete=extend_schema(tags=["Readers"]),
)
class ReaderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    queryset = Reader.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReaderDetailSerializer
        return ReaderSerializer



@extend_schema_view(
    get=extend_schema(tags=["Loans"]),
    post=extend_schema(tags=["Loans"]),
)
class LoanListCreateAPIView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        loan = serializer.save()

        stock = BookStock.objects.select_for_update().filter(
            book=loan.book,
            hall=loan.hall
        ).first()
        if stock is None:
            raise ValidationError({"book": "В этом зале нет строки BookStock для этой книги."})

        if stock.copies < loan.qty:
            raise ValidationError({"qty": f"Недостаточно экземпляров: доступно {stock.copies}, нужно {loan.qty}."})

        stock.copies -= loan.qty
        stock.save(update_fields=["copies"])


@extend_schema_view(
    get=extend_schema(tags=["Loans"]),
    patch=extend_schema(tags=["Loans"]),
    delete=extend_schema(tags=["Loans"]),
)
class LoanRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def perform_update(self, serializer):
        old = self.get_object()  # состояние ДО обновления
        was_returned = old.returned_at is not None

        loan = serializer.save()  # состояние ПОСЛЕ
        is_returned = loan.returned_at is not None

        # если впервые отметили возврат -> увеличиваем stock
        if (not was_returned) and is_returned:
            stock = BookStock.objects.select_for_update().filter(
                book=loan.book,
                hall=loan.hall
            ).first()
            if stock is None:
                raise ValidationError({"book": "В этом зале нет строки BookStock для этой книги."})

            stock.copies += loan.qty
            stock.save(update_fields=["copies"])

    @transaction.atomic
    def perform_destroy(self, instance):
        # если займ активный, то удаление = отмена выдачи -> вернуть остаток
        if instance.returned_at is None:
            stock = BookStock.objects.select_for_update().filter(
                book=instance.book,
                hall=instance.hall
            ).first()
            if stock is None:
                raise ValidationError({"book": "В этом зале нет строки BookStock для этой книги."})

            stock.copies += instance.qty
            stock.save(update_fields=["copies"])

        instance.delete()


@extend_schema_view(
    get=extend_schema(tags=["Stock"]),
    post=extend_schema(tags=["Stock"]),
)
class BookStockListCreateAPIView(generics.ListCreateAPIView):
    queryset = BookStock.objects.all()
    serializer_class = BookStockSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    get=extend_schema(tags=["Stock"]),
    patch=extend_schema(tags=["Stock"]),
    delete=extend_schema(tags=["Stock"]),
)
class BookStockRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    queryset = BookStock.objects.all()
    serializer_class = BookStockSerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema_view(
    get=extend_schema(tags=["Movements"]),
    post=extend_schema(tags=["Movements"]),
)
class BookMovementListCreateAPIView(generics.ListCreateAPIView):
    queryset = BookMovement.objects.all()
    serializer_class = BookMovementSerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema_view(
    get=extend_schema(tags=["Movements"]),
    patch=extend_schema(tags=["Movements"]),
    delete=extend_schema(tags=["Movements"]),
)
class BookMovementRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete"]
    queryset = BookMovement.objects.all()
    serializer_class = BookMovementSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    get=extend_schema(tags=["Book Codes"]),
    post=extend_schema(tags=["Book Codes"]),
)
class BookCodeHistoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = BookCodeHistory.objects.all()
    serializer_class = BookCodeHistorySerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    get=extend_schema(tags=["Book Codes"]),
    patch=extend_schema(tags=["Book Codes"]),
    delete=extend_schema(tags=["Book Codes"]),
)
class BookCodeHistoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookCodeHistory.objects.all()
    serializer_class = BookCodeHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch", "delete"]


@extend_schema_view(get=extend_schema(tags=["Reader Hall History"]),
                    post=extend_schema(tags=["Reader Hall History"]))
class ReaderHallHistoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = ReaderHallHistory.objects.all()
    serializer_class = ReaderHallHistorySerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(get=extend_schema(tags=["Reader Hall History"]),
                    patch=extend_schema(tags=["Reader Hall History"]),
                    delete=extend_schema(tags=["Reader Hall History"]))
class ReaderHallHistoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReaderHallHistory.objects.all()
    serializer_class = ReaderHallHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch", "delete"]


@extend_schema_view(get=extend_schema(tags=["Membership Events"]),
                    post=extend_schema(tags=["Membership Events"]))
class ReaderMembershipHistoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = ReaderMembershipHistory.objects.all()
    serializer_class = ReaderMembershipHistorySerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(get=extend_schema(tags=["Membership Events"]),
                    patch=extend_schema(tags=["Membership Events"]),
                    delete=extend_schema(tags=["Membership Events"]))
class ReaderMembershipHistoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReaderMembershipHistory.objects.all()
    serializer_class = ReaderMembershipHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch", "delete"]


@extend_schema_view(get=extend_schema(tags=["Ticket History"]),
                    post=extend_schema(tags=["Ticket History"]))
class ReaderTicketHistoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = ReaderTicketHistory.objects.all()
    serializer_class = ReaderTicketHistorySerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(get=extend_schema(tags=["Ticket History"]),
                    patch=extend_schema(tags=["Ticket History"]),
                    delete=extend_schema(tags=["Ticket History"]))
class ReaderTicketHistoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReaderTicketHistory.objects.all()
    serializer_class = ReaderTicketHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch", "delete"]



class PurgeOldReadersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Readers"],
        description="Удаляет читателей, которые записались > 1 года назад и не прошли перерегистрацию."
    )
    def post(self, request):
        cutoff = timezone.localdate() - timedelta(days=365)

        # последняя дата enroll для каждого reader
        last_enroll_sq = Subquery(
            ReaderMembershipHistory.objects.filter(
                reader_id=OuterRef("pk"),
                event_type=ReaderMembershipHistory.ENROLL,
            )
            .order_by("-event_date")
            .values("event_date")[:1],
            output_field=DateField(),
        )

        # последняя дата reregister для каждого reader
        last_reregister_sq = Subquery(
            ReaderMembershipHistory.objects.filter(
                reader_id=OuterRef("pk"),
                event_type=ReaderMembershipHistory.REREGISTER,
            )
            .order_by("-event_date")
            .values("event_date")[:1],
            output_field=DateField(),
        )

        qs = (
            Reader.objects
            .annotate(last_enroll=last_enroll_sq, last_reregister=last_reregister_sq)
            .filter(last_enroll__isnull=False)                 # был enroll
            .filter(last_enroll__lt=cutoff)                    # enroll старше года
            .filter(last_reregister__isnull=True)              # и ни разу не было reregister
        )

        ids = list(qs.values_list("id", flat=True))

        with transaction.atomic():
            deleted_count, _ = qs.delete()

        return Response(
            {
                "cutoff": str(cutoff),
                "deleted_count": deleted_count,
                "deleted_reader_ids": ids,
            }
        )


def daterange(d1: date, d2: date):
    cur = d1
    while cur <= d2:
        yield cur
        cur += timedelta(days=1)


class MonthlyReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Analytics"],
        description="Отчёт за месяц: кол-во книг (экземпляров) и читателей на каждый день по залам и по библиотеке + кол-во записавшихся за месяц.",
        parameters=[
            OpenApiParameter("year", int, required=False),
            OpenApiParameter("month", int, required=False),
        ],
    )
    def get(self, request):
        today = timezone.localdate()
        year = int(request.query_params.get("year", today.year))
        month = int(request.query_params.get("month", today.month))
        if month < 1 or month > 12:
            raise ValidationError({"month": "month должен быть 1..12"})

        last_day = calendar.monthrange(year, month)[1]
        d_start = date(year, month, 1)
        d_end = date(year, month, last_day)

        halls = list(Hall.objects.all().values("id", "hall_number", "name"))


        def active_reader_ids_on(day: date):

            last_event_qs = (
                ReaderMembershipHistory.objects
                .filter(event_date__lte=day)
                .order_by("reader_id", "-event_date", "-id")
            )

            last_by_reader = {}
            for ev in last_event_qs.values("reader_id", "event_type", "event_date", "id"):
                rid = ev["reader_id"]
                if rid not in last_by_reader:
                    last_by_reader[rid] = ev["event_type"]

            active_ids = [rid for rid, etype in last_by_reader.items() if etype != ReaderMembershipHistory.UNREGISTER]
            return active_ids

        def hall_reader_count_on(hall_id: int, day: date, active_ids):
            # читатель закреплён за залом на day
            return ReaderHallHistory.objects.filter(
                hall_id=hall_id,
                valid_from__lte=day
            ).filter(
                Q(valid_to__isnull=True) | Q(valid_to__gt=day)
            ).filter(
                reader_id__in=active_ids
            ).values("reader_id").distinct().count()

        def hall_book_copies_on(hall_id: int, day: date):
            current = (
                BookStock.objects.filter(hall_id=hall_id)
                .aggregate(total=Sum("copies"))["total"] or 0
            )

            if day >= today:
                return int(current)

            after_start = day + timedelta(days=1)
            after_end = today

            in_qty = (
                BookMovement.objects.filter(
                    movement_date__gte=after_start,
                    movement_date__lte=after_end,
                    to_hall_id=hall_id
                ).aggregate(s=Sum("qty"))["s"] or 0
            )
            out_qty = (
                BookMovement.objects.filter(
                    movement_date__gte=after_start,
                    movement_date__lte=after_end,
                    from_hall_id=hall_id
                ).aggregate(s=Sum("qty"))["s"] or 0
            )

            past = current - (in_qty - out_qty)
            return int(max(past, 0))

        daily = []
        for day in daterange(d_start, d_end):
            active_ids = active_reader_ids_on(day)

            halls_rows = []
            total_books = 0
            total_readers = 0

            for h in halls:
                hid = h["id"]
                books_copies = hall_book_copies_on(hid, day)
                readers_cnt = hall_reader_count_on(hid, day, active_ids)

                total_books += books_copies
                total_readers += readers_cnt

                halls_rows.append({
                    "hall_id": hid,
                    "hall_number": h["hall_number"],
                    "name": h["name"],
                    "books_copies": books_copies,      # экземпляры
                    "readers": readers_cnt,            # активные закреплённые
                })

            daily.append({
                "date": str(day),
                "by_hall": halls_rows,
                "total": {
                    "books_copies": total_books,
                    "readers": total_readers,
                }
            })

        #записавшиеся за месяц (enroll events) по залам и всего
        enroll_events = ReaderMembershipHistory.objects.filter(
            event_type=ReaderMembershipHistory.ENROLL,
            event_date__gte=d_start,
            event_date__lte=d_end,
        ).values("reader_id", "event_date")

        enroll_by_hall = {h["id"]: 0 for h in halls}
        enroll_total = 0

        for ev in enroll_events:
            rid = ev["reader_id"]
            ev_date = ev["event_date"]

            hall_row = ReaderHallHistory.objects.filter(
                reader_id=rid,
                valid_from__lte=ev_date
            ).filter(
                Q(valid_to__isnull=True) | Q(valid_to__gt=ev_date)
            ).order_by("-valid_from").values("hall_id").first()

            if hall_row:
                enroll_by_hall[hall_row["hall_id"]] += 1
            enroll_total += 1

        enrollments_month = []
        for h in halls:
            enrollments_month.append({
                "hall_id": h["id"],
                "hall_number": h["hall_number"],
                "name": h["name"],
                "enroll_count": enroll_by_hall.get(h["id"], 0)
            })

        return Response({
            "period": {"year": year, "month": month, "from": str(d_start), "to": str(d_end)},
            "enrollments_month": {
                "by_hall": enrollments_month,
                "total": enroll_total
            },
            "daily": daily
        })
