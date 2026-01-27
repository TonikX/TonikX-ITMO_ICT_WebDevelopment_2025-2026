from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Position(models.Model):
    position = models.CharField(max_length=100, verbose_name="Название должности")
    minimum_wage = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Минимальная зарплата",
        validators=[MinValueValidator(0)]
    )
    
    def __str__(self):
        return self.position
    
    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class Employee(models.Model):
    CATEGORY_CHOICES = [
        ('chef', 'Шеф-повар'),
        ('cook', 'Повар'),
        ('waiter', 'Официант'),
    ]
    
    full_name = models.CharField(max_length=150, verbose_name="ФИО")
    passport_data = models.CharField(max_length=20, verbose_name="Паспортные данные")
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        verbose_name="Категория"
    )
    position = models.ForeignKey(
        Position, 
        on_delete=models.CASCADE, 
        related_name='employees',
        verbose_name="Должность"
    )
    salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Оклад",
        validators=[MinValueValidator(0)]
    )
    
    def __str__(self):
        return f"{self.full_name} - {self.get_category_display()}"
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Ingredient(models.Model):
    INGREDIENT_TYPES = [
        ('meat', 'Мясо'),
        ('vegetable', 'Овощи'),
        ('dairy', 'Молочные продукты'),
        ('spice', 'Специи'),
        ('other', 'Другое'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Наименование")
    stock_quantity = models.FloatField(
        verbose_name="Количество на складе",
        validators=[MinValueValidator(0)]
    )
    minimum_stock = models.FloatField(
        verbose_name="Необходимый запас",
        validators=[MinValueValidator(0)]
    )
    price_per_unit = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Цена за единицу",
        validators=[MinValueValidator(0)]
    )
    supplier = models.CharField(max_length=100, verbose_name="Поставщик")
    ingredient_type = models.CharField(
        max_length=20, 
        choices=INGREDIENT_TYPES, 
        verbose_name="Тип ингредиента"
    )
    
    def __str__(self):
        return self.name
    
    def is_low_on_stock(self):
        return self.stock_quantity <= self.minimum_stock
    
    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class Dish(models.Model):
    DISH_TYPES = [
        ('appetizer', 'Закуска'),
        ('soup', 'Суп'),
        ('main', 'Основное блюдо'),
        ('dessert', 'Десерт'),
        ('drink', 'Напиток'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Название")
    dish_type = models.CharField(
        max_length=20, 
        choices=DISH_TYPES, 
        verbose_name="Тип блюда"
    )
    ingredients = models.ManyToManyField(
        Ingredient, 
        through='DishIngredient',
        related_name='dishes',
        verbose_name="Ингредиенты"
    )
    
    def calculate_price(self):
        ingredients_cost = sum(
            di.ingredient.price_per_unit * di.quantity 
            for di in self.dish_ingredients.all()
        )
        return ingredients_cost * 1.4
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"


class DishIngredient(models.Model):
    dish = models.ForeignKey(
        Dish, 
        on_delete=models.CASCADE,
        related_name='dish_ingredients',
        verbose_name="Блюдо"
    )
    ingredient = models.ForeignKey(
        Ingredient, 
        on_delete=models.CASCADE,
        related_name='ingredient_dishes',
        verbose_name="Ингредиент"
    )
    quantity = models.FloatField(
        verbose_name="Количество",
        validators=[MinValueValidator(0)]
    )
    
    def __str__(self):
        return f"{self.dish.name} - {self.ingredient.name} ({self.quantity})"
    
    class Meta:
        verbose_name = "Ингредиент блюда"
        verbose_name_plural = "Ингредиенты блюд"
        unique_together = ['dish', 'ingredient']


class Table(models.Model):
    STATUS_CHOICES = [
        ('free', 'Свободен'),
        ('occupied', 'Занят'),
    ]
    
    table_number = models.IntegerField(
        unique=True,
        verbose_name="Номер стола",
        validators=[MinValueValidator(1)]
    )
    capacity = models.IntegerField(
        verbose_name="Вместимость",
        validators=[MinValueValidator(1)]
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='free',
        verbose_name="Статус"
    )
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tables',
        verbose_name="Обслуживающий официант"
    )
    
    def __str__(self):
        return f"Стол №{self.table_number}"
    
    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"


class Order(models.Model):
    STATUS_CHOICES = [
        ('received', 'Принят'),
        ('cooking', 'Готовится'),
        ('ready', 'Готов'),
        ('served', 'Выдан'),
        ('paid', 'Оплачен'),
    ]
    
    table = models.ForeignKey(
        Table, 
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Стол"
    )
    order_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата заказа"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='received',
        verbose_name="Статус"
    )
    comments = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Комментарии"
    )
    
    def calculate_total_price(self):
        return sum(
            detail.dish.calculate_price() * detail.quantity 
            for detail in self.order_details.all()
        )
    
    def __str__(self):
        return f"Заказ №{self.id} - Стол {self.table.table_number}"
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE,
        related_name='order_details',
        verbose_name="Заказ"
    )
    dish = models.ForeignKey(
        Dish, 
        on_delete=models.CASCADE,
        related_name='dish_orders',
        verbose_name="Блюдо"
    )
    quantity = models.IntegerField(
        default=1,
        verbose_name="Количество",
        validators=[MinValueValidator(1)]
    )
    special_requests = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Особые пожелания"
    )
    
    def __str__(self):
        return f"{self.dish.name} x{self.quantity}"
    
    class Meta:
        verbose_name = "Деталь заказа"
        verbose_name_plural = "Детали заказа"


class ChefDish(models.Model):
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE,
        related_name='chef_dishes',
        verbose_name="Повар"
    )
    dish = models.ForeignKey(
        Dish, 
        on_delete=models.CASCADE,
        related_name='dish_chefs',
        verbose_name="Блюдо"
    )
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.dish.name}"
    
    class Meta:
        verbose_name = "Блюдо повара"
        verbose_name_plural = "Блюда поваров"
        unique_together = ['employee', 'dish']
