from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation, GuestStay


@receiver(post_save, sender=Reservation)
def create_guest_stay(sender, instance, created, **kwargs):
    # автоматически создает запись GuestStay при создании бронирования
    if created:
        GuestStay.create_for_reservation(instance)