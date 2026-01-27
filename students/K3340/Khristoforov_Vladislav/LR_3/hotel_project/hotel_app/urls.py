from django.urls import path
from .views import *

urlpatterns = [
    # Справочники
    path('room-types/', RoomTypeList.as_view()),
    path('cities/', CityList.as_view()),
    
    # Основные
    path('rooms/', RoomList.as_view()),
    path('rooms/<int:pk>/', RoomDetail.as_view()),
    path('guests/', GuestList.as_view()),
    path('guests/<int:pk>/', GuestDetail.as_view()),
    path('employees/', EmployeeList.as_view()),
    
    # Операции
    path('bookings/', BookingList.as_view()),
    path('bookings/<int:pk>/', BookingDetail.as_view()),
    path('schedules/', CleaningScheduleList.as_view()),
]
