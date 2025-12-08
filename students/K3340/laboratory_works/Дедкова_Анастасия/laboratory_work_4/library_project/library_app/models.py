from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.utils import timezone

STATUS_AVAILABLE = "available"
STATUS_ON_LOAN = "on_loan"
STATUS_WRITTEN_OFF = "written_off"

STATUS_CHOICES = [
    (STATUS_AVAILABLE, "Доступен"),
    (STATUS_ON_LOAN, "На руках"),
    (STATUS_WRITTEN_OFF, "Списан"),
]

# авторы


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    full_name = models.CharField("ФИО автора", max_length=255)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.full_name


# книги


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)

    title = models.CharField("Название", max_length=255)
    publisher = models.CharField("Издательство", max_length=255)
    publication_year = models.IntegerField(
        verbose_name="Год издания",
        validators=[
            MinValueValidator(1),  # книги с нулевого года не существует
            MaxValueValidator(datetime.datetime.now().year)  # максимум - текущий год
        ]
    )
    section = models.CharField("Раздел", max_length=255)
    cipher = models.CharField("Шифр книги", max_length=100)
    is_active = models.BooleanField("Активна ли книга", default=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return f"{self.title} ({self.publication_year})"


# M2M через промежуточную таблицу


class BookAuthor(models.Model):
    book_author_id = models.AutoField(primary_key=True)

    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")

    class Meta:
        verbose_name = "Автор книги"
        verbose_name_plural = "Авторы книги"
        unique_together = ("book", "author")  # чтобы не дублировать связи

    def __str__(self):
        return f"{self.book} — {self.author}"


# Залы


class ReadingHall(models.Model):
    hall_id = models.AutoField(primary_key=True)

    number = models.IntegerField("Номер зала", unique=True)
    name = models.CharField("Название", max_length=255)

    capacity = models.PositiveIntegerField(
        "Вместимость",
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = "Читальный зал"
        verbose_name_plural = "Читальные залы"

    def __str__(self):
        return f"Зал {self.number}: {self.name}"


# Читатели


class Reader(models.Model):
    reader_id = models.AutoField(primary_key=True)

    card_number = models.CharField("Номер читательского билета", max_length=50, unique=True)
    full_name = models.CharField("ФИО", max_length=255)
    passport_number = models.CharField("Номер паспорта", max_length=50)

    birth_date = models.DateField("Дата рождения")
    address = models.CharField("Адрес", max_length=255)
    phone = models.CharField("Телефон", max_length=50)

    education_level = models.CharField("Образование", max_length=50)
    has_academic_degree = models.BooleanField(
        "Наличие учёной степени",
        default=False,
    )

    hall = models.ForeignKey(
        ReadingHall,
        on_delete=models.SET_NULL,
        null=True,
        related_name="readers",
        verbose_name="Закреплён за залом",
    )

    is_active = models.BooleanField("Активен", default=True)
    registered_at = models.DateField("Дата регистрации", auto_now_add=True)
    last_reregistration_at = models.DateField(
        "Дата последней перерегистрации",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"

    def __str__(self):
        return f"{self.full_name} (билет {self.card_number})"


# Экземпляры книг


class BookCopy(models.Model):
    copy_id = models.AutoField(primary_key=True, verbose_name="ID экземпляра")
    book = models.ForeignKey("Book", on_delete=models.CASCADE, verbose_name="Книга")
    hall = models.ForeignKey("ReadingHall", on_delete=models.CASCADE, verbose_name="Читальный зал")

    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_AVAILABLE,
    )

    date_received = models.DateField("Дата поступления")
    date_written_off = models.DateField("Дата списания", null=True, blank=True)

    class Meta:
        verbose_name = "Экземпляр книги"
        verbose_name_plural = "Экземпляры книги"

    def __str__(self):
        return f"Экз. {self.copy_id} — {self.book.title}"

# Выдача книг


class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True, verbose_name="ID выдачи")

    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
        verbose_name="Читатель",
        related_name="loans",
    )
    copy = models.ForeignKey(
        BookCopy,
        on_delete=models.CASCADE,
        verbose_name="Экземпляр книги",
        related_name="loans",
    )
    assigned_at = models.DateTimeField(
        verbose_name="Дата выдачи",
        default=timezone.now,
    )
    returned_at = models.DateTimeField(
        verbose_name="Дата возврата",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Выдача"
        verbose_name_plural = "Выдачи"

    def __str__(self):
        return f"{self.copy} → {self.reader}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.returned_at is None:
            if self.copy.status != STATUS_ON_LOAN:
                self.copy.status = STATUS_ON_LOAN
                self.copy.save(update_fields=["status"])
        else:
            if self.copy.status != STATUS_AVAILABLE:
                self.copy.status = STATUS_AVAILABLE
                self.copy.save(update_fields=["status"])
