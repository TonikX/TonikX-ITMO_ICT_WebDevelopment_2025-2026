from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.utils import ensure_period
from stays.models import Stay
from stays.serializers import StaySerializer
from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city']

    @action(detail=False, methods=['get'], url_path='count-by-city')
    def count_by_city(self, request):
        city = request.query_params.get('city')
        if not city:
            return Response({'detail': 'Необходимо указать параметр city.'}, status=status.HTTP_400_BAD_REQUEST)
        count = Client.objects.filter(city__iexact=city).count()
        return Response({'city': city, 'count': count})

    @action(detail=True, methods=['get'])
    def stays(self, request, pk=None):
        client = self.get_object()
        serializer = StaySerializer(client.stays.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='overlaps')
    def overlapping_clients(self, request, pk=None):
        client = self.get_object()
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        try:
            start_date, end_date = ensure_period(start, end)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        target_stays = client.stays.filter(
            Q(check_out__isnull=True) | Q(check_out__gte=start_date)
        ).filter(check_in__lte=end_date)

        if not target_stays.exists():
            return Response([], status=status.HTTP_200_OK)

        overlapping_clients = Client.objects.filter(
            stays__room__in=target_stays.values('room_id'),
            stays__check_in__lte=end_date,
        ).filter(
            Q(stays__check_out__isnull=True) | Q(stays__check_out__gte=start_date)
        ).exclude(id=client.id).distinct()

        serializer = ClientSerializer(overlapping_clients, many=True)
        return Response(serializer.data)
