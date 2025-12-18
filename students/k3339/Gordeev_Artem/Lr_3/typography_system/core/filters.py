from django_filters import rest_framework as filters

from .models import Book


class BookFilter(filters.FilterSet):
    # Поиск по частичному совпадению имени автора
    author = filters.CharFilter(field_name='authors__full_name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['author', 'has_illustrations', 'isbn']
