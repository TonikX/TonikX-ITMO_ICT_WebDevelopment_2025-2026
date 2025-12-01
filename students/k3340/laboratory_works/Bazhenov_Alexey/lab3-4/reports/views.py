from datetime import date

from django.db.models import Count, Sum, Q
from rest_framework import status, views
from rest_framework.response import Response

from rooms.models import Room
from stays.models import Stay


def quarter_boundaries(year: int, quarter: int) -> tuple[date, date]:
    if quarter not in {1, 2, 3, 4}:
        raise ValueError('Квартал должен быть числом от 1 до 4.')
    start_month = (quarter - 1) * 3 + 1
    start = date(year, start_month, 1)
    if quarter == 4:
        end = date(year + 1, 1, 1) - date.resolution
    else:
        end_month = start_month + 3
        end = date(year, end_month, 1) - date.resolution
    return start, end


class QuarterlyReportView(views.APIView):
    def get(self, request):
        quarter = request.query_params.get('quarter')
        year = request.query_params.get('year')
        if not quarter or not year:
            return Response({'detail': 'Нужно указать quarter и year.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            quarter = int(quarter)
            year = int(year)
            start, end = quarter_boundaries(year, quarter)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        stays_in_period = Stay.objects.filter(
            check_in__lte=end,
        ).filter(
            Q(check_out__isnull=True) | Q(check_out__gte=start)
        )

        clients_per_room = stays_in_period.values('room__id', 'room__number').annotate(
            client_count=Count('client', distinct=True),
        ).order_by('room__number')

        rooms_per_floor = Room.objects.values('floor').annotate(room_count=Count('id')).order_by('floor')

        income_qs = Stay.objects.filter(
            status=Stay.Status.COMPLETED,
            check_out__range=(start, end),
        ).values('room__id', 'room__number').annotate(total_income=Sum('total_cost')).order_by('room__number')
        total_income = sum(item['total_income'] or 0 for item in income_qs)

        response = {
            'period': {
                'quarter': quarter,
                'year': year,
                'start': start,
                'end': end,
            },
            'clients_per_room': list(clients_per_room),
            'rooms_per_floor': list(rooms_per_floor),
            'income_per_room': list(income_qs),
            'total_income': total_income,
        }
        return Response(response)
