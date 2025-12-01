from django.db import models


class Client(models.Model):
    passport_number = models.CharField(max_length=32, unique=True)
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=128)
    phone = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name}'

    @property
    def full_name(self) -> str:
        return ' '.join(filter(None, [self.last_name, self.first_name, self.middle_name]))
