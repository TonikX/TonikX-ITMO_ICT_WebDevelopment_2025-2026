from django.contrib import admin
from .models import (
    Position, Employee, Ingredient, Dish, 
    DishIngredient, Table, Order, OrderDetail, ChefDish
)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['position', 'minimum_wage']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'category', 'position', 'salary']
    list_filter = ['category', 'position']
    search_fields = ['full_name']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'ingredient_type', 'stock_quantity', 'minimum_stock', 'price_per_unit']
    list_filter = ['ingredient_type']
    search_fields = ['name', 'supplier']


class DishIngredientInline(admin.TabularInline):
    model = DishIngredient
    extra = 1


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'dish_type']
    list_filter = ['dish_type']
    search_fields = ['name']
    inlines = [DishIngredientInline]


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['table_number', 'capacity', 'status', 'employee']
    list_filter = ['status', 'capacity']


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'table', 'status', 'order_date']
    list_filter = ['status', 'order_date']
    inlines = [OrderDetailInline]


@admin.register(ChefDish)
class ChefDishAdmin(admin.ModelAdmin):
    list_display = ['employee', 'dish']
    list_filter = ['employee__category']
