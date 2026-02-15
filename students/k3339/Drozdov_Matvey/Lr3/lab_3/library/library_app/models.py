from django.db import models

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Hall(models.Model):
    hall_number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"Hall {self.hall_number}: {self.name}"


class Author(models.Model):
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class Book(models.Model):
    title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    section = models.CharField(max_length=255)

    authors = models.ManyToManyField(
        "Author",
        through="BookAuthor",
        related_name="books"
    )

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("book", "author")



class BookCodeHistory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="code_history")
    code = models.CharField(max_length=100)
    valid_from = models.DateField(default=timezone.now)
    valid_to = models.DateField(blank=True, null=True)

    class Meta:
        indexes = [models.Index(fields=["book", "valid_to"])]

    def __str__(self):
        return f"{self.book_id} -> {self.code}"


class Reader(models.Model):
    full_name = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    education_lvl = models.CharField(max_length=50, blank=True, null=True)  # можно заменить на choices
    degree = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class ReaderHallHistory(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name="hall_history")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="readers_history")
    valid_from = models.DateField(default=timezone.now)
    valid_to = models.DateField(blank=True, null=True)

    class Meta:
        indexes = [models.Index(fields=["reader", "valid_to"])]

    def __str__(self):
        return f"{self.reader_id} -> hall {self.hall_id}"


class ReaderMembershipHistory(models.Model):
    ENROLL = "enroll"
    UNREGISTER = "unregister"
    REREGISTER = "reregister"
    EVENT_CHOICES = [
        (ENROLL, "Enroll"),
        (UNREGISTER, "Unregister"),
        (REREGISTER, "Reregister"),
    ]

    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name="membership_events")
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    event_date = models.DateField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [models.Index(fields=["reader", "event_date"])]

    def __str__(self):
        return f"{self.reader_id} {self.event_type} {self.event_date}"


class ReaderTicketHistory(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name="ticket_history")
    ticket_number = models.CharField(max_length=100, unique=True)
    valid_from = models.DateField(default=timezone.now)
    valid_to = models.DateField(blank=True, null=True)

    class Meta:
        indexes = [models.Index(fields=["reader", "valid_to"])]

    def __str__(self):
        return f"{self.reader_id} ticket {self.ticket_number}"


class BookMovement(models.Model):
    ACQUIRE = "acquire"
    WRITEOFF = "writeoff"
    TRANSFER = "transfer"
    TYPE_CHOICES = [
        (ACQUIRE, "Acquire"),
        (WRITEOFF, "Writeoff"),
        (TRANSFER, "Transfer"),
    ]

    movement_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="movements")
    from_hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True, related_name="movements_out")
    to_hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True, related_name="movements_in")
    qty = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    movement_date = models.DateField(default=timezone.localdate)

    def clean(self):
        # Валидация логики залов (упрощённо, DRF тоже может проверять)
        if self.movement_type == self.ACQUIRE and (self.to_hall is None or self.from_hall is not None):
            raise ValueError("Acquire: to_hall обязателен, from_hall должен быть пустым")
        if self.movement_type == self.WRITEOFF and (self.from_hall is None or self.to_hall is not None):
            raise ValueError("Writeoff: from_hall обязателен, to_hall должен быть пустым")
        if self.movement_type == self.TRANSFER and (self.from_hall is None or self.to_hall is None or self.from_hall_id == self.to_hall_id):
            raise ValueError("Transfer: нужны оба зала и они должны отличаться")


class BookStock(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="stock_rows")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="stock_rows")
    copies = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("book", "hall")

    def __str__(self):
        return f"{self.book_id}@{self.hall_id}={self.copies}"


class Loan(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name="loans")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="loans")
    assigned_at = models.DateField(default=timezone.localdate)
    returned_at = models.DateField(blank=True, null=True)
    qty = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"loan {self.reader_id} book {self.book_id}"

