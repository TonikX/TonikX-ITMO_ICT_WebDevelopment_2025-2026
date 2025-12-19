from rest_framework import serializers
from django.db.models import Count, Sum
from .models import (
    Employee, Author, Book, Contract, BookAuthor, BookEditor,
    Customer, Order, OrderItem
)


# ===== Basic Serializers =====

class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для сотрудников"""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'last_name', 'middle_name', 'full_name',
            'email', 'role', 'position_title', 'hire_date', 'phone'
        ]

    def get_full_name(self, obj):
        return obj.get_full_name()


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для авторов"""

    full_name = serializers.SerializerMethodField()
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            'id', 'first_name', 'last_name', 'middle_name', 'full_name',
            'email', 'bio', 'birth_date', 'phone', 'books_count'
        ]

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_books_count(self, obj):
        return obj.books.count()


class BookAuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для связи книга-автор"""

    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = BookAuthor
        fields = ['id', 'book', 'book_title', 'author', 'author_name', 'author_order', 'royalty_percentage']

    def validate(self, data):
        """Проверка что процент гонорара не превышает 100% для книги"""
        book = data.get('book')
        royalty_percentage = data.get('royalty_percentage', 0)

        if book:
            # Получаем сумму гонораров для всех других авторов этой книги
            existing_royalties = BookAuthor.objects.filter(book=book).exclude(
                pk=self.instance.pk if self.instance else None
            ).aggregate(total=Sum('royalty_percentage'))['total'] or 0

            total_royalties = existing_royalties + royalty_percentage

            if total_royalties > 100:
                raise serializers.ValidationError({
                    'royalty_percentage': f'Сумма процентов гонорара для всех авторов книги не может превышать 100%. '
                                          f'Текущая сумма: {existing_royalties}%, добавляете: {royalty_percentage}%, '
                                          f'итого: {total_royalties}%'
                })

        return data


class BookEditorSerializer(serializers.ModelSerializer):
    """Сериализатор для связи книга-редактор"""

    editor_name = serializers.CharField(source='editor.get_full_name', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = BookEditor
        fields = ['id', 'book', 'book_title', 'editor', 'editor_name', 'is_chief_editor', 'assigned_date']
        read_only_fields = ['assigned_date']

    def validate_editor(self, value):
        """CRITICAL: Проверка что editor имеет роль EDITOR"""
        if value.role != 'EDITOR':
            raise serializers.ValidationError(
                f'Редактором книги может быть только сотрудник с ролью "Редактор". '
                f'У сотрудника {value.get_full_name()} роль "{value.get_role_display()}"'
            )
        return value

    def validate(self, data):
        """CRITICAL: Проверка что у книги только один ответственный редактор"""
        book = data.get('book')
        is_chief_editor = data.get('is_chief_editor', False)

        if book and is_chief_editor:
            existing_chief = BookEditor.objects.filter(
                book=book,
                is_chief_editor=True
            ).exclude(pk=self.instance.pk if self.instance else None)

            if existing_chief.exists():
                raise serializers.ValidationError({
                    'is_chief_editor': f'У книги "{book.title}" уже есть ответственный редактор: '
                                       f'{existing_chief.first().editor.get_full_name()}'
                })

        return data


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор для книг"""

    authors_display = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'pages', 'has_illustrations',
            'publication_date', 'cover_price', 'description', 'genre',
            'language', 'authors_display'
        ]

    def get_authors_display(self, obj):
        return obj.get_authors_display()


class BookDetailSerializer(serializers.ModelSerializer):
    """Подробный сериализатор для книг с авторами и редакторами"""

    authors = BookAuthorSerializer(source='book_authors', many=True, read_only=True)
    editors = BookEditorSerializer(source='book_editors', many=True, read_only=True)
    contract = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'pages', 'has_illustrations',
            'publication_date', 'cover_price', 'description', 'genre',
            'language', 'authors', 'editors', 'contract'
        ]

    def get_contract(self, obj):
        if hasattr(obj, 'contract'):
            return {
                'id': obj.contract.id,
                'contract_number': obj.contract.contract_number,
                'status': obj.contract.status,
                'signed_date': obj.contract.signed_date
            }
        return None


class ContractSerializer(serializers.ModelSerializer):
    """Сериализатор для контрактов"""

    book_title = serializers.CharField(source='book.title', read_only=True)
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)

    class Meta:
        model = Contract
        fields = [
            'id', 'contract_number', 'book', 'book_title', 'manager', 'manager_name',
            'signed_date', 'status', 'advance_payment', 'total_budget', 'expiry_date', 'notes'
        ]

    def validate_manager(self, value):
        """CRITICAL: Проверка что manager имеет роль MANAGER"""
        if value.role != 'MANAGER':
            raise serializers.ValidationError(
                f'Контракт может быть подписан только менеджером. '
                f'У сотрудника {value.get_full_name()} роль "{value.get_role_display()}"'
            )
        return value

    def validate(self, data):
        """CRITICAL: Проверка что аванс не превышает общий бюджет"""
        advance_payment = data.get('advance_payment')
        total_budget = data.get('total_budget')

        # Для обновления получаем существующие значения
        if self.instance:
            if advance_payment is None:
                advance_payment = self.instance.advance_payment
            if total_budget is None:
                total_budget = self.instance.total_budget

        if advance_payment and total_budget and advance_payment > total_budget:
            raise serializers.ValidationError({
                'advance_payment': f'Аванс ({advance_payment}) не может превышать общий бюджет ({total_budget})'
            })

        return data


class CustomerSerializer(serializers.ModelSerializer):
    """Сериализатор для заказчиков"""

    orders_count = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'address', 'company_name', 'orders_count']

    def get_orders_count(self, obj):
        return obj.orders.count()


class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор для позиций заказа"""

    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'book', 'book_title', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['subtotal']


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для заказов"""

    customer_name = serializers.CharField(source='customer.name', read_only=True)
    items_count = serializers.SerializerMethodField()
    calculated_total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'customer_name', 'order_date',
            'total_amount', 'status', 'items_count', 'calculated_total'
        ]
        read_only_fields = ['order_date']

    def get_items_count(self, obj):
        return obj.items.count()

    def get_calculated_total(self, obj):
        if obj.pk:
            return obj.calculate_total()
        return 0


class OrderDetailSerializer(serializers.ModelSerializer):
    """Подробный сериализатор для заказов с позициями"""

    customer_details = CustomerSerializer(source='customer', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    calculated_total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'customer_details', 'order_date',
            'total_amount', 'status', 'items', 'calculated_total'
        ]
        read_only_fields = ['order_date']

    def get_calculated_total(self, obj):
        if obj.pk:
            return obj.calculate_total()
        return 0


# ===== Report Serializers =====

class BooksByAuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для отчета: книги по автору"""

    contract_number = serializers.CharField(source='contract.contract_number', read_only=True)
    publication_year = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'pages', 'publication_date', 'publication_year', 'contract_number']

    def get_publication_year(self, obj):
        if obj.publication_date:
            return obj.publication_date.year
        return None


class ChiefEditorsReportSerializer(serializers.ModelSerializer):
    """Сериализатор для отчета: ответственные редакторы"""

    book_id = serializers.IntegerField(source='book.id')
    book_title = serializers.CharField(source='book.title')
    book_isbn = serializers.CharField(source='book.isbn')
    editor_id = serializers.IntegerField(source='editor.id')
    editor_name = serializers.CharField(source='editor.get_full_name')
    editor_email = serializers.CharField(source='editor.email')

    class Meta:
        model = BookEditor
        fields = ['id', 'book_id', 'book_title', 'book_isbn', 'editor_id', 'editor_name', 'editor_email', 'assigned_date']


class EditorsPerBookSerializer(serializers.Serializer):
    """Сериализатор для отчета: количество редакторов каждой книги"""

    book_id = serializers.IntegerField()
    book_title = serializers.CharField()
    editors_count = serializers.IntegerField()
    chief_editor = serializers.CharField(allow_null=True)


class ContractsByMonthSerializer(serializers.Serializer):
    """Сериализатор для отчета: контракты по месяцам"""

    month = serializers.DateField()
    count = serializers.IntegerField()


class TopManagersSerializer(serializers.Serializer):
    """Сериализатор для отчета: топ менеджеры"""

    manager_id = serializers.IntegerField()
    manager_name = serializers.CharField()
    manager_email = serializers.CharField()
    contracts_count = serializers.IntegerField()


class QuarterlyContractDetailSerializer(serializers.Serializer):
    """Сериализатор для детального квартального отчета"""

    contract_id = serializers.IntegerField()
    contract_number = serializers.CharField()
    book_title = serializers.CharField()
    authors_count = serializers.IntegerField()
    editors_count = serializers.IntegerField()
    pages = serializers.IntegerField()
    has_illustrations = serializers.BooleanField()
    signed_date = serializers.DateField()
    month = serializers.CharField()


class QuarterlyContractSummarySerializer(serializers.Serializer):
    """Сериализатор для итогов квартального отчета"""

    month = serializers.CharField()
    contracts_count = serializers.IntegerField()
