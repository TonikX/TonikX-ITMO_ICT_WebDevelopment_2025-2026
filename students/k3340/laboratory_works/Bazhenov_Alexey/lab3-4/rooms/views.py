from collections import defaultdict

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.utils import ensure_period
from stays.models import Stay
from .models import Room
from .serializers import RoomSerializer, RoomStaySerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.prefetch_related('stays')
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room_type', 'floor', 'is_active']

    @action(detail=True, methods=['get'])
    def clients(self, request, pk=None):
        room = self.get_object()
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        try:
            start_date, end_date = ensure_period(start, end)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        stays = Stay.objects.filter(room=room).filter(
            Q(check_out__isnull=True) | Q(check_out__gte=start_date)
        ).filter(check_in__lte=end_date)

        serializer = RoomStaySerializer(stays, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='free-count')
    def free_count(self, request):
        data = defaultdict(int)
        total_free = 0
        rooms = Room.objects.filter(is_active=True).prefetch_related('stays')
        for room in rooms:
            occupied = room.stays.filter(status=Stay.Status.ACTIVE).count()
            free_places = room.capacity - occupied
            if free_places > 0:
                data[room.room_type] += 1
                total_free += 1
        response = {
            'total_free_rooms': total_free,
            'by_type': [
                {
                    'room_type': room_type,
                    'label': Room.RoomType(room_type).label if room_type in Room.RoomType.values else room_type,
                    'count': count,
                }
                for room_type, count in data.items()
            ],
        }
        return Response(response)
