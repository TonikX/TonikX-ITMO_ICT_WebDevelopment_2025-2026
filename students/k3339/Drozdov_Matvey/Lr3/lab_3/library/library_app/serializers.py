from rest_framework import serializers
from django.db import transaction
from .models import (
    Hall, Author, Book, BookAuthor, BookCodeHistory,
    Reader, ReaderHallHistory, ReaderMembershipHistory, ReaderTicketHistory,
    BookMovement, BookStock, Loan
)
from django.db.models import F

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

    class Meta:
        model = Book
        fields = ["id", "title", "publisher", "publication_year", "section", "authors"]



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
    class Meta:
        model = Reader
        fields = "__all__"


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

class ReaderTicketHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReaderTicketHistory
        fields = "__all__"


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

        if mtype == BookMovement.ACQUIRE:
            if to_hall is None or from_hall is not None:
                raise serializers.ValidationError(
                    "Acquire: to_hall обязателен, from_hall должен быть пустым."
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
        """
        Создаём движение и сразу обновляем BookStock.
        """
        movement = super().create(validated_data)

        book = movement.book
        qty = movement.qty
        mtype = movement.movement_type

        def inc_stock(hall, delta):
            """
            delta может быть +qty или -qty.
            """
            stock, _ = BookStock.objects.get_or_create(book=book, hall=hall, defaults={"copies": 0})

            # если списываем/переносим — проверяем остаток
            if delta < 0 and stock.copies < (-delta):
                raise serializers.ValidationError(
                    f"Недостаточно экземпляров в зале {hall.hall_number}. "
                    f"Есть {stock.copies}, пытаемся списать/перенести {-delta}."
                )

            # атомарное обновление
            BookStock.objects.filter(pk=stock.pk).update(copies=F("copies") + delta)
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

class LoanShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id", "book", "hall", "assigned_at", "returned_at", "qty"]

class ReaderDetailSerializer(serializers.ModelSerializer):
    loans = LoanShortSerializer(many=True, read_only=True)
    hall_history = ReaderHallHistorySerializer(many=True, read_only=True)
    membership_events = ReaderMembershipHistorySerializer(many=True, read_only=True)
    ticket_history = ReaderTicketHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Reader
        fields = "__all__"









