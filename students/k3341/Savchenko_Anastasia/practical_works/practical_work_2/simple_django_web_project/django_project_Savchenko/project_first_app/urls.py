from django.urls import path
from . import views

# импорт наши классовые представления
from .views import CarListView, CarDetailView, CarUpdateView, CarCreateView, CarDeleteView
# список всех URL-адресов приложения
urlpatterns = [
    # СТАРЫЕ URL (функциональные представления)

    # детальная информация о владельце по id
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),

    # список всех владельцев
    path('owners/', views.owner_list, name='owner_list'),

    # пример из задания - вывод времени
    path('time/', views.example_view, name='example_view'),

    # главная страница - показывает список владельцев
    path('', views.owner_list, name='home'),

    # НОВЫЕ URL (классовые представления для автомобилей)

    # список всех автомобилей
    path('cars/', CarListView.as_view(), name='car_list'),

    # детальная информация об автомобиле по id (pk - primary key)
    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),

    # форма редактирования автомобиля по id
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),

    # НОВЫЕ URL (классовые представления для автомобилей)

    # список всех автомобилей
    path('cars/', CarListView.as_view(), name='car_list'),

    # детальная информация об автомобиле по id (pk - primary key)
    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),

    # форма редактирования автомобиля по id
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),

    # форма создания нового автомобиля
    path('car/create/', CarCreateView.as_view(), name='car_create'),

    # подтверждение удаления автомобиля
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),

    # форма для создания нового владельца (функциональное представление)
    path('owner/create/', views.create_owner, name='owner_create'),
]