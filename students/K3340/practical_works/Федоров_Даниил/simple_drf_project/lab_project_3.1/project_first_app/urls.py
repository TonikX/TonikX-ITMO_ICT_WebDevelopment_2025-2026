from django.urls import path
from . import views

urlpatterns = [
    path('owner/<int:owner_id>', views.owner_information),
    path('owners/', views.all_owners, name='owners_list'),
    path('cars/', views.all_cars.as_view(), name='cars'),
    path('car/<int:pk>', views.one_car.as_view()),
    path('owner_form/', views.create_owner),
    path('car/<int:pk>/update', views.update_car.as_view()),
    path('car/add/', views.add_car.as_view()),
    path('car/<int:pk>/delete/', views.delete_car.as_view()),

]