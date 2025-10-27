from django.db import models
from django.contrib.auth.models import User

class Reader(models.Model):
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    email = models.EmailField("Электронная почта", unique=True)
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, 
                                verbose_name="Пользователь", related_name="reader")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"

class Book(models.Model):
    title = models.CharField("Название книги", max_length=200)
    author = models.CharField("Автор", max_length=100)
    year = models.PositiveIntegerField("Год издания")
    available = models.BooleanField("Доступна", default=True)
    description = models.TextField("Описание", blank=True, default="")

    def __str__(self):
        return f"{self.title} — {self.author}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

class Borrowing(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name="Читатель")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    date_from = models.DateField("Дата выдачи")
    date_to = models.DateField("Дата возврата", null=True, blank=True)
    is_returned = models.BooleanField("Возвращена", default=False)

    def __str__(self):
        return f"{self.reader} взял '{self.book}'"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews", verbose_name="Книга")
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name="Читатель")
    rating = models.PositiveIntegerField("Рейтинг", choices=[(i, i) for i in range(1, 11)])
    comment = models.TextField("Комментарий")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Отзыв {self.reader} на '{self.book}' ({self.rating}/10)"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ('book', 'reader')  # Один отзыв от читателя на книгу
