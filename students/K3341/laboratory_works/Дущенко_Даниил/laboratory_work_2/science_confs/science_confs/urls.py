from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    
    # Auth
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # Logic
    path('conf/<int:pk>/', views.conference_detail, name='conference_detail'),
    path('conf/<int:pk>/join/', views.participate, name='participate'),
    path('part/edit/<int:pk>/', views.edit_participation, name='edit_part'),
    path('part/del/<int:pk>/', views.delete_participation, name='del_part'),
]