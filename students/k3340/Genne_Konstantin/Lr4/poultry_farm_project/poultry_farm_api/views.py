from datetime import date, timedelta
from django.utils import timezone
from statistics import mean
from django.db.models import Q, Count, Sum, Avg, Prefetch
from rest_framework import permissions, viewsets, generics, status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, 
    OpenApiExample, OpenApiResponse, OpenApiTypes
)
from drf_spectacular.types import OpenApiTypes

from poultry_farm_app.models import (
    Hen, HenEggs, Cage, HenCage,
    Employee, EmployeeCage, Breed, Diet, Employment, BreedDiet
)
from .serializers import *
from .permissions import IsDirector


@extend_schema_view(
    list=extend_schema(
        summary="Получить список пород",
        description="Возвращает список всех пород кур",
        tags=['Породы'],
        responses={200: BreedSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Получить породу",
        description="Возвращает информацию о конкретной породе",
        tags=['Породы'],
        responses={200: BreedSerializer}
    ),
    create=extend_schema(
        summary="Создать породу",
        description="Создает новую породу кур",
        tags=['Породы'],
        responses={201: BreedSerializer}
    ),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(
        summary="Частично обновить породу",
        description="Частично обновляет информацию о породе",
        tags=['Породы'],
        responses={200: BreedSerializer}
    ),
    destroy=extend_schema(
        summary="Удалить породу",
        description="Удаляет породу кур. Нельзя удалить породу, к которой привязаны куры",
        tags=['Породы'],
        responses={
            204: OpenApiResponse(description="Порода успешно удалена"),
            400: OpenApiResponse(description="Нельзя удалить породу, к которой привязаны куры")
        }
    )
)
class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def partial_update(self, request, *args, **kwargs):
        print(">>> partial_update вызван! Метод:", request.method)
        print(">>> Данные:", request.data)
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.hens.exists():
            return Response(
                {"error": "Нельзя удалить породу, к которой привязаны куры"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        summary="Получить список диет",
        description="Возвращает список всех диет",
        tags=['Диеты'],
        responses={200: DietSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Получить диету",
        description="Возвращает информацию о конкретной диете",
        tags=['Диеты'],
        responses={200: DietSerializer}
    ),
    create=extend_schema(
        summary="Создать диету",
        description="Создает новую диету",
        tags=['Диеты'],
        responses={201: DietSerializer}
    ),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(
        summary="Частично обновить диету",
        description="Частично обновляет информацию о диете",
        tags=['Диеты'],
        responses={200: DietSerializer}
    ),
    destroy=extend_schema(
        summary="Удалить диету",
        description="Удаляет диету. Нельзя удалить диету, к которой привязаны породы",
        tags=['Диеты'],
        responses={
            204: OpenApiResponse(description="Диета успешно удалена"),
            400: OpenApiResponse(description="Нельзя удалить диету, к которой привязаны породы")
        }
    )
)
class DietViewSet(viewsets.ModelViewSet):
    queryset = Diet.objects.all()
    serializer_class = DietSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.breeds.exists():
            return Response(
                {"error": "Нельзя удалить диету, к которой привязаны породы"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        summary="Получить список связей пород и диет",
        description="Возвращает список связей пород с диетами по сезонам",
        tags=['Диеты пород'],
        parameters=[
            OpenApiParameter(
                name='breed_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='ID породы для фильтрации'
            )
        ],
        responses={200: BreedDietSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Получить связь породы и диеты",
        description="Возвращает информацию о конкретной связи породы с диетой",
        tags=['Диеты пород'],
        responses={200: BreedDietSerializer}
    ),
    create=extend_schema(
        summary="Создать связь породы и диеты",
        description="Создает новую связь породы с диетой для определенного сезона",
        tags=['Диеты пород'],
        responses={201: BreedDietSerializer}
    ),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(
        summary="Частично обновить связь породы и диеты",
        description="Частично обновляет информацию о связи породы с диетой",
        tags=['Диеты пород'],
        responses={200: BreedDietSerializer}
    ),
    destroy=extend_schema(
        summary="Удалить связь породы и диеты",
        description="Удаляет связь породы с диетой",
        tags=['Диеты пород'],
        responses={204: OpenApiResponse(description="Связь успешно удалена")}
    )
)
class BreedDietViewSet(viewsets.ModelViewSet):
    queryset = BreedDiet.objects.all()
    serializer_class = BreedDietSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        breed = self.request.query_params.get('breed_id')
        if breed:
            queryset = queryset.filter(breed__id=breed)
        return queryset


@extend_schema_view(
    list=extend_schema(
        summary="Получить список живых кур",
        description="Возвращает список всех живых кур (без умерших)",
        tags=['Курицы'],
        responses={200: HenSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Получить курицу",
        description="Возвращает информацию о конкретной курице",
        tags=['Курицы'],
        responses={200: HenSerializer}
    ),
    create=extend_schema(
        summary="Создать курицу",
        description="Создает новую курицу",
        tags=['Курицы'],
        responses={201: HenSerializer}
    ),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(
        summary="Частично обновить курицу",
        description="Частично обновляет информацию о курице (только вес и дату смерти)",
        tags=['Курицы'],
        responses={200: HenSerializer}
    ),
    destroy=extend_schema(
        summary="Удалить курицу",
        description="Удаление запрещено. Используйте поле death_date для пометки о смерти",
        tags=['Курицы'],
        responses={
            405: OpenApiResponse(description="Удаление кур запрещено")
        }
    )
)
class HenViewSet(viewsets.ModelViewSet):
    queryset = Hen.objects.all()
    serializer_class = HenSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        return Response(
            {"error": "Используйте PATCH для частичного обновления"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ['list', 'retrieve']:
            queryset = queryset.filter(death_date__isnull=True)
        return queryset
    
    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        allowed_fields = ['weight', 'death_date']
        for field in request.data.keys():
            if field not in allowed_fields:
                return Response(
                    {"error": f"Обновление поля '{field}' запрещено"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        data = {}
        for field in allowed_fields:
            if field in request.data:
                data[field] = request.data[field]
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"error": "Удаление кур запрещено. Используйте поле death_date для пометки о смерти"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@extend_schema_view(
    list=extend_schema(
        summary="Получить записи о яйценоскости",
        description="Возвращает записи о яйценоскости с возможностью фильтрации",
        tags=['Яйценоскость'],
        parameters=[
            OpenApiParameter(
                name='hen_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='ID курицы для фильтрации'
            ),
            OpenApiParameter(
                name='date_from',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Дата начала периода (YYYY-MM-DD)'
            ),
            OpenApiParameter(
                name='date_to',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Дата окончания периода (YYYY-MM-DD)'
            )
        ],
        responses={200: HenEggsSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Получить запись о яйценоскости",
        description="Возвращает конкретную запись о яйценоскости",
        tags=['Яйценоскость'],
        responses={200: HenEggsSerializer}
    ),
    create=extend_schema(
        summary="Создать запись о яйценоскости",
        description="Создает новую запись о количестве снесенных яиц",
        tags=['Яйценоскость'],
        responses={201: HenEggsSerializer}
    ),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(
        summary="Обновить запись о яйценоскости",
        description="Обновляет запись о яйценоскости",
        tags=['Яйценоскость'],
        responses={200: HenEggsSerializer}
    ),
    destroy=extend_schema(
        summary="Удалить запись о яйценоскости",
        description="Удаляет запись о яйценоскости (только в течение 24 часов)",
        tags=['Яйценоскость'],
        responses={
            204: OpenApiResponse(description="Запись успешно удалена"),
            403: OpenApiResponse(description="Удаление разрешено только в течение 24 часов")
        }
    )
)
class HenEggsViewSet(viewsets.ModelViewSet):
    queryset = HenEggs.objects.all()
    serializer_class = HenEggsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        return Response(
            {"error": "Используйте PATCH для частичного обновления"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def get_queryset(self):
        queryset = super().get_queryset()
        hen_id = self.request.query_params.get('hen_id')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if hen_id:
            queryset = queryset.filter(hen_id=hen_id)
        if date_from and date_to:
            queryset = queryset.filter(date__range=[date_from, date_to])
        
        return queryset.order_by('-date')
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if (timezone.now().date() - instance.date).days > 1:
            return Response(
                {"error": "Удаление записей о яйценоскости разрешено только в течение 24 часов"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        summary="Получить список клеток",
        description="Возвращает список всех клеток",
        tags=['Клетки'],
        responses={200: CageSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Получить клетку",
        description="Возвращает информацию о конкретной клетке",
        tags=['Клетки'],
        responses={200: CageSerializer}
    ),
    create=extend_schema(
        summary="Создать клетку",
        description="Создает новую клетку",
        tags=['Клетки'],
        responses={201: CageSerializer}
    ),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(
        summary="Удалить клетку",
        description="Удаляет клетку. Нельзя удалить клетку с курами или работниками",
        tags=['Клетки'],
        responses={
            204: OpenApiResponse(description="Клетка успешно удалена"),
            400: OpenApiResponse(description="Нельзя удалить клетку с курами или работниками")
        }
    )
)
class CageViewSet(viewsets.ModelViewSet):
    queryset = Cage.objects.all()
    serializer_class = CageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        return Response(
            {"error": "Обновление параметров клетки запрещено"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"error": "Обновление параметров клетки запрещено"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.hencage_set.exists() or instance.employeecage_set.exists():
            return Response(
                {"error": "Нельзя удалить клетку, в которой есть куры или за которой закреплены работники"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        summary="Получить историю заселения кур",
        description="Возвращает историю заселения кур в клетки",
        tags=['Размещение кур'],
        responses={200: HenCageSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Получить запись о заселении",
        description="Возвращает конкретную запись о заселении курицы",
        tags=['Размещение кур'],
        responses={200: HenCageSerializer}
    ),
    create=extend_schema(
        summary="Создать запись о заселении",
        description="Создает новую запись о заселении курицы в клетку",
        tags=['Размещение кур'],
        responses={201: HenCageSerializer}
    ),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(
        summary="Удалить запись о заселении",
        description="Удаление записей о заселении запрещено",
        tags=['Размещение кур'],
        responses={
            405: OpenApiResponse(description="Удаление записей о заселении запрещено")
        }
    )
)
class HenCageViewSet(viewsets.ModelViewSet):
    queryset = HenCage.objects.all()
    serializer_class = HenCageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Добавляем фильтрацию по hen_id и current_only
        hen_id = self.request.query_params.get('hen')
        current_only = self.request.query_params.get('current_only')
        
        if hen_id:
            queryset = queryset.filter(hen_id=hen_id)
        if current_only == 'true':
            queryset = queryset.filter(date_end__isnull=True)
        
        return queryset.order_by('-date_start')
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"error": "Удаление записей о заселении запрещено. Используйте обновление даты выселения"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@extend_schema_view(
    list=extend_schema(
        summary="Получить список сотрудников",
        description="Возвращает список всех сотрудников",
        tags=['Сотрудники'],
        responses={200: EmployeeSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Получить сотрудника",
        description="Возвращает информацию о конкретном сотруднике",
        tags=['Сотрудники'],
        responses={200: EmployeeSerializer}
    ),
    create=extend_schema(
        summary="Создать сотрудника",
        description="Создает нового сотрудника",
        tags=['Сотрудники'],
        responses={201: EmployeeSerializer}
    ),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(
        summary="Частично обновить сотрудника",
        description="Частично обновляет информацию о сотруднике",
        tags=['Сотрудники'],
        responses={200: EmployeeSerializer}
    ),
    destroy=extend_schema(
        summary="Удалить сотрудника",
        description="Удаление сотрудников запрещено",
        tags=['Сотрудники'],
        responses={
            405: OpenApiResponse(description="Удаление сотрудников запрещено")
        }
    )
)
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"error": "Удаление сотрудников запрещено. Используйте увольнение через Employment"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@extend_schema_view(
    list=extend_schema(
        summary="Получить историю закрепления клеток",
        description="Возвращает историю закрепления клеток за сотрудниками",
        tags=['Закрепление клеток'],
        parameters=[
            OpenApiParameter(
                name='employee_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='ID сотрудника для фильтрации'
            ),
            OpenApiParameter(
                name='cage_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='ID клетки для фильтрации'
            ),
            OpenApiParameter(
                name='active',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description='Фильтр по активным/неактивным закреплениям'
            )
        ],
        responses={200: EmployeeCageSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Получить запись о закреплении",
        description="Возвращает конкретную запись о закреплении клетки",
        tags=['Закрепление клеток'],
        responses={200: EmployeeCageSerializer}
    ),
    create=extend_schema(
        summary="Создать запись о закреплении",
        description="Создает новую запись о закреплении клетки за сотрудником",
        tags=['Закрепление клеток'],
        responses={201: EmployeeCageSerializer}
    ),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(
        summary="Обновить запись о закреплении",
        description="Обновляет запись о закреплении клетки",
        tags=['Закрепление клеток'],
        responses={200: EmployeeCageSerializer}
    ),
    destroy=extend_schema(
        summary="Удалить запись о закреплении",
        description="Удаление записей о закреплении запрещено",
        tags=['Закрепление клеток'],
        responses={
            405: OpenApiResponse(description="Удаление записей о закреплении запрещено")
        }
    )
)
class EmployeeCageViewSet(viewsets.ModelViewSet):
    queryset = EmployeeCage.objects.all()
    serializer_class = EmployeeCageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        employee = self.request.query_params.get('employee_id')
        cage = self.request.query_params.get('cage_id')
        active = self.request.query_params.get('active')
        
        if employee:
            queryset = queryset.filter(employee=employee)
        if cage:
            queryset = queryset.filter(cage=cage)
        if active:
            if active == 'true':
                queryset = queryset.filter(date_end__isnull=True)
            elif active == 'false':
                queryset = queryset.filter(date_end__isnull=False)
        
        return queryset.order_by('-date_start')
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"error": "Удаление записей о закреплении запрещено. Используйте обновление даты открепления"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@extend_schema_view(
    list=extend_schema(
        summary="Получить историю трудоустройства",
        description="Возвращает историю трудоустройства сотрудников",
        tags=['Трудоустройство'],
        parameters=[
            OpenApiParameter(
                name='employee_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='ID сотрудника для фильтрации'
            ),
            OpenApiParameter(
                name='active',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description='Фильтр по активным/неактивным трудоустройствам'
            )
        ],
        responses={200: EmploymentSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Получить запись о трудоустройстве",
        description="Возвращает конкретную запись о трудоустройстве",
        tags=['Трудоустройство'],
        responses={200: EmploymentSerializer}
    ),
    create=extend_schema(
        summary="Создать запись о трудоустройстве",
        description="Создает новую запись о трудоустройстве сотрудника",
        tags=['Трудоустройство'],
        responses={201: EmploymentSerializer}
    ),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(
        summary="Обновить запись о трудоустройстве",
        description="Обновляет запись о трудоустройстве",
        tags=['Трудоустройство'],
        responses={200: EmploymentSerializer}
    ),
    destroy=extend_schema(
        summary="Удалить запись о трудоустройстве",
        description="Удаление записей о трудоустройстве запрещено",
        tags=['Трудоустройство'],
        responses={
            405: OpenApiResponse(description="Удаление записей о трудоустройстве запрещено")
        }
    )
)
class EmploymentViewSet(viewsets.ModelViewSet):
    queryset = Employment.objects.all()
    serializer_class = EmploymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        return Response(
            {"error": "Используйте PATCH для частичного обновления"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def get_queryset(self):
        queryset = super().get_queryset()
        employee = self.request.query_params.get('employee_id')
        active = self.request.query_params.get('active')
        
        if employee:
            queryset = queryset.filter(employee=employee)
        if active:
            if active == 'true':
                queryset = queryset.filter(date_end__isnull=True)
            elif active == 'false':
                queryset = queryset.filter(date_end__isnull=False)
        
        return queryset.order_by('-date_start')
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"error": "Удаление записей о трудоустройстве запрещено. Используйте пометку об увольнении"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@extend_schema(
    summary="Получить детальную информацию о курице",
    description="Возвращает детальную информацию о курице с текущим размещением",
    tags=['Курицы'],
    responses={200: HenWithBreedSerializer}
)
class HenDetailView(generics.RetrieveAPIView):
    queryset = Hen.objects.select_related('breed').prefetch_related(
        Prefetch(
            'hen_cages',
            queryset=HenCage.objects.select_related('cage').filter(
                Q(date_end__gte=date.today()) | Q(date_end__isnull=True)
            ).order_by('-date_start'),
            to_attr='current_cage_assignments'
        )
    )
    serializer_class = HenWithBreedSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


@extend_schema(
    summary="Получить детальную информацию о сотруднике",
    description="Возвращает детальную информацию о сотруднике с закрепленными клетками",
    tags=['Сотрудники'],
    responses={200: EmployeeWithCagesSerializer}
)
class EmployeeDetailView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeWithCagesSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


@extend_schema(
    summary="Получить детальную информацию о клетке",
    description="Возвращает детальную информацию о клетке с текущими курами",
    tags=['Клетки'],
    responses={200: CageWithHensSerializer}
)
class CageDetailView(generics.RetrieveAPIView):
    serializer_class = CageWithHensSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Cage.objects.prefetch_related(
            Prefetch(
                'cage_hens',
                queryset=HenCage.objects.filter(
                    date_start__lte=date.today()
                ).filter(
                    Q(date_end__gte=date.today()) | Q(date_end__isnull=True)
                ).select_related('hen__breed'),
                to_attr='current_hen_assignments'
            )
        )


@extend_schema(
    summary="Яйценоскость по характеристикам",
    description="Возвращает среднее количество яиц от каждой курицы данного веса, породы, возраста",
    tags=['Отчеты'],
    parameters=[
        OpenApiParameter(
            name='breed',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Порода (можно несколько через запятую)'
        ),
        OpenApiParameter(
            name='weight_category',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Категория веса (можно несколько через запятую): до_1.5_кг, 1.5-2.0_кг, свыше_2.0_кг'
        ),
        OpenApiParameter(
            name='age_category',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Категория возраста (можно несколько через запятую): до_6_месяцев, 6-12_месяцев, старше_года'
        )
    ],
    responses={200: EggsByCharacteristicsSerializer(many=True)},
    examples=[
        OpenApiExample(
            'Пример запроса',
            value={
                "hen_id": 1,
                "breed_name": "Леггорн",
                "weight": 1800,
                "age_months": 8.5,
                "birth_date": "2024-01-15",
                "avg_eggs": 0.85
            }
        )
    ]
)
class EggsByCharacteristicsView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector]
    serializer_class = EggsByCharacteristicsSerializer

    def get_queryset(self):
        today = date.today()
        last_month = today - timedelta(days=30)

        breed_filter = self.request.GET.get('breed')
        weight_category_filter = self.request.GET.get('weight_category')
        age_category_filter = self.request.GET.get('age_category')

        hens_qs = Hen.objects.filter(
            birth_date__lte=today - timedelta(days=150),
            death_date__isnull=True
        ).select_related('breed').prefetch_related('egg_records')

        if breed_filter:
            breed_names = [b.strip() for b in breed_filter.split(',') if b.strip()]
            if breed_names:
                hens_qs = hens_qs.filter(breed__name__in=breed_names)

        results = []
        for hen in hens_qs:
            birth = hen.birth_date.date() if hasattr(hen.birth_date, 'date') else hen.birth_date
            age_days = (today - birth).days
            age_months = age_days / 30.0

            if age_months < 6:
                age_category = 'до_6_месяцев'
            elif age_months < 12:
                age_category = '6-12_месяцев'
            else:
                age_category = 'старше_года'

            if hen.weight < 1500:
                weight_category = 'до_1.5_кг'
            elif hen.weight < 2000:
                weight_category = '1.5-2.0_кг'
            else:
                weight_category = 'свыше_2.0_кг'

            if age_category_filter:
                allowed = [c.strip() for c in age_category_filter.split(',') if c.strip()]
                if allowed and age_category not in allowed:
                    continue
            if weight_category_filter:
                allowed = [c.strip() for c in weight_category_filter.split(',') if c.strip()]
                if allowed and weight_category not in allowed:
                    continue

            egg_qs = hen.egg_records.filter(date__gte=last_month, date__lte=today)
            eggs_list = [e.count_eggs for e in egg_qs]
            avg_eggs = round(mean(eggs_list), 2) if eggs_list else 0.0

            results.append({
                'hen_id': hen.id,
                'breed_name': hen.breed.name if hen.breed else None,
                'weight': hen.weight,
                'age_months': round(age_months, 1),
                'birth_date': birth,
                'avg_eggs': avg_eggs
            })

        return results


@extend_schema(
    summary="Цех с наибольшим количеством кур определенной породы",
    description="Возвращает цех(и) с наибольшим количеством кур указанной породы",
    tags=['Отчеты'],
    responses={200: TopWorkshopSerializer(many=True)},
    examples=[
        OpenApiExample(
            'Пример ответа',
            value=[
                {
                    "workshop_number": 1,
                    "breed_count": 15
                }
            ]
        )
    ]
)
class TopWorkshopByBreedView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector]
    serializer_class = TopWorkshopSerializer

    def get_queryset(self):
        breed_name = self.kwargs.get('breed_name')
        today = date.today()

        placements = HenCage.objects.filter(
            hen__breed__name=breed_name
        ).filter(
            Q(date_start__lte=today) & (Q(date_end__isnull=True) | Q(date_end__gte=today))
        )

        workshop_counts = placements.values('cage__workshop_number').annotate(
            breed_count=Count('hen', distinct=True)
        ).order_by('-breed_count')

        if not workshop_counts:
            return []

        max_count = workshop_counts[0]['breed_count']

        return [
            {'workshop_number': item['cage__workshop_number'], 'breed_count': item['breed_count']}
            for item in workshop_counts if item['breed_count'] == max_count
        ]


@extend_schema(
    summary="Средняя яйценоскость на работника",
    description="Возвращает среднее количество яиц, которое получает в день каждый работник от обслуживаемых им кур",
    tags=['Отчеты'],
    responses={200: EmployeeAvgEggsSerializer(many=True)},
    examples=[
        OpenApiExample(
            'Пример ответа',
            value=[
                {
                    "employee_id": 1,
                    "employee_name": "Иванов Иван Иванович",
                    "avg_eggs_per_day": 8.5
                }
            ]
        )
    ]
)
class EmployeeAvgEggsView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector]
    serializer_class = EmployeeAvgEggsSerializer

    def get_queryset(self):
        today = date.today()
        last_month = today - timedelta(days=30)

        employees = Employee.objects.filter(
            employee_cages__in=EmployeeCage.objects.filter(
                Q(date_start__lte=today) & (Q(date_end__isnull=True) | Q(date_end__gte=today))
            )
        ).distinct()

        results = []
        for emp in employees:
            cages_qs = Cage.objects.filter(
                employee_cages__employee=emp
            ).filter(
                Q(employee_cages__date_start__lte=today) & (Q(employee_cages__date_end__isnull=True) | Q(employee_cages__date_end__gte=today))
            ).distinct()

            hens_qs = Hen.objects.filter(
                hen_cages__cage__in=cages_qs
            ).filter(
                Q(hen_cages__date_start__lte=today) & (Q(hen_cages__date_end__isnull=True) | Q(hen_cages__date_end__gte=today))
            ).distinct()

            total_eggs = HenEggs.objects.filter(
                hen__in=hens_qs,
                date__gte=last_month,
                date__lte=today
            ).aggregate(total=Sum('count_eggs'))['total'] or 0
            avg_per_day = round(total_eggs / 30.0, 2) if total_eggs else 0.0

            results.append({
                'employee_id': emp.id,
                'employee_name': emp.full_name,
                'avg_eggs_per_day': avg_per_day
            })

        return results


@extend_schema(
    summary="Распределение пород по цехам",
    description="Возвращает количество кур каждой породы в каждом цехе",
    tags=['Отчеты'],
    responses={200: BreedDistributionSerializer(many=True)},
    examples=[
        OpenApiExample(
            'Пример ответа',
            value=[
                {
                    "workshop_number": 1,
                    "breed_name": "Леггорн",
                    "count": 10
                }
            ]
        )
    ]
)
class BreedDistributionView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector]
    serializer_class = BreedDistributionSerializer

    def get_queryset(self):
        today = date.today()

        placement_qs = HenCage.objects.filter(
            Q(date_start__lte=today) & (Q(date_end__isnull=True) | Q(date_end__gte=today))
        ).values('cage__workshop_number', 'hen__breed__name').annotate(count=Count('hen'))

        result = []
        for p in placement_qs:
            result.append({
                'workshop_number': p['cage__workshop_number'],
                'breed_name': p['hen__breed__name'],
                'count': p['count']
            })
        return result


@extend_schema(
    summary="Разница показателей пород",
    description="Возвращает разницу между показателями породы и средними показателями по птицефабрике",
    tags=['Отчеты'],
    responses={200: BreedEfficiencyDiffSerializer(many=True)},
    examples=[
        OpenApiExample(
            'Пример ответа',
            value=[
                {
                    "breed_name": "Леггорн",
                    "breed_efficiency": 28,
                    "factory_avg": 0.8,
                    "difference": 0.15
                }
            ]
        )
    ]
)
class BreedEfficiencyDiffView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector]
    serializer_class = BreedEfficiencyDiffSerializer

    def get_queryset(self):
        today = date.today()
        last_month = today - timedelta(days=30)

        factory_avg = HenEggs.objects.filter(
            date__gte=last_month,
            date__lte=today
        ).aggregate(avg=Avg('count_eggs'))['avg'] or 0.0

        results = []
        for breed in Breed.objects.all():
            breed_avg = HenEggs.objects.filter(
                hen__breed=breed,
                date__gte=last_month,
                date__lte=today
            ).aggregate(avg=Avg('count_eggs'))['avg'] or 0.0

            print(breed_avg)

            results.append({
                'breed_name': breed.name,
                'breed_efficiency': breed.efficiency,
                'factory_avg': round(factory_avg, 2),
                'difference': round(breed_avg - factory_avg, 2)
            })

        return results


@extend_schema(
    summary="Ежемесячный отчет",
    description="Формирует отчет о работе птицефабрики за прошедший месяц",
    tags=['Отчеты'],
    responses={200: MonthlyReportSerializer},
    examples=[
        OpenApiExample(
            'Пример ответа',
            value={
                "period": "2024-01-01 - 2024-01-31",
                "workshops": [
                    {
                        "workshop_number": 1,
                        "total_hens": 25,
                        "total_eggs": 625,
                        "breeds": [
                            {
                                "breed_name": "Леггорн",
                                "count": 15,
                                "eggs": 375
                            }
                        ]
                    }
                ],
                "total_hens": 100,
                "total_eggs": 2100
            }
        )
    ]
)
class MonthlyReportView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDirector]

    def get(self, request, *args, **kwargs):
        today = date.today()
        first_day_of_month = today.replace(day=1)
        last_day_of_last_month = first_day_of_month - timedelta(days=1)
        first_day_of_last_month = last_day_of_last_month.replace(day=1)

        period = f"{first_day_of_last_month} - {last_day_of_last_month}"

        total_eggs = HenEggs.objects.filter(
            date__range=(first_day_of_last_month, last_day_of_last_month)
        ).aggregate(total=Sum('count_eggs'))['total'] or 0

        total_hens = Hen.objects.filter(
            birth_date__lte=last_day_of_last_month
        ).filter(
            Q(death_date__isnull=True) | Q(death_date__gte=first_day_of_last_month)
        ).count()
        workshops = []
        workshop_numbers = Cage.objects.values_list('workshop_number', flat=True).distinct()

        overlap_q = Q(date_start__lte=last_day_of_last_month) & (Q(date_end__isnull=True) | Q(date_end__gte=first_day_of_last_month))

        for ws in workshop_numbers:
            placements = HenCage.objects.filter(
                cage__workshop_number=ws
            ).filter(overlap_q)

            hens_in_workshop = Hen.objects.filter(hen_cages__in=placements).distinct()

            eggs_in_workshop = HenEggs.objects.filter(
                hen__in=hens_in_workshop,
                date__range=(first_day_of_last_month, last_day_of_last_month)
            ).aggregate(total=Sum('count_eggs'))['total'] or 0

            breed_counts = hens_in_workshop.values('breed__name').annotate(count=Count('id'))

            breeds_data = []
            for b in breed_counts:
                breed_name = b['breed__name']
                breed_count = b['count']

                breed_eggs = HenEggs.objects.filter(
                    hen__in=hens_in_workshop,
                    hen__breed__name=breed_name,
                    date__range=(first_day_of_last_month, last_day_of_last_month)
                ).aggregate(total=Sum('count_eggs'))['total'] or 0

                breeds_data.append({
                    'breed_name': breed_name,
                    'count': breed_count,
                    'eggs': breed_eggs
                })

            workshops.append({
                'workshop_number': ws,
                'total_hens': hens_in_workshop.count(),
                'total_eggs': eggs_in_workshop,
                'breeds': breeds_data
            })

        data = {
            'period': period,
            'workshops': workshops,
            'total_hens': total_hens,
            'total_eggs': total_eggs
        }

        serializer = MonthlyReportSerializer(data)
        return Response(serializer.data)