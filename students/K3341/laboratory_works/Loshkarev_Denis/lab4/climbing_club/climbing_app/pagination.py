from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class FlexiblePageNumberPagination(PageNumberPagination):
    '''отключение пагинации при ?page_size=all'''
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def paginate_queryset(self, queryset, request, view=None):
        if request.query_params.get(self.page_size_query_param) == 'all':
            return None 
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })