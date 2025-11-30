"""
Views and ViewSets for library API.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, F, Sum
from django.utils import timezone
from datetime import timedelta, datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from .models import (
    Author, Publisher, BookSection, Book, BookAuthor,
    Hall, Reader, BookCopy, BookIssue, HallBookStock, Staff
)
from .serializers import (
    AuthorSerializer, PublisherSerializer, BookSectionSerializer,
    BookSerializer, BookCreateUpdateSerializer,
    HallSerializer, ReaderSerializer,
    BookCopySerializer, BookIssueSerializer,
    HallBookStockSerializer, StaffSerializer,
    StaffLoginSerializer, StaffRegistrationSerializer, BookAcceptSerializer
)

AUTH_DOCS = [{'BearerAuth': []}]


@extend_schema_view(
    list=extend_schema(
        summary='Список авторов',
        description='Получить список всех авторов. Требуется JWT аутентификация.',
        tags=['Authors'],
        auth=AUTH_DOCS,
    ),
    retrieve=extend_schema(
        summary='Детали автора',
        description='Получить информацию об авторе по ID. Требуется JWT аутентификация.',
        tags=['Authors'],
        auth=AUTH_DOCS,
    ),
    create=extend_schema(
        summary='Создать автора',
        description='Создать нового автора. Требуется JWT аутентификация.',
        tags=['Authors'],
        auth=AUTH_DOCS,
    ),
    update=extend_schema(
        summary='Обновить автора',
        description='Полностью обновить информацию об авторе. Требуется JWT аутентификация.',
        tags=['Authors'],
        auth=AUTH_DOCS,
    ),
    partial_update=extend_schema(
        summary='Частично обновить автора',
        description='Частично обновить информацию об авторе. Требуется JWT аутентификация.',
        tags=['Authors'],
        auth=AUTH_DOCS,
    ),
    destroy=extend_schema(
        summary='Удалить автора',
        description='Удалить автора. Требуется JWT аутентификация.',
        tags=['Authors'],
        auth=AUTH_DOCS,
    ),
)
class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet для авторов."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]  # Явно указываем, что требуется аутентификация
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name']
    ordering_fields = ['full_name', 'created_at']
    ordering = ['full_name']


@extend_schema_view(
    list=extend_schema(
        summary='Список издательств',
        description='Получить список всех издательств. Требуется JWT аутентификация.',
        tags=['Publishers'],
        auth=AUTH_DOCS,
    ),
    retrieve=extend_schema(
        summary='Детали издательства',
        description='Получить информацию об издательстве по ID. Требуется JWT аутентификация.',
        tags=['Publishers'],
        auth=AUTH_DOCS,
    ),
    create=extend_schema(
        summary='Создать издательство',
        description='Создать новое издательство. Требуется JWT аутентификация.',
        tags=['Publishers'],
        auth=AUTH_DOCS,
    ),
    update=extend_schema(
        summary='Обновить издательство',
        description='Полностью обновить информацию об издательстве. Требуется JWT аутентификация.',
        tags=['Publishers'],
        auth=AUTH_DOCS,
    ),
    partial_update=extend_schema(
        summary='Частично обновить издательство',
        description='Частично обновить информацию об издательстве. Требуется JWT аутентификация.',
        tags=['Publishers'],
        auth=AUTH_DOCS,
    ),
    destroy=extend_schema(
        summary='Удалить издательство',
        description='Удалить издательство. Требуется JWT аутентификация.',
        tags=['Publishers'],
        auth=AUTH_DOCS,
    ),
)
class PublisherViewSet(viewsets.ModelViewSet):
    """ViewSet для издательств."""
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAuthenticated]  # Явно указываем, что требуется аутентификация
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @extend_schema(
        summary='Книги издательства',
        description='Получить список всех книг, изданных данным издательством (вложенные объекты). Требуется JWT аутентификация.',
        responses={200: BookSerializer(many=True)},
        tags=['Publishers'],
        auth=AUTH_DOCS,
    )
    @action(detail=True, methods=['get'], url_path='books')
    def publisher_books(self, request, pk=None):
        """Получить книги издательства."""
        publisher = self.get_object()
        books = Book.objects.filter(publisher=publisher).select_related('publisher', 'section').prefetch_related('authors')
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary='Список разделов книг',
        description='Получить список всех разделов книг. Требуется JWT аутентификация.',
        tags=['Book Sections'],
        auth=AUTH_DOCS,
    ),
    retrieve=extend_schema(
        summary='Детали раздела',
        description='Получить информацию о разделе книг по ID. Требуется JWT аутентификация.',
        tags=['Book Sections'],
        auth=AUTH_DOCS,
    ),
    create=extend_schema(
        summary='Создать раздел',
        description='Создать новый раздел книг. Требуется JWT аутентификация.',
        tags=['Book Sections'],
        auth=AUTH_DOCS,
    ),
    update=extend_schema(
        summary='Обновить раздел',
        description='Полностью обновить информацию о разделе книг. Требуется JWT аутентификация.',
        tags=['Book Sections'],
        auth=AUTH_DOCS,
    ),
    partial_update=extend_schema(
        summary='Частично обновить раздел',
        description='Частично обновить информацию о разделе книг. Требуется JWT аутентификация.',
        tags=['Book Sections'],
        auth=AUTH_DOCS,
    ),
    destroy=extend_schema(
        summary='Удалить раздел',
        description='Удалить раздел книг. Требуется JWT аутентификация.',
        tags=['Book Sections'],
        auth=AUTH_DOCS,
    ),
)
class BookSectionViewSet(viewsets.ModelViewSet):
    """ViewSet для разделов книг."""
    queryset = BookSection.objects.all()
    serializer_class = BookSectionSerializer
    permission_classes = [IsAuthenticated]  # Явно указываем, что требуется аутентификация
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


@extend_schema_view(
    list=extend_schema(
        summary='Список книг',
        description='Получить список всех книг. Требуется JWT аутентификация.',
        tags=['Books'],
        auth=AUTH_DOCS,
    ),
    retrieve=extend_schema(
        summary='Детали книги',
        description='Получить информацию о книге по ID. Требуется JWT аутентификация.',
        tags=['Books'],
        auth=AUTH_DOCS,
    ),
    create=extend_schema(
        summary='Создать книгу',
        description='Создать новую книгу. Требуется JWT аутентификация.',
        tags=['Books'],
        auth=AUTH_DOCS,
    ),
    update=extend_schema(
        summary='Обновить книгу',
        description='Полностью обновить информацию о книге. Требуется JWT аутентификация.',
        tags=['Books'],
        auth=AUTH_DOCS,
    ),
    partial_update=extend_schema(
        summary='Частично обновить книгу',
        description='Частично обновить информацию о книге. Требуется JWT аутентификация.',
        tags=['Books'],
        auth=AUTH_DOCS,
    ),
    destroy=extend_schema(
        summary='Удалить книгу',
        description='Удалить книгу. Требуется JWT аутентификация.',
        tags=['Books'],
        auth=AUTH_DOCS,
    ),
)
class BookViewSet(viewsets.ModelViewSet):
    """ViewSet для книг."""
    queryset = Book.objects.select_related('publisher', 'section').prefetch_related('authors').all()
    permission_classes = [IsAuthenticated]  # Явно указываем, что требуется аутентификация
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'cipher']
    ordering_fields = ['title', 'publish_year', 'cipher', 'created_at']
    ordering = ['title']
    filterset_fields = ['publisher', 'section', 'publish_year']
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия."""
        if self.action in ['create', 'update', 'partial_update']:
            return BookCreateUpdateSerializer
        return BookSerializer
    
    @extend_schema(
        summary='Экземпляры книги',
        description='Получить список всех экземпляров данной книги (вложенные объекты). Требуется JWT аутентификация.',
        responses={200: BookCopySerializer(many=True)},
        tags=['Books'],
        auth=AUTH_DOCS,
    )
    @action(detail=True, methods=['get'], url_path='copies')
    def book_copies(self, request, pk=None):
        """Получить экземпляры книги."""
        book = self.get_object()
        copies = BookCopy.objects.filter(book=book).select_related('book', 'hall')
        serializer = BookCopySerializer(copies, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary='Список залов',
        description='Получить список всех читальных залов. Требуется JWT аутентификация.',
        tags=['Halls'],
        auth=AUTH_DOCS,
    ),
    retrieve=extend_schema(
        summary='Детали зала',
        description='Получить информацию о читальном зале по ID. Требуется JWT аутентификация.',
        tags=['Halls'],
        auth=AUTH_DOCS,
    ),
    create=extend_schema(
        summary='Создать зал',
        description='Создать новый читальный зал. Требуется JWT аутентификация.',
        tags=['Halls'],
        auth=AUTH_DOCS,
    ),
    update=extend_schema(
        summary='Обновить зал',
        description='Полностью обновить информацию о читальном зале. Требуется JWT аутентификация.',
        tags=['Halls'],
        auth=AUTH_DOCS,
    ),
    partial_update=extend_schema(
        summary='Частично обновить зал',
        description='Частично обновить информацию о читальном зале. Требуется JWT аутентификация.',
        tags=['Halls'],
        auth=AUTH_DOCS,
    ),
    destroy=extend_schema(
        summary='Удалить зал',
        description='Удалить читальный зал. Требуется JWT аутентификация.',
        tags=['Halls'],
        auth=AUTH_DOCS,
    ),
)
class HallViewSet(viewsets.ModelViewSet):
    """ViewSet для читальных залов."""
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [IsAuthenticated]  # Явно указываем, что требуется аутентификация
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['hall_number', 'name', 'capacity']
    ordering = ['hall_number']
    
    @extend_schema(
        summary='Читатели зала',
        description='Получить список всех читателей, закреплённых за данным залом (вложенные объекты). Требуется JWT аутентификация.',
        responses={200: ReaderSerializer(many=True)},
        tags=['Halls'],
        auth=AUTH_DOCS,
    )
    @action(detail=True, methods=['get'], url_path='readers')
    def hall_readers(self, request, pk=None):
        """Получить читателей зала."""
        hall = self.get_object()
        readers = Reader.objects.filter(hall=hall).select_related('hall')
        serializer = ReaderSerializer(readers, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary='Список читателей',
        description='Получить список всех читателей. Требуется JWT аутентификация.',
        tags=['Readers'],
        auth=AUTH_DOCS,
    ),
    retrieve=extend_schema(
        summary='Детали читателя',
        description='Получить информацию о читателе по ID. Требуется JWT аутентификация.',
        tags=['Readers'],
        auth=AUTH_DOCS,
    ),
    create=extend_schema(
        summary='Создать читателя',
        description='Создать нового читателя. Требуется JWT аутентификация.',
        tags=['Readers'],
        auth=AUTH_DOCS,
    ),
    update=extend_schema(
        summary='Обновить читателя',
        description='Полностью обновить информацию о читателе. Требуется JWT аутентификация.',
        tags=['Readers'],
        auth=AUTH_DOCS,
    ),
    partial_update=extend_schema(
        summary='Частично обновить читателя',
        description='Частично обновить информацию о читателе. Требуется JWT аутентификация.',
        tags=['Readers'],
        auth=AUTH_DOCS,
    ),
    destroy=extend_schema(
        summary='Удалить читателя',
        description='Удалить читателя. Требуется JWT аутентификация.',
        tags=['Readers'],
        auth=AUTH_DOCS,
    ),
)
class ReaderViewSet(viewsets.ModelViewSet):
    """ViewSet для читателей."""
    queryset = Reader.objects.select_related('hall').all()
    serializer_class = ReaderSerializer
    permission_classes = [IsAuthenticated]  # Явно указываем, что требуется аутентификация
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['card_number', 'full_name', 'passport_number', 'phone']
    ordering_fields = ['full_name', 'card_number', 'birth_date', 'registration_date']
    ordering = ['full_name']
    filterset_fields = ['hall', 'education_level', 'has_academic_degree', 'is_active']
    
    @extend_schema(
        summary='Книги закреплённые за читателем',
        description='Получить список всех книг, которые закреплены за указанным читателем и ещё не возвращены. Требуется JWT аутентификация.',
        responses={200: BookIssueSerializer(many=True)},
        tags=['Readers'],
        auth=AUTH_DOCS,
    )
    @action(detail=True, methods=['get'], url_path='books')
    def reader_books(self, request, pk=None):
        """Получить книги, закреплённые за читателем."""
        reader = self.get_object()
        issues = BookIssue.objects.filter(
            reader=reader,
            return_date__isnull=True
        ).select_related('copy__book', 'hall')
        
        serializer = BookIssueSerializer(issues, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary='Статистика по возрасту читателей',
        description='Получить количество активных читателей младше указанного возраста. Требуется JWT аутентификация.',
        parameters=[
            OpenApiParameter('age', OpenApiTypes.INT, description='Максимальный возраст читателей', required=True, location=OpenApiParameter.QUERY)
        ],
        responses={200: OpenApiTypes.OBJECT},
        tags=['Readers'],
        auth=AUTH_DOCS,
    )
    @action(detail=False, methods=['get'], url_path='statistics/age')
    def age_statistics(self, request):
        """Статистика по возрасту читателей."""
        max_age = request.query_params.get('age', 20)
        try:
            max_age = int(max_age)
        except ValueError:
            return Response(
                {'error': 'Параметр age должен быть числом.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        today = timezone.now().date()
        min_birth_date = today - timedelta(days=max_age * 365)
        
        count = Reader.objects.filter(
            birth_date__gte=min_birth_date,
            is_active=True
        ).count()
        
        return Response({
            'max_age': max_age,
            'readers_count': count
        })
    
    @extend_schema(
        summary='Статистика по образованию читателей',
        description='Получить процентное соотношение активных читателей по уровню образования. Включает: начальное, среднее, высшее образование, не указано, и наличие учёной степени. Проценты считаются от общего количества активных читателей. Требуется JWT аутентификация.',
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'total': {
                        'type': 'integer',
                        'description': 'Общее количество активных читателей',
                        'example': 100
                    },
                    'percentages': {
                        'type': 'object',
                        'description': 'Процентное соотношение читателей по категориям образования',
                        'properties': {
                            'начальное': {
                                'type': 'number',
                                'format': 'float',
                                'description': 'Процент читателей с начальным образованием',
                                'example': 10.0
                            },
                            'среднее': {
                                'type': 'number',
                                'format': 'float',
                                'description': 'Процент читателей со средним образованием',
                                'example': 30.0
                            },
                            'высшее': {
                                'type': 'number',
                                'format': 'float',
                                'description': 'Процент читателей с высшим образованием',
                                'example': 50.0
                            },
                            'не_указано': {
                                'type': 'number',
                                'format': 'float',
                                'description': 'Процент читателей без указанного уровня образования',
                                'example': 10.0
                            },
                            'учёная_степень': {
                                'type': 'number',
                                'format': 'float',
                                'description': 'Процент читателей с учёной степенью (независимо от уровня образования). Может быть больше 0 даже если у читателя указан уровень образования.',
                                'example': 15.0
                            }
                        }
                    }
                },
                'example': {
                    'total': 100,
                    'percentages': {
                        'начальное': 10.0,
                        'среднее': 30.0,
                        'высшее': 50.0,
                        'не_указано': 10.0,
                        'учёная_степень': 15.0
                    }
                }
            },
            401: {
                'type': 'object',
                'description': 'Требуется аутентификация'
            }
        },
        tags=['Readers'],
        auth=AUTH_DOCS,
    )
    @action(detail=False, methods=['get'], url_path='statistics/education')
    def education_statistics(self, request):
        """Статистика по образованию читателей."""
        active_readers = Reader.objects.filter(is_active=True)
        total = active_readers.count()
        
        if total == 0:
            return Response({
                'total': 0,
                'percentages': {
                    'начальное': 0,
                    'среднее': 0,
                    'высшее': 0,
                    'не_указано': 0,
                    'учёная_степень': 0
                }
            })
        
        # Подсчитываем по уровням образования
        primary_count = active_readers.filter(education_level='начальное').count()
        secondary_count = active_readers.filter(education_level='среднее').count()
        higher_count = active_readers.filter(education_level='высшее').count()
        not_specified_count = active_readers.filter(education_level__isnull=True).count()
        
        # Подсчитываем читателей с учёной степенью (независимо от уровня образования)
        academic_degree_count = active_readers.filter(has_academic_degree=True).count()
        
        result = {
            'total': total,
            'percentages': {
                'начальное': round(primary_count / total * 100, 2),
                'среднее': round(secondary_count / total * 100, 2),
                'высшее': round(higher_count / total * 100, 2),
                'не_указано': round(not_specified_count / total * 100, 2),
                'учёная_степень': round(academic_degree_count / total * 100, 2)
            }
        }
        
        return Response(result)


@extend_schema_view(
    list=extend_schema(
        summary='Список экземпляров книг',
        description='Получить список всех экземпляров книг. Требуется JWT аутентификация.',
        tags=['Book Copies'],
        auth=AUTH_DOCS,
    ),
    retrieve=extend_schema(
        summary='Детали экземпляра',
        description='Получить информацию об экземпляре книги по ID. Требуется JWT аутентификация.',
        tags=['Book Copies'],
        auth=AUTH_DOCS,
    ),
    create=extend_schema(
        summary='Создать экземпляр',
        description='Создать новый экземпляр книги. Требуется JWT аутентификация.',
        tags=['Book Copies'],
        auth=AUTH_DOCS,
    ),
    update=extend_schema(
        summary='Обновить экземпляр',
        description='Полностью обновить информацию об экземпляре книги. Требуется JWT аутентификация.',
        tags=['Book Copies'],
        auth=AUTH_DOCS,
    ),
    partial_update=extend_schema(
        summary='Частично обновить экземпляр',
        description='Частично обновить информацию об экземпляре книги. Требуется JWT аутентификация.',
        tags=['Book Copies'],
        auth=AUTH_DOCS,
    ),
    destroy=extend_schema(
        summary='Удалить экземпляр',
        description='Удалить экземпляр книги. Требуется JWT аутентификация.',
        tags=['Book Copies'],
        auth=AUTH_DOCS,
    ),
)
class BookCopyViewSet(viewsets.ModelViewSet):
    """ViewSet для экземпляров книг."""
    queryset = BookCopy.objects.select_related('book', 'hall').all()
    serializer_class = BookCopySerializer
    permission_classes = [IsAuthenticated]  # Явно указываем, что требуется аутентификация
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['inventory_number', 'book__title']
    ordering_fields = ['registration_date', 'inventory_number']
    ordering = ['-registration_date']
    filterset_fields = ['book', 'hall', 'is_written_off']


@extend_schema_view(
    list=extend_schema(
        summary='Список выдач книг',
        description='Получить список всех выдач книг читателям. Требуется JWT аутентификация.',
        tags=['Book Issues'],
        auth=AUTH_DOCS,
    ),
    retrieve=extend_schema(
        summary='Детали выдачи',
        description='Получить информацию о выдаче книги по ID. Требуется JWT аутентификация.',
        tags=['Book Issues'],
        auth=AUTH_DOCS,
    ),
    create=extend_schema(
        summary='Выдать книгу читателю',
        description='Создать запись о выдаче книги читателю. Проверяет, что экземпляр не выдан другому читателю. Требуется JWT аутентификация.',
        request=BookIssueSerializer,
        responses={201: BookIssueSerializer},
        tags=['Book Issues'],
        auth=AUTH_DOCS,
    ),
    update=extend_schema(
        summary='Обновить выдачу',
        description='Полностью обновить информацию о выдаче книги. Требуется JWT аутентификация.',
        tags=['Book Issues'],
        auth=AUTH_DOCS,
    ),
    partial_update=extend_schema(
        summary='Частично обновить выдачу',
        description='Частично обновить информацию о выдаче книги. Требуется JWT аутентификация.',
        tags=['Book Issues'],
        auth=AUTH_DOCS,
    ),
    destroy=extend_schema(
        summary='Удалить выдачу',
        description='Удалить запись о выдаче книги. Требуется JWT аутентификация.',
        tags=['Book Issues'],
        auth=AUTH_DOCS,
    ),
)
class BookIssueViewSet(viewsets.ModelViewSet):
    """ViewSet для выдач книг."""
    queryset = BookIssue.objects.select_related(
        'reader', 'copy__book', 'hall'
    ).all()
    serializer_class = BookIssueSerializer
    permission_classes = [IsAuthenticated]  # Явно указываем, что требуется аутентификация
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['reader__full_name', 'copy__book__title', 'copy__inventory_number']
    ordering_fields = ['issue_date', 'return_date']
    ordering = ['-issue_date']
    filterset_fields = ['reader', 'copy', 'hall', 'issue_date', 'return_date']
    
    @extend_schema(
        summary='Просроченные выдачи',
        description='Получить список выдач книг, которые были выданы более месяца назад и ещё не возвращены. Требуется JWT аутентификация.',
        responses={200: BookIssueSerializer(many=True)},
        tags=['Book Issues'],
        auth=AUTH_DOCS,
    )
    @action(detail=False, methods=['get'], url_path='overdue')
    def overdue_issues(self, request):
        """Читатели с книгами, взятыми более месяца назад."""
        month_ago = timezone.now().date() - timedelta(days=30)
        issues = BookIssue.objects.filter(
            issue_date__lt=month_ago,
            return_date__isnull=True
        ).select_related('reader', 'copy__book', 'hall')
        
        serializer = BookIssueSerializer(issues, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary='Читатели с редкими книгами',
        description='Получить список активных выдач книг, у которых общее количество экземпляров в библиотеке (во всех залах) не превышает 2. Требуется JWT аутентификация.',
        responses={200: BookIssueSerializer(many=True)},
        tags=['Book Issues'],
        auth=AUTH_DOCS,
    )
    @action(detail=False, methods=['get'], url_path='rare-books')
    def rare_books_readers(self, request):
        """Читатели с редкими книгами (≤2 экземпляра во всей библиотеке)."""
        # Считаем количество не списанных экземпляров каждой книги во всех залах
        # Находим книги, у которых общее количество не списанных экземпляров ≤ 2
        rare_books = BookCopy.objects.filter(
            is_written_off=False
        ).values('book_id').annotate(
            total_copies=Count('copy_id')
        ).filter(
            total_copies__lte=2
        ).values_list('book_id', flat=True)
        
        # Находим активные выдачи этих книг
        issues = BookIssue.objects.filter(
            copy__book_id__in=rare_books,
            return_date__isnull=True
        ).select_related('reader', 'copy__book', 'hall')
        
        serializer = BookIssueSerializer(issues, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Выдать книгу читателю с проверкой на активную выдачу."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Проверяем, что экземпляр не выдан
        copy_id = serializer.validated_data['copy'].copy_id
        active_issue = BookIssue.objects.filter(
            copy_id=copy_id,
            return_date__isnull=True
        ).exists()
        
        if active_issue:
            return Response(
                {'error': 'Этот экземпляр уже выдан другому читателю.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
@extend_schema_view(
    list=extend_schema(
        summary='Список складов книг',
        description='Получить список всех записей о количестве книг в залах. Требуется JWT аутентификация.',
        tags=['Hall Book Stock'],
        auth=AUTH_DOCS,
    ),
    retrieve=extend_schema(
        summary='Детали склада',
        description='Получить информацию о количестве конкретной книги в зале по ID. Требуется JWT аутентификация.',
        tags=['Hall Book Stock'],
        auth=AUTH_DOCS,
    ),
    create=extend_schema(
        summary='Создать запись склада',
        description='Создать новую запись о количестве книги в зале. Требуется JWT аутентификация.',
        tags=['Hall Book Stock'],
        auth=AUTH_DOCS,
    ),
    update=extend_schema(
        summary='Обновить запись склада',
        description='Полностью обновить информацию о количестве книги в зале. Требуется JWT аутентификация.',
        tags=['Hall Book Stock'],
        auth=AUTH_DOCS,
    ),
    partial_update=extend_schema(
        summary='Частично обновить запись склада',
        description='Частично обновить информацию о количестве книги в зале. Требуется JWT аутентификация.',
        tags=['Hall Book Stock'],
        auth=AUTH_DOCS,
    ),
    destroy=extend_schema(
        summary='Удалить запись склада',
        description='Удалить запись о количестве книги в зале. Требуется JWT аутентификация.',
        tags=['Hall Book Stock'],
        auth=AUTH_DOCS,
    ),
)
class HallBookStockViewSet(viewsets.ModelViewSet):
    """ViewSet для склада книг в залах."""
    serializer_class = HallBookStockSerializer
    permission_classes = [IsAuthenticated]  # Явно указываем, что требуется аутентификация
    filter_backends = []  # Отключаем стандартные фильтры, используем raw SQL
    ordering_fields = ['copies_total']
    ordering = ['hall', 'book']
    
    def list(self, request, *args, **kwargs):
        """Переопределяем list для работы с raw SQL, так как в таблице нет поля id."""
        from django.db import connection
        
        # Строим SQL запрос
        sql = """
            SELECT 
                hbs.hall_id,
                hbs.book_id,
                hbs.copies_total,
                hbs.created_at,
                hbs.updated_at
            FROM hall_book_stock hbs
        """
        
        params = []
        where_clauses = []
        
        # Применяем фильтры из query params
        hall_id = request.query_params.get('hall')
        if hall_id:
            where_clauses.append("hbs.hall_id = %s")
            params.append(hall_id)
        
        book_id = request.query_params.get('book')
        if book_id:
            where_clauses.append("hbs.book_id = %s")
            params.append(book_id)
        
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)
        
        sql += " ORDER BY hbs.hall_id, hbs.book_id"
        
        # Выполняем запрос
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            results = []
            for row in cursor.fetchall():
                row_dict = dict(zip(columns, row))
                # Создаём объект модели вручную
                hall = Hall.objects.get(hall_id=row_dict['hall_id'])
                book = Book.objects.get(book_id=row_dict['book_id'])
                
                stock = HallBookStock(
                    hall=hall,
                    book=book,
                    copies_total=row_dict['copies_total'],
                    created_at=row_dict['created_at'],
                    updated_at=row_dict['updated_at']
                )
                # Устанавливаем pk вручную для идентификации (используем составной ключ)
                stock.pk = f"{hall.hall_id}_{book.book_id}"
                results.append(stock)
        
        # Сериализуем результаты
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Получаем объект по составному ключу (hall_id и book_id)."""
        from django.db import connection
        from rest_framework.exceptions import NotFound
        
        pk = kwargs.get('pk', '')
        # Пытаемся разобрать составной ключ
        if '_' in str(pk):
            parts = str(pk).split('_')
            if len(parts) == 2:
                try:
                    hall_id = int(parts[0])
                    book_id = int(parts[1])
                except ValueError:
                    raise NotFound("Неверный формат ключа. Используйте 'hall_id_book_id'.")
            else:
                raise NotFound("Неверный формат ключа. Используйте 'hall_id_book_id'.")
        else:
            raise NotFound("Неверный формат ключа. Используйте 'hall_id_book_id'.")
        
        # Получаем объект через raw SQL
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    hbs.hall_id,
                    hbs.book_id,
                    hbs.copies_total,
                    hbs.created_at,
                    hbs.updated_at
                FROM hall_book_stock hbs
                WHERE hbs.hall_id = %s AND hbs.book_id = %s
            """, [hall_id, book_id])
            
            row = cursor.fetchone()
            if not row:
                raise NotFound("Объект не найден.")
            
            columns = [col[0] for col in cursor.description]
            row_dict = dict(zip(columns, row))
            
            hall = Hall.objects.get(hall_id=row_dict['hall_id'])
            book = Book.objects.get(book_id=row_dict['book_id'])
            
            stock = HallBookStock(
                hall=hall,
                book=book,
                copies_total=row_dict['copies_total'],
                created_at=row_dict['created_at'],
                updated_at=row_dict['updated_at']
            )
            stock.pk = f"{hall.hall_id}_{book.book_id}"
        
        serializer = self.get_serializer(stock)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Создаём запись через raw SQL."""
        from django.db import connection
        from rest_framework.exceptions import ValidationError
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        hall = serializer.validated_data['hall']
        book = serializer.validated_data['book']
        copies_total = serializer.validated_data['copies_total']
        
        # Проверяем, существует ли запись
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM hall_book_stock 
                WHERE hall_id = %s AND book_id = %s
            """, [hall.hall_id, book.book_id])
            
            if cursor.fetchone()[0] > 0:
                raise ValidationError({'error': 'Запись с таким залом и книгой уже существует.'})
            
            # Создаём запись
            cursor.execute("""
                INSERT INTO hall_book_stock (hall_id, book_id, copies_total, created_at, updated_at)
                VALUES (%s, %s, %s, NOW(), NOW())
            """, [hall.hall_id, book.book_id, copies_total])
        
        # Получаем созданный объект
        stock = HallBookStock(
            hall=hall,
            book=book,
            copies_total=copies_total
        )
        stock.pk = f"{hall.hall_id}_{book.book_id}"
        
        serializer = self.get_serializer(stock)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """Обновляем запись через raw SQL."""
        from django.db import connection
        from rest_framework.exceptions import NotFound
        
        pk = kwargs.get('pk', '')
        if '_' not in str(pk):
            raise NotFound("Неверный формат ключа. Используйте 'hall_id_book_id'.")
        
        parts = str(pk).split('_')
        if len(parts) != 2:
            raise NotFound("Неверный формат ключа. Используйте 'hall_id_book_id'.")
        
        try:
            hall_id = int(parts[0])
            book_id = int(parts[1])
        except ValueError:
            raise NotFound("Неверный формат ключа. Используйте 'hall_id_book_id'.")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_hall = serializer.validated_data['hall']
        new_book = serializer.validated_data['book']
        copies_total = serializer.validated_data['copies_total']
        
        # Обновляем запись
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE hall_book_stock 
                SET hall_id = %s, book_id = %s, copies_total = %s, updated_at = NOW()
                WHERE hall_id = %s AND book_id = %s
            """, [new_hall.hall_id, new_book.book_id, copies_total, hall_id, book_id])
            
            if cursor.rowcount == 0:
                raise NotFound("Объект не найден.")
        
        stock = HallBookStock(
            hall=new_hall,
            book=new_book,
            copies_total=copies_total
        )
        stock.pk = f"{new_hall.hall_id}_{new_book.book_id}"
        
        serializer = self.get_serializer(stock)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Удаляем запись через raw SQL."""
        from django.db import connection
        from rest_framework.exceptions import NotFound
        
        pk = kwargs.get('pk', '')
        if '_' not in str(pk):
            raise NotFound("Неверный формат ключа. Используйте 'hall_id_book_id'.")
        
        parts = str(pk).split('_')
        if len(parts) != 2:
            raise NotFound("Неверный формат ключа. Используйте 'hall_id_book_id'.")
        
        try:
            hall_id = int(parts[0])
            book_id = int(parts[1])
        except ValueError:
            raise NotFound("Неверный формат ключа. Используйте 'hall_id_book_id'.")
        
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM hall_book_stock 
                WHERE hall_id = %s AND book_id = %s
            """, [hall_id, book_id])
            
            if cursor.rowcount == 0:
                raise NotFound("Объект не найден.")
        
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=extend_schema(
        summary='Список сотрудников',
        description='Получить список всех сотрудников библиотеки. Требуется JWT аутентификация.',
        tags=['Staff'],
        auth=AUTH_DOCS,
    ),
    retrieve=extend_schema(
        summary='Детали сотрудника',
        description='Получить информацию о сотруднике по ID. Требуется JWT аутентификация.',
        tags=['Staff'],
        auth=AUTH_DOCS,
    ),
    create=extend_schema(exclude=True),  # Исключаем create из Swagger документации
    update=extend_schema(
        summary='Обновить сотрудника',
        description='Полностью обновить информацию о сотруднике. Требуется JWT аутентификация.',
        tags=['Staff'],
        auth=AUTH_DOCS,
    ),
    partial_update=extend_schema(
        summary='Частично обновить сотрудника',
        description='Частично обновить информацию о сотруднике. Требуется JWT аутентификация.',
        tags=['Staff'],
        auth=AUTH_DOCS,
    ),
    destroy=extend_schema(
        summary='Удалить сотрудника',
        description='Удалить сотрудника. Требуется JWT аутентификация.',
        tags=['Staff'],
        auth=AUTH_DOCS,
    ),
)
class StaffViewSet(viewsets.ModelViewSet):
    """ViewSet для сотрудников."""
    queryset = Staff.objects.all()
    permission_classes = [IsAuthenticated]  # Явно указываем, что требуется аутентификация
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['login', 'email']
    ordering_fields = ['login', 'created_at']
    ordering = ['login']
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия."""
        return StaffSerializer
    
    def create(self, request, *args, **kwargs):
        """Запрещаем создание сотрудника через стандартный POST /api/staff/."""
        from rest_framework.exceptions import MethodNotAllowed
        raise MethodNotAllowed('POST', detail='Используйте /api/staff/register-staff/ для регистрации нового сотрудника с секретным ключом.')
    
    @extend_schema(
        summary='Регистрация нового читателя',
        description='Зарегистрировать нового читателя в библиотеке. Требуется JWT аутентификация.',
        request=ReaderSerializer,
        responses={201: ReaderSerializer},
        tags=['Staff'],
        auth=AUTH_DOCS,
    )
    @action(detail=False, methods=['post'], url_path='register-reader', permission_classes=[IsAuthenticated])
    def register_reader(self, request):
        """Записать нового читателя в библиотеку."""
        serializer = ReaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary='Регистрация нового сотрудника',
        description='Зарегистрировать нового сотрудника библиотеки. Требуется JWT аутентификация и секретный ключ регистрации.',
        request=StaffRegistrationSerializer,
        responses={201: StaffSerializer},
        tags=['Staff'],
        auth=AUTH_DOCS,
    )
    @action(detail=False, methods=['post'], url_path='register-staff', permission_classes=[IsAuthenticated])
    def register_staff(self, request):
        """Зарегистрировать нового сотрудника (по секретному ключу)."""
        serializer = StaffRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff = serializer.save()
        return Response(StaffSerializer(staff).data, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        summary='Исключить неактивных читателей',
        description='Исключить читателей, которые записались в библиотеку более года назад и не прошли перерегистрацию. Требуется JWT аутентификация.',
        responses={200: OpenApiTypes.OBJECT},
        tags=['Staff'],
        auth=AUTH_DOCS,
    )
    @action(detail=False, methods=['post'], url_path='deactivate-old-readers', permission_classes=[IsAuthenticated])
    def deactivate_old_readers(self, request):
        """Исключить читателей, записавшихся более года назад без перерегистрации."""
        year_ago = timezone.now().date() - timedelta(days=365)
        
        readers = Reader.objects.filter(
            registration_date__lt=year_ago,
            last_reregistration_date__isnull=True,
            is_active=True
        )
        
        count = readers.count()
        readers.update(is_active=False)
        
        return Response({
            'deactivated_count': count,
            'message': f'Исключено {count} читателей.'
        })
    
    @extend_schema(
        summary='Списать книгу',
        description='Пометить экземпляр книги как списанный. Книга не должна быть выдана читателю. Требуется JWT аутентификация.',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'copy_id': {
                        'type': 'integer',
                        'description': 'ID экземпляра книги',
                        'example': 115
                    }
                },
                'required': ['copy_id']
            }
        },
        responses={200: BookCopySerializer},
        tags=['Staff'],
        auth=AUTH_DOCS,
    )
    @action(detail=False, methods=['post'], url_path='writeoff-book', permission_classes=[IsAuthenticated])
    def writeoff_book(self, request):
        """Списать книгу."""
        # Пробуем получить copy_id из тела запроса
        copy_id = request.data.get('copy_id')
        
        # Если не нашли в data, пробуем в query_params (на случай, если отправлен как query parameter)
        if not copy_id:
            copy_id = request.query_params.get('copy_id')
            if copy_id:
                try:
                    copy_id = int(copy_id)
                except (ValueError, TypeError):
                    copy_id = None
        
        if not copy_id:
            return Response(
                {'error': 'Параметр copy_id обязателен.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            copy = BookCopy.objects.get(copy_id=copy_id, is_written_off=False)
        except BookCopy.DoesNotExist:
            return Response(
                {'error': 'Экземпляр не найден или уже списан.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Проверяем, что книга не выдана
        active_issue = BookIssue.objects.filter(
            copy=copy,
            return_date__isnull=True
        ).exists()
        
        if active_issue:
            return Response(
                {'error': 'Нельзя списать книгу, которая выдана читателю.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        copy.is_written_off = True
        copy.writeoff_date = timezone.now().date()
        copy.save()
        
        # Обновляем склад
        HallBookStock.objects.filter(
            hall=copy.hall,
            book=copy.book
        ).update(copies_total=F('copies_total') - 1)
        
        serializer = BookCopySerializer(copy)
        return Response(serializer.data)
    
    @extend_schema(
        summary='Принять книгу в фонд',
        description='Принять книгу в фонд библиотеки. Если книги ещё нет в библиотеке, создаёт её, затем создаёт экземпляр книги и обновляет склад. Требуется JWT аутентификация.\n\n**Вариант 1: Принять экземпляр существующей книги**\n- Укажите `book_id` существующей книги\n- Укажите `hall` и `inventory_number` для экземпляра\n\n**Вариант 2: Принять новую книгу**\n- Не указывайте `book_id`\n- Укажите `title` и `cipher` (обязательно)\n- Опционально: `publisher`, `publish_year`, `section`, `author_ids`\n- Укажите `hall` и `inventory_number` для экземпляра',
        request=BookAcceptSerializer,
        responses={
            201: BookCopySerializer,
            400: {
                'type': 'object',
                'description': 'Ошибка валидации данных',
                'properties': {
                    'book_id': {'type': 'array', 'items': {'type': 'string'}},
                    'title': {'type': 'array', 'items': {'type': 'string'}},
                    'cipher': {'type': 'array', 'items': {'type': 'string'}},
                    'inventory_number': {'type': 'array', 'items': {'type': 'string'}},
                    'hall': {'type': 'array', 'items': {'type': 'string'}},
                    'non_field_errors': {'type': 'array', 'items': {'type': 'string'}}
                }
            },
            401: {
                'type': 'object',
                'description': 'Требуется аутентификация'
            }
        },
        tags=['Staff'],
        auth=AUTH_DOCS,
    )
    @action(detail=False, methods=['post'], url_path='accept-book', permission_classes=[IsAuthenticated])
    def accept_book(self, request):
        """Принять книгу в фонд библиотеки."""
        serializer = BookAcceptSerializer(data=request.data)
        if serializer.is_valid():
            copy = serializer.save()
            # Возвращаем данные экземпляра через BookCopySerializer для единообразия
            copy_serializer = BookCopySerializer(copy)
            return Response(copy_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary='Отчёт за месяц',
        description='Получить отчёт о работе библиотеки за указанный месяц. Включает: количество книг и читателей на каждый день в каждом зале и в библиотеке в целом, количество читателей, записавшихся в каждый зал и в библиотеку за отчетный месяц. Требуется JWT аутентификация.',
        parameters=[
            OpenApiParameter('year', OpenApiTypes.INT, description='Год отчёта', required=True, location=OpenApiParameter.QUERY),
            OpenApiParameter('month', OpenApiTypes.INT, description='Месяц отчёта (1-12)', required=True, location=OpenApiParameter.QUERY)
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'period': {
                        'type': 'object',
                        'properties': {
                            'year': {'type': 'integer', 'description': 'Год отчёта'},
                            'month': {'type': 'integer', 'description': 'Месяц отчёта (1-12)'},
                            'start_date': {'type': 'string', 'format': 'date', 'description': 'Начало периода'},
                            'end_date': {'type': 'string', 'format': 'date', 'description': 'Конец периода'}
                        }
                    },
                    'daily_statistics': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'date': {'type': 'string', 'format': 'date', 'description': 'Дата'},
                                'halls': {
                                    'type': 'object',
                                    'description': 'Статистика по каждому залу. Ключи объекта - это hall_id (идентификаторы залов). В Swagger UI отображаются как additionalProp1, additionalProp2 и т.д., но в реальном ответе это числовые ID залов.',
                                    'additionalProperties': {
                                        'type': 'object',
                                        'description': 'Статистика по конкретному залу',
                                        'properties': {
                                            'hall_name': {'type': 'string', 'description': 'Название зала'},
                                            'books_count': {'type': 'integer', 'description': 'Количество книг в зале на эту дату'},
                                            'readers_count': {'type': 'integer', 'description': 'Количество читателей в зале на эту дату'}
                                        }
                                    },
                                    'example': {
                                        '1': {
                                            'hall_name': 'Зал 1',
                                            'books_count': 100,
                                            'readers_count': 50
                                        },
                                        '2': {
                                            'hall_name': 'Зал 2',
                                            'books_count': 150,
                                            'readers_count': 75
                                        }
                                    }
                                },
                                'total': {
                                    'type': 'object',
                                    'properties': {
                                        'books_count': {'type': 'integer', 'description': 'Общее количество книг в библиотеке на эту дату'},
                                        'readers_count': {'type': 'integer', 'description': 'Общее количество читателей в библиотеке на эту дату'}
                                    }
                                }
                            }
                        },
                        'description': 'Статистика на каждый день месяца'
                    },
                    'new_readers': {
                        'type': 'object',
                        'properties': {
                            'by_hall': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'hall_id': {'type': 'integer', 'description': 'ID зала'},
                                        'hall_name': {'type': 'string', 'description': 'Название зала'},
                                        'new_readers_count': {'type': 'integer', 'description': 'Количество новых читателей в зале за месяц'}
                                    }
                                },
                                'description': 'Количество новых читателей по залам'
                            },
                            'total': {'type': 'integer', 'description': 'Общее количество новых читателей в библиотеке за месяц'}
                        }
                    }
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'description': 'Описание ошибки валидации'}
                },
                'description': 'Ошибка валидации параметров (неверный формат года/месяца)'
            },
            401: {
                'type': 'object',
                'description': 'Требуется аутентификация'
            }
        },
        tags=['Staff'],
        auth=AUTH_DOCS,
    )
    @action(detail=False, methods=['get'], url_path='monthly-report', permission_classes=[IsAuthenticated])
    def monthly_report(self, request):
        """Отчёт о работе библиотеки за месяц."""
        try:
            year = int(request.query_params.get('year', timezone.now().year))
            month = int(request.query_params.get('month', timezone.now().month))
        except ValueError:
            return Response(
                {'error': 'Параметры year и month должны быть числами.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not (1 <= month <= 12):
            return Response(
                {'error': 'Месяц должен быть от 1 до 12.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date()
        else:
            end_date = datetime(year, month + 1, 1).date()
        
        # Количество книг и читателей на каждый день в каждом зале
        halls = Hall.objects.all()
        daily_stats = []
        
        current_date = start_date
        while current_date < end_date:
            day_stats = {
                'date': current_date.isoformat(),
                'halls': {}
            }
            
            for hall in halls:
                # Количество книг в зале на текущую дату
                # Учитываем книги, зарегистрированные до или в этот день,
                # и не списанные на эту дату (либо не списанные вообще, либо списанные после этой даты)
                books_count = BookCopy.objects.filter(
                    hall=hall,
                    registration_date__lte=current_date
                ).filter(
                    Q(is_written_off=False) | Q(writeoff_date__gt=current_date)
                ).count()
                
                # Количество читателей в зале на текущую дату
                # Учитываем активных читателей, зарегистрированных до или в этот день
                readers_count = Reader.objects.filter(
                    hall=hall,
                    is_active=True,
                    registration_date__lte=current_date
                ).count()
                
                day_stats['halls'][hall.hall_id] = {
                    'hall_name': hall.name,
                    'books_count': books_count,
                    'readers_count': readers_count
                }
            
            # Общее по библиотеке на текущую дату
            total_books = BookCopy.objects.filter(
                registration_date__lte=current_date
            ).filter(
                Q(is_written_off=False) | Q(writeoff_date__gt=current_date)
            ).count()
            total_readers = Reader.objects.filter(
                is_active=True,
                registration_date__lte=current_date
            ).count()
            
            day_stats['total'] = {
                'books_count': total_books,
                'readers_count': total_readers
            }
            
            daily_stats.append(day_stats)
            current_date += timedelta(days=1)
        
        # Количество читателей, записавшихся в каждый зал за месяц
        new_readers_by_hall = []
        for hall in halls:
            count = Reader.objects.filter(
                hall=hall,
                registration_date__gte=start_date,
                registration_date__lt=end_date
            ).count()
            new_readers_by_hall.append({
                'hall_id': hall.hall_id,
                'hall_name': hall.name,
                'new_readers_count': count
            })
        
        total_new_readers = Reader.objects.filter(
            registration_date__gte=start_date,
            registration_date__lt=end_date
        ).count()
        
        return Response({
            'period': {
                'year': year,
                'month': month,
                'start_date': start_date.isoformat(),
                'end_date': (end_date - timedelta(days=1)).isoformat()
            },
            'daily_statistics': daily_stats,
            'new_readers': {
                'by_hall': new_readers_by_hall,
                'total': total_new_readers
            }
        })

