from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.db.models import Count, Avg, Q, Sum, Prefetch
from django.utils import timezone
from datetime import timedelta

from .models import (
    SecurityCompany, Category, Service, ServiceCategory,
    ServiceDiscount, ServiceRequest, Review, UserFavorite
)
from .serializers import (
    UserSerializer, CategorySerializer, ServiceDiscountSerializer,
    ReviewSerializer, UserFavoriteSerializer,
    ServiceRequestCreateSerializer, SecurityCompanyListSerializer,
    SecurityCompanyDetailSerializer, SecurityCompanyCreateUpdateSerializer, SecurityCompanyMySerializer,
    ServiceListSerializer, ServiceDetailSerializer, ServiceCreateUpdateSerializer, SimpleServiceRequestSerializer,
    UserDetailSerializer, SimpleServiceSerializer, ServiceRequestSerializer, AnalyticsSerializer,
    ServiceRequestUpdateSerializer, SimpleUserFavoriteSerializer, UserFavoriteCreateSerializer, SimpleReviewSerializer,
    ReviewUpdateSerializer, ReviewCreateSerializer, CompanyAnalyticsSerializer
)
from .permissions import (
    IsServiceOwnerOrReadOnly, IsDiscountOwnerOrReadOnly,
    IsRequestOwnerOrCompanyOwner, IsCompanyOwnerOrAdmin, IsCompanyOwnerOnly, IsAdminOrReadOnly, IsRequestOwnerOrAdmin,
    IsRequestOwnerOrCompanyOwnerOrAdmin, IsFavoriteOwnerOrAdmin, IsReviewOwnerOrAdmin
)
from .exceptions import (
    AlreadyHaveCompanyError, NoCompanyError, CompanyPermissionDeniedError,
    ServicePermissionDeniedError, DiscountPermissionDeniedError, DiscountDateError,
    RequestPermissionDeniedError, InvalidStatusError, SelfRequestStatusError,
    AnalyticsPermissionDeniedError, CompanyNotFoundError, UserActionForbiddenError,
    CompanyActionForbiddenError
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'name', 'surname']
    ordering_fields = ['created_at', 'email']
    http_method_names = ['get', 'head', 'options']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'me']:
            return UserDetailSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'me':
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ['list', 'retrieve', 'me']:
            queryset = queryset.prefetch_related(
                'security_companies',
                Prefetch('favorites', queryset=UserFavorite.objects.select_related(
                    'service',
                    'service__security_company'
                )),
                Prefetch('service_requests', queryset=ServiceRequest.objects.select_related(
                    'service',
                    'service__security_company'
                )),
                Prefetch('reviews', queryset=Review.objects.select_related('security_company'))
            )
        return queryset

    @action(detail=False, methods=['get'], filter_backends=[])
    def me(self, request):
        user = request.user
        user_instance = self.get_queryset().get(pk=user.pk)
        serializer = self.get_serializer(user_instance)
        return Response(serializer.data)


class SecurityCompanyViewSet(viewsets.ModelViewSet):
    queryset = SecurityCompany.objects.all()
    serializer_class = SecurityCompanyListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    http_method_names = ['get', 'post', 'delete', 'head', 'options', 'patch', 'put']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SecurityCompanyDetailSerializer
        elif self.action in ['create', 'update_my', 'partial_update_my']:
            return SecurityCompanyCreateUpdateSerializer
        elif self.action == 'my':
            return SecurityCompanyMySerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update_my', 'partial_update_my', 'destroy_my']:
            permission_classes = [IsAuthenticated, IsCompanyOwnerOnly]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsCompanyOwnerOrAdmin]
        elif self.action == 'my':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        now = timezone.now()
        queryset = queryset.annotate(
            services_count=Count('services'),
            avg_rating=Avg('reviews__rating')
        ).select_related('user')

        active_discounts = ServiceDiscount.objects.filter(
            start_date__lte=now,
            end_date__gte=now
        )

        if self.action in ['retrieve', 'my']:
            queryset = queryset.prefetch_related(
                Prefetch('services', queryset=Service.objects.prefetch_related(
                    Prefetch('discounts', queryset=active_discounts)
                )),
                Prefetch('reviews', queryset=Review.objects.select_related('user'))
            )

        if self.action == 'list':
            queryset = queryset.prefetch_related(
                Prefetch('services', queryset=Service.objects.prefetch_related(
                    Prefetch('discounts', queryset=active_discounts)
                ))
            )

        if self.request.user.is_authenticated and self.action == 'destroy':
            if not self.request.user.is_staff:
                queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        if SecurityCompany.objects.filter(user=self.request.user).exists():
            raise AlreadyHaveCompanyError()
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Http404:
            raise CompanyPermissionDeniedError()

    @action(detail=False, methods=['get'], filter_backends=[])
    def my(self, request):
        company = SecurityCompany.objects.filter(user=request.user).first()
        if not company:
            raise NoCompanyError()
        now = timezone.now()
        active_discounts = ServiceDiscount.objects.filter(
            start_date__lte=now,
            end_date__gte=now
        )
        company = SecurityCompany.objects.annotate(
            avg_rating=Avg('reviews__rating')
        ).prefetch_related(
            Prefetch('services', queryset=Service.objects.prefetch_related(
                Prefetch('discounts', queryset=active_discounts)
            )),
            Prefetch('reviews', queryset=Review.objects.select_related('user')),
            Prefetch('services__requests',
                     queryset=ServiceRequest.objects.select_related('user'))
        ).get(pk=company.pk)

        serializer = self.get_serializer(company)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], filter_backends=[])
    def update_my(self, request):
        return self._update_my_company(request, partial=False)

    @action(detail=False, methods=['patch'], filter_backends=[])
    def partial_update_my(self, request):
        return self._update_my_company(request, partial=True)

    def _update_my_company(self, request, partial=False):
        company = SecurityCompany.objects.filter(user=request.user).first()
        if not company:
            raise NoCompanyError()
        serializer = self.get_serializer(
            company,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=['delete'], filter_backends=[])
    def destroy_my(self, request):
        company = SecurityCompany.objects.filter(user=request.user).first()
        if not company:
            raise NoCompanyError()
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        raise CompanyActionForbiddenError()

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        raise CompanyActionForbiddenError()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        category = self.get_object()
        now = timezone.now()
        active_discounts = ServiceDiscount.objects.filter(
            start_date__lte=now,
            end_date__gte=now
        )
        services = Service.objects.filter(
            categories=category
        ).select_related('security_company').prefetch_related(
            Prefetch('discounts', queryset=active_discounts)
        )
        serializer = SimpleServiceSerializer(services, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    permission_classes = [IsServiceOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ServiceCreateUpdateSerializer
        elif self.action == 'requests':
            return SimpleServiceRequestSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'requests':
            return [IsAuthenticated(), IsServiceOwnerOrReadOnly()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        now = timezone.now()
        active_discounts = ServiceDiscount.objects.filter(
            start_date__lte=now,
            end_date__gte=now
        )
        if self.action in ['list', 'retrieve']:
            queryset = queryset.select_related('security_company').prefetch_related(
                'categories',
                Prefetch('discounts', queryset=active_discounts)
            )
        if self.request.user.is_authenticated and self.action in ['update', 'partial_update', 'destroy']:
            queryset = queryset.filter(security_company__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        user_companies = SecurityCompany.objects.filter(user=self.request.user)
        if not user_companies.exists():
            raise ServicePermissionDeniedError("У вас нет компании. Сначала создайте компанию.")
        user_company = user_companies.first()
        serializer.save(security_company=user_company)

    def perform_update(self, serializer):
        if 'security_company' in serializer.validated_data:
            serializer.validated_data.pop('security_company')
        serializer.save()

    @action(detail=True, methods=['get'])
    def requests(self, request, pk=None):
        service = self.get_object()
        if service.security_company.user != request.user and not request.user.is_staff:
            raise ServicePermissionDeniedError("Вы не можете просматривать заявки на эту услугу")
        service_requests = ServiceRequest.objects.filter(service=service).select_related('user', 'service').order_by('-created_at')
        serializer = self.get_serializer(service_requests, many=True)
        return Response(serializer.data)


class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'service__security_company', 'user']
    search_fields = [
        'description',
        'service__name',
        'user__name',
        'user__surname',
    ]
    ordering_fields = ['created_at', 'updated_at', 'status', 'id']
    ordering = ['-created_at']
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'create':
            return ServiceRequestCreateSerializer
        elif self.action == 'partial_update':
            return ServiceRequestUpdateSerializer
        return ServiceRequestSerializer

    def get_permissions(self):
        if self.action in ['create', 'my', 'company']:
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsRequestOwnerOrAdmin]
        elif self.action in ['retrieve', 'partial_update']:
            permission_classes = [IsAuthenticated, IsRequestOwnerOrCompanyOwnerOrAdmin]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'user',
            'service',
            'service__security_company'
        )
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        if not user.is_staff:
            user_requests = queryset.filter(user=user)
            user_company = SecurityCompany.objects.filter(user=user)
            if user_company.exists():
                company_services = Service.objects.filter(security_company=user_company)
                company_requests = queryset.filter(service__in=company_services)
                queryset = (user_requests | company_requests).distinct() # объединяем запрсы
            else:
                queryset = user_requests

        return queryset

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {'detail': 'У вас нет прав для просмотра всех заявок'},
                status=status.HTTP_403_FORBIDDEN
            )
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        Частичное обновление заявки.
        - Все поля доступны для отправки
        - Валидация прав происходит в сериализаторе
        """
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='my')
    def my_requests(self, request):
        user_requests = ServiceRequest.objects.filter(
            user=request.user
        ).select_related(
            'service',
            'service__security_company'
        )

        filtered_requests = self.filter_queryset(user_requests)

        serializer = self.get_serializer(filtered_requests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='company')
    def company_requests(self, request):
        user_companies = SecurityCompany.objects.filter(user=request.user)

        if not user_companies.exists():
            return Response(
                {'detail': 'У вас нет компаний'},
                status=status.HTTP_404_NOT_FOUND
            )

        company_services = Service.objects.filter(
            security_company__in=user_companies
        )

        company_requests = ServiceRequest.objects.filter(
            service__in=company_services
        ).select_related(
            'user',
            'service',
            'service__security_company'
        )

        filtered_requests = self.filter_queryset(company_requests)

        serializer = self.get_serializer(filtered_requests, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rating', 'security_company', 'user']
    search_fields = ['comment', 'security_company__name', 'user__email', 'user__name',
                     'user__surname']
    ordering_fields = ['created_at', 'rating', 'id']
    ordering = ['-created_at']
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ReviewUpdateSerializer
        elif self.action == 'list':
            return SimpleReviewSerializer
        return ReviewSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'my':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsReviewOwnerOrAdmin]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsReviewOwnerOrAdmin]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'user',
            'security_company'
        )
        return queryset

    @action(detail=False, methods=['get'], url_path='my')
    def my_reviews(self, request):
        user_reviews = Review.objects.filter(
            user=request.user
        ).select_related(
            'security_company'
        )
        filtered_reviews = self.filter_queryset(user_reviews)

        serializer = self.get_serializer(filtered_reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='company')
    def company_reviews(self, request):
        user_companies = SecurityCompany.objects.filter(user=request.user)

        if not user_companies.exists():
            return Response(
                {'detail': 'У вас нет компаний'},
                status=status.HTTP_404_NOT_FOUND
            )
        company_reviews = Review.objects.filter(
            security_company__in=user_companies
        ).select_related(
            'user',
            'security_company'
        )

        filtered_reviews = self.filter_queryset(company_reviews)

        serializer = self.get_serializer(filtered_reviews, many=True)
        return Response(serializer.data)


class UserFavoriteViewSet(viewsets.ModelViewSet):
    queryset = UserFavorite.objects.all()
    serializer_class = UserFavoriteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['service__security_company']
    search_fields = ['service__name', 'service__description']
    ordering_fields = ['created_at', 'id']
    ordering = ['-created_at']
    http_method_names = ['get', 'post', 'delete', 'head', 'options']  # Только GET, POST, DELETE

    def get_serializer_class(self):
        if self.action == 'list':  # Для администраторов
            return SimpleUserFavoriteSerializer
        elif self.action == 'create':
            return UserFavoriteCreateSerializer
        return UserFavoriteSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'my':
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsFavoriteOwnerOrAdmin]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list':  # Для администраторов
            queryset = queryset.select_related('user', 'service', 'service__security_company')
        elif self.action in ['my', 'destroy']:  # Для пользователей
            queryset = queryset.filter(user=self.request.user).select_related(
                'service',
                'service__security_company'
            )

        return queryset.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {'detail': 'У вас нет прав для просмотра всех избранных'},
                status=status.HTTP_403_FORBIDDEN
            )

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Метод не разрешен'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Метод не разрешен'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Метод не разрешен'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='my')
    def my_favorites(self, request):
        favorites = UserFavorite.objects.filter(
            user=request.user
        ).select_related(
            'service',
            'service__security_company'
        ).order_by('-created_at')

        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)


class ServiceDiscountViewSet(viewsets.ModelViewSet):
    queryset = ServiceDiscount.objects.all()
    serializer_class = ServiceDiscountSerializer
    permission_classes = [IsDiscountOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['start_date', 'end_date', 'discount_percent']

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return ServiceDiscount.objects.all()
        if self.request.method in permissions.SAFE_METHODS:
            now = timezone.now()
            active_discounts = ServiceDiscount.objects.filter(
                start_date__lte=now,
                end_date__gte=now
            )
            if user.is_authenticated:
                user_companies = SecurityCompany.objects.filter(user=user)
                if user_companies.exists():
                    user_services = Service.objects.filter(security_company__in=user_companies)
                    my_discounts = ServiceDiscount.objects.filter(service__in=user_services)
                    return (active_discounts | my_discounts).distinct()

            return active_discounts

        user_companies = SecurityCompany.objects.filter(user=user)
        user_services = Service.objects.filter(security_company__in=user_companies)
        return ServiceDiscount.objects.filter(service__in=user_services)

    def perform_create(self, serializer):
        service = serializer.validated_data.get('service')
        if not service.security_company.user == self.request.user:
            raise DiscountPermissionDeniedError()
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')
        if start_date >= end_date:
            raise DiscountDateError()
        serializer.save()


class AnalyticsView(generics.GenericAPIView):

    permission_classes = [IsAdminUser]
    serializer_class = AnalyticsSerializer

    def get(self, request):
        """Получение общей статистики."""
        # Статистика по компаниям
        companies_stats = SecurityCompany.objects.annotate(
            services_count=Count('services'),
            avg_rating=Avg('reviews__rating'),
            total_requests=Count('services__requests')
        ).values('id', 'name', 'services_count', 'avg_rating', 'total_requests')

        # Статистика по услугам
        services_stats = Service.objects.annotate(
            favorites_count=Count('favorites'),
            requests_count=Count('requests'),
            active_discounts=Count('discounts', filter=Q(
                discounts__start_date__lte=timezone.now(),
                discounts__end_date__gte=timezone.now()
            ))
        ).values('id', 'name', 'price', 'favorites_count', 'requests_count', 'active_discounts')

        # Статистика по пользователям
        users_stats = User.objects.annotate(
            requests_count=Count('service_requests'),
            reviews_count=Count('reviews'),
            favorites_count=Count('favorites')
        ).values('id', 'email', 'name', 'requests_count', 'reviews_count', 'favorites_count')

        # Общая статистика
        total_stats = {
            'total_companies': SecurityCompany.objects.count(),
            'total_services': Service.objects.count(),
            'total_users': User.objects.count(),
            'total_requests': ServiceRequest.objects.count(),
            'total_reviews': Review.objects.count(),
            'avg_company_rating': Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0,
            'requests_by_status': dict(ServiceRequest.objects.values_list('status').annotate(
                count=Count('id')
            ))
        }

        return Response({
            'companies_stats': list(companies_stats),
            'services_stats': list(services_stats),
            'users_stats': list(users_stats),
            'total_stats': total_stats
        })


class CompanyAnalyticsView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class=CompanyAnalyticsSerializer

    def get(self, request, company_id):
        """Получение аналитики по компании."""
        try:
            company = SecurityCompany.objects.get(id=company_id)

            if not (request.user.is_staff or company.user == request.user):
                raise AnalyticsPermissionDeniedError()

            # Статистика по услугам компании
            services_stats = Service.objects.filter(security_company=company).annotate(
                requests_count=Count('requests'),
                favorites_count=Count('favorites'),
                total_revenue=Sum('requests__service__price', filter=Q(requests__status='completed'))
            ).values('id', 'name', 'price', 'requests_count', 'favorites_count', 'total_revenue')

            # Статистика по заявкам
            requests_stats = ServiceRequest.objects.filter(service__security_company=company).aggregate(
                total=Count('id'),
                pending=Count('id', filter=Q(status='pending')),
                confirmed=Count('id', filter=Q(status='confirmed')),
                in_progress=Count('id', filter=Q(status='in_progress')),
                completed=Count('id', filter=Q(status='completed')),
                cancelled=Count('id', filter=Q(status='cancelled'))
            )

            # Статистика по отзывам
            reviews_stats = Review.objects.filter(security_company=company).aggregate(
                total=Count('id'),
                avg_rating=Avg('rating'),
                rating_5=Count('id', filter=Q(rating=5)),
                rating_4=Count('id', filter=Q(rating=4)),
                rating_3=Count('id', filter=Q(rating=3)),
                rating_2=Count('id', filter=Q(rating=2)),
                rating_1=Count('id', filter=Q(rating=1))
            )

            # Доход за последние 30 дней
            thirty_days_ago = timezone.now() - timedelta(days=30)
            recent_revenue = ServiceRequest.objects.filter(
                service__security_company=company,
                status='completed',
                created_at__gte=thirty_days_ago
            ).aggregate(
                revenue=Sum('service__price')
            )['revenue'] or 0

            return Response({
                'company': {
                    'id': company.id,
                    'name': company.name,
                    'avg_rating': company.average_rating
                },
                'services_stats': list(services_stats),
                'requests_stats': requests_stats,
                'reviews_stats': reviews_stats,
                'recent_revenue': float(recent_revenue),
                'period': 'last_30_days'
            })

        except SecurityCompany.DoesNotExist:
            raise CompanyNotFoundError()