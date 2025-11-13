from django.db import models

class Reader(models.Model):
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    email = models.EmailField("Электронная почта", unique=True)
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField("Название книги", max_length=200)
    author = models.CharField("Автор", max_length=100)
    year = models.PositiveIntegerField("Год издания")
    available = models.BooleanField("Доступна", default=True)

    def __str__(self):
        return f"{self.title} — {self.author}"

class Borrowing(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name="Читатель")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    date_from = models.DateField("Дата выдачи")
    date_to = models.DateField("Дата возврата", null=True, blank=True)

    def __str__(self):
        return f"{self.reader} взял '{self.book}'"
