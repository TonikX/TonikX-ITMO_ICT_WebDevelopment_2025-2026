from django.urls import path
from . import views

app_name = 'tourism'

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('tour/<int:tour_id>/reserve/', views.make_reservation, name='make_reservation'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('reservation/<int:reservation_id>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservation/<int:reservation_id>/delete/', views.delete_reservation, name='delete_reservation'),
    path('tour/<int:tour_id>/review/', views.add_review, name='add_review'),
    path('tours-by-country/', views.tours_by_country, name='tours_by_country'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('manage/reservations/', views.admin_reservations, name='admin_reservations'),
    path('manage/reservation/<int:reservation_id>/confirm/', views.confirm_reservation, name='confirm_reservation'),
    path('manage/reservation/<int:reservation_id>/cancel/', views.cancel_reservation_admin, name='cancel_reservation_admin'),
    path('country/<str:country>/reservations/', views.reservations_by_country, name='reservations_by_country'),
]

