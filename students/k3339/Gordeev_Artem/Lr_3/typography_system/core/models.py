from django.conf import settings  # Импорт для ссылки на модель User
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('manager', 'Менеджер'),
        ('editor', 'Редактор'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='editor', verbose_name="Роль")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Author(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Customer(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название компании / ФИО")
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    pages_count = models.PositiveIntegerField(verbose_name="Кол-во страниц")
    has_illustrations = models.BooleanField(default=False, verbose_name="Наличие иллюстраций")

    authors = models.ManyToManyField(Author, through='BookAuthor', verbose_name="Авторы")

    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BookEditor', related_name='edited_books',
                                     verbose_name="Редакторы")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Contract(models.Model):
    number = models.CharField(max_length=50, unique=True, verbose_name="Номер контракта")
    date_signed = models.DateField(verbose_name="Дата подписания")

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='contracts',
        limit_choices_to={'role': 'manager'},
        verbose_name="Менеджер"
    )

    # одна книга = один контракт
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='contract', verbose_name="Книга")

    def __str__(self):
        return f"Контракт №{self.number} ({self.book.title})"

    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name="Заказчик")

    books = models.ManyToManyField(Book, through='OrderItem', verbose_name="Книги в заказе")

    def __str__(self):
        return f"Заказ №{self.id} от {self.created_at.strftime('%d.%m.%Y')}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class BookAuthor(models.Model):
    """Таблица связи Книга <-> Автор. Хранит порядок авторов."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    order_position = models.PositiveIntegerField(default=1, verbose_name="Порядковый номер на обложке")

    class Meta:
        ordering = ['order_position']
        unique_together = ('book', 'author')
        verbose_name = "Автор книги"
        verbose_name_plural = "Авторы книги"


class BookEditor(models.Model):
    """Таблица связи Книга <-> Редактор. Хранит статус ответственного."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Редактор")
    is_responsible = models.BooleanField(default=False, verbose_name="Ответственный редактор")

    class Meta:
        unique_together = ('book', 'editor')
        verbose_name = "Редактор книги"
        verbose_name_plural = "Редакторы книги"


class OrderItem(models.Model):
    """Таблица связи Заказ <-> Книга. Хранит количество штук."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество экземпляров")
