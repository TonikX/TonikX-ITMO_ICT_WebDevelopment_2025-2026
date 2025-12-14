from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('race/<int:race_id>/', views.race_detail, name='race_detail'),
    path('register/', views.register_user, name='register'),
    path('create-racer-profile/', views.create_racer_profile, name='create_racer_profile'),
    path('racer-profile/', views.racer_profile, name='racer_profile'),
    path('race/<int:race_id>/register/', views.register_for_race, name='register_for_race'),
    path('registration/<int:registration_id>/edit/', views.edit_registration, name='edit_registration'),
    path('registration/<int:registration_id>/delete/', views.delete_registration, name='delete_registration'),
    path('race/<int:race_id>/comment/', views.add_comment, name='add_comment'),
    path('race/<int:race_id>/results/', views.race_results, name='race_results'),
]

