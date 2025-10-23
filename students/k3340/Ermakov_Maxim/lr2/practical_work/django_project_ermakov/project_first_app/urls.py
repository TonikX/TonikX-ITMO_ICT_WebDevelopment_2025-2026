from django.urls import path
from .views import UserCreateView, owners_list, owner_detail, CarListView, CarDetailView, CarUpdateView, CarCreateView, CarDeleteView

urlpatterns = [
    path('owners/', owners_list, name='owners_list'),
    path('owner/<int:owner_id>/', owner_detail, name='owner_detail'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),

    # твои маршруты для cars:
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/create/', CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
]
