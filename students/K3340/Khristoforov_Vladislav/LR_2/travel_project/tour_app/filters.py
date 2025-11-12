import django_filters
from django.db import models 
from django import forms
from .models import Tour, Booking

class TourFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search',
        label='Поиск'
    )
    country = django_filters.CharFilter(
        field_name='country',
        lookup_expr='icontains',
        label='Страна'
    )
    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Минимальная цена'
    )
    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Максимальная цена'
    )

    class Meta:
        model = Tour
        fields = ['country', 'agency']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(country__icontains=value) |
            models.Q(agency__icontains=value)
        )
    
class BookingFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search',
        label='Поиск'
    )
    status = django_filters.ChoiceFilter(
        choices=Booking.STATUS_CHOICES,
        label='Статус'
    )
    country = django_filters.CharFilter(
        field_name='tour__country',
        lookup_expr='icontains',
        label='Страна'
    )
    date_after = django_filters.DateFilter(
        field_name='booking_date',
        lookup_expr='gte',
        label='Дата от'
    )
    date_before = django_filters.DateFilter(
        field_name='booking_date', 
        lookup_expr='lte',
        label='Дата до'
    )

    class Meta:
        model = Booking
        fields = ['status']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(user__username__icontains=value) |
            models.Q(user__first_name__icontains=value) |
            models.Q(user__last_name__icontains=value) |
            models.Q(tour__title__icontains=value) |
            models.Q(tour__country__icontains=value) |
            models.Q(tour__agency__icontains=value)
        )