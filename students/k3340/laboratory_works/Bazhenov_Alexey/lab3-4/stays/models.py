from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class StayQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=Stay.Status.ACTIVE)


class Stay(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Проживает'
        COMPLETED = 'completed', 'Выселен'

    client = models.ForeignKey('clients.Client', related_name='stays', on_delete=models.CASCADE)
    room = models.ForeignKey('rooms.Room', related_name='stays', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StayQuerySet.as_manager()

    class Meta:
        ordering = ['-check_in']
        verbose_name = 'Проживание'
        verbose_name_plural = 'Проживания'
        constraints = [
            models.UniqueConstraint(
                fields=['client', 'status'],
                condition=models.Q(status='active'),
                name='unique_active_stay_per_client',
            )
        ]

    def __str__(self) -> str:
        return f'{self.client.full_name} — {self.room.number}'

    def clean(self):
        if self.check_out and self.check_out <= self.check_in:
            raise ValidationError('Дата выезда должна быть позже даты заселения.')
        if self.room_id:
            overlapping = self._count_overlapping_stays()
            if overlapping >= self.room.capacity:
                raise ValidationError('В выбранном номере нет свободных мест на указанные даты.')

    def _count_overlapping_stays(self) -> int:
        end_date = self.check_out or date.max
        qs = Stay.objects.filter(room=self.room).exclude(pk=self.pk)
        qs = qs.filter(
            models.Q(check_out__isnull=True) | models.Q(check_out__gt=self.check_in)
        ).filter(check_in__lt=end_date)
        return qs.count()

    @property
    def nights(self) -> int:
        if not self.check_out:
            return 0
        return (self.check_out - self.check_in).days

    def close(self, checkout_date: date):
        if checkout_date <= self.check_in:
            raise ValidationError('Дата выезда должна быть позже заселения.')
        self.check_out = checkout_date
        self.status = self.Status.COMPLETED
        nights = (checkout_date - self.check_in).days
        nights = max(nights, 1)
        self.total_cost = Decimal(nights) * self.room.daily_rate
