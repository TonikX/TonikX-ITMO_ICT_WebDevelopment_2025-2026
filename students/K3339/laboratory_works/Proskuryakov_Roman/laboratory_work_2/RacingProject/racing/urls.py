from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'racing'

urlpatterns = [
    path('', views.races_list, name='races_list'),
    path('accounts/login/', views.index, name='index'),
    path('login/', views.AppLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='racing:races_list'), name='logout'),
    path('register/', views.register, name='register'),
    path('participant/create/', views.participant_create, name='participant_create'),
    path('participant/edit/', views.participant_edit, name='participant_edit'),
    path('car/create/', views.car_create, name='car_create'),
    path('team/create/', views.team_create, name='team_create'),
    path('races/', views.races_list, name='races_list'),
    path("races/create/", views.race_create, name="race_create"),
    path('races/<int:pk>/', views.race_detail, name='race_detail'),
    path('races/<int:race_pk>/register/', views.race_register, name='race_register'),
    path('races/<int:race_pk>/toggle-registration/', views.race_unregister, name='race_unregister'),
    path('races/<int:race_pk>/comment/', views.add_comment, name='add_comment'),
    path('races/<int:race_pk>/race_session_create/', views.race_session_create, name='race_session_create'),
    path('races/<int:race_pk>/sessions/<int:session_pk>/result/add', views.add_result, name='add_result'),
]