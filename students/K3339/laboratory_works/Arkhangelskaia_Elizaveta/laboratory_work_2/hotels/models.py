from django.db import models
from django.contrib.auth.models import AbstractUser


class Hotel(models.Model):
    name = models.CharField(max_length=100, null=False)
    owner = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500, null=False)
    capacity = models.IntegerField(null=False)


class HotelUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)


class RoomType(models.Model):
    id_hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=30, null=False)
    price = models.IntegerField(null=False)
    capacity = models.IntegerField(null=False)
    count = models.IntegerField(null=True)


class Facility(models.Model):
    id_room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    facility = models.CharField(max_length=30, null=False)


class Reservation(models.Model):
    id_user = models.ForeignKey(HotelUser, on_delete=models.CASCADE)
    id_rooms = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    reservation_date = models.DateField(null=False)

class Review(models.Model):
    id_reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False)
    review_text = models.CharField(max_length=500, null=False)

