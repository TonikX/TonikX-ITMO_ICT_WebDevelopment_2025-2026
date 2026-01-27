from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Position, Employee, Ingredient, Dish, Table, Order, ChefDish
from .serializers import (
    PositionSerializer, EmployeeSerializer, IngredientSerializer,
    DishSerializer, TableSerializer, OrderSerializer, ChefDishSerializer,
    OrderCreateSerializer
)


class PositionListCreateView(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.select_related('position').all()
    serializer_class = EmployeeSerializer


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.select_related('position').all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class IngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def low_stock_ingredients(request):
    ingredients = Ingredient.objects.all()
    low_stock = [ing for ing in ingredients if ing.is_low_on_stock()]
    serializer = IngredientSerializer(low_stock, many=True)
    return Response(serializer.data)


class DishListCreateView(generics.ListCreateAPIView):
    queryset = Dish.objects.prefetch_related('dish_ingredients__ingredient').all()
    serializer_class = DishSerializer


class DishDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dish.objects.prefetch_related('dish_ingredients__ingredient').all()
    serializer_class = DishSerializer


class TableListCreateView(generics.ListCreateAPIView):
    queryset = Table.objects.select_related('employee').all()
    serializer_class = TableSerializer


class TableDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.select_related('employee').all()
    serializer_class = TableSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_table_status(request, pk):
    table = get_object_or_404(Table, pk=pk)
    new_status = request.data.get('status')
    
    if new_status in ['free', 'occupied']:
        table.status = new_status
        table.save()
        serializer = TableSerializer(table)
        return Response(serializer.data)
    
    return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.select_related('table').prefetch_related('order_details__dish').all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.select_related('table').prefetch_related('order_details__dish').all()
    serializer_class = OrderSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    new_status = request.data.get('status')
    
    valid_statuses = ['received', 'cooking', 'ready', 'served', 'paid']
    if new_status in valid_statuses:
        order.status = new_status
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


class ChefDishListCreateView(generics.ListCreateAPIView):
    queryset = ChefDish.objects.select_related('employee', 'dish').all()
    serializer_class = ChefDishSerializer


class ChefDishDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChefDish.objects.select_related('employee', 'dish').all()
    serializer_class = ChefDishSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chef_available_dishes(request, chef_id):
    chef = get_object_or_404(Employee, pk=chef_id, category__in=['chef', 'cook'])
    dishes = Dish.objects.filter(dish_chefs__employee=chef).prefetch_related('dish_ingredients__ingredient')
    serializer = DishSerializer(dishes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def orders_by_status(request, order_status):
    valid_statuses = ['received', 'cooking', 'ready', 'served', 'paid']
    if order_status not in valid_statuses:
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    
    orders = Order.objects.filter(status=order_status).select_related('table').prefetch_related('order_details__dish')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
