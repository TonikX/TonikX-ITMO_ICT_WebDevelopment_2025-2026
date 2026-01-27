from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Employee, Author, Book, FinancialStatus, Report


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор сотрудника"""
    user = UserSerializer(read_only=True)
    position_display = serializers.CharField(source='get_position_display', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'user', 'position', 'position_display', 'phone', 'hire_date', 
                 'salary', 'department']
        read_only_fields = ['id']


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор автора"""
    full_name = serializers.CharField(read_only=True)
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'full_name', 
                 'birth_date', 'email', 'phone', 'biography', 'created_at', 'books_count']
        read_only_fields = ['id', 'created_at']
    
    def get_books_count(self, obj):
        """Количество книг автора"""
        return obj.books.count()


class BookListSerializer(serializers.ModelSerializer):
    """Сериализатор списка книг"""
    authors = AuthorSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    editor_name = serializers.SerializerMethodField()
    profit = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'authors', 'status', 'status_display', 
                 'editor_name', 'pages', 'publication_date', 'print_run', 
                 'price', 'cost', 'profit', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_editor_name(self, obj):
        """Имя редактора"""
        if obj.editor:
            return str(obj.editor.user.get_full_name())
        return None


class BookDetailSerializer(serializers.ModelSerializer):
    """Сериализатор детальной информации о книге"""
    authors = AuthorSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        many=True,
        write_only=True,
        source='authors'
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    editor = EmployeeSerializer(read_only=True)
    editor_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.filter(position='editor'),
        write_only=True,
        source='editor',
        allow_null=True,
        required=False
    )
    profit = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'authors', 'author_ids', 'editor', 'editor_id',
                 'pages', 'publication_date', 'print_date', 'print_run', 'price', 
                 'cost', 'profit', 'status', 'status_display', 'description', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class FinancialStatusSerializer(serializers.ModelSerializer):
    """Сериализатор финансовой записи"""
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = FinancialStatus
        fields = ['id', 'date', 'transaction_type', 'transaction_type_display',
                 'category', 'category_display', 'amount', 'description', 
                 'book', 'book_title', 'created_at']
        read_only_fields = ['id', 'created_at']


class ReportSerializer(serializers.ModelSerializer):
    """Сериализатор отчёта"""
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Report
        fields = ['id', 'title', 'report_type', 'report_type_display', 'created_by',
                 'created_by_name', 'start_date', 'end_date', 'data', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_created_by_name(self, obj):
        """Имя создателя отчёта"""
        if obj.created_by:
            return str(obj.created_by.user.get_full_name())
        return None
