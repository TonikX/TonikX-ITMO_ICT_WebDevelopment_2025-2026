from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from uuid import uuid4
from django.utils import timezone
from .models import (
    Author,
    Book,
    BookAuthor,
    ReadingHall,
    Reader,
    BookCopy,
    Loan,
)

# Авторы

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("author_id", "full_name")


# Книги
class BookAuthorSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = BookAuthor
        fields = ("book_author_id", "author")


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    halls = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "book_id",
            "title",
            "publisher",
            "publication_year",
            "section",
            "cipher",
            "is_active",
            "authors",
            "halls",
        )

    def get_authors(self, obj: Book):
        # связи через промежуточную таблицу BookAuthor
        book_authors = BookAuthor.objects.filter(book=obj).select_related("author")
        return AuthorSerializer(
            [ba.author for ba in book_authors],
            many=True,
        ).data

    def get_halls(self, obj: Book):
        hall_names = (
            BookCopy.objects
            .filter(book=obj)
            .select_related("hall")
            .values_list("hall__name", flat=True)
            .distinct()
        )
        return list(hall_names)


# залы

class ReadingHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingHall
        fields = ("hall_id", "number", "name", "capacity")


# Читатели

class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = "__all__"

    def create(self, validated_data):
        """
        При создании читателя, если номер билета не передан –
        генерируем его автоматически/
        """
        card_number = validated_data.get("card_number")

        # если не передали или передали пустую строку
        if not card_number:
            validated_data["card_number"] = uuid4().hex[:10].upper()

        return super().create(validated_data)

# Экземпляры книг

class BookCopySerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source="book",
        write_only=True,
    )
    hall = ReadingHallSerializer(read_only=True)
    hall_id = serializers.PrimaryKeyRelatedField(
        queryset=ReadingHall.objects.all(),
        source="hall",
        write_only=True,
    )

    class Meta:
        model = BookCopy
        fields = (
            "copy_id",
            "book",
            "book_id",
            "hall",
            "hall_id",
            "status",
            "date_received",
            "date_written_off",
        )


# Выдачи

class LoanSerializer(serializers.ModelSerializer):
    days_on_loan = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = (
            "loan_id",
            "copy",
            "reader",
            "assigned_at",
            "returned_at",
            "days_on_loan",
        )

    def get_days_on_loan(self, obj):
        """
        Сколько дней книга находится на руках (на сегодняшний день).
        """
        if obj.returned_at is not None:
            return 0

        now = timezone.now()
        delta = now - obj.assigned_at
        return delta.days


class CurrentUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ("is_staff",)
