from django.contrib import admin
from .models import (
    Employee, Author, Book, Contract, BookAuthor, BookEditor,
    Customer, Order, OrderItem
)


class BookAuthorInline(admin.TabularInline):
    """Инлайн для авторов книги"""
    model = BookAuthor
    extra = 1
    fields = ('author', 'author_order', 'royalty_percentage')
    autocomplete_fields = ['author']


class BookEditorInline(admin.TabularInline):
    """Инлайн для редакторов книги"""
    model = BookEditor
    extra = 1
    fields = ('editor', 'is_chief_editor', 'assigned_date')
    readonly_fields = ('assigned_date',)
    autocomplete_fields = ['editor']


class OrderItemInline(admin.TabularInline):
    """Инлайн для позиций заказа"""
    model = OrderItem
    extra = 1
    fields = ('book', 'quantity', 'unit_price', 'subtotal')
    readonly_fields = ('subtotal',)
    autocomplete_fields = ['book']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Админка для сотрудников"""
    list_display = ('last_name', 'first_name', 'role', 'position_title', 'email', 'hire_date')
    list_filter = ('role', 'hire_date')
    search_fields = ('last_name', 'first_name', 'middle_name', 'email', 'position_title')
    ordering = ('last_name', 'first_name')
    date_hierarchy = 'hire_date'
    fields = (
        ('last_name', 'first_name', 'middle_name'),
        'email',
        ('role', 'position_title'),
        'hire_date',
        'phone',
        'user',
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Админка для авторов"""
    list_display = ('last_name', 'first_name', 'email', 'birth_date', 'books_count')
    search_fields = ('last_name', 'first_name', 'middle_name', 'email')
    list_filter = ('birth_date',)
    ordering = ('last_name', 'first_name')
    fields = (
        ('last_name', 'first_name', 'middle_name'),
        'email',
        'phone',
        'birth_date',
        'bio',
    )

    def books_count(self, obj):
        """Количество книг автора"""
        return obj.books.count()
    books_count.short_description = 'Книг'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Админка для книг"""
    list_display = ('title', 'isbn', 'display_authors', 'pages', 'has_illustrations', 'publication_date', 'cover_price')
    list_filter = ('has_illustrations', 'genre', 'language', 'publication_date')
    search_fields = ('title', 'isbn', 'description')
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date', 'title')
    readonly_fields = ('display_authors',)
    inlines = [BookAuthorInline, BookEditorInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'isbn', 'genre', 'language')
        }),
        ('Детали', {
            'fields': ('pages', 'has_illustrations', 'publication_date', 'cover_price')
        }),
        ('Описание', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Авторы и редакторы', {
            'fields': ('display_authors',),
            'classes': ('collapse',)
        }),
    )

    def display_authors(self, obj):
        """Отображает список авторов в порядке обложки"""
        if obj.pk:
            return obj.get_authors_display() or "Нет авторов"
        return "Сохраните книгу, чтобы добавить авторов"
    display_authors.short_description = 'Авторы'


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """Админка для контрактов"""
    list_display = ('contract_number', 'book', 'manager', 'signed_date', 'status', 'advance_payment', 'total_budget')
    list_filter = ('status', 'signed_date', 'manager')
    search_fields = ('contract_number', 'book__title', 'manager__last_name', 'notes')
    date_hierarchy = 'signed_date'
    ordering = ('-signed_date',)
    autocomplete_fields = ['book', 'manager']
    fieldsets = (
        ('Основная информация', {
            'fields': ('contract_number', 'book', 'manager', 'status')
        }),
        ('Даты', {
            'fields': ('signed_date', 'expiry_date')
        }),
        ('Финансы', {
            'fields': ('advance_payment', 'total_budget')
        }),
        ('Примечания', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )


@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    """Админка для связи книга-автор"""
    list_display = ('book', 'author', 'author_order', 'royalty_percentage')
    list_filter = ('book', 'author')
    search_fields = ('book__title', 'author__last_name', 'author__first_name')
    ordering = ('book', 'author_order')
    autocomplete_fields = ['book', 'author']


@admin.register(BookEditor)
class BookEditorAdmin(admin.ModelAdmin):
    """Админка для связи книга-редактор"""
    list_display = ('book', 'editor', 'is_chief_editor', 'assigned_date')
    list_filter = ('is_chief_editor', 'assigned_date', 'editor')
    search_fields = ('book__title', 'editor__last_name', 'editor__first_name')
    ordering = ('book', '-is_chief_editor', 'editor')
    readonly_fields = ('assigned_date',)
    autocomplete_fields = ['book', 'editor']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Админка для заказчиков"""
    list_display = ('name', 'company_name', 'email', 'phone', 'orders_count')
    search_fields = ('name', 'company_name', 'email', 'phone')
    list_filter = ('company_name',)
    ordering = ('name',)
    fields = (
        'name',
        'company_name',
        ('email', 'phone'),
        'address',
    )

    def orders_count(self, obj):
        """Количество заказов заказчика"""
        return obj.orders.count()
    orders_count.short_description = 'Заказов'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Админка для заказов"""
    list_display = ('order_number', 'customer', 'order_date', 'status', 'total_amount', 'items_count')
    list_filter = ('status', 'order_date')
    search_fields = ('order_number', 'customer__name', 'customer__company_name')
    date_hierarchy = 'order_date'
    ordering = ('-order_date',)
    readonly_fields = ('order_date', 'calculated_total')
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('order_number', 'customer', 'status')
        }),
        ('Даты', {
            'fields': ('order_date',)
        }),
        ('Финансы', {
            'fields': ('total_amount', 'calculated_total')
        }),
    )

    def items_count(self, obj):
        """Количество позиций в заказе"""
        return obj.items.count()
    items_count.short_description = 'Позиций'

    def calculated_total(self, obj):
        """Расчетная сумма заказа"""
        if obj.pk:
            return obj.calculate_total()
        return "Сохраните заказ, чтобы добавить позиции"
    calculated_total.short_description = 'Расчетная сумма'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Админка для позиций заказа"""
    list_display = ('order', 'book', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('order', 'book')
    search_fields = ('order__order_number', 'book__title')
    ordering = ('order', 'book')
    readonly_fields = ('subtotal',)
    autocomplete_fields = ['order', 'book']
