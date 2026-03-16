from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class ReadingRoom(models.Model):
    """Читальный зал библиотеки"""
    number = models.CharField(max_length=50, unique=True, verbose_name="Номер зала")
    name = models.CharField(max_length=200, verbose_name="Название зала")
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Вместимость"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Читальный зал"
        verbose_name_plural = "Читальные залы"
        ordering = ['number']
    
    def __str__(self):
        return f"{self.number} - {self.name}"


class Reader(models.Model):
    """Читатель библиотеки"""
    EDUCATION_CHOICES = [
        ('primary', 'Начальное'),
        ('secondary', 'Среднее'),
        ('higher', 'Высшее'),
        ('degree', 'Ученая степень'),
    ]
    
    ticket_number = models.CharField(max_length=50, unique=True, verbose_name="Номер читательского билета")
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    passport_number = models.CharField(max_length=50, verbose_name="Номер паспорта")
    birth_date = models.DateField(verbose_name="Дата рождения")
    address = models.TextField(verbose_name="Адрес")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    education = models.CharField(
        max_length=20,
        choices=EDUCATION_CHOICES,
        verbose_name="Образование"
    )
    has_degree = models.BooleanField(default=False, verbose_name="Наличие ученой степени")
    reading_room = models.ForeignKey(
        ReadingRoom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='readers',
        verbose_name="Читальный зал"
    )
    registration_date = models.DateField(auto_now_add=True, verbose_name="Дата записи в библиотеку")
    unregistration_date = models.DateField(null=True, blank=True, verbose_name="Дата выписки из библиотеки")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"
        ordering = ['ticket_number']
    
    def __str__(self):
        return f"{self.ticket_number} - {self.full_name}"
    
    @property
    def age(self):
        """Возраст читателя"""
        today = timezone.now().date()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))


class Book(models.Model):
    """Книга в библиотеке"""
    title = models.CharField(max_length=300, verbose_name="Название книги")
    authors = models.CharField(max_length=500, verbose_name="Автор(ы)")
    publisher = models.CharField(max_length=200, verbose_name="Издательство")
    publication_year = models.PositiveIntegerField(verbose_name="Год издания")
    section = models.CharField(max_length=200, verbose_name="Раздел")
    code = models.CharField(max_length=100, verbose_name="Шифр книги")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['title']
    
    def __str__(self):
        return f"{self.code} - {self.title}"


class BookCopy(models.Model):
    """Экземпляр книги в читальном зале"""
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='copies',
        verbose_name="Книга"
    )
    reading_room = models.ForeignKey(
        ReadingRoom,
        on_delete=models.CASCADE,
        related_name='book_copies',
        verbose_name="Читальный зал"
    )
    quantity = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Количество экземпляров"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Экземпляр книги в зале"
        verbose_name_plural = "Экземпляры книг в залах"
        unique_together = ['book', 'reading_room']
        ordering = ['book', 'reading_room']
    
    def __str__(self):
        return f"{self.book.title} в зале {self.reading_room.number} ({self.quantity} шт.)"


class BookAssignment(models.Model):
    """Закрепление книги за читателем"""
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name="Книга"
    )
    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
        related_name='book_assignments',
        verbose_name="Читатель"
    )
    assignment_date = models.DateField(auto_now_add=True, verbose_name="Дата закрепления")
    return_date = models.DateField(null=True, blank=True, verbose_name="Дата возврата")
    is_returned = models.BooleanField(default=False, verbose_name="Возвращена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Закрепление книги"
        verbose_name_plural = "Закрепления книг"
        ordering = ['-assignment_date']
    
    def __str__(self):
        return f"{self.book.title} закреплена за {self.reader.full_name} ({self.assignment_date})"
    
    @property
    def days_since_assignment(self):
        """Количество дней с момента закрепления"""
        if self.is_returned and self.return_date:
            return None
        from django.utils import timezone
        delta = timezone.now().date() - self.assignment_date
        return delta.days
