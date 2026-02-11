from datetime import date

from django.db import models


class Author(models.Model):
    """Автор книги"""
    author_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200, verbose_name='Полное имя')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'Author'


class Book(models.Model):
    """Книга / Библиографическое описание"""
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300, verbose_name='Название')
    publisher = models.CharField(max_length=200, verbose_name='Издательство')
    publication_year = models.IntegerField(verbose_name='Год издания')
    section = models.CharField(max_length=100, verbose_name='Раздел')
    inventory_code = models.CharField(max_length=50, unique=True, verbose_name='Инвентарный номер')
    is_in_catalog = models.BooleanField(default=True, verbose_name='В каталоге')

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

    class Meta:
        db_table = 'Book'


class BookAuthor(models.Model):
    """Связь книги и автора"""
    book_author_id = models.AutoField(primary_key=True)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='author_id')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='book_id')
    author_order = models.IntegerField(default=1, verbose_name='Порядок автора')

    class Meta:
        db_table = 'BookAuthor'
        unique_together = ['author_id', 'book_id']
        ordering = ['author_order']

    def __str__(self):
        return f"{self.author_id} - {self.book_id}"


class ReadingHall(models.Model):
    """Читальный зал"""
    hall_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Название зала')
    hall_number = models.IntegerField(unique=True, verbose_name='Номер зала')
    capacity = models.IntegerField(verbose_name='Вместимость')

    def __str__(self):
        return f"{self.name} (№{self.hall_number})"

    class Meta:
        db_table = 'ReadingHall'


# Логика генерации номера:
# Формат: Б-ГГ-XXXX
#
# Б - префикс "Библиотека"
#
# ГГ - последние две цифры года (24 для 2024)
#
# XXXX - порядковый номер в году (с ведущими нулями)
from django.db import models
from datetime import date  # Добавляем импорт


class Reader(models.Model):
    """Читатель"""
    EDUCATION_CHOICES = [
        ('primary', 'Начальное'),
        ('secondary', 'Среднее'),
        ('higher', 'Высшее'),
        ('degree', 'Ученая степень'),
    ]

    reader_id = models.AutoField(primary_key=True)
    library_card_id = models.CharField(max_length=50, unique=True, verbose_name='Номер читательского билета',
                                       editable=False)
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    birth_date = models.DateField(verbose_name='Дата рождения')
    education_level = models.CharField(max_length=20, choices=EDUCATION_CHOICES, verbose_name='Образование')
    passport = models.CharField(max_length=50, verbose_name='Номер паспорта')
    phone_number = models.CharField(max_length=20, verbose_name='Телефон')
    home_address = models.TextField(verbose_name='Адрес')
    hall_id = models.ForeignKey(ReadingHall, on_delete=models.PROTECT, db_column='hall_id', verbose_name='Зал')
    is_active_member = models.BooleanField(default=True, verbose_name='Активный читатель')
    first_registered_at = models.DateField(auto_now_add=True, verbose_name='Дата первой регистрации')

    # ИЗМЕНЯЕМ: убираем auto_now=True, ставим default=date.today
    last_registration_at = models.DateField(default=date.today,
                                            verbose_name='Дата последней регистрации/перерегистрации')

    def save(self, *args, **kwargs):
        # Генерируем номер билета только при создании нового читателя
        if not self.pk:  # Если объект еще не сохранен в БД
            from datetime import datetime
            current_year = datetime.now().strftime("%y")

            last_reader = Reader.objects.filter(
                library_card_id__startswith=f'Б-{current_year}-'
            ).order_by('-library_card_id').first()

            if last_reader:
                last_number = int(last_reader.library_card_id.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.library_card_id = f'Б-{current_year}-{new_number:04d}'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.library_card_id})"

    class Meta:
        db_table = 'Reader'


class CopyOfBook(models.Model):
    """Экземпляр книги"""
    AVAILABILITY_STATUS_CHOICES = [
        ('available', 'Доступен'),
        ('on_loan', 'Выдан'),
        ('reserved', 'Зарезервирован'),
        ('decommissioned', 'Списан'),
    ]

    CONDITION_CHOICES = [
        ('excellent', 'Отличное'),
        ('good', 'Хорошее'),
        ('fair', 'Удовлетворительное'),
        ('poor', 'Плохое'),
        ('damaged', 'Поврежден'),
    ]

    copy_book_id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='book_id', verbose_name='Книга')
    hall_id = models.ForeignKey(ReadingHall, on_delete=models.PROTECT, db_column='hall_id', verbose_name='Зал')
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS_CHOICES, default='available',
                                           verbose_name='Статус доступности')
    received_date = models.DateField(auto_now_add=True, verbose_name='Дата поступления')
    copy_condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good',
                                      verbose_name='Состояние')
    decommission_date = models.DateField(null=True, blank=True, verbose_name='Дата списания')

    def __str__(self):
        return f"Экз. книги: {self.book_id.title} (ID: {self.copy_book_id})"

    class Meta:
        db_table = 'CopyOfBook'


class LoanRecord(models.Model):
    """Запись выдачи книги"""
    loan_id = models.AutoField(primary_key=True)
    copy_book_id = models.ForeignKey(CopyOfBook, on_delete=models.PROTECT, db_column='copy_book_id',
                                     verbose_name='Экземпляр книги')
    reader_id = models.ForeignKey(Reader, on_delete=models.PROTECT, db_column='reader_id', verbose_name='Читатель')
    issued_at = models.DateField(default=date.today, verbose_name='Дата выдачи')
    due_date = models.DateField(verbose_name='Срок возврата')
    returned_at = models.DateField(null=True, blank=True, verbose_name='Дата возврата')

    def __str__(self):
        return f"Выдача #{self.loan_id}: {self.reader_id} → {self.copy_book_id}"

    class Meta:
        db_table = 'LoanRecord'