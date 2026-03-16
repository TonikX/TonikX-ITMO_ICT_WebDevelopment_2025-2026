from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ReadingRoom, Reader, Book, BookCopy, BookAssignment


class ReadingRoomSerializer(serializers.ModelSerializer):
    """Сериализатор для читального зала"""
    readers_count = serializers.SerializerMethodField()
    total_books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ReadingRoom
        fields = ['id', 'number', 'name', 'capacity', 'readers_count', 'total_books_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_readers_count(self, obj):
        """Количество активных читателей в зале"""
        return obj.readers.filter(is_active=True).count()
    
    def get_total_books_count(self, obj):
        """Общее количество книг в зале"""
        return sum(copy.quantity for copy in obj.book_copies.all())


class ReaderSerializer(serializers.ModelSerializer):
    """Сериализатор для читателя"""
    age = serializers.ReadOnlyField()
    reading_room_name = serializers.SerializerMethodField()
    active_books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Reader
        fields = [
            'id', 'ticket_number', 'full_name', 'passport_number', 'birth_date',
            'age', 'address', 'phone_number', 'education', 'has_degree',
            'reading_room', 'reading_room_name', 'registration_date',
            'unregistration_date', 'is_active', 'active_books_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'registration_date', 'created_at', 'updated_at']
    
    def get_reading_room_name(self, obj):
        """Название читального зала"""
        return obj.reading_room.name if obj.reading_room else None
    
    def get_active_books_count(self, obj):
        """Количество активных закреплений книг"""
        return obj.book_assignments.filter(is_returned=False).count()


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор для книги"""
    total_copies = serializers.SerializerMethodField()
    active_assignments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'authors', 'publisher', 'publication_year',
            'section', 'code', 'total_copies', 'active_assignments_count',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_copies(self, obj):
        """Общее количество экземпляров книги во всех залах"""
        return sum(copy.quantity for copy in obj.copies.all())
    
    def get_active_assignments_count(self, obj):
        """Количество активных закреплений"""
        return obj.assignments.filter(is_returned=False).count()


class BookCopySerializer(serializers.ModelSerializer):
    """Сериализатор для экземпляра книги в зале"""
    book_title = serializers.SerializerMethodField()
    reading_room_name = serializers.SerializerMethodField()
    
    class Meta:
        model = BookCopy
        fields = [
            'id', 'book', 'book_title', 'reading_room', 'reading_room_name',
            'quantity', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_book_title(self, obj):
        """Название книги"""
        return obj.book.title
    
    def get_reading_room_name(self, obj):
        """Название читального зала"""
        return obj.reading_room.name


class BookAssignmentSerializer(serializers.ModelSerializer):
    """Сериализатор для закрепления книги"""
    book_title = serializers.SerializerMethodField()
    reader_name = serializers.SerializerMethodField()
    reader_ticket = serializers.SerializerMethodField()
    days_since_assignment = serializers.SerializerMethodField()
    
    class Meta:
        model = BookAssignment
        fields = [
            'id', 'book', 'book_title', 'reader', 'reader_name', 'reader_ticket',
            'assignment_date', 'return_date', 'is_returned', 'days_since_assignment',
            'created_at'
        ]
        read_only_fields = ['id', 'assignment_date', 'created_at']
    
    def get_book_title(self, obj):
        """Название книги"""
        return obj.book.title
    
    def get_reader_name(self, obj):
        """ФИО читателя"""
        return obj.reader.full_name
    
    def get_reader_ticket(self, obj):
        """Номер читательского билета"""
        return obj.reader.ticket_number
    
    def get_days_since_assignment(self, obj):
        """Количество дней с момента закрепления"""
        from django.utils import timezone
        if obj.is_returned and obj.return_date:
            return None
        delta = timezone.now().date() - obj.assignment_date
        return delta.days
