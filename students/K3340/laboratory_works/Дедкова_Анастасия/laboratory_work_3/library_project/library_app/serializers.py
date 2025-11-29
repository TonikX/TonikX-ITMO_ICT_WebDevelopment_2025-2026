from rest_framework import serializers
from .models import (
    Author,
    Book,
    BookAuthor,
    ReadingHall,
    Reader,
    BookCopy,
    Loan,
    STATUS_CHOICES,
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
        )

    def get_authors(self, obj: Book):
        book_authors = BookAuthor.objects.filter(book=obj).select_related("author")
        return AuthorSerializer(
            [ba.author for ba in book_authors],
            many=True,
        ).data


# залы

class ReadingHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingHall
        fields = ("hall_id", "number", "name", "capacity")


# Читатели

class ReaderSerializer(serializers.ModelSerializer):
    hall = ReadingHallSerializer(read_only=True)
    hall_id = serializers.PrimaryKeyRelatedField(
        queryset=ReadingHall.objects.all(),
        source="hall",
        write_only=True,
    )

    class Meta:
        model = Reader
        fields = (
            "reader_id",
            "card_number",
            "full_name",
            "passport_number",
            "birth_date",
            "address",
            "phone",
            "education_level",
            "has_academic_degree",
            "is_active",
            "hall",
            "hall_id",
            "registered_at",
            "last_reregistration_at",
        )


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
    reader = ReaderSerializer(read_only=True)
    reader_id = serializers.PrimaryKeyRelatedField(
        queryset=Reader.objects.all(),
        source="reader",
        write_only=True,
    )
    copy = BookCopySerializer(read_only=True)
    copy_id = serializers.PrimaryKeyRelatedField(
        queryset=BookCopy.objects.all(),
        source="copy",
        write_only=True,
    )

    class Meta:
        model = Loan
        fields = (
            "loan_id",
            "reader",
            "reader_id",
            "copy",
            "copy_id",
            "assigned_at",
            "returned_at",
        )
        read_only_fields = ("assigned_at",)
