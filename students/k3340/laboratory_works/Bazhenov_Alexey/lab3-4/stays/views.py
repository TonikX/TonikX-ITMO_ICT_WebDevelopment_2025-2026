from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.utils import parse_date_param
from .models import Stay
from .serializers import StaySerializer


class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.select_related('client', 'room')
    serializer_class = StaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'room', 'status']

    def get_queryset(self):
        queryset = super().get_queryset()
        room_number = self.request.query_params.get('room_number')
        if room_number:
            queryset = queryset.filter(room__number=room_number)
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.status = Stay.Status.ACTIVE
        instance.save()

    @action(detail=True, methods=['post'], url_path='checkout')
    def checkout(self, request, pk=None):
        stay = self.get_object()
        check_out_value = request.data.get('check_out')
        if not check_out_value:
            return Response({'detail': 'Укажите дату check_out.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            checkout_date = parse_date_param(check_out_value, 'check_out')
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        stay.close(checkout_date)
        stay.save()
        return Response(self.get_serializer(stay).data)
