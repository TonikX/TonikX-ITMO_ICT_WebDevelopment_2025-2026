from rest_framework import serializers
from django.utils import timezone
from django.db import transaction
from django.db.models import Q, Sum
from .models import (
    Hall, Author, Book, BookAuthor, BookCodeHistory,
    Reader, ReaderHallHistory, ReaderMembershipHistory, ReaderTicketHistory,
    BookMovement, BookStock, Loan
)

from django.db.models import F,Q

class ReaderMembershipHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReaderMembershipHistory
        fields = "__all__"

class ReaderTicketHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReaderTicketHistory
        fields = "__all__"

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "full_name"]


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source="authors",
        queryset=Author.objects.all()
    )
    current_code = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "publisher",
            "publication_year",
            "section",
            "authors",     
            "author_ids",   # ← для POST/PUT
            "current_code",
        ]

    def get_current_code(self, obj):
        current = obj.code_history.filter(valid_to__isnull=True).order_by("-valid_from").first()
        return current.code if current else None


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    author_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Book
        fields = ["id", "title", "publisher", "publication_year", "section", "author_ids"]

    def to_representation(self, instance):
        return BookSerializer(instance, context=self.context).data

    def create(self, validated_data):
        author_ids = validated_data.pop("author_ids", [])
        book = Book.objects.create(**validated_data)

        for author_id in author_ids:
            BookAuthor.objects.create(
                book=book,
                author_id=author_id
            )

        return book


class ReaderSerializer(serializers.ModelSerializer):
    active_ticket_number = serializers.SerializerMethodField()

    class Meta:
        model = Reader
        fields = [
            "id",
            "full_name",
            "phone",
            "passport_number",
            "birth_date",
            "education_lvl",
            "degree",
            "active_ticket_number",
        ]

    def get_active_ticket_number(self, obj):
        today = timezone.localdate()
        t = (
            obj.ticket_history
            .filter(valid_from__lte=today)
            .filter(Q(valid_to__isnull=True) | Q(valid_to__gte=today))
            .order_by("-valid_from", "-id")
            .first()
        )
        return t.ticket_number if t else None
    



class ReaderMembershipHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReaderMembershipHistory
        fields = "__all__"


class BookCodeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCodeHistory
        fields = "__all__"

class BookDetailSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    code_history = BookCodeHistorySerializer(many=True, read_only=True)  # related_name="code_history"

    class Meta:
        model = Book
        fields = ["id", "title", "publisher", "publication_year", "section", "authors", "code_history"]


class ReaderHallHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReaderHallHistory
        fields = "__all__"

    def validate(self, attrs):
        # если фронт не прислал valid_from — ставим сегодня
        if attrs.get("valid_from") is None:
            attrs["valid_from"] = timezone.localdate()
        return attrs
    
class BookStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStock
        fields = "__all__"


class BookMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMovement
        fields = "__all__"

    def validate(self, attrs):
        mtype = attrs.get("movement_type")
        from_hall = attrs.get("from_hall")
        to_hall = attrs.get("to_hall")

        book = attrs.get("book")
        movement_date = attrs.get("movement_date")
        if mtype == BookMovement.ACQUIRE:
            if to_hall is None or from_hall is not None:
                raise serializers.ValidationError(
                    "Acquire: to_hall обязателен, from_hall должен быть пустым."
                )
        has_code = book.code_history.filter(
            valid_from__lte=movement_date
        ).filter(
            Q(valid_to__isnull=True) | Q(valid_to__gte=movement_date)
        ).exists()

        if not has_code:
            raise serializers.ValidationError(
                {"book": "Нельзя принять книгу без действующего шифра на дату движения."}
            )
        elif mtype == BookMovement.WRITEOFF:
            if from_hall is None or to_hall is not None:
                raise serializers.ValidationError(
                    "Writeoff: from_hall обязателен, to_hall должен быть пустым."
                )

        elif mtype == BookMovement.TRANSFER:
            if from_hall is None or to_hall is None or from_hall == to_hall:
                raise serializers.ValidationError(
                    "Transfer: нужны from_hall и to_hall, и они должны отличаться."
                )

        return attrs

    @transaction.atomic
    def create(self, validated_data):

        movement = super().create(validated_data)

        book = movement.book
        qty = movement.qty
        mtype = movement.movement_type

        def inc_stock(hall, delta):
            stock, _ = BookStock.objects.select_for_update().get_or_create(
                book=book, hall=hall, defaults={"copies": 0}
            )

            if delta < 0 and stock.copies < (-delta):
                raise serializers.ValidationError(
                    f"Недостаточно экземпляров в зале {hall.hall_number}. "
                    f"Есть {stock.copies}, пытаемся списать/перенести {-delta}."
                )

            stock.copies = F("copies") + delta
            stock.save(update_fields=["copies"])
            stock.refresh_from_db()
            return stock

        if mtype == BookMovement.ACQUIRE:
            inc_stock(movement.to_hall, +qty)

        elif mtype == BookMovement.WRITEOFF:
            inc_stock(movement.from_hall, -qty)

        elif mtype == BookMovement.TRANSFER:
            inc_stock(movement.from_hall, -qty)
            inc_stock(movement.to_hall, +qty)

        return movement



class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"

    def validate(self, attrs):
        instance = getattr(self, "instance", None)

        # достаем поля: из attrs (если пришли) иначе из instance (при PATCH)
        reader = attrs.get("reader") or (instance.reader if instance else None)
        book   = attrs.get("book")   or (instance.book   if instance else None)
        hall   = attrs.get("hall")   or (instance.hall   if instance else None)
        qty    = attrs.get("qty",    instance.qty if instance else 1)

        assigned_at = attrs.get("assigned_at") or (instance.assigned_at if instance else None)
        if assigned_at is None:
            assigned_at = timezone.localdate()

        # если это PATCH только на returned_at и ничего не меняли в выдаче — можно вообще не валидировать бизнес-правила
        if instance and set(attrs.keys()).issubset({"returned_at"}):
            return attrs

        # дальше твои проверки
        if reader is None:
            raise serializers.ValidationError({"reader": "reader обязателен"})
        if book is None:
            raise serializers.ValidationError({"book": "book обязателен"})
        if hall is None:
            raise serializers.ValidationError({"hall": "hall обязателен"})

        if not reader.has_active_ticket(assigned_at):
            raise serializers.ValidationError(
                {"reader": "У читателя нет действующего читательского билета."}
            )

        is_reader_in_hall = ReaderHallHistory.objects.filter(
            reader=reader,
            hall=hall,
            valid_from__lte=assigned_at
        ).filter(
            Q(valid_to__isnull=True) | Q(valid_to__gte=assigned_at)
        ).exists()

        if not is_reader_in_hall:
            raise serializers.ValidationError({
                "hall": "Читатель не закреплён за этим залом на дату выдачи."
            })

        stock = BookStock.objects.filter(book=book, hall=hall).first()
        if stock is None:
            raise serializers.ValidationError({
                "book": "В этом зале нет этой книги (нет строки в BookStock)."
            })

        # (желательно) учесть активные выдачи
        active_qty = Loan.objects.filter(
            book=book, hall=hall, returned_at__isnull=True
        ).aggregate(s=Sum("qty"))["s"] or 0

        available = stock.copies - active_qty
        if available < qty:
            raise serializers.ValidationError({
                "qty": f"Недостаточно экземпляров: доступно {available}, запрошено {qty}."
            })

        return attrs

class LoanShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id", "book", "hall", "assigned_at", "returned_at", "qty"]

class ReaderDetailSerializer(serializers.ModelSerializer):
    active_ticket_number = serializers.SerializerMethodField()

    class Meta:
        model = Reader
        fields = [
            "id",
            "full_name",
            "phone",
            "address",
            "passport_number",
            "birth_date",
            "education_lvl",
            "degree",
            "active_ticket_number",
        ]

    def get_active_ticket_number(self, obj):
        ticket = (
            obj.ticket_history
            .filter(valid_to__isnull=True)
            .order_by("-valid_from", "-id")
            .first()
        )
        return ticket.ticket_number if ticket else None








