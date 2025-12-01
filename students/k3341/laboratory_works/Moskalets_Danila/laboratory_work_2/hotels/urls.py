from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('room-type/<int:room_type_id>/', views.room_type_detail, name='room_type_detail'),
    path('reserve/<int:room_type_id>/', views.make_reservation, name='make_reservation'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('edit-reservation/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('delete-reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('add-review/<int:reservation_id>/', views.add_review, name='add_review'),
    path('login/', auth_views.LoginView.as_view(template_name='hotels/login.html', next_page='home'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('guests/', views.guest_list, name='guest_list'),
]