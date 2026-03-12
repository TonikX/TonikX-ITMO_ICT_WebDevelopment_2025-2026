from datetime import date
from django.db import models


class Hall(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    year = models.IntegerField()
    section = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class BookInHall(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    copies = models.IntegerField()

    class Meta:
        unique_together = ('book', 'hall')

    def __str__(self):
        return f"{self.book.title} in {self.hall.name} ({self.copies} copies)"


class Reader(models.Model):
    ticket_number = models.CharField(max_length=50)
    full_name = models.CharField(max_length=200)
    passport_number = models.CharField(max_length=50)

    birth_date = models.DateField()
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    education = models.CharField(max_length=50)
    academic_degree = models.BooleanField(default=False)

    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    registration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class BookIssue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book_in_hall = models.ForeignKey(
        BookInHall, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Из какого зала выдана книга (для учета копий)"
    )

    issue_date = models.DateField(default=date.today)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book} -> {self.reader}"