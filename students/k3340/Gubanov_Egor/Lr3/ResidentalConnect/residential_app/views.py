from rest_framework import viewsets, status, filters, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum, Avg, Q

from .models import Building, Apartment, ServiceCategory, ServiceRequest, MeterReading
from .serializers import (
    BuildingSerializer, BuildingListSerializer,
    ApartmentSerializer,
    ServiceCategorySerializer,
    ServiceRequestSerializer, ServiceRequestCreateSerializer,
    MeterReadingSerializer,
    ServiceRequestBaseSerializer,
    RequestApartmentSerializer,
    RequestCategorySerializer,
    RequestDetailSerializer
)
from .permissions import (
    IsDispatcher, IsOwnerOrDispatcher, IsAssignedWorkerOrDispatcher,
    IsRequesterOrWorkerOrDispatcher
)


@api_view(['GET'])
@permission_classes([AllowAny])
def test_cors(request):
    return Response({"message": "CORS работает!"})


def api_root(request):
    """Корневая страница API с информацией о доступных эндпоинтах"""
    base_url = request.build_absolute_uri('/').rstrip('/')
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ЖК Коннект - API Documentation</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background-color: #fafafa;
                color: #424242;
                line-height: 1.6;
                padding: 0;
            }}
            .md-container {{
                max-width: 1220px;
                margin: 0 auto;
                padding: 2rem 1rem;
            }}
            .md-main {{
                background: #fff;
                border-radius: 2px;
                box-shadow: 0 2px 2px 0 rgba(0,0,0,.14), 0 1px 5px 0 rgba(0,0,0,.12), 0 3px 1px -2px rgba(0,0,0,.2);
                padding: 2rem;
            }}
            h1 {{
                color: #1976d2;
                font-size: 2rem;
                font-weight: 400;
                margin-bottom: 0.5rem;
                border-bottom: 1px solid rgba(0,0,0,.12);
                padding-bottom: 0.5rem;
            }}
            .md-typeset h2 {{
                color: #424242;
                font-size: 1.5rem;
                font-weight: 400;
                margin-top: 2rem;
                margin-bottom: 1rem;
                border-bottom: 1px solid rgba(0,0,0,.12);
                padding-bottom: 0.5rem;
            }}
            .md-typeset h3 {{
                color: #616161;
                font-size: 1.25rem;
                font-weight: 400;
                margin-top: 1.5rem;
                margin-bottom: 0.75rem;
            }}
            .subtitle {{
                color: #757575;
                font-size: 0.9rem;
                margin-bottom: 2rem;
            }}
            .admonition {{
                margin: 1.5rem 0;
                padding: 0 1rem;
                border-left: 4px solid #1976d2;
                background-color: rgba(25, 118, 210, 0.05);
            }}
            .admonition-title {{
                font-weight: 500;
                margin-bottom: 0.5rem;
                color: #1976d2;
            }}
            .admonition p {{
                margin: 0.5rem 0;
                color: #424242;
            }}
            .endpoint-list {{
                list-style: none;
                margin: 1rem 0;
            }}
            .endpoint-item {{
                margin: 0.75rem 0;
                padding: 0.75rem;
                background-color: #fafafa;
                border-left: 3px solid #1976d2;
            }}
            .endpoint-method {{
                display: inline-block;
                padding: 0.25rem 0.5rem;
                border-radius: 2px;
                font-size: 0.75rem;
                font-weight: 500;
                margin-right: 0.5rem;
                text-transform: uppercase;
            }}
            .method-get {{ background-color: #4caf50; color: white; }}
            .method-post {{ background-color: #2196f3; color: white; }}
            .method-put {{ background-color: #ff9800; color: white; }}
            .method-patch {{ background-color: #00bcd4; color: white; }}
            .method-delete {{ background-color: #f44336; color: white; }}
            .endpoint-link {{
                color: #1976d2;
                text-decoration: none;
                font-weight: 500;
                word-break: break-all;
            }}
            .endpoint-link:hover {{
                text-decoration: underline;
            }}
            .endpoint-desc {{
                color: #757575;
                font-size: 0.875rem;
                margin-top: 0.5rem;
                margin-left: 3.5rem;
            }}
            code {{
                background-color: rgba(0,0,0,.05);
                padding: 0.2rem 0.4rem;
                border-radius: 2px;
                font-family: 'Roboto Mono', 'Courier New', monospace;
                font-size: 0.875em;
                color: #e91e63;
            }}
            .footer {{
                margin-top: 3rem;
                padding-top: 1.5rem;
                border-top: 1px solid rgba(0,0,0,.12);
                text-align: center;
                color: #757575;
                font-size: 0.875rem;
            }}
            .footer a {{
                color: #1976d2;
                text-decoration: none;
            }}
            .footer a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="md-container">
            <div class="md-main">
                <h1>ЖК Коннект - API</h1>
                <p class="subtitle">Информационная система для автоматизации работы Управляющей Компании ЖК</p>
                
                <div class="admonition">
                    <div class="admonition-title">Аутентификация</div>
                    <p><strong>Как это работает:</strong></p>
                    <p>1. <strong>Регистрация:</strong> POST <code>{base_url}/api/auth/users/</code> - создайте пользователя с полями: username, password, email, role</p>
                    <p>2. <strong>Получение токена:</strong> POST <code>{base_url}/api/auth/token/login/</code> - отправьте JSON: {{"username": "...", "password": "..."}}</p>
                    <p>3. <strong>Использование токена:</strong> Добавьте заголовок <code>Authorization: Token ваш_токен</code> к каждому запросу</p>
                    <p>4. <strong>Текущий пользователь:</strong> GET <code>{base_url}/api/auth/users/me/</code> - получите информацию о себе</p>
                    <p><strong>Роли:</strong> <code>resident</code> (Жилец), <code>master</code> (Мастер), <code>dispatcher</code> (Диспетчер)</p>
                    <p><strong>Технология:</strong> Djoser использует <code>rest_framework.authtoken</code> для создания токенов при логине</p>
                </div>
                
                <h2 class="md-typeset">Аутентификация (Djoser)</h2>
                <ul class="endpoint-list">
                    <li class="endpoint-item">
                        <span class="endpoint-method method-post">POST</span>
                        <a href="{base_url}/api/auth/users/" class="endpoint-link">{base_url}/api/auth/users/</a>
                        <p class="endpoint-desc">Регистрация нового пользователя</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-post">POST</span>
                        <a href="{base_url}/api/auth/token/login/" class="endpoint-link">{base_url}/api/auth/token/login/</a>
                        <p class="endpoint-desc">Получение токена авторизации</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-post">POST</span>
                        <a href="{base_url}/api/auth/token/logout/" class="endpoint-link">{base_url}/api/auth/token/logout/</a>
                        <p class="endpoint-desc">Выход (удаление токена)</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-get">GET</span>
                        <a href="{base_url}/api/auth/users/me/" class="endpoint-link">{base_url}/api/auth/users/me/</a>
                        <p class="endpoint-desc">Информация о текущем пользователе</p>
                    </li>
                </ul>
                
                <h2 class="md-typeset">Generic Views</h2>
                <ul class="endpoint-list">
                    <li class="endpoint-item">
                        <span class="endpoint-method method-get">GET</span>
                        <a href="{base_url}/api/requests-with-apartment/" class="endpoint-link">{base_url}/api/requests-with-apartment/</a>
                        <p class="endpoint-desc">Список заявок с данными квартир (ListAPIView)</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-get">GET</span>
                        <a href="{base_url}/api/requests-with-category/" class="endpoint-link">{base_url}/api/requests-with-category/</a>
                        <p class="endpoint-desc">Список заявок с категориями (ListAPIView)</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-get">GET</span>
                        <a href="{base_url}/api/request-detail/1/" class="endpoint-link">{base_url}/api/request-detail/&lt;id&gt;/</a>
                        <p class="endpoint-desc">Детальная информация, обновление, удаление (RetrieveUpdateDestroyAPIView)</p>
                    </li>
                </ul>
                
                <h2 class="md-typeset">ViewSets (CRUD операции)</h2>
                <ul class="endpoint-list">
                    <li class="endpoint-item">
                        <span class="endpoint-method method-get">GET</span>
                        <a href="{base_url}/api/buildings/" class="endpoint-link">{base_url}/api/buildings/</a>
                        <p class="endpoint-desc">Список домов</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-get">GET</span>
                        <a href="{base_url}/api/apartments/" class="endpoint-link">{base_url}/api/apartments/</a>
                        <p class="endpoint-desc">Список квартир</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-get">GET</span>
                        <a href="{base_url}/api/categories/" class="endpoint-link">{base_url}/api/categories/</a>
                        <p class="endpoint-desc">Категории услуг</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-get">GET</span>
                        <a href="{base_url}/api/service-requests/" class="endpoint-link">{base_url}/api/service-requests/</a>
                        <p class="endpoint-desc">Заявки на обслуживание</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-get">GET</span>
                        <a href="{base_url}/api/meter-readings/" class="endpoint-link">{base_url}/api/meter-readings/</a>
                        <p class="endpoint-desc">Показания счетчиков</p>
                    </li>
                </ul>
                
                <h2 class="md-typeset">Кастомные действия (Service Requests)</h2>
                <ul class="endpoint-list">
                    <li class="endpoint-item">
                        <span class="endpoint-method method-post">POST</span>
                        <a href="{base_url}/api/service-requests/1/assign_worker/" class="endpoint-link">{base_url}/api/service-requests/&lt;id&gt;/assign_worker/</a>
                        <p class="endpoint-desc">Назначить мастера на заявку</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-post">POST</span>
                        <a href="{base_url}/api/service-requests/1/change_status/" class="endpoint-link">{base_url}/api/service-requests/&lt;id&gt;/change_status/</a>
                        <p class="endpoint-desc">Изменить статус заявки</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-post">POST</span>
                        <a href="{base_url}/api/service-requests/1/add_comment/" class="endpoint-link">{base_url}/api/service-requests/&lt;id&gt;/add_comment/</a>
                        <p class="endpoint-desc">Добавить комментарий к заявке</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-get">GET</span>
                        <a href="{base_url}/api/service-requests/my_requests/" class="endpoint-link">{base_url}/api/service-requests/my_requests/</a>
                        <p class="endpoint-desc">Мои заявки (для жильца)</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-get">GET</span>
                        <a href="{base_url}/api/service-requests/assigned_to_me/" class="endpoint-link">{base_url}/api/service-requests/assigned_to_me/</a>
                        <p class="endpoint-desc">Заявки, назначенные на меня (для мастера)</p>
                    </li>
                </ul>
                
                <h2 class="md-typeset">Агрегационные запросы (Statistics)</h2>
                <ul class="endpoint-list">
                    <li class="endpoint-item">
                        <span class="endpoint-method method-get">GET</span>
                        <a href="{base_url}/api/service-requests/statistics/" class="endpoint-link">{base_url}/api/service-requests/statistics/</a>
                        <p class="endpoint-desc">Статистика по заявкам (количество по статусам, приоритетам, среднее время решения)</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-get">GET</span>
                        <a href="{base_url}/api/meter-readings/statistics/" class="endpoint-link">{base_url}/api/meter-readings/statistics/</a>
                        <p class="endpoint-desc">Статистика по показаниям счетчиков (суммарный расход, средние значения)</p>
                    </li>
                    <li class="endpoint-item">
                        <span class="endpoint-method method-get">GET</span>
                        <a href="{base_url}/api/buildings/statistics/" class="endpoint-link">{base_url}/api/buildings/statistics/</a>
                        <p class="endpoint-desc">Статистика по домам и квартирам (количество, площадь, заселенность)</p>
                    </li>
                </ul>
                
                <div class="footer">
                    <p>Полная документация: <a href="https://egorr-gubanov.github.io/TonikX-ITMO_ICT_WebDevelopment_2025-2026/Lr3/ResidentalConnect/" target="_blank">GitHub Pages</a></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)


class BuildingViewSet(viewsets.ModelViewSet):
    """ViewSet для домов (только для диспетчеров)"""
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated, IsDispatcher]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['address', 'description']
    ordering_fields = ['address', 'created_at']
    ordering = ['address']


    # агрегационный запрос
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsDispatcher])
    def statistics(self, request):

        from .models import Apartment

        buildings_stats = list(
            Building.objects.annotate(
                apartment_count=Count('apartments'),
                total_area=Sum('apartments__area'),
                avg_area=Avg('apartments__area'),
                occupied_count=Count('apartments', filter=Q(apartments__owner__isnull=False))
            )
            .values(
                'id', 'address', 'total_floors', 'year_built',
                'apartment_count', 'total_area', 'avg_area', 'occupied_count'
            )
            .order_by('-apartment_count')
        )

        total_buildings = Building.objects.count()
        total_apartments = Apartment.objects.count()
        total_area = Apartment.objects.aggregate(total=Sum('area'))['total'] or 0
        occupied_apartments = Apartment.objects.filter(owner__isnull=False).count()
        vacant_apartments = Apartment.objects.filter(owner__isnull=True).count()

        avg_apartments_per_building = total_apartments / total_buildings if total_buildings > 0 else 0
        avg_area_per_apartment = total_area / total_apartments if total_apartments > 0 else 0

        floor_stats = list(
            Apartment.objects.values('floor')
            .annotate(count=Count('id'))
            .order_by('floor')
        )

        rooms_stats = list(
            Apartment.objects.filter(rooms__isnull=False)
            .values('rooms')
            .annotate(count=Count('id'))
            .order_by('rooms')
        )
        
        stats = {
            'total_buildings': total_buildings,
            'total_apartments': total_apartments,
            'occupied_apartments': occupied_apartments,
            'vacant_apartments': vacant_apartments,
            'occupancy_rate': round((occupied_apartments / total_apartments * 100), 2) if total_apartments > 0 else 0,
            'total_area': float(total_area),
            'avg_apartments_per_building': round(avg_apartments_per_building, 2),
            'avg_area_per_apartment': round(float(avg_area_per_apartment), 2),
            'buildings_statistics': [
                {
                    'id': item['id'],
                    'address': item['address'],
                    'total_floors': item['total_floors'],
                    'year_built': item['year_built'],
                    'apartment_count': item['apartment_count'],
                    'total_area': float(item['total_area']) if item['total_area'] else 0,
                    'avg_area': float(item['avg_area']) if item['avg_area'] else 0,
                    'occupied_count': item['occupied_count'],
                    'vacant_count': item['apartment_count'] - item['occupied_count']
                }
                for item in buildings_stats
            ],
            'floor_distribution': floor_stats,
            'rooms_distribution': rooms_stats,
        }
        
        return Response(stats)


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

    # агрегационный запрос
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def statistics(self, request):

        queryset = self.get_queryset()

        status_stats = list(
            queryset.values('status')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        priority_stats = list(
            queryset.values('priority')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        category_stats = list(
            queryset.filter(category__isnull=False)
            .values('category__name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        total_requests = queryset.count()
        completed_requests = queryset.filter(status='done').count()

        completed_with_dates = queryset.filter(
            status='done',
            created_at__isnull=False,
            resolved_at__isnull=False
        )
        
        avg_resolution_time = None
        if completed_with_dates.exists():
            from datetime import timedelta
            resolution_times = []
            for req in completed_with_dates:
                if req.resolved_at and req.created_at:
                    delta = req.resolved_at - req.created_at
                    resolution_times.append(delta.total_seconds() / 86400)  # дни
            
            if resolution_times:
                avg_resolution_time = sum(resolution_times) / len(resolution_times)
        
        stats = {
            'total_requests': total_requests,
            'completed_requests': completed_requests,
            'in_progress_requests': queryset.filter(status='in_progress').count(),
            'new_requests': queryset.filter(status='new').count(),
            'canceled_requests': queryset.filter(status='canceled').count(),
            'status_distribution': status_stats,
            'priority_distribution': priority_stats,
            'category_distribution': category_stats,
            'average_resolution_time_days': round(avg_resolution_time, 2) if avg_resolution_time else None,
        }
        
        return Response(stats)


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

    # агрегационный запрос
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def statistics(self, request):

        queryset = self.get_queryset()

        consumption_by_type = list(
            queryset.filter(consumption__isnull=False)
            .values('meter_type')
            .annotate(
                total_consumption=Sum('consumption'),
                count=Count('id'),
                avg_consumption=Avg('consumption')
            )
            .order_by('-total_consumption')
        )

        avg_values_by_type = list(
            queryset.values('meter_type')
            .annotate(
                avg_value=Avg('value'),
                count=Count('id')
            )
            .order_by('meter_type')
        )

        total_readings = queryset.count()
        total_consumption = queryset.filter(consumption__isnull=False).aggregate(
            total=Sum('consumption')
        )['total'] or 0

        top_apartments = list(
            queryset.filter(consumption__isnull=False)
            .values('apartment__number', 'apartment__building__address')
            .annotate(
                total_consumption=Sum('consumption'),
                reading_count=Count('id')
            )
            .order_by('-total_consumption')[:10]
        )
        
        stats = {
            'total_readings': total_readings,
            'total_consumption': float(total_consumption),
            'consumption_by_type': [
                {
                    'meter_type': item['meter_type'],
                    'meter_type_display': dict(MeterReading.METER_TYPES).get(item['meter_type'], item['meter_type']),
                    'total_consumption': float(item['total_consumption']),
                    'count': item['count'],
                    'avg_consumption': float(item['avg_consumption'])
                }
                for item in consumption_by_type
            ],
            'avg_values_by_type': [
                {
                    'meter_type': item['meter_type'],
                    'meter_type_display': dict(MeterReading.METER_TYPES).get(item['meter_type'], item['meter_type']),
                    'avg_value': float(item['avg_value']),
                    'count': item['count']
                }
                for item in avg_values_by_type
            ],
            'top_apartments_by_consumption': top_apartments,
        }
        
        return Response(stats)



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

