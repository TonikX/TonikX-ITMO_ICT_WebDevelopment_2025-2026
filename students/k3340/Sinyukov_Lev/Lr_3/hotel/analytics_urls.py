from django.urls import path
from .analytics import clients_in_room_period
from .analytics import clients_from_city
from .analytics import who_cleaned_client_room
from .analytics import free_rooms_count
from .analytics import clients_overlap


urlpatterns = [
    path("clients-in-room/", clients_in_room_period, name="clients_in_room_period"),
    path("clients-in-room/", clients_in_room_period),
    path("clients-from-city/", clients_from_city),
    path("who-cleaned-client-room/", who_cleaned_client_room),
    path("free-rooms/", free_rooms_count),
    path("clients-overlap/", clients_overlap),
]