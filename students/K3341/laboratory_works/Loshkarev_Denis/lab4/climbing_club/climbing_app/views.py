from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Count
from .models import Alpinist, Mountain, Climb, Participation, Club, Route
from .serializers import (
    AlpinistSerializer, MountainSerializer, ClimbSerializer,
    ClubSerializer, ClimbCreateSerializer, RouteSerializer,
)


class AlpinistListCreateView(generics.ListCreateAPIView):
    queryset = Alpinist.objects.prefetch_related('clubs').all()
    serializer_class = AlpinistSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'address', 'clubs__name']


class MountainListCreateView(generics.ListCreateAPIView):
    queryset = Mountain.objects.all()
    serializer_class = MountainSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['id', 'name', 'height', 'country', 'region']
    search_fields = ['name', 'country', 'region']


class ClubListCreateView(generics.ListCreateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'country', 'city', 'contact_person']


class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.select_related('mountain').all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]


class RecentClimbsView(generics.ListAPIView):
    serializer_class = ClimbSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Climb.objects.select_related(
            'route__mountain'
        ).order_by('-id')[:10]


class ClimbListView(generics.ListAPIView):
    serializer_class = ClimbSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['group_name', 'route__mountain__name']

    def get_queryset(self):
        return Climb.objects.select_related(
            'route__mountain'
        ).prefetch_related(
            'details__alpinist'
        ).order_by('-id')


@extend_schema(
    parameters=[
        OpenApiParameter(name='start', description='Дата начала (ГГГГ-ММ-ДД)', required=True, type=str),
        OpenApiParameter(name='end', description='Дата окончания (ГГГГ-ММ-ДД)', required=True, type=str),
    ],
    description="Список альпинистов, осуществлявших восхождение в указанный интервал дат."
)
class AlpinistsInDateRangeView(generics.ListAPIView):
    serializer_class = AlpinistSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start')
        end_date = self.request.query_params.get('end')
        if start_date and end_date:
            return Alpinist.objects.prefetch_related('clubs').filter(
                participations__climb__start_actual__range=[start_date, end_date]
            ).distinct()
        return Alpinist.objects.none()


@extend_schema(
    parameters=[
        OpenApiParameter(name='start', description='Дата начала (ГГГГ-ММ-ДД)', required=True, type=str),
        OpenApiParameter(name='end', description='Дата окончания (ГГГГ-ММ-ДД)', required=True, type=str),
    ],
    description="Список восхождений (групп), которые осуществлялись в указанный период времени."
)
class ClimbListByPeriodView(generics.ListAPIView):
    serializer_class = ClimbSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start')
        end_date = self.request.query_params.get('end')
        if start_date and end_date:
            return Climb.objects.filter(
                start_actual__range=[start_date, end_date]
            ).order_by('start_actual')
        return Climb.objects.none()


class MountainStatsView(APIView):
    @extend_schema(
        responses={200: serializers.ListSerializer(child=serializers.DictField())},
        description="Статистика: сколько уникальных альпинистов побывали на каждой горе."
    )
    def get(self, request):
        stats = Mountain.objects.annotate(
            climbers_count=Count('routes__climbs__participants', distinct=True)
        ).values('name', 'climbers_count')
        return Response(stats)


class UnclimbedMountainsView(generics.ListAPIView):
    serializer_class = MountainSerializer

    def get_queryset(self):
        climbed_ids = Mountain.objects.filter(
            routes__climbs__isnull=False
        ).values_list('id', flat=True).distinct()
        return Mountain.objects.exclude(id__in=climbed_ids)


class AlpinistMountainClimbsView(APIView):
    @extend_schema(
        responses={200: serializers.ListSerializer(child=serializers.DictField())},
        description="Количество восхождений каждого альпиниста на каждую гору."
    )
    def get(self, request):
        stats = Participation.objects.values(
            'alpinist__name', 'climb__route__mountain__name'
        ).annotate(count=Count('id'))
        return Response(stats)


class MountainReportView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name='start', description='Дата начала (ГГГГ-ММ-ДД)', required=True, type=str),
            OpenApiParameter(name='end', description='Дата окончания (ГГГГ-ММ-ДД)', required=True, type=str),
        ],
        responses={200: dict}
    )
    def get(self, request):
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')
        if not start_date or not end_date:
            return Response({"error": "Укажите параметры start и end (ГГГГ-ММ-ДД)"}, status=400)

        report_data = []
        total_participants_in_report = 0

        for mtn in Mountain.objects.all():
            climbs = Climb.objects.filter(
                route__mountain=mtn,
                start_actual__range=[start_date, end_date]
            ).annotate(members_count=Count('participants')).order_by('start_actual')

            if climbs.exists():
                mountain_groups = []
                for cl in climbs:
                    mountain_groups.append({
                        "group_name": cl.group_name,
                        "date": cl.start_actual.strftime('%Y-%m-%d'),
                        "members_count": cl.members_count,
                    })
                    total_participants_in_report += cl.members_count
                report_data.append({
                    "mountain": mtn.name,
                    "height": mtn.height,
                    "groups": mountain_groups,
                })

        return Response({
            "period": {"from": start_date, "to": end_date},
            "mountains": report_data,
            "grand_total_participants": total_participants_in_report,
        })


class ClimbCreateView(generics.CreateAPIView):
    queryset = Climb.objects.all()
    serializer_class = ClimbCreateSerializer
    permission_classes = [IsAuthenticated]


class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.select_related('mountain').all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['mountain__name', 'description'] 