from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Employee(models.Model):
    """Модель сотрудника типографии"""

    ROLE_CHOICES = [
        ('MANAGER', 'Менеджер'),
        ('EDITOR', 'Редактор'),
        ('OTHER', 'Другое'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь',
        help_text='Связь с учетной записью пользователя для аутентификации'
    )
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    middle_name = models.CharField('Отчество', max_length=100, blank=True)
    email = models.EmailField('Email', unique=True)
    role = models.CharField('Роль', max_length=10, choices=ROLE_CHOICES, default='OTHER')
    position_title = models.CharField('Должность', max_length=200)
    hire_date = models.DateField('Дата приема на работу')
    phone = models.CharField('Телефон', max_length=20, blank=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.get_role_display()})"

    def get_full_name(self):
        """Возвращает полное имя сотрудника"""
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"


class Author(models.Model):
    """Модель автора книги"""

    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    middle_name = models.CharField('Отчество', max_length=100, blank=True)
    email = models.EmailField('Email', blank=True)
    bio = models.TextField('Биография', blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_full_name(self):
        """Возвращает полное имя автора"""
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"


class Book(models.Model):
    """Модель книги"""

    title = models.CharField('Название', max_length=500)
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    pages = models.IntegerField('Количество страниц', validators=[MinValueValidator(1)])
    has_illustrations = models.BooleanField('Наличие иллюстраций', default=False)
    publication_date = models.DateField('Дата публикации', null=True, blank=True)
    cover_price = models.DecimalField(
        'Цена на обложке',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    description = models.TextField('Описание', blank=True)
    genre = models.CharField('Жанр', max_length=100, blank=True)
    language = models.CharField('Язык', max_length=10, default='RU')

    # Many-to-Many relationships through intermediate tables
    authors = models.ManyToManyField(Author, through='BookAuthor', related_name='books')
    editors = models.ManyToManyField(Employee, through='BookEditor', related_name='edited_books_m2m')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-publication_date', 'title']
        indexes = [
            models.Index(fields=['publication_date']),
            models.Index(fields=['isbn']),
        ]

    def __str__(self):
        return self.title

    def get_authors_display(self):
        """Возвращает строку с именами всех авторов в правильном порядке"""
        book_authors = self.book_authors.select_related('author').order_by('author_order')
        return ', '.join([ba.author.get_full_name() for ba in book_authors])


class Contract(models.Model):
    """Модель контракта на издание книги"""

    STATUS_CHOICES = [
        ('DRAFT', 'Черновик'),
        ('ACTIVE', 'Активный'),
        ('COMPLETED', 'Завершен'),
        ('TERMINATED', 'Расторгнут'),
    ]

    contract_number = models.CharField('Номер контракта', max_length=100, unique=True)
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        verbose_name='Книга',
        related_name='contract'
    )
    manager = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        verbose_name='Менеджер',
        related_name='managed_contracts',
        limit_choices_to={'role': 'MANAGER'}
    )
    signed_date = models.DateField('Дата подписания')
    status = models.CharField('Статус', max_length=15, choices=STATUS_CHOICES, default='DRAFT')
    advance_payment = models.DecimalField(
        'Аванс',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    total_budget = models.DecimalField(
        'Общий бюджет',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    expiry_date = models.DateField('Дата окончания', null=True, blank=True)
    notes = models.TextField('Примечания', blank=True)

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'
        ordering = ['-signed_date']
        indexes = [
            models.Index(fields=['signed_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Контракт {self.contract_number} - {self.book.title}"

    def clean(self):
        """Валидация модели"""
        super().clean()

        # Проверка что manager имеет роль MANAGER
        if self.manager and self.manager.role != 'MANAGER':
            raise ValidationError({
                'manager': 'Контракт может быть подписан только менеджером'
            })

        # Проверка что аванс не превышает общий бюджет
        if self.advance_payment and self.total_budget and self.advance_payment > self.total_budget:
            raise ValidationError({
                'advance_payment': 'Аванс не может превышать общий бюджет'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class BookAuthor(models.Model):
    """Промежуточная модель для связи книги и автора с порядком и процентом гонорара"""

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name='Книга',
        related_name='book_authors'
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='book_authors'
    )
    author_order = models.IntegerField(
        'Порядок на обложке',
        validators=[MinValueValidator(1)],
        help_text='Порядок автора на обложке книги (1, 2, 3...)'
    )
    royalty_percentage = models.DecimalField(
        'Процент гонорара',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Процент от гонорара (0-100%)'
    )

    class Meta:
        verbose_name = 'Автор книги'
        verbose_name_plural = 'Авторы книг'
        unique_together = [
            ('book', 'author'),  # Автор не может быть добавлен дважды к одной книге
            ('book', 'author_order'),  # Порядок авторов должен быть уникальным для каждой книги
        ]
        ordering = ['book', 'author_order']

    def __str__(self):
        return f"{self.book.title} - {self.author.get_full_name()} (#{self.author_order}, {self.royalty_percentage}%)"


class BookEditor(models.Model):
    """Промежуточная модель для связи книги и редактора"""

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name='Книга',
        related_name='book_editors'
    )
    editor = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='Редактор',
        related_name='edited_books',
        limit_choices_to={'role': 'EDITOR'}
    )
    is_chief_editor = models.BooleanField('Ответственный редактор', default=False)
    assigned_date = models.DateField('Дата назначения', auto_now_add=True)

    class Meta:
        verbose_name = 'Редактор книги'
        verbose_name_plural = 'Редакторы книг'
        unique_together = ('book', 'editor')
        ordering = ['book', '-is_chief_editor', 'editor']

    def __str__(self):
        chief = " (Ответственный)" if self.is_chief_editor else ""
        return f"{self.book.title} - {self.editor.get_full_name()}{chief}"

    def clean(self):
        """Валидация модели"""
        super().clean()

        # Проверка что editor имеет роль EDITOR
        if self.editor and self.editor.role != 'EDITOR':
            raise ValidationError({
                'editor': 'Редактором книги может быть только сотрудник с ролью "Редактор"'
            })

        # Проверка что у книги только один ответственный редактор
        if self.is_chief_editor:
            existing_chief = BookEditor.objects.filter(
                book=self.book,
                is_chief_editor=True
            ).exclude(pk=self.pk)

            if existing_chief.exists():
                raise ValidationError({
                    'is_chief_editor': f'У книги "{self.book.title}" уже есть ответственный редактор: {existing_chief.first().editor.get_full_name()}'
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Customer(models.Model):
    """Модель заказчика"""

    name = models.CharField('Имя', max_length=200)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    address = models.TextField('Адрес', blank=True)
    company_name = models.CharField('Название компании', max_length=300, blank=True)

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'
        ordering = ['name']

    def __str__(self):
        if self.company_name:
            return f"{self.name} ({self.company_name})"
        return self.name


class Order(models.Model):
    """Модель заказа на покупку"""

    STATUS_CHOICES = [
        ('PENDING', 'Ожидает обработки'),
        ('PROCESSING', 'В обработке'),
        ('COMPLETED', 'Завершен'),
        ('CANCELLED', 'Отменен'),
    ]

    order_number = models.CharField('Номер заказа', max_length=100, unique=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        verbose_name='Заказчик',
        related_name='orders'
    )
    order_date = models.DateTimeField('Дата заказа', auto_now_add=True)
    total_amount = models.DecimalField(
        'Общая сумма',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    status = models.CharField('Статус', max_length=15, choices=STATUS_CHOICES, default='PENDING')

    # Many-to-Many relationship with Book through OrderItem
    books = models.ManyToManyField(Book, through='OrderItem', related_name='orders')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-order_date']

    def __str__(self):
        return f"Заказ {self.order_number} от {self.customer.name}"

    def calculate_total(self):
        """Вычисляет общую сумму заказа на основе позиций"""
        total = sum(item.subtotal for item in self.items.all())
        return total


class OrderItem(models.Model):
    """Промежуточная модель для позиций заказа"""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='items'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        verbose_name='Книга',
        related_name='order_items'
    )
    quantity = models.IntegerField(
        'Количество',
        validators=[MinValueValidator(1)]
    )
    unit_price = models.DecimalField(
        'Цена за единицу',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    subtotal = models.DecimalField(
        'Подытог',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'
        ordering = ['order', 'book']

    def __str__(self):
        return f"{self.book.title} x {self.quantity} = {self.subtotal}"

    def save(self, *args, **kwargs):
        """Автоматический расчет подытога"""
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
