from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from .tours import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  
    path('tours/', views.tour_list, name='tour_list'), 
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tours/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('reserve/<int:tour_id>/', views.reserve_tour, name='reserve_tour'),
    path('review/<int:tour_id>/', views.submit_review, name='submit_review'),
    path('sold-tours/', views.sold_tours_by_country, name='sold_tours_by_country'),
    path('reservation/edit/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('reservation/delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
]