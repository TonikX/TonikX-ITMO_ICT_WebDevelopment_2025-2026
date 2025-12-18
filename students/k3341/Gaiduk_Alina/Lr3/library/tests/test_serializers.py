"""
Tests for library serializers.
"""
import pytest
from django.utils import timezone
from datetime import date, timedelta
from rest_framework.exceptions import ValidationError
from library.models import (
    Author, Publisher, BookSection, Book, BookAuthor,
    Hall, Reader, BookCopy, BookIssue, Staff
)
from library.serializers import (
    AuthorSerializer, BookSerializer, BookCreateUpdateSerializer,
    ReaderSerializer, BookCopySerializer, BookIssueSerializer,
    StaffCreateSerializer
)


@pytest.mark.django_db
class TestAuthorSerializer:
    """Тесты для сериализатора Author."""
    
    def test_serialize_author(self):
        """Тест сериализации автора."""
        author = Author.objects.create(full_name='Лев Толстой')
        serializer = AuthorSerializer(author)
        data = serializer.data
        
        assert data['author_id'] == author.author_id
        assert data['full_name'] == 'Лев Толстой'
        assert 'created_at' in data
    
    def test_deserialize_author(self):
        """Тест десериализации автора."""
        data = {'full_name': 'Фёдор Достоевский'}
        serializer = AuthorSerializer(data=data)
        assert serializer.is_valid()
        
        author = serializer.save()
        assert author.full_name == 'Фёдор Достоевский'


@pytest.mark.django_db
class TestBookSerializer:
    """Тесты для сериализатора Book."""
    
    def test_serialize_book(self):
        """Тест сериализации книги."""
        publisher = Publisher.objects.create(name='Эксмо')
        section = BookSection.objects.create(name='Художественная литература')
        author = Author.objects.create(full_name='Лев Толстой')
        
        book = Book.objects.create(
            title='Война и мир',
            publisher=publisher,
            publish_year=1869,
            section=section,
            cipher='84(2Рос=Рус)1'
        )
        BookAuthor.objects.create(book=book, author=author)
        
        serializer = BookSerializer(book)
        data = serializer.data
        
        assert data['title'] == 'Война и мир'
        assert data['publisher_name'] == 'Эксмо'
        assert data['section_name'] == 'Художественная литература'
        assert len(data['authors']) == 1


@pytest.mark.django_db
class TestBookCreateUpdateSerializer:
    """Тесты для сериализатора создания/обновления книги."""
    
    def test_create_book_with_authors(self):
        """Тест создания книги с авторами."""
        publisher = Publisher.objects.create(name='Эксмо')
        section = BookSection.objects.create(name='Художественная литература')
        author1 = Author.objects.create(full_name='Лев Толстой')
        author2 = Author.objects.create(full_name='Фёдор Достоевский')
        
        data = {
            'title': 'Война и мир',
            'publisher': publisher.publisher_id,
            'publish_year': 1869,
            'section': section.section_id,
            'cipher': '84(2Рос=Рус)1',
            'author_ids': [author1.author_id, author2.author_id]
        }
        
        serializer = BookCreateUpdateSerializer(data=data)
        assert serializer.is_valid()
        
        book = serializer.save()
        assert book.title == 'Война и мир'
        assert book.authors.count() == 2


@pytest.mark.django_db
class TestReaderSerializer:
    """Тесты для сериализатора Reader."""
    
    def test_serialize_reader_with_age(self):
        """Тест сериализации читателя с вычислением возраста."""
        hall = Hall.objects.create(hall_number=1, name='Зал №1', capacity=50)
        reader = Reader.objects.create(
            card_number='R001',
            full_name='Иванов Иван Иванович',
            passport_number='1234567890',
            birth_date=date(1990, 1, 1),
            hall=hall
        )
        
        serializer = ReaderSerializer(reader)
        data = serializer.data
        
        assert data['card_number'] == 'R001'
        assert 'age' in data
        assert isinstance(data['age'], int)
        assert data['age'] > 0


@pytest.mark.django_db
class TestBookCopySerializer:
    """Тесты для сериализатора BookCopy."""
    
    def test_validate_writeoff(self):
        """Тест валидации списания книги."""
        book = Book.objects.create(title='Тестовая книга', cipher='TEST001')
        hall = Hall.objects.create(hall_number=1, name='Зал №1', capacity=50)
        
        data = {
            'book': book.book_id,
            'hall': hall.hall_id,
            'inventory_number': 'INV001',
            'is_written_off': True
            # writeoff_date не указан
        }
        
        serializer = BookCopySerializer(data=data)
        assert not serializer.is_valid()
        assert 'writeoff_date' in serializer.errors


@pytest.mark.django_db
class TestBookIssueSerializer:
    """Тесты для сериализатора BookIssue."""
    
    def test_validate_return_date(self):
        """Тест валидации даты возврата."""
        book = Book.objects.create(title='Тестовая книга', cipher='TEST001')
        hall = Hall.objects.create(hall_number=1, name='Зал №1', capacity=50)
        reader = Reader.objects.create(
            card_number='R001',
            full_name='Иванов Иван Иванович',
            passport_number='1234567890',
            birth_date=date(1990, 1, 1)
        )
        copy = BookCopy.objects.create(
            book=book,
            hall=hall,
            inventory_number='INV001'
        )
        
        issue = BookIssue.objects.create(
            reader=reader,
            copy=copy,
            hall=hall,
            issue_date=timezone.now().date()
        )
        
        # Попытка установить дату возврата раньше даты выдачи
        data = {
            'return_date': (issue.issue_date - timedelta(days=1)).isoformat()
        }
        
        serializer = BookIssueSerializer(issue, data=data, partial=True)
        assert not serializer.is_valid()
        assert 'return_date' in serializer.errors


@pytest.mark.django_db
class TestStaffCreateSerializer:
    """Тесты для сериализатора создания сотрудника."""
    
    def test_create_staff_with_password(self):
        """Тест создания сотрудника с паролем."""
        data = {
            'login': 'admin',
            'email': 'admin@library.ru',
            'password': 'securepassword123'
        }
        
        serializer = StaffCreateSerializer(data=data)
        assert serializer.is_valid()
        
        staff = serializer.save()
        assert staff.login == 'admin'
        assert staff.password_hash is not None
        assert staff.password_hash != 'securepassword123'  # Должен быть хеш

