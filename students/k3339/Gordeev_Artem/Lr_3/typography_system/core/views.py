from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import BookFilter
from .models import Author, Book, Contract, Customer, Order, BookAuthor, BookEditor, OrderItem
from .serializers import (
    AuthorSerializer, BookSerializer, ContractSerializer,
    CustomerSerializer, OrderSerializer, BookAuthorSerializer,
    BookEditorSerializer, OrderItemSerializer, UserSerializer
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_queryset(self):
        return super().get_queryset().annotate(
            editors_count=Count('editors')
        ).prefetch_related('bookauthor_set__author', 'bookeditor_set')

    @action(detail=False, methods=['get'])
    def with_stats(self, request):
        """
        список книг с дополнительной статистикой
        """
        books = self.get_queryset()
        data = []
        for book in books:
            serializer = self.get_serializer(book)
            book_data = serializer.data
            book_data['editors_count'] = book.editors_count
            data.append(book_data)
        return Response(data)


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def yearly_stats(self, request):
        """
        количество контрактов за каждый месяц за истекший год
        """
        one_year_ago = timezone.now() - timedelta(days=365)
        stats = Contract.objects.filter(date_signed__gte=one_year_ago) \
            .annotate(month=TruncMonth('date_signed')) \
            .values('month') \
            .annotate(count=Count('id')) \
            .order_by('month')

        return Response(stats)

    @action(detail=False, methods=['get'])
    def top_managers(self, request):
        """
        менеджеры с максимальным количеством контрактов за период
        """
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')

        if not start_date or not end_date:
            return Response({"error": "Укажите start и end параметры даты"}, status=400)

        stats = Contract.objects.filter(date_signed__range=[start_date, end_date]) \
            .values('manager') \
            .annotate(total_contracts=Count('id')) \
            .order_by('-total_contracts')

        if not stats:
            return Response([])

        max_contracts = stats[0]['total_contracts']
        top_managers_ids = [s['manager'] for s in stats if s['total_contracts'] == max_contracts]

        from django.contrib.auth import get_user_model
        User = get_user_model()
        users = User.objects.filter(id__in=top_managers_ids)
        serializer = UserSerializer(users, many=True)

        return Response({
            "max_contracts": max_contracts,
            "managers": serializer.data
        })

    @action(detail=False, methods=['get'])
    def quarterly_report(self, request):
        """
        отчет за истекший квартал
        """
        today = timezone.now().date()
        three_months_ago = today - timedelta(days=90)

        contracts = Contract.objects.filter(date_signed__range=[three_months_ago, today]) \
            .select_related('book') \
            .prefetch_related('book__authors', 'book__editors')

        report_data = []
        monthly_counts = {}
        total_publications = 0

        for contract in contracts:
            book = contract.book

            authors_count = book.authors.count()
            editors_count = book.editors.count()

            month_key = contract.date_signed.strftime('%Y-%m')
            monthly_counts[month_key] = monthly_counts.get(month_key, 0) + 1
            total_publications += 1

            report_data.append({
                "contract_number": contract.number,
                "date": contract.date_signed,
                "book_title": book.title,
                "authors_count": authors_count,
                "editors_count": editors_count,
                "pages": book.pages_count,
                "has_illustrations": book.has_illustrations
            })

        return Response({
            "period": f"{three_months_ago} - {today}",
            "total_publications_quarter": total_publications,
            "publications_by_month": monthly_counts,
            "details": report_data
        })


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


# Вспомогательные
class BookAuthorViewSet(viewsets.ModelViewSet):
    queryset = BookAuthor.objects.all()
    serializer_class = BookAuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookEditorViewSet(viewsets.ModelViewSet):
    queryset = BookEditor.objects.all()
    serializer_class = BookEditorSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_responsible', 'book']


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
