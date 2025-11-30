"""
Tests for library API endpoints.
"""
import pytest
from django.utils import timezone
from datetime import date, timedelta
from rest_framework.test import APIClient
from rest_framework import status
from library.models import (
    Author, Publisher, BookSection, Book, BookAuthor,
    Hall, Reader, BookCopy, BookIssue, HallBookStock, Staff
)
from django.contrib.auth.hashers import make_password


@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    return APIClient()


@pytest.fixture
def staff_user():
    """Фикстура для создания сотрудника."""
    return Staff.objects.create(
        login='test_staff',
        email='test@library.ru',
        password_hash=make_password('testpassword123')
    )


@pytest.fixture
def authenticated_client(api_client, staff_user):
    """Фикстура для аутентифицированного клиента."""
    # Получаем токен
    response = api_client.post('/api/token/', {
        'login': 'test_staff',
        'password': 'testpassword123'
    })
    if response.status_code != 200:
        pytest.fail(f"Failed to get token: {response.data}")
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def hall():
    """Фикстура для создания зала."""
    return Hall.objects.create(hall_number=1, name='Читальный зал №1', capacity=50)


@pytest.fixture
def author():
    """Фикстура для создания автора."""
    return Author.objects.create(full_name='Лев Толстой')


@pytest.fixture
def publisher():
    """Фикстура для создания издательства."""
    return Publisher.objects.create(name='Эксмо')


@pytest.fixture
def book_section():
    """Фикстура для создания раздела."""
    return BookSection.objects.create(name='Художественная литература')


@pytest.fixture
def book(publisher, book_section, author):
    """Фикстура для создания книги."""
    book = Book.objects.create(
        title='Война и мир',
        publisher=publisher,
        publish_year=1869,
        section=book_section,
        cipher='84(2Рос=Рус)1'
    )
    BookAuthor.objects.create(book=book, author=author)
    return book


@pytest.fixture
def reader(hall):
    """Фикстура для создания читателя."""
    return Reader.objects.create(
        card_number='R001',
        full_name='Иванов Иван Иванович',
        passport_number='1234567890',
        birth_date=date(1990, 1, 1),
        hall=hall
    )


@pytest.fixture
def book_copy(book, hall):
    """Фикстура для создания экземпляра книги."""
    return BookCopy.objects.create(
        book=book,
        hall=hall,
        inventory_number='INV001'
    )


@pytest.mark.django_db
class TestAuthentication:
    """Тесты для аутентификации."""
    
    def test_get_token_success(self, api_client, staff_user):
        """Тест успешного получения токена."""
        response = api_client.post('/api/token/', {
            'login': 'test_staff',
            'password': 'testpassword123'
        })
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_get_token_invalid_credentials(self, api_client):
        """Тест получения токена с неверными данными."""
        response = api_client.post('/api/token/', {
            'login': 'wrong_user',
            'password': 'wrong_password'
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_authenticated_request(self, authenticated_client):
        """Тест аутентифицированного запроса."""
        response = authenticated_client.get('/api/authors/')
        assert response.status_code == status.HTTP_200_OK
    
    def test_unauthenticated_request(self, api_client):
        """Тест неаутентифицированного запроса."""
        response = api_client.get('/api/authors/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestAuthorAPI:
    """Тесты для API авторов."""
    
    def test_list_authors(self, authenticated_client, author):
        """Тест получения списка авторов."""
        response = authenticated_client.get('/api/authors/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_create_author(self, authenticated_client):
        """Тест создания автора."""
        data = {'full_name': 'Фёдор Достоевский'}
        response = authenticated_client.post('/api/authors/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['full_name'] == 'Фёдор Достоевский'
    
    def test_retrieve_author(self, authenticated_client, author):
        """Тест получения автора."""
        response = authenticated_client.get(f'/api/authors/{author.author_id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['full_name'] == 'Лев Толстой'
    
    def test_update_author(self, authenticated_client, author):
        """Тест обновления автора."""
        data = {'full_name': 'Лев Николаевич Толстой'}
        response = authenticated_client.patch(f'/api/authors/{author.author_id}/', data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['full_name'] == 'Лев Николаевич Толстой'
    
    def test_delete_author(self, authenticated_client, author):
        """Тест удаления автора."""
        response = authenticated_client.delete(f'/api/authors/{author.author_id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Author.objects.filter(author_id=author.author_id).exists()


@pytest.mark.django_db
class TestBookAPI:
    """Тесты для API книг."""
    
    def test_list_books(self, authenticated_client, book):
        """Тест получения списка книг."""
        response = authenticated_client.get('/api/books/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == 'Война и мир'
    
    def test_create_book(self, authenticated_client, publisher, book_section, author):
        """Тест создания книги."""
        data = {
            'title': 'Преступление и наказание',
            'publisher': publisher.publisher_id,
            'publish_year': 1866,
            'section': book_section.section_id,
            'cipher': '84(2Рос=Рус)1-4',
            'author_ids': [author.author_id]
        }
        response = authenticated_client.post('/api/books/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Преступление и наказание'


@pytest.mark.django_db
class TestReaderAPI:
    """Тесты для API читателей."""
    
    def test_list_readers(self, authenticated_client, reader):
        """Тест получения списка читателей."""
        response = authenticated_client.get('/api/readers/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_reader_books(self, authenticated_client, reader, book_copy):
        """Тест получения книг читателя."""
        BookIssue.objects.create(
            reader=reader,
            copy=book_copy,
            hall=book_copy.hall,
            issue_date=timezone.now().date()
        )
        
        response = authenticated_client.get(f'/api/readers/{reader.reader_id}/books/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
    
    def test_age_statistics(self, authenticated_client, hall):
        """Тест статистики по возрасту."""
        Reader.objects.create(
            card_number='R002',
            full_name='Молодой читатель',
            passport_number='1111111111',
            birth_date=date(2010, 1, 1),
            hall=hall
        )
        
        response = authenticated_client.get('/api/readers/statistics/age/?age=20')
        assert response.status_code == status.HTTP_200_OK
        assert 'readers_count' in response.data
    
    def test_education_statistics(self, authenticated_client, reader):
        """Тест статистики по образованию."""
        response = authenticated_client.get('/api/readers/statistics/education/')
        assert response.status_code == status.HTTP_200_OK
        assert 'percentages' in response.data
        assert 'total' in response.data


@pytest.mark.django_db
class TestBookIssueAPI:
    """Тесты для API выдач книг."""
    
    def test_overdue_issues(self, authenticated_client, reader, book_copy):
        """Тест получения просроченных выдач."""
        month_ago = timezone.now().date() - timedelta(days=31)
        BookIssue.objects.create(
            reader=reader,
            copy=book_copy,
            hall=book_copy.hall,
            issue_date=month_ago
        )
        
        response = authenticated_client.get('/api/book-issues/overdue/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
    
    def test_issue_book(self, authenticated_client, reader, book_copy):
        """Тест выдачи книги."""
        data = {
            'reader': reader.reader_id,
            'copy': book_copy.copy_id,
            'hall': book_copy.hall.hall_id
        }
        response = authenticated_client.post('/api/book-issues/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['reader'] == reader.reader_id
    

@pytest.mark.django_db
class TestStaffOperations:
    """Тесты для операций сотрудников."""
    
    def test_register_reader(self, authenticated_client, hall):
        """Тест регистрации нового читателя."""
        data = {
            'card_number': 'R003',
            'full_name': 'Новый читатель',
            'passport_number': '2222222222',
            'birth_date': '1995-05-05',
            'hall': hall.hall_id
        }
        response = authenticated_client.post('/api/staff/register-reader/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['card_number'] == 'R003'
    
    def test_writeoff_book(self, authenticated_client, book_copy):
        """Тест списания книги."""
        HallBookStock.objects.create(
            hall=book_copy.hall,
            book=book_copy.book,
            copies_total=1
        )
        
        data = {'copy_id': book_copy.copy_id}
        response = authenticated_client.post('/api/staff/writeoff-book/', data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_written_off'] is True
    
    def test_accept_book(self, authenticated_client, book, hall):
        """Тест приёма книги в фонд."""
        data = {
            'book': book.book_id,
            'hall': hall.hall_id,
            'inventory_number': 'INV002'
        }
        response = authenticated_client.post('/api/staff/accept-book/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['inventory_number'] == 'INV002'
    
    def test_monthly_report(self, authenticated_client):
        """Тест получения отчёта за месяц."""
        year = timezone.now().year
        month = timezone.now().month
        response = authenticated_client.get(f'/api/staff/monthly-report/?year={year}&month={month}')
        assert response.status_code == status.HTTP_200_OK
        assert 'daily_statistics' in response.data
        assert 'new_readers' in response.data

