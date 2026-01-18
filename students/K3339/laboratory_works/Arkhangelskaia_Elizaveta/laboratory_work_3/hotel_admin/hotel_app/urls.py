from django.urls import path
from .views import *


app_name = "hotel_app"

urlpatterns = [
   path('residents/', ResidentsListCreateAPIView.as_view()),
   path('residents/<int:pk>/', ResidentsRetrieveUpdateDestroyAPIView.as_view()),
   path('rooms/', RoomsListCreateAPIView.as_view()),
   path('rooms/<int:pk>/', RoomsRetrieveUpdateDestroyAPIView.as_view()),
   path('room_types/', RoomTypeListCreateAPIView.as_view()),
   path('room_types/<int:pk>/', RoomTypeRetrieveUpdateDestroyAPIView.as_view()),
   path('reservations/', ReservationsListCreateAPIView.as_view()),
   path('reservations/<int:pk>/', ReservationsRetrieveUpdateDestroyAPIView.as_view()),
   path('workers/', WorkersListCreateAPIView.as_view()),
   path('workers/<int:pk>/', WorkersRetrieveUpdateDestroyAPIView.as_view()),
   path('cleaning_info/', CleaningInformationListCreateAPIView.as_view()),
   path('cleaning_info/<int:pk>/', CleaningInformationRetrieveUpdateDestroyAPIView.as_view()),
   path('cleaning/', CleaningListCreateAPIView.as_view()),
   path('cleaning/<int:pk>/', CleaningRetrieveUpdateDestroyAPIView.as_view()),


   path('req/clients/',  ResidentsAPIView.as_view()),
   path('req/from_city/', CityAPIView.as_view()),
   path('req/available_rooms/', AvailableRoomsAPIView.as_view()),
   path('req/clients_with_city/', ClientsAPIView.as_view()),
   path('req/report/', ReportAPIView.as_view()),
   path('req/cleaing_staff/', CleaningStaffAPIView.as_view()),
]


