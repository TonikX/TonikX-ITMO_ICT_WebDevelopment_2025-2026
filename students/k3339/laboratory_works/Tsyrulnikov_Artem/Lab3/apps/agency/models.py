from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    """Заказчик (рекламодатель)"""

    name = models.CharField("Название компании", max_length=200)
    contact_person = models.CharField("Контактное лицо", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email")

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Сотрудник (исполнитель)"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email")
    position = models.CharField("Должность", max_length=100)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class ServiceCategory(models.Model):
    """Категория услуг"""

    name = models.CharField("Название категории", max_length=100)

    class Meta:
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"

    def __str__(self):
        return self.name


class Service(models.Model):
    """Рекламная услуга (прайс-лист)"""

    category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE, verbose_name="Категория"
    )
    name = models.CharField("Наименование услуги", max_length=200)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    unit = models.CharField("Единица измерения", max_length=50)
    materials = models.TextField("Материалы", blank=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


class Order(models.Model):
    """Заявка на рекламу"""

    STATUS_CHOICES = [
        ("new", "Новая"),
        ("in_progress", "В работе"),
        ("completed", "Выполнена"),
    ]

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name="Заказчик"
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, verbose_name="Услуга"
    )
    executor = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Исполнитель"
    )
    quantity = models.PositiveIntegerField("Количество")
    total_cost = models.DecimalField("Стоимость", max_digits=12, decimal_places=2)
    status = models.CharField(
        "Статус", max_length=20, choices=STATUS_CHOICES, default="new"
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"Заявка #{self.id} - {self.client}"


class PaymentOrder(models.Model):
    """Платежное поручение"""

    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="Заявка")
    issued_date = models.DateField("Дата выставления", auto_now_add=True)
    payment_date = models.DateField("Дата оплаты", null=True, blank=True)
    is_paid = models.BooleanField("Оплачено", default=False)

    class Meta:
        verbose_name = "Платежное поручение"
        verbose_name_plural = "Платежные поручения"

    def __str__(self):
        return f"ПП #{self.id} для заявки #{self.order.id}"
