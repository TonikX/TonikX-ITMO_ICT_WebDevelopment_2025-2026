from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    """Модель сотрудника типографии"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    position = models.CharField(max_length=100, verbose_name="Должность")
    hire_date = models.DateField(verbose_name="Дата найма")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Зарплата")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес")
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"


class Manager(Employee):
    """Модель менеджера (наследуется от Employee)"""
    department = models.CharField(max_length=100, verbose_name="Отдел")
    
    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"
    
    def __str__(self):
        return f"Менеджер: {self.user.get_full_name()}"


class Editor(Employee):
    """Модель редактора (наследуется от Employee)"""
    specialization = models.CharField(max_length=100, verbose_name="Специализация")
    experience_years = models.IntegerField(verbose_name="Опыт работы (лет)")
    
    class Meta:
        verbose_name = "Редактор"
        verbose_name_plural = "Редакторы"
    
    def __str__(self):
        return f"Редактор: {self.user.get_full_name()}"


class Author(models.Model):
    """Модель автора книги"""
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    birth_date = models.DateField(verbose_name="Дата рождения")
    biography = models.TextField(blank=True, null=True, verbose_name="Биография")
    contact_email = models.EmailField(verbose_name="Email")
    contact_phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес")
    
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        middle = f" {self.middle_name}" if self.middle_name else ""
        return f"{self.last_name} {self.first_name}{middle}"
    
    @property
    def full_name(self):
        """Полное имя автора"""
        middle = f" {self.middle_name}" if self.middle_name else ""
        return f"{self.last_name} {self.first_name}{middle}"


class Book(models.Model):
    """Модель книги"""
    title = models.CharField(max_length=200, verbose_name="Название")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    publication_date = models.DateField(verbose_name="Дата публикации")
    pages = models.IntegerField(verbose_name="Количество страниц")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['title']
    
    def __str__(self):
        return self.title


class Contract(models.Model):
    """Модель контракта"""
    contract_number = models.CharField(max_length=50, unique=True, verbose_name="Номер контракта")
    signing_date = models.DateField(verbose_name="Дата подписания")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Общая сумма")
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Черновик'),
            ('signed', 'Подписан'),
            ('active', 'Активен'),
            ('completed', 'Завершен'),
            ('cancelled', 'Отменен')
        ],
        default='draft',
        verbose_name="Статус"
    )
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name="Менеджер")
    book = models.OneToOneField(Book, on_delete=models.CASCADE, verbose_name="Книга")
    
    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"
        ordering = ['-signing_date']
    
    def __str__(self):
        return f"Контракт {self.contract_number} - {self.book.title}"


class ContractAuthor(models.Model):
    """Промежуточная модель для связи контракта и авторов с указанием порядка и гонорара"""
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name="Контракт")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    order_on_cover = models.IntegerField(verbose_name="Порядок на обложке")
    royalty_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процент гонорара")
    royalty_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма гонорара")
    
    class Meta:
        verbose_name = "Автор контракта"
        verbose_name_plural = "Авторы контрактов"
        unique_together = ['contract', 'author']
        ordering = ['order_on_cover']
    
    def __str__(self):
        return f"{self.author.full_name} в контракте {self.contract.contract_number}"


class BookEditor(models.Model):
    """Промежуточная модель для связи книги и редакторов"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE, verbose_name="Редактор")
    is_lead_editor = models.BooleanField(default=False, verbose_name="Ответственный редактор")
    start_date = models.DateField(verbose_name="Дата начала работы")
    end_date = models.DateField(blank=True, null=True, verbose_name="Дата окончания работы")
    
    class Meta:
        verbose_name = "Редактор книги"
        verbose_name_plural = "Редакторы книг"
        unique_together = ['book', 'editor']
    
    def __str__(self):
        lead = " (ответственный)" if self.is_lead_editor else ""
        return f"{self.editor.user.get_full_name()} - {self.book.title}{lead}"


class Customer(models.Model):
    """Модель заказчика"""
    name = models.CharField(max_length=200, verbose_name="Название/Имя")
    contact_person = models.CharField(max_length=200, verbose_name="Контактное лицо")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес")
    customer_type = models.CharField(
        max_length=20,
        choices=[
            ('individual', 'Физическое лицо'),
            ('organization', 'Организация')
        ],
        verbose_name="Тип заказчика"
    )
    
    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Order(models.Model):
    """Модель заказа"""
    order_number = models.CharField(max_length=50, unique=True, verbose_name="Номер заказа")
    order_date = models.DateField(verbose_name="Дата заказа")
    delivery_date = models.DateField(verbose_name="Дата доставки")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Общая сумма")
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'В ожидании'),
            ('processing', 'В обработке'),
            ('shipped', 'Отправлен'),
            ('delivered', 'Доставлен'),
            ('cancelled', 'Отменен')
        ],
        default='pending',
        verbose_name="Статус"
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Заказчик")
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-order_date']
    
    def __str__(self):
        return f"Заказ {self.order_number} - {self.customer.name}"


class OrderItem(models.Model):
    """Модель позиции заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    quantity = models.IntegerField(verbose_name="Количество")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая цена")
    
    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"
        unique_together = ['order', 'book']
    
    def __str__(self):
        return f"{self.book.title} x{self.quantity} в заказе {self.order.order_number}"
    
    def save(self, *args, **kwargs):
        """Автоматический расчет общей цены"""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class FinancialRecord(models.Model):
    """Модель финансовой записи"""
    date = models.DateField(verbose_name="Дата")
    record_type = models.CharField(
        max_length=20,
        choices=[
            ('income', 'Доход'),
            ('expense', 'Расход'),
            ('royalty', 'Гонорар'),
            ('salary', 'Зарплата'),
            ('other', 'Прочее')
        ],
        verbose_name="Тип записи"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма")
    description = models.TextField(verbose_name="Описание")
    related_contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Связанный контракт")
    related_order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Связанный заказ")
    
    class Meta:
        verbose_name = "Финансовая запись"
        verbose_name_plural = "Финансовые записи"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.get_record_type_display()} - {self.amount} ({self.date})"


# Модели для системы распределения газет по почтовым отделениям

class Newspaper(models.Model):
    """Модель газеты"""
    title = models.CharField(max_length=200, verbose_name="Название газеты")
    publication_index = models.CharField(max_length=20, unique=True, verbose_name="Индекс издания")
    editor_first_name = models.CharField(max_length=100, verbose_name="Имя редактора")
    editor_last_name = models.CharField(max_length=100, verbose_name="Фамилия редактора")
    editor_middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество редактора")
    price_per_copy = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена экземпляра")
    
    class Meta:
        verbose_name = "Газета"
        verbose_name_plural = "Газеты"
        ordering = ['title']
    
    def __str__(self):
        return f"{self.title} ({self.publication_index})"
    
    @property
    def editor_full_name(self):
        """Полное имя редактора"""
        middle = f" {self.editor_middle_name}" if self.editor_middle_name else ""
        return f"{self.editor_last_name} {self.editor_first_name}{middle}"


class PrintingHouse(models.Model):
    """Модель типографии"""
    name = models.CharField(max_length=200, verbose_name="Название типографии")
    address = models.TextField(verbose_name="Адрес")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    class Meta:
        verbose_name = "Типография"
        verbose_name_plural = "Типографии"
        ordering = ['name']
    
    def __str__(self):
        status = "Активна" if self.is_active else "Закрыта"
        return f"{self.name} ({status})"


class PostOffice(models.Model):
    """Модель почтового отделения"""
    number = models.CharField(max_length=20, unique=True, verbose_name="Номер почтового отделения")
    address = models.TextField(verbose_name="Адрес")
    
    class Meta:
        verbose_name = "Почтовое отделение"
        verbose_name_plural = "Почтовые отделения"
        ordering = ['number']
    
    def __str__(self):
        return f"Почтовое отделение №{self.number}"


class PrintingRun(models.Model):
    """Модель тиража - связь между типографией и газетой с указанием тиража"""
    printing_house = models.ForeignKey(PrintingHouse, on_delete=models.CASCADE, verbose_name="Типография")
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE, verbose_name="Газета")
    circulation = models.IntegerField(verbose_name="Тираж")
    
    class Meta:
        verbose_name = "Тираж"
        verbose_name_plural = "Тиражи"
        unique_together = ['printing_house', 'newspaper']
        ordering = ['-circulation']
    
    def __str__(self):
        return f"{self.newspaper.title} в {self.printing_house.name} - тираж {self.circulation}"


class Distribution(models.Model):
    """Модель распределения - связь между почтовым отделением, газетой и типографией с количеством"""
    post_office = models.ForeignKey(PostOffice, on_delete=models.CASCADE, verbose_name="Почтовое отделение")
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE, verbose_name="Газета")
    printing_house = models.ForeignKey(PrintingHouse, on_delete=models.CASCADE, verbose_name="Типография")
    quantity = models.IntegerField(verbose_name="Количество экземпляров")
    
    class Meta:
        verbose_name = "Распределение"
        verbose_name_plural = "Распределения"
        unique_together = ['post_office', 'newspaper', 'printing_house']
        ordering = ['post_office', 'newspaper']
    
    def __str__(self):
        return f"{self.newspaper.title} ({self.printing_house.name}) -> {self.post_office.number}: {self.quantity} шт."