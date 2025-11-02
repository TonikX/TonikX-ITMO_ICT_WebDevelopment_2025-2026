from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Доступно без авторизации
    path('', views.HotelListView.as_view(), name='hotel_list'),
    path('hotel/<int:pk>/', views.HotelDetailView.as_view(), name='hotel_detail'),
    path('room-type/<int:pk>/', views.RoomTypeDetailView.as_view(), name='room_type_detail'),
    
    # Авторизация и выход
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Только для авторизованных
    path('reservation/<int:room_type_id>/', views.MakeReservationView.as_view(), name='make_reservation'),
    path('my-reservations/', views.MyReservationsListView.as_view(), name='my_reservations'),
    path('reservation/edit/<int:pk>/', views.EditReservationView.as_view(), name='edit_reservation'),
    path('reservation/delete/<int:pk>/', views.DeleteReservationView.as_view(), name='delete_reservation'),
    path('review/<int:reservation_id>/', views.AddReviewView.as_view(), name='add_review'),

    # Только для персонала
    path('guests-last-month/', views.GuestsLastMonthView.as_view(), name='guests_last_month')
]