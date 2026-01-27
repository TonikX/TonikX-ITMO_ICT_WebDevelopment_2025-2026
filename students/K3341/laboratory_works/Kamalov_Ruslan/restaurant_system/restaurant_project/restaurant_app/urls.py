from django.urls import path
from . import views

app_name = 'restaurant_app'

urlpatterns = [
    path('positions/', views.PositionListCreateView.as_view(), name='position-list'),
    path('positions/<int:pk>/', views.PositionDetailView.as_view(), name='position-detail'),
    
    path('employees/', views.EmployeeListCreateView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    
    path('ingredients/', views.IngredientListCreateView.as_view(), name='ingredient-list'),
    path('ingredients/<int:pk>/', views.IngredientDetailView.as_view(), name='ingredient-detail'),
    path('ingredients/low-stock/', views.low_stock_ingredients, name='low-stock-ingredients'),
    
    path('dishes/', views.DishListCreateView.as_view(), name='dish-list'),
    path('dishes/<int:pk>/', views.DishDetailView.as_view(), name='dish-detail'),
    
    path('tables/', views.TableListCreateView.as_view(), name='table-list'),
    path('tables/<int:pk>/', views.TableDetailView.as_view(), name='table-detail'),
    path('tables/<int:pk>/status/', views.update_table_status, name='update-table-status'),
    
    path('orders/', views.OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', views.update_order_status, name='update-order-status'),
    path('orders/status/<str:order_status>/', views.orders_by_status, name='orders-by-status'),
    
    path('chef-dishes/', views.ChefDishListCreateView.as_view(), name='chef-dish-list'),
    path('chef-dishes/<int:pk>/', views.ChefDishDetailView.as_view(), name='chef-dish-detail'),
    path('chefs/<int:chef_id>/dishes/', views.chef_available_dishes, name='chef-available-dishes'),
]