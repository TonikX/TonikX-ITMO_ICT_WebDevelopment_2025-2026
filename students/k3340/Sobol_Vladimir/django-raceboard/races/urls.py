from django.urls import path
from . import views

app_name = "races"

urlpatterns = [
    path('', views.RaceListView.as_view(), name='race_list'),
    path('<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),

    path('register/', views.register, name='user_register'),
    path('profile/', views.profile, name='profile'),

    path('<int:pk>/register/', views.create_registration, name='create_registration'),
    path('registrations/<int:pk>/delete/', views.delete_registration, name='delete_registration'),

    path('<int:pk>/comment/', views.create_comment, name='create_comment'),
]
