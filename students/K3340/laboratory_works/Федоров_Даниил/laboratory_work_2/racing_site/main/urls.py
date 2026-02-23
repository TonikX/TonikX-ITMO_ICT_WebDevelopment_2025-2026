from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_function, name='root'),
    path('Hello/', views.HelloView.as_view(), name='Hello'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('races/', views.RaceListView.as_view(), name='race_list'),
    path('race/<int:pk>/delete/', views.RaceDeleteView.as_view(), name='race_delete'),
    path('race/create/', views.RaceCreateView.as_view(), name='race_create'),
    path('race/<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),
    path('racer/<int:pk>/update/', views.RacerUpdateView.as_view(), name='racer_update'),
    path('racer/<int:pk>/delete/', views.RacerDeleteView.as_view(), name='racer_delete'),
]