from django.urls import path
from . import views

urlpatterns = [
    # Главная страница со списком всех владельцев
    path('', views.owner_list, name='owner_list'),
    
    # ========== ФУНКЦИОНАЛЬНЫЕ ПРЕДСТАВЛЕНИЯ ДЛЯ ВЛАДЕЛЬЦЕВ ==========
    # URL для просмотра информации о владельце
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    # URL для создания нового владельца
    path('owner/create/', views.owner_create, name='owner_create'),
    
    # ========== КЛАССОВЫЕ ПРЕДСТАВЛЕНИЯ ДЛЯ АВТОМОБИЛЕЙ ==========
    # Список всех автомобилей
    path('avtomobil/', views.AvtomobilListView.as_view(), name='avtomobil_list'),
    # Детальная информация об автомобиле
    path('avtomobil/<int:avtomobil_id>/', views.AvtomobilDetailView.as_view(), name='avtomobil_detail'),
    # Создание нового автомобиля
    path('avtomobil/create/', views.AvtomobilCreateView.as_view(), name='avtomobil_create'),
    # Редактирование автомобиля
    path('avtomobil/<int:avtomobil_id>/update/', views.AvtomobilUpdateView.as_view(), name='avtomobil_update'),
    # Удаление автомобиля
    path('avtomobil/<int:avtomobil_id>/delete/', views.AvtomobilDeleteView.as_view(), name='avtomobil_delete'),
]

