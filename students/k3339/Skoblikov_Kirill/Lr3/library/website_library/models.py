from django.contrib.auth.models import AbstractUser
from django.db import models


class LibraryEmployee(AbstractUser):
    patronymic = models.CharField(max_length=32, blank=True, verbose_name="Отчество")
    job_title = models.CharField(max_length=32, blank=True, verbose_name="Должность")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=128)
    authors = models.CharField(max_length=256)
    publishing_house = models.CharField(max_length=64)
    publication_year = models.DateField()
    cipher = models.CharField(max_length=20)

    def __str__(self):
        return self.book_name


class Hall(models.Model):
    hall_number = models.IntegerField(primary_key=True)
    hall_name = models.CharField(max_length=64)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.hall_name} ({self.hall_number})"


class LibraryReader(models.Model):
    reader_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=32, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=32, blank=True, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=32, blank=True, verbose_name="Отчество")
    reader_card_number = models.CharField(max_length=10, unique=True)
    birth_date = models.DateField()
    passport_number = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=12)
    education_types = [
        ('se', 'secondary education'),
        ('he', 'higher education'),
        ('ad', 'academic degree'),
    ]
    education = models.CharField(max_length=2, choices=education_types, verbose_name='Образование')
    academic_degree = models.BooleanField()
    address = models.CharField(max_length=256)
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, related_name="readers", null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class ReaderRegistration(models.Model):
    registration_id = models.AutoField(primary_key=True)
    reader = models.ForeignKey(
        LibraryReader,
        on_delete=models.CASCADE,
        related_name="registrations"
    )
    hall = models.ForeignKey(
        Hall,
        on_delete=models.PROTECT,
        related_name="registrations"
    )
    registration_date = models.DateField()

    class Meta:
        verbose_name = "Регистрация читателя"
        verbose_name_plural = "Регистрации читателей"


class Reading(models.Model):
    reading_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(LibraryReader, on_delete=models.CASCADE)
    issued_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.reader} — {self.book}"


class ReaderHallHistory(models.Model):
    id = models.AutoField(primary_key=True)
    reader = models.ForeignKey(LibraryReader, on_delete=models.CASCADE)
    old_hall = models.ForeignKey(Hall, related_name="old_reader_hall", on_delete=models.CASCADE)
    new_hall = models.ForeignKey(Hall, related_name="new_reader_hall", on_delete=models.CASCADE)
    date_update = models.DateField()


class ReaderCardHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    reader = models.ForeignKey(LibraryReader, on_delete=models.CASCADE)
    old_card_number = models.CharField(max_length=10)
    new_card_number = models.CharField(max_length=10)
    update_date = models.DateField()


class BookMovement(models.Model):
    move_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    old_hall = models.ForeignKey(Hall, related_name="old_hall_books", on_delete=models.CASCADE)
    new_hall = models.ForeignKey(Hall, related_name="new_hall_books", on_delete=models.CASCADE)
    date = models.DateField()


class BookSet(models.Model):
    set_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("book", "hall")
