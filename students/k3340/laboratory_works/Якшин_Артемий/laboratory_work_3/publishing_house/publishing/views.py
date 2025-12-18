from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Q, Prefetch, F
from django.db.models.functions import TruncMonth
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from datetime import datetime, timedelta
from calendar import month_name

from .models import (
    Employee, Author, Book, Contract, BookAuthor, BookEditor,
    Customer, Order, OrderItem
)
from .serializers import (
    EmployeeSerializer, AuthorSerializer, BookSerializer, BookDetailSerializer,
    ContractSerializer, CustomerSerializer, OrderSerializer, OrderDetailSerializer,
    BookAuthorSerializer, BookEditorSerializer, OrderItemSerializer,
    BooksByAuthorSerializer, ChiefEditorsReportSerializer, EditorsPerBookSerializer,
    ContractsByMonthSerializer, TopManagersSerializer,
    QuarterlyContractDetailSerializer, QuarterlyContractSummarySerializer
)


# ===== CRUD ViewSets =====

class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с сотрудниками"""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'hire_date']
    search_fields = ['first_name', 'last_name', 'middle_name', 'email', 'position_title']
    ordering_fields = ['last_name', 'hire_date', 'role']
    ordering = ['last_name', 'first_name']


class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с авторами"""

    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'middle_name', 'email']
    ordering_fields = ['last_name', 'birth_date']
    ordering = ['last_name', 'first_name']


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с книгами"""

    queryset = Book.objects.prefetch_related(
        Prefetch('book_authors', queryset=BookAuthor.objects.select_related('author').order_by('author_order')),
        Prefetch('book_editors', queryset=BookEditor.objects.select_related('editor'))
    ).select_related('contract').all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['has_illustrations', 'genre', 'language', 'publication_date']
    search_fields = ['title', 'isbn', 'description']
    ordering_fields = ['title', 'publication_date', 'pages', 'cover_price']
    ordering = ['-publication_date', 'title']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer


class ContractViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с контрактами"""

    queryset = Contract.objects.select_related('book', 'manager').all()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'signed_date', 'manager']
    search_fields = ['contract_number', 'book__title', 'manager__last_name', 'notes']
    ordering_fields = ['signed_date', 'contract_number', 'total_budget']
    ordering = ['-signed_date']


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с заказчиками"""

    queryset = Customer.objects.prefetch_related('orders').all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'company_name', 'email', 'phone']
    ordering_fields = ['name', 'company_name']
    ordering = ['name']


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с заказами"""

    queryset = Order.objects.select_related('customer').prefetch_related(
        Prefetch('items', queryset=OrderItem.objects.select_related('book'))
    ).all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'order_date', 'customer']
    search_fields = ['order_number', 'customer__name', 'customer__company_name']
    ordering_fields = ['order_date', 'total_amount']
    ordering = ['-order_date']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer


class BookAuthorViewSet(viewsets.ModelViewSet):
    """ViewSet для работы со связью книга-автор"""

    queryset = BookAuthor.objects.select_related('book', 'author').all()
    serializer_class = BookAuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['book', 'author']
    ordering_fields = ['author_order', 'royalty_percentage']
    ordering = ['book', 'author_order']


class BookEditorViewSet(viewsets.ModelViewSet):
    """ViewSet для работы со связью книга-редактор"""

    queryset = BookEditor.objects.select_related('book', 'editor').all()
    serializer_class = BookEditorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['book', 'editor', 'is_chief_editor']
    ordering_fields = ['assigned_date']
    ordering = ['book', '-is_chief_editor', 'editor']


class OrderItemViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с позициями заказа"""

    queryset = OrderItem.objects.select_related('order', 'book').all()
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'book']
    ordering = ['order', 'book']


# ===== Report Views =====

class BooksByAuthorReportView(APIView):
    """
    Отчет 1: Список всех изданных книг заданного автора
    GET /api/v1/reports/books-by-author/?author_id=X
    """

    def get(self, request):
        author_id = request.query_params.get('author_id')

        if not author_id:
            return Response(
                {'error': 'Параметр author_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response(
                {'error': f'Автор с ID {author_id} не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        books = Book.objects.filter(
            book_authors__author_id=author_id
        ).select_related('contract').distinct()

        serializer = BooksByAuthorSerializer(books, many=True)

        return Response({
            'author': {
                'id': author.id,
                'name': author.get_full_name(),
                'email': author.email
            },
            'books_count': books.count(),
            'books': serializer.data
        })


class ChiefEditorsReportView(APIView):
    """
    Отчет 2: Список ответственных редакторов для всех изданий
    GET /api/v1/reports/chief-editors/
    """

    def get(self, request):
        chief_editors = BookEditor.objects.filter(
            is_chief_editor=True
        ).select_related('book', 'editor').order_by('book__title')

        serializer = ChiefEditorsReportSerializer(chief_editors, many=True)

        return Response({
            'total_books': chief_editors.count(),
            'chief_editors': serializer.data
        })


class EditorsPerBookReportView(APIView):
    """
    Отчет 3: Количество редакторов каждой книги
    GET /api/v1/reports/editors-per-book/
    """

    def get(self, request):
        books_with_editors = Book.objects.annotate(
            editors_count=Count('book_editors')
        ).prefetch_related(
            Prefetch('book_editors', queryset=BookEditor.objects.filter(is_chief_editor=True).select_related('editor'))
        ).order_by('title')

        result = []
        for book in books_with_editors:
            chief_editor_obj = book.book_editors.filter(is_chief_editor=True).first()
            chief_editor_name = chief_editor_obj.editor.get_full_name() if chief_editor_obj else None

            result.append({
                'book_id': book.id,
                'book_title': book.title,
                'editors_count': book.editors_count,
                'chief_editor': chief_editor_name
            })

        serializer = EditorsPerBookSerializer(result, many=True)

        return Response({
            'total_books': len(result),
            'books': serializer.data
        })


class ContractsByMonthReportView(APIView):
    """
    Отчет 4: Количество контрактов за каждый месяц за истекший год
    GET /api/v1/reports/contracts-by-month/?year=2024
    """

    def get(self, request):
        year = request.query_params.get('year')

        if not year:
            # По умолчанию - текущий год
            year = datetime.now().year
        else:
            try:
                year = int(year)
            except ValueError:
                return Response(
                    {'error': 'Параметр year должен быть числом'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Получаем контракты за год и группируем по месяцам
        contracts_by_month = Contract.objects.filter(
            signed_date__year=year
        ).annotate(
            month=TruncMonth('signed_date')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')

        serializer = ContractsByMonthSerializer(contracts_by_month, many=True)

        total_contracts = sum(item['count'] for item in contracts_by_month)

        return Response({
            'year': year,
            'total_contracts': total_contracts,
            'by_month': serializer.data
        })


class TopManagersReportView(APIView):
    """
    Отчет 5: Список всех менеджеров с максимальным количеством контрактов за период
    GET /api/v1/reports/top-managers/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
    """

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response(
                {'error': 'Параметры start_date и end_date обязательны'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Формат даты должен быть YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Получаем менеджеров с количеством контрактов за период
        managers_with_contracts = Employee.objects.filter(
            role='MANAGER',
            managed_contracts__signed_date__range=[start_date, end_date]
        ).annotate(
            contracts_count=Count('managed_contracts')
        ).order_by('-contracts_count')

        if not managers_with_contracts.exists():
            return Response({
                'start_date': start_date,
                'end_date': end_date,
                'message': 'За указанный период контрактов не найдено',
                'top_managers': []
            })

        # Находим максимальное количество контрактов
        max_contracts = managers_with_contracts.first().contracts_count

        # Фильтруем только менеджеров с максимальным количеством
        top_managers = managers_with_contracts.filter(contracts_count=max_contracts)

        result = []
        for manager in top_managers:
            result.append({
                'manager_id': manager.id,
                'manager_name': manager.get_full_name(),
                'manager_email': manager.email,
                'contracts_count': manager.contracts_count
            })

        serializer = TopManagersSerializer(result, many=True)

        return Response({
            'start_date': start_date,
            'end_date': end_date,
            'max_contracts_count': max_contracts,
            'top_managers': serializer.data
        })


class QuarterlyContractsReportView(APIView):
    """
    Отчет 6: Отчет о всех контрактах за каждый месяц истекшего квартала
    GET /api/v1/reports/quarterly-contracts/?quarter=1&year=2024

    Включает: название книги, кол-во авторов/редакторов, страницы, иллюстрации
    Итоги: кол-во изданий за месяц и общее за квартал
    """

    def get(self, request):
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')

        if not quarter:
            return Response(
                {'error': 'Параметр quarter обязателен (1, 2, 3 или 4)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quarter = int(quarter)
            if quarter not in [1, 2, 3, 4]:
                raise ValueError
        except ValueError:
            return Response(
                {'error': 'Параметр quarter должен быть числом от 1 до 4'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not year:
            year = datetime.now().year
        else:
            try:
                year = int(year)
            except ValueError:
                return Response(
                    {'error': 'Параметр year должен быть числом'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Определяем диапазон месяцев для квартала
        start_month = (quarter - 1) * 3 + 1
        end_month = start_month + 2

        # Получаем контракты за квартал с аннотациями
        contracts = Contract.objects.filter(
            signed_date__year=year,
            signed_date__month__gte=start_month,
            signed_date__month__lte=end_month
        ).select_related('book').annotate(
            authors_count=Count('book__book_authors', distinct=True),
            editors_count=Count('book__book_editors', distinct=True),
            month=TruncMonth('signed_date')
        ).order_by('signed_date')

        # Группируем контракты по месяцам
        contracts_by_month = {}
        for contract in contracts:
            month_key = contract.month.strftime('%Y-%m')
            month_name_ru = self._get_russian_month_name(contract.month.month)

            if month_key not in contracts_by_month:
                contracts_by_month[month_key] = {
                    'month': month_name_ru,
                    'contracts': []
                }

            contracts_by_month[month_key]['contracts'].append({
                'contract_id': contract.id,
                'contract_number': contract.contract_number,
                'book_title': contract.book.title,
                'authors_count': contract.authors_count,
                'editors_count': contract.editors_count,
                'pages': contract.book.pages,
                'has_illustrations': contract.book.has_illustrations,
                'signed_date': contract.signed_date,
                'month': month_name_ru
            })

        # Формируем итоговую статистику
        monthly_summary = []
        total_contracts = 0

        for month_key in sorted(contracts_by_month.keys()):
            month_data = contracts_by_month[month_key]
            contracts_count = len(month_data['contracts'])
            total_contracts += contracts_count

            monthly_summary.append({
                'month': month_data['month'],
                'contracts_count': contracts_count
            })

        # Формируем детальные данные
        all_contracts = []
        for month_key in sorted(contracts_by_month.keys()):
            all_contracts.extend(contracts_by_month[month_key]['contracts'])

        contracts_serializer = QuarterlyContractDetailSerializer(all_contracts, many=True)
        summary_serializer = QuarterlyContractSummarySerializer(monthly_summary, many=True)

        return Response({
            'quarter': quarter,
            'year': year,
            'period': f'{start_month}-{end_month} месяцы {year} года',
            'total_contracts': total_contracts,
            'monthly_summary': summary_serializer.data,
            'contracts': contracts_serializer.data
        })

    def _get_russian_month_name(self, month_number):
        """Возвращает русское название месяца"""
        months_ru = {
            1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
            5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
            9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
        }
        return months_ru.get(month_number, '')
