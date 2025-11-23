from rest_framework import viewsets, status, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.http import JsonResponse

from .models import Building, Apartment, ServiceCategory, ServiceRequest, MeterReading
from .serializers import (
    BuildingSerializer, BuildingListSerializer,
    ApartmentSerializer,
    ServiceCategorySerializer,
    ServiceRequestSerializer, ServiceRequestCreateSerializer,
    MeterReadingSerializer,
    # Сериализаторы согласно ТЗ
    ServiceRequestBaseSerializer,
    RequestApartmentSerializer,
    RequestCategorySerializer,
    RequestDetailSerializer
)
from .permissions import (
    IsDispatcher, IsOwnerOrDispatcher, IsAssignedWorkerOrDispatcher,
    IsRequesterOrWorkerOrDispatcher
)


def api_root(request):
    """Корневая страница API с информацией о доступных эндпоинтах"""
    return JsonResponse({
        'message': 'ЖК Коннект - API',
        'version': '1.0',
        'endpoints': {
            'authentication': {
                'login': '/api/auth/token/login/',
                'logout': '/api/auth/token/logout/',
                'current_user': '/api/auth/users/me/',
                'register': '/api/auth/users/',
            },
            'generic_views': {
                'requests_with_apartment': '/api/requests-with-apartment/',
                'requests_with_category': '/api/requests-with-category/',
                'request_detail': '/api/request-detail/<id>/',
            },
            'viewsets': {
                'buildings': '/api/buildings/',
                'apartments': '/api/apartments/',
                'categories': '/api/categories/',
                'service_requests': '/api/service-requests/',
                'meter_readings': '/api/meter-readings/',
            },
            'admin': '/admin/',
        },
        'documentation': 'См. файл HOW_TO_RUN.md для подробной документации',
        'test_credentials': {
            'username': 'admin',
            'password': 'admin123'
        }
    })


class BuildingViewSet(viewsets.ModelViewSet):
    """ViewSet для домов (только для диспетчеров)"""
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated, IsDispatcher]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['address', 'description']
    ordering_fields = ['address', 'created_at']
    ordering = ['address']


class ApartmentViewSet(viewsets.ModelViewSet):
    """ViewSet для квартир"""
    queryset = Apartment.objects.select_related('building', 'owner').all()
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['building', 'owner', 'floor']
    search_fields = ['number', 'building__address']
    ordering_fields = ['number', 'floor', 'created_at']
    ordering = ['building', 'number']
    
    def get_queryset(self):
        """Фильтрация: жилец видит только свои квартиры"""
        queryset = super().get_queryset()
        if self.request.user.role == 'resident':
            return queryset.filter(owner=self.request.user)
        return queryset
    
    def get_permissions(self):
        """Настройка прав доступа"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsDispatcher()]
        return [IsAuthenticated()]


class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для категорий услуг (только чтение)"""
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']


class ServiceRequestViewSet(viewsets.ModelViewSet):
    """ViewSet для заявок"""
    queryset = ServiceRequest.objects.select_related(
        'category', 'apartment', 'apartment__building',
        'requester', 'worker'
    ).all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category', 'apartment', 'requester', 'worker']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return ServiceRequestCreateSerializer
        return ServiceRequestSerializer
    
    def get_queryset(self):
        """Фильтрация по ролям"""
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.role == 'resident':
            # Жилец видит только свои заявки
            return queryset.filter(requester=user)
        elif user.role == 'master':
            # Мастер видит назначенные ему заявки
            return queryset.filter(worker=user)
        # Диспетчер видит все
        return queryset
    
    def get_permissions(self):
        """Настройка прав доступа"""
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsRequesterOrWorkerOrDispatcher()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        """Автоматическое назначение requester при создании"""
        serializer.save(requester=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsDispatcher])
    def assign_worker(self, request, pk=None):
        """Назначение мастера на заявку (только диспетчер)"""
        request_obj = self.get_object()
        worker_id = request.data.get('worker_id')
        
        if not worker_id:
            return Response(
                {'error': 'worker_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            worker = User.objects.get(id=worker_id, role='master')
        except User.DoesNotExist:
            return Response(
                {'error': 'Мастер с таким ID не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        request_obj.worker = worker
        if not request_obj.assigned_at:
            request_obj.assigned_at = timezone.now()
        if request_obj.status == 'new':
            request_obj.status = 'in_progress'
            if not request_obj.started_at:
                request_obj.started_at = timezone.now()
        request_obj.save()
        
        serializer = self.get_serializer(request_obj)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAssignedWorkerOrDispatcher])
    def change_status(self, request, pk=None):
        """Изменение статуса заявки (мастер/диспетчер)"""
        request_obj = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(ServiceRequest.STATUS_CHOICES):
            return Response(
                {'error': 'Некорректный статус'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_status = request_obj.status
        request_obj.status = new_status
        
        # Отслеживание дат изменения статуса
        if new_status == 'in_progress' and old_status == 'new':
            if not request_obj.started_at:
                request_obj.started_at = timezone.now()
        elif new_status == 'done' and not request_obj.resolved_at:
            request_obj.resolved_at = timezone.now()
        
        request_obj.save()
        
        serializer = self.get_serializer(request_obj)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAssignedWorkerOrDispatcher])
    def add_comment(self, request, pk=None):
        """Добавление комментария мастера (мастер/диспетчер)"""
        request_obj = self.get_object()
        comment = request.data.get('comment')
        
        if not comment:
            return Response(
                {'error': 'Комментарий обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request_obj.worker_comment = comment
        request_obj.save()
        
        serializer = self.get_serializer(request_obj)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_requests(self, request):
        """Мои заявки как жилец"""
        if request.user.role != 'resident':
            return Response(
                {'error': 'Доступно только для жильцов'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        requests = self.get_queryset().filter(requester=request.user)
        page = self.paginate_queryset(requests)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(requests, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def assigned_to_me(self, request):
        """Заявки, назначенные мне как мастер"""
        if request.user.role != 'master':
            return Response(
                {'error': 'Доступно только для мастеров'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        requests = self.get_queryset().filter(worker=request.user)
        page = self.paginate_queryset(requests)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(requests, many=True)
        return Response(serializer.data)


class MeterReadingViewSet(viewsets.ModelViewSet):
    """ViewSet для показаний счетчиков"""
    queryset = MeterReading.objects.select_related('apartment', 'apartment__building').all()
    serializer_class = MeterReadingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['apartment', 'meter_type', 'date_recorded']
    ordering_fields = ['date_recorded', 'created_at']
    ordering = ['-date_recorded', '-created_at']
    
    def get_queryset(self):
        """Фильтрация: жилец видит только показания своих квартир"""
        queryset = super().get_queryset()
        if self.request.user.role == 'resident':
            return queryset.filter(apartment__owner=self.request.user)
        return queryset
    
    def get_permissions(self):
        """Настройка прав доступа"""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsDispatcher()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        """Автоматический поиск предыдущего показания и расчет расхода"""
        apartment = serializer.validated_data['apartment']
        meter_type = serializer.validated_data['meter_type']
        value = serializer.validated_data['value']
        
        # Поиск предыдущего показания для этой квартиры и типа счетчика
        previous_reading = MeterReading.objects.filter(
            apartment=apartment,
            meter_type=meter_type
        ).order_by('-date_recorded', '-created_at').first()
        
        if previous_reading:
            serializer.validated_data['previous_value'] = previous_reading.value
            serializer.validated_data['consumption'] = value - previous_reading.value
        
        serializer.save()


# ========== GENERIC-КЛАССЫ СОГЛАСНО ТЗ ==========

class RequestListApartmentView(generics.ListAPIView):
    """
    Список заявок с развернутой квартирой (ListAPIView)
    Использует RequestApartmentSerializer для вложенного объекта apartment
    """
    queryset = ServiceRequest.objects.select_related(
        'apartment', 'apartment__building', 'apartment__owner'
    ).all()
    serializer_class = RequestApartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'apartment']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Фильтрация по ролям"""
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.role == 'resident':
            return queryset.filter(requester=user)
        elif user.role == 'master':
            return queryset.filter(worker=user)
        return queryset


class RequestListCategoryView(generics.ListAPIView):
    """
    Список заявок с развернутой категорией (ListAPIView)
    Использует RequestCategorySerializer для вложенного объекта category
    """
    queryset = ServiceRequest.objects.select_related('category').all()
    serializer_class = RequestCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Фильтрация по ролям"""
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.role == 'resident':
            return queryset.filter(requester=user)
        elif user.role == 'master':
            return queryset.filter(worker=user)
        return queryset


class RequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Комбайн для просмотра, изменения и удаления одной заявки по ID
    Логика выбора сериализатора:
    - GET -> RequestDetailSerializer (детальный с развернутыми объектами)
    - PUT/PATCH/DELETE -> ServiceRequestBaseSerializer (плоская структура)
    """
    queryset = ServiceRequest.objects.select_related(
        'apartment', 'apartment__building', 'apartment__owner',
        'category', 'requester', 'worker'
    ).all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от метода запроса"""
        if self.request.method == 'GET':
            # Для GET используем детальный сериализатор с развернутыми объектами
            return RequestDetailSerializer
        else:
            # Для PUT, PATCH, DELETE используем базовый плоский сериализатор
            return ServiceRequestBaseSerializer
    
    def get_queryset(self):
        """Фильтрация по ролям"""
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.role == 'resident':
            return queryset.filter(requester=user)
        elif user.role == 'master':
            return queryset.filter(worker=user)
        return queryset
    
    def perform_update(self, serializer):
        """Автоматическое назначение requester при обновлении, если не указан"""
        if 'requester_id' not in serializer.validated_data:
            serializer.save(requester=self.request.user)
        else:
            serializer.save()

