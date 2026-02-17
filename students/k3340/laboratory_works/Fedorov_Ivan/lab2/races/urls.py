from django.urls import path
from . import views

urlpatterns = [
    path('', views.race_list, name='race_list'),
    path('race/<int:race_id>/', views.race_detail, name='race_detail'),
    path('race/<int:race_id>/register/', views.register_for_race, name='register_for_race'),
    path('race/<int:race_id>/unregister/', views.unregister_from_race, name='unregister_from_race'),
]