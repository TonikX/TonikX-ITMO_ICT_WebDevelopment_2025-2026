from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta

from .models import Employee, Author, Book, FinancialStatus, Report
from .serializers import (
    EmployeeSerializer, AuthorSerializer, BookListSerializer, 
    BookDetailSerializer, FinancialStatusSerializer, ReportSerializer
)


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet для сотрудников"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Employee.objects.all()
        position = self.request.query_params.get('position', None)
        department = self.request.query_params.get('department', None)
        
        if position:
            queryset = queryset.filter(position=position)
        if department:
            queryset = queryset.filter(department__icontains=department)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Статистика по сотрудникам"""
        total_employees = Employee.objects.count()
        by_position = Employee.objects.values('position').annotate(
            count=Count('id')
        )
        avg_salary = Employee.objects.aggregate(avg=Avg('salary'))['avg'] or 0
        
        return Response({
            'total_employees': total_employees,
            'by_position': list(by_position),
            'average_salary': float(avg_salary)
        })


class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet для авторов"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Author.objects.all()
        search = self.request.query_params.get('search', None)
        
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(middle_name__icontains=search)
            )
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Книги автора"""
        author = self.get_object()
        books = author.books.all()
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet для книг"""
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookDetailSerializer
    
    def get_queryset(self):
        queryset = Book.objects.all()
        status_filter = self.request.query_params.get('status', None)
        author_id = self.request.query_params.get('author', None)
        search = self.request.query_params.get('search', None)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if author_id:
            queryset = queryset.filter(authors__id=author_id)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(isbn__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.distinct()
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Статистика по книгам"""
        total_books = Book.objects.count()
        by_status = Book.objects.values('status').annotate(
            count=Count('id')
        )
        total_profit = sum(book.profit for book in Book.objects.all())
        avg_price = Book.objects.aggregate(avg=Avg('price'))['avg'] or 0
        
        return Response({
            'total_books': total_books,
            'by_status': list(by_status),
            'total_profit': float(total_profit),
            'average_price': float(avg_price)
        })


class FinancialStatusViewSet(viewsets.ModelViewSet):
    """ViewSet для финансовых записей"""
    queryset = FinancialStatus.objects.all()
    serializer_class = FinancialStatusSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = FinancialStatus.objects.all()
        transaction_type = self.request.query_params.get('type', None)
        category = self.request.query_params.get('category', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        if category:
            queryset = queryset.filter(category=category)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Сводка по финансам"""
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        queryset = FinancialStatus.objects.all()
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        total_income = queryset.filter(transaction_type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        total_expense = queryset.filter(transaction_type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        balance = total_income - total_expense
        
        by_category = queryset.values('category', 'transaction_type').annotate(
            total=Sum('amount')
        )
        
        return Response({
            'total_income': float(total_income),
            'total_expense': float(total_expense),
            'balance': float(balance),
            'by_category': list(by_category)
        })


class ReportViewSet(viewsets.ModelViewSet):
    """ViewSet для отчётов"""
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Report.objects.all()
        report_type = self.request.query_params.get('type', None)
        created_by = self.request.query_params.get('created_by', None)
        
        if report_type:
            queryset = queryset.filter(report_type=report_type)
        if created_by:
            queryset = queryset.filter(created_by_id=created_by)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Создание отчёта с автоматическим заполнением данных"""
        user = request.user
        employee = Employee.objects.filter(user=user).first()
        
        if not employee:
            return Response(
                {'error': 'Пользователь не является сотрудником'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        report_type = serializer.validated_data.get('report_type')
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')
        
        # Генерация данных отчёта в зависимости от типа
        data = {}
        
        if report_type == 'financial':
            financial_records = FinancialStatus.objects.all()
            if start_date:
                financial_records = financial_records.filter(date__gte=start_date)
            if end_date:
                financial_records = financial_records.filter(date__lte=end_date)
            
            data = {
                'total_income': float(financial_records.filter(transaction_type='income').aggregate(
                    total=Sum('amount'))['total'] or 0),
                'total_expense': float(financial_records.filter(transaction_type='expense').aggregate(
                    total=Sum('amount'))['total'] or 0),
                'records_count': financial_records.count()
            }
        
        elif report_type == 'books':
            books = Book.objects.all()
            if start_date:
                books = books.filter(publication_date__gte=start_date)
            if end_date:
                books = books.filter(publication_date__lte=end_date)
            
            data = {
                'total_books': books.count(),
                'by_status': list(books.values('status').annotate(count=Count('id'))),
                'total_profit': float(sum(book.profit for book in books))
            }
        
        elif report_type == 'employees':
            data = {
                'total_employees': Employee.objects.count(),
                'by_position': list(Employee.objects.values('position').annotate(
                    count=Count('id'))),
                'average_salary': float(Employee.objects.aggregate(avg=Avg('salary'))['avg'] or 0)
            }
        
        elif report_type == 'sales':
            books = Book.objects.filter(status='published')
            if start_date:
                books = books.filter(publication_date__gte=start_date)
            if end_date:
                books = books.filter(publication_date__lte=end_date)
            
            data = {
                'total_sold': books.aggregate(total=Sum('print_run'))['total'] or 0,
                'total_revenue': float(sum(book.price * book.print_run for book in books)),
                'books_count': books.count()
            }
        
        serializer.save(created_by=employee, data=data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
