"""
Django models for library management system.
Все модели соответствуют схеме БД из migrations/schema.sql
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class TimestampMixin(models.Model):
    """Миксин для полей created_at и updated_at."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class Author(TimestampMixin):
    """Автор книги."""
    author_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100, verbose_name='Полное имя')

    class Meta:
        db_table = 'author'
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['full_name']

    def __str__(self) -> str:
        return self.full_name


class Publisher(TimestampMixin):
    """Издательство."""
    publisher_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    class Meta:
        db_table = 'publisher'
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class BookSection(TimestampMixin):
    """Раздел/категория книги."""
    section_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, verbose_name='Название раздела')

    class Meta:
        db_table = 'book_section'
        verbose_name = 'Раздел книги'
        verbose_name_plural = 'Разделы книг'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Book(TimestampMixin):
    """Книга."""
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name='Название')
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name='Издательство'
    )
    publish_year = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1000)],
        verbose_name='Год издания'
    )
    section = models.ForeignKey(
        BookSection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name='Раздел'
    )
    cipher = models.CharField(max_length=50, db_index=True, verbose_name='Шифр книги')
    authors = models.ManyToManyField(Author, through='BookAuthor', related_name='books')

    class Meta:
        db_table = 'book'
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['title']
        indexes = [
            models.Index(fields=['cipher'], name='idx_book_cipher'),
        ]

    def __str__(self) -> str:
        return self.title


class BookAuthor(TimestampMixin):
    """Связь между книгой и автором (Many-to-Many)."""
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_authors')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='book_authors')

    class Meta:
        db_table = 'book_author'
        unique_together = [['book', 'author']]
        verbose_name = 'Автор книги'
        verbose_name_plural = 'Авторы книг'

    def __str__(self) -> str:
        return f'{self.book.title} - {self.author.full_name}'


class Hall(TimestampMixin):
    """Читальный зал."""
    hall_id = models.AutoField(primary_key=True)
    hall_number = models.IntegerField(unique=True, verbose_name='Номер зала')
    name = models.CharField(max_length=100, verbose_name='Название')
    capacity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Вместимость'
    )

    class Meta:
        db_table = 'hall'
        verbose_name = 'Читальный зал'
        verbose_name_plural = 'Читальные залы'
        ordering = ['hall_number']

    def __str__(self) -> str:
        return f'{self.hall_number}. {self.name}'


class Reader(TimestampMixin):
    """Читатель библиотеки."""
    EDUCATION_CHOICES = [
        ('начальное', 'Начальное'),
        ('среднее', 'Среднее'),
        ('высшее', 'Высшее'),
    ]

    reader_id = models.AutoField(primary_key=True)
    card_number = models.CharField(max_length=20, unique=True, verbose_name='Номер читательского билета')
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    passport_number = models.CharField(max_length=11, unique=True, verbose_name='Номер паспорта')
    birth_date = models.DateField(db_index=True, verbose_name='Дата рождения')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='Адрес')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    education_level = models.CharField(
        max_length=20,
        choices=EDUCATION_CHOICES,
        blank=True,
        null=True,
        verbose_name='Уровень образования'
    )
    has_academic_degree = models.BooleanField(default=False, verbose_name='Наличие учёной степени')
    hall = models.ForeignKey(
        Hall,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='readers',
        verbose_name='Зал'
    )
    registration_date = models.DateField(default=lambda: timezone.now().date(), verbose_name='Дата регистрации')
    last_reregistration_date = models.DateField(null=True, blank=True, verbose_name='Дата последней перерегистрации')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        db_table = 'reader'
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'
        ordering = ['full_name']
        indexes = [
            models.Index(fields=['birth_date'], name='idx_reader_birth'),
            models.Index(fields=['hall'], name='idx_reader_hall'),
        ]

    def __str__(self) -> str:
        return f'{self.card_number} - {self.full_name}'


class BookCopy(TimestampMixin):
    """Экземпляр книги."""
    copy_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies', verbose_name='Книга')
    hall = models.ForeignKey(Hall, on_delete=models.PROTECT, related_name='book_copies', verbose_name='Зал')
    inventory_number = models.CharField(max_length=50, unique=True, verbose_name='Инвентарный номер')
    registration_date = models.DateField(default=lambda: timezone.now().date(), verbose_name='Дата регистрации')
    writeoff_date = models.DateField(null=True, blank=True, verbose_name='Дата списания')
    is_written_off = models.BooleanField(default=False, verbose_name='Списана')

    class Meta:
        db_table = 'book_copy'
        verbose_name = 'Экземпляр книги'
        verbose_name_plural = 'Экземпляры книг'
        ordering = ['-registration_date']
        indexes = [
            models.Index(fields=['book'], name='idx_copy_book'),
            models.Index(fields=['hall'], name='idx_copy_hall'),
        ]

    def __str__(self) -> str:
        return f'{self.inventory_number} - {self.book.title}'

    def clean(self):
        """Валидация: если is_written_off=True, то writeoff_date должен быть заполнен."""
        from django.core.exceptions import ValidationError
        if self.is_written_off and not self.writeoff_date:
            raise ValidationError({'writeoff_date': 'Дата списания обязательна для списанных книг.'})
        if not self.is_written_off and self.writeoff_date:
            raise ValidationError({'is_written_off': 'Книга должна быть помечена как списанная, если указана дата списания.'})


class BookIssue(TimestampMixin):
    """Выдача книги читателю."""
    issue_id = models.AutoField(primary_key=True)
    reader = models.ForeignKey(Reader, on_delete=models.PROTECT, related_name='book_issues', verbose_name='Читатель')
    copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT, related_name='issues', verbose_name='Экземпляр')
    hall = models.ForeignKey(Hall, on_delete=models.PROTECT, related_name='book_issues', verbose_name='Зал')
    issue_date = models.DateField(default=lambda: timezone.now().date(), db_index=True, verbose_name='Дата выдачи')
    return_date = models.DateField(null=True, blank=True, db_index=True, verbose_name='Дата возврата')

    class Meta:
        db_table = 'book_issue'
        verbose_name = 'Выдача книги'
        verbose_name_plural = 'Выдачи книг'
        ordering = ['-issue_date']
        indexes = [
            models.Index(fields=['reader'], name='idx_issue_reader'),
            models.Index(fields=['copy'], name='idx_issue_copy'),
            models.Index(fields=['issue_date', 'return_date'], name='idx_issue_dates'),
            models.Index(
                fields=['copy'],
                condition=models.Q(return_date__isnull=True),
                name='uq_issue_active_per_copy'
            ),
        ]

    def __str__(self) -> str:
        status = 'возвращена' if self.return_date else 'на руках'
        return f'{self.reader.full_name} - {self.copy.book.title} ({status})'

    def clean(self):
        """Валидация: return_date должен быть >= issue_date."""
        from django.core.exceptions import ValidationError
        if self.return_date and self.return_date < self.issue_date:
            raise ValidationError({'return_date': 'Дата возврата не может быть раньше даты выдачи.'})


class HallBookStock(TimestampMixin):
    """Количество экземпляров книги в каждом зале."""
    id = models.AutoField(primary_key=True)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='book_stocks', verbose_name='Зал')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='hall_stocks', verbose_name='Книга')
    copies_total = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Всего экземпляров'
    )

    class Meta:
        db_table = 'hall_book_stock'
        unique_together = [['hall', 'book']]
        verbose_name = 'Склад книги в зале'
        verbose_name_plural = 'Склады книг в залах'
        indexes = [
            models.Index(fields=['book'], name='idx_stock_book'),
        ]

    def __str__(self) -> str:
        return f'{self.hall.name} - {self.book.title}: {self.copies_total} экз.'


class Staff(TimestampMixin):
    """Сотрудник библиотеки (для авторизации)."""
    staff_id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=50, unique=True, verbose_name='Логин')
    email = models.EmailField(unique=True, verbose_name='Email')
    password_hash = models.CharField(max_length=512, verbose_name='Хеш пароля')
    refresh_token = models.TextField(null=True, blank=True, verbose_name='Refresh токен')
    refresh_token_expires_at = models.DateTimeField(null=True, blank=True, verbose_name='Срок действия refresh токена')

    class Meta:
        db_table = 'staff'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['login']

    def __str__(self) -> str:
        return self.login
    
    @property
    def is_authenticated(self) -> bool:
        """Всегда True для аутентифицированного сотрудника."""
        return True
    
    @property
    def is_anonymous(self) -> bool:
        """Всегда False для аутентифицированного сотрудника."""
        return False

