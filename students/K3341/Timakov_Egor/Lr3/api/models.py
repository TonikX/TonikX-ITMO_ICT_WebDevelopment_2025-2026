from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Employee(models.Model):
    """Модель сотрудника типографии"""
    
    POSITION_CHOICES = [
        ('editor', 'Редактор'),
        ('manager', 'Менеджер'),
        ('designer', 'Дизайнер'),
        ('printer', 'Печатник'),
        ('accountant', 'Бухгалтер'),
        ('director', 'Директор'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, verbose_name='Должность')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    hire_date = models.DateField(verbose_name='Дата найма')
    salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Зарплата')
    department = models.CharField(max_length=100, verbose_name='Отдел')
    
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['-hire_date']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_position_display()}"


class Author(models.Model):
    """Модель автора книги"""
    
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отчество')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    biography = models.TextField(blank=True, null=True, verbose_name='Биография')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"
    
    @property
    def full_name(self):
        """Полное имя автора"""
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"


class Book(models.Model):
    """Модель книги"""
    
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('editing', 'Редактирование'),
        ('design', 'Дизайн'),
        ('printing', 'Печать'),
        ('published', 'Опубликована'),
        ('archived', 'Архив'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название')
    isbn = models.CharField(max_length=17, unique=True, blank=True, null=True, verbose_name='ISBN')
    authors = models.ManyToManyField(Author, related_name='books', verbose_name='Авторы')
    editor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, 
                              related_name='edited_books', limit_choices_to={'position': 'editor'}, verbose_name='Редактор')
    pages = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Количество страниц')
    publication_date = models.DateField(blank=True, null=True, verbose_name='Дата публикации')
    print_date = models.DateField(blank=True, null=True, verbose_name='Дата печати')
    print_run = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Тираж')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Цена')
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Себестоимость')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def profit(self):
        """Прибыль от книги"""
        return (self.price - self.cost) * self.print_run


class FinancialStatus(models.Model):
    """Модель финансового состояния компании"""
    
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]
    
    CATEGORY_CHOICES = [
        ('book_sales', 'Продажа книг'),
        ('printing_services', 'Услуги печати'),
        ('salary', 'Зарплата'),
        ('materials', 'Материалы'),
        ('equipment', 'Оборудование'),
        ('rent', 'Аренда'),
        ('utilities', 'Коммунальные услуги'),
        ('other', 'Прочее'),
    ]
    
    date = models.DateField(verbose_name='Дата')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, verbose_name='Тип операции')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Категория')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Сумма')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, 
                            related_name='financial_records', verbose_name='Связанная книга')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Финансовая запись'
        verbose_name_plural = 'Финансовые записи'
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} ({self.date})"


class Report(models.Model):
    """Модель отчёта"""
    
    REPORT_TYPE_CHOICES = [
        ('financial', 'Финансовый отчёт'),
        ('books', 'Отчёт по книгам'),
        ('employees', 'Отчёт по сотрудникам'),
        ('sales', 'Отчёт по продажам'),
        ('custom', 'Пользовательский отчёт'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название отчёта')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, verbose_name='Тип отчёта')
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reports', verbose_name='Создан')
    start_date = models.DateField(blank=True, null=True, verbose_name='Начальная дата')
    end_date = models.DateField(blank=True, null=True, verbose_name='Конечная дата')
    data = models.JSONField(default=dict, verbose_name='Данные отчёта')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_report_type_display()})"
