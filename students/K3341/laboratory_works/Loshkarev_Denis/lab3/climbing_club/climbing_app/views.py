from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Count, Q
from .models import Alpinist, Mountain, Climb, Participation
from .serializers import AlpinistSerializer, MountainSerializer, ClimbSerializer, ClimbCreateSerializer


class AlpinistListCreateView(generics.ListCreateAPIView):
    queryset = Alpinist.objects.all()
    serializer_class = AlpinistSerializer

class MountainListCreateView(generics.ListCreateAPIView):
    queryset = Mountain.objects.all()
    serializer_class = MountainSerializer
    permission_classes = [IsAuthenticated] 


# 1. Список альпинистов, осуществлявших восхождение в интервал дат
@extend_schema(
    parameters=[
        OpenApiParameter(name='start', description='Дата начала (ГГГГ-ММ-ДД)', required=True, type=str),
        OpenApiParameter(name='end', description='Дата окончания (ГГГГ-ММ-ДД)', required=True, type=str),
    ],
    description="Показать список альпинистов, осуществлявших восхождение в указанный интервал дат."
)
class AlpinistsInDateRangeView(generics.ListAPIView):
    serializer_class = AlpinistSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start')
        end_date = self.request.query_params.get('end')
        if start_date and end_date:
            return Alpinist.objects.filter(
                participations__climb__start_actual__range=[start_date, end_date]
            ).distinct()
        return Alpinist.objects.none()

# 2. Список восхождений (групп) за указанный период времени
@extend_schema(
    parameters=[
        OpenApiParameter(name='start', description='Дата начала (ГГГГ-ММ-ДД)', required=True, type=str),
        OpenApiParameter(name='end', description='Дата окончания (ГГГГ-ММ-ДД)', required=True, type=str),
    ],
    description="Показать список восхождений (групп), которые осуществлялись в указанный период времени."
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

# 3. Сколько альпинистов побывали на каждой горе 
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

# 4. Вершины, на которых не было восхождений
class UnclimbedMountainsView(generics.ListAPIView):
    serializer_class = MountainSerializer
    queryset = Mountain.objects.filter(routes__climbs__isnull=True)

# 5. Количество восхождений каждого альпиниста на каждую гору
class AlpinistMountainClimbsView(APIView):
    @extend_schema(
        responses={200: serializers.ListSerializer(child=serializers.DictField())},
        description="Информация о количестве восхождений каждого альпиниста на каждую гору."
    )
    def get(self, request):
        stats = Participation.objects.values(
            'alpinist__name', 'climb__route__mountain__name'
        ).annotate(count=Count('id'))
        return Response(stats)

class MountainReportView(APIView):
    """
    Отчет: для каждой горы список групп в заданный период + количество участников.
    Итоговое значение по всему отчету.
    """
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
        mountains = Mountain.objects.all()

        for mtn in mountains:
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
                        "members_count": cl.members_count
                    })
                    total_participants_in_report += cl.members_count
                
                report_data.append({
                    "mountain": mtn.name,
                    "height": mtn.height,
                    "groups": mountain_groups
                })

        return Response({
            "period": {"from": start_date, "to": end_date},
            "mountains": report_data,
            "grand_total_participants": total_participants_in_report
        })


class ClimbCreateView(generics.CreateAPIView):
    """Создание нового восхождения с участниками"""
    queryset = Climb.objects.all()
    serializer_class = ClimbCreateSerializer
    permission_classes = [IsAuthenticated] # Только авторизованные