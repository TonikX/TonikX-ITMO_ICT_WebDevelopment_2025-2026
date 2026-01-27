from rest_framework import serializers
from .models import (
    Position, Employee, Ingredient, Dish, DishIngredient,
    Table, Order, OrderDetail, ChefDish
)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    position_name = serializers.CharField(source='position.position', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Employee
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    ingredient_type_display = serializers.CharField(source='get_ingredient_type_display', read_only=True)
    is_low_stock = serializers.BooleanField(source='is_low_on_stock', read_only=True)
    
    class Meta:
        model = Ingredient
        fields = '__all__'


class DishIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)
    ingredient_price = serializers.DecimalField(source='ingredient.price_per_unit', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = DishIngredient
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    dish_type_display = serializers.CharField(source='get_dish_type_display', read_only=True)
    ingredients_info = DishIngredientSerializer(source='dish_ingredients', many=True, read_only=True)
    calculated_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Dish
        fields = '__all__'
    
    def get_calculated_price(self, obj):
        return obj.calculate_price()


class TableSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    waiter_name = serializers.CharField(source='employee.full_name', read_only=True)
    
    class Meta:
        model = Table
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    dish_name = serializers.CharField(source='dish.name', read_only=True)
    dish_price = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderDetail
        fields = '__all__'
    
    def get_dish_price(self, obj):
        return obj.dish.calculate_price()


class OrderSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    table_number = serializers.IntegerField(source='table.table_number', read_only=True)
    order_details = OrderDetailSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = '__all__'
    
    def get_total_price(self, obj):
        return obj.calculate_total_price()


class ChefDishSerializer(serializers.ModelSerializer):
    chef_name = serializers.CharField(source='employee.full_name', read_only=True)
    dish_name = serializers.CharField(source='dish.name', read_only=True)
    
    class Meta:
        model = ChefDish
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['table', 'comments', 'order_details']
    
    def create(self, validated_data):
        order_details_data = validated_data.pop('order_details')
        order = Order.objects.create(**validated_data)
        
        for detail_data in order_details_data:
            OrderDetail.objects.create(order=order, **detail_data)
        
        return order
    