from django.contrib import admin
from django.urls import path, include
from projects import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('homeworks/', views.homework_list, name='homework_list'),
    path('homeworks/<int:pk>/', views.homework_detail, name='homework_detail'),
    path('my-grades/', views.my_grades, name='my_grades'),
    path('class-grades/', views.my_class_grades, name='class_grades'),
]
