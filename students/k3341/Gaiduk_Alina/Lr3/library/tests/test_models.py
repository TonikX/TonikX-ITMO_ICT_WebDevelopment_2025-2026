"""
Tests for library models.
"""
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from datetime import date, timedelta
from library.models import (
    Author, Publisher, BookSection, Book, BookAuthor,
    Hall, Reader, BookCopy, BookIssue, HallBookStock, Staff
)


@pytest.mark.django_db
class TestAuthor:
    """Тесты для модели Author."""
    
    def test_create_author(self):
        """Тест создания автора."""
        author = Author.objects.create(full_name='Лев Толстой')
        assert author.author_id is not None
        assert author.full_name == 'Лев Толстой'
        assert str(author) == 'Лев Толстой'
    
    def test_author_timestamps(self):
        """Тест автоматического создания временных меток."""
        author = Author.objects.create(full_name='Фёдор Достоевский')
        assert author.created_at is not None
        assert author.updated_at is not None


@pytest.mark.django_db
class TestPublisher:
    """Тесты для модели Publisher."""
    
    def test_create_publisher(self):
        """Тест создания издательства."""
        publisher = Publisher.objects.create(name='Эксмо')
        assert publisher.publisher_id is not None
        assert publisher.name == 'Эксмо'
        assert str(publisher) == 'Эксмо'
    
    def test_publisher_unique_name(self):
        """Тест уникальности названия издательства."""
        Publisher.objects.create(name='АСТ')
        with pytest.raises(IntegrityError):
            Publisher.objects.create(name='АСТ')


@pytest.mark.django_db
class TestBook:
    """Тесты для модели Book."""
    
    def test_create_book(self):
        """Тест создания книги."""
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
        
        assert book.book_id is not None
        assert book.title == 'Война и мир'
        assert book.publisher == publisher
        assert book.authors.count() == 1
        assert str(book) == 'Война и мир'


@pytest.mark.django_db
class TestReader:
    """Тесты для модели Reader."""
    
    def test_create_reader(self):
        """Тест создания читателя."""
        hall = Hall.objects.create(hall_number=1, name='Читальный зал №1', capacity=50)
        reader = Reader.objects.create(
            card_number='R001',
            full_name='Иванов Иван Иванович',
            passport_number='1234567890',
            birth_date=date(1990, 1, 1),
            address='г. Москва, ул. Ленина, д. 1',
            phone='+79991234567',
            education_level='высшее',
            has_academic_degree=False,
            hall=hall
        )
        
        assert reader.reader_id is not None
        assert reader.card_number == 'R001'
        assert reader.is_active is True
        assert reader.registration_date == timezone.now().date() or isinstance(reader.registration_date, date)
    
    def test_reader_unique_card_number(self):
        """Тест уникальности номера читательского билета."""
        Reader.objects.create(
            card_number='R001',
            full_name='Иванов Иван Иванович',
            passport_number='1234567890',
            birth_date=date(1990, 1, 1)
        )
        with pytest.raises(IntegrityError):
            Reader.objects.create(
                card_number='R001',
                full_name='Петров Петр Петрович',
                passport_number='0987654321',
                birth_date=date(1985, 5, 5)
            )


@pytest.mark.django_db
class TestBookCopy:
    """Тесты для модели BookCopy."""
    
    def test_create_book_copy(self):
        """Тест создания экземпляра книги."""
        book = Book.objects.create(title='Тестовая книга', cipher='TEST001')
        hall = Hall.objects.create(hall_number=1, name='Зал №1', capacity=50)
        
        copy = BookCopy.objects.create(
            book=book,
            hall=hall,
            inventory_number='INV001'
        )
        
        assert copy.copy_id is not None
        assert copy.book == book
        assert copy.hall == hall
        assert copy.is_written_off is False
        assert copy.registration_date == timezone.now().date() or isinstance(copy.registration_date, date)
    
    def test_book_copy_writeoff_validation(self):
        """Тест валидации списания книги."""
        book = Book.objects.create(title='Тестовая книга', cipher='TEST001')
        hall = Hall.objects.create(hall_number=1, name='Зал №1', capacity=50)
        copy = BookCopy.objects.create(
            book=book,
            hall=hall,
            inventory_number='INV001'
        )
        
        # Попытка списать без даты должна вызвать ошибку при clean()
        copy.is_written_off = True
        with pytest.raises(ValidationError):
            copy.clean()
        
        # Правильное списание
        copy.writeoff_date = timezone.now().date()
        copy.clean()  # Должно пройти без ошибок


@pytest.mark.django_db
class TestBookIssue:
    """Тесты для модели BookIssue."""
    
    def test_create_book_issue(self):
        """Тест создания выдачи книги."""
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
        
        assert issue.issue_id is not None
        assert issue.reader == reader
        assert issue.copy == copy
        assert issue.return_date is None
    
    def test_book_issue_return_date_validation(self):
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
        issue.return_date = issue.issue_date - timedelta(days=1)
        with pytest.raises(ValidationError):
            issue.clean()
        
        # Правильная дата возврата
        issue.return_date = issue.issue_date + timedelta(days=1)
        issue.clean()  # Должно пройти без ошибок


@pytest.mark.django_db
class TestHallBookStock:
    """Тесты для модели HallBookStock."""
    
    def test_create_hall_book_stock(self):
        """Тест создания записи о количестве книг в зале."""
        book = Book.objects.create(title='Тестовая книга', cipher='TEST001')
        hall = Hall.objects.create(hall_number=1, name='Зал №1', capacity=50)
        
        stock = HallBookStock.objects.create(
            hall=hall,
            book=book,
            copies_total=5
        )
        
        assert stock.hall == hall
        assert stock.book == book
        assert stock.copies_total == 5
    
    def test_hall_book_stock_unique(self):
        """Тест уникальности пары зал-книга."""
        book = Book.objects.create(title='Тестовая книга', cipher='TEST001')
        hall = Hall.objects.create(hall_number=1, name='Зал №1', capacity=50)
        
        HallBookStock.objects.create(hall=hall, book=book, copies_total=5)
        
        with pytest.raises(IntegrityError):
            HallBookStock.objects.create(hall=hall, book=book, copies_total=3)

