from rest_framework import viewsets, generics, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from datetime import timedelta

from .models import (
    SecurityCompany, Category, Service, ServiceCategory,
    ServiceDiscount, ServiceRequest, Review, UserFavorite
)
from .serializers import (
    UserSerializer, SecurityCompanySerializer, CategorySerializer,
    ServiceSerializer, ServiceDiscountSerializer, ServiceRequestSerializer,
    ReviewSerializer, UserFavoriteSerializer,
    ServiceWithCompanySerializer, CompanyWithServicesSerializer, SimpleServiceSerializer, AnalyticsSerializer,
    ServiceRequestCreateSerializer
)
from .permissions import (
    IsCompanyOwner, IsCompanyOwnerOrReadOnly,
    IsServiceOwnerOrReadOnly, IsDiscountOwnerOrReadOnly,
    IsRequestOwnerOrCompanyOwner
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'name', 'surname']
    ordering_fields = ['created_at', 'email']

    @action(detail=True, methods=['get'])
    def requests(self, request, pk=None):
        user = self.get_object()
        requests = ServiceRequest.objects.filter(user=user)
        serializer = ServiceRequestSerializer(requests, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def favorites(self, request, pk=None):
        user = self.get_object()
        favorites = UserFavorite.objects.filter(user=user)
        serializer = UserFavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        user = self.get_object()
        reviews = Review.objects.filter(user=user)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class SecurityCompanyViewSet(viewsets.ModelViewSet):
    queryset = SecurityCompany.objects.all()
    serializer_class = SecurityCompanySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'average_rating']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsCompanyOwner]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Проверяем, что у пользователя еще нет компании
        if SecurityCompany.objects.filter(user=self.request.user).exists():
            raise ValidationError({"detail": "У вас уже есть компания"})
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Для методов редактирования показываем только свои компании
        if self.request.user.is_authenticated and self.action in ['update', 'partial_update', 'destroy']:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        company = self.get_object()
        services = Service.objects.filter(security_company=company)
        serializer = SimpleServiceSerializer(services, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        company = self.get_object()
        reviews = Review.objects.filter(security_company=company)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], serializer_class=CompanyWithServicesSerializer)
    def detail_with_services(self, request, pk=None):
        company = self.get_object()
        serializer = self.get_serializer(company)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        category = self.get_object()
        services = Service.objects.filter(categories=category)
        serializer = SimpleServiceSerializer(services, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    permission_classes = [IsServiceOwnerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Для методов редактирования показываем только услуги своих компаний
        if self.request.user.is_authenticated and self.action in ['update', 'partial_update', 'destroy']:
            queryset = queryset.filter(security_company__user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        # Проверяем, что у пользователя есть компания
        user_companies = SecurityCompany.objects.filter(user=self.request.user)
        if not user_companies.exists():
            raise PermissionDenied("У вас нет компании. Сначала создайте компанию.")
        # Берем первую компанию пользователя (если у него одна компания)
        user_company = user_companies.first()
        # Проверяем, не пытается ли пользователь указать чужую компанию
        company = serializer.validated_data.get('security_company')
        if company and company.user != self.request.user:
            raise PermissionDenied("Вы не можете создавать услуги для чужой компании")
        # Если компания не указана, используем компанию пользователя
        if not company:
            serializer.save(security_company=user_company)
        else:
            serializer.save()

    @action(detail=True, methods=['get'], serializer_class=ServiceWithCompanySerializer)
    def detail_with_company(self, request, pk=None):
        service = self.get_object()
        serializer = self.get_serializer(service)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def discounts(self, request, pk=None):
        service = self.get_object()
        discounts = ServiceDiscount.objects.filter(service=service)
        serializer = ServiceDiscountSerializer(discounts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def requests(self, request, pk=None):
        service = self.get_object()
        service_requests = ServiceRequest.objects.filter(service=service)
        serializer = ServiceRequestSerializer(service_requests, many=True)
        return Response(serializer.data)


class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated, IsRequestOwnerOrCompanyOwner]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'status']

    def get_serializer_class(self):
        if self.action == 'create':
            return ServiceRequestCreateSerializer
        return ServiceRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ServiceRequest.objects.all()
        user_requests = ServiceRequest.objects.filter(user=user)
        user_companies = SecurityCompany.objects.filter(user=user)

        if user_companies.exists():
            company_services = Service.objects.filter(security_company__in=user_companies)
            company_requests = ServiceRequest.objects.filter(service__in=company_services)
            # Объединяем: свои заявки + заявки на услуги своих компаний
            return (user_requests | company_requests).distinct()

        return user_requests

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'])
    def change_status(self, request, pk=None):
        request_obj = self.get_object()
        new_status = request.data.get('status')
        comment = request.data.get('admin_comment', '')

        if new_status not in dict(ServiceRequest.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, кто может менять статус:
        user = request.user

        if user.is_staff:
            pass
        elif hasattr(request_obj, 'service') and hasattr(request_obj.service, 'security_company'):
            if request_obj.service.security_company.user == user:
                pass
            else:
                return Response(
                    {'error': 'Вы не можете менять статус этой заявки'},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif user == request_obj.user:
            return Response(
                {'error': 'Вы не можете менять статус своей заявки'},
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            return Response(
                {'error': 'Доступ запрещен'},
                status=status.HTTP_403_FORBIDDEN
            )
        request_obj.status = new_status
        if comment:
            request_obj.admin_comment = comment
        request_obj.save()

        serializer = self.get_serializer(request_obj)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at', 'rating']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and self.action in ['update', 'partial_update', 'destroy']:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class UserFavoriteViewSet(viewsets.ModelViewSet):
    queryset = UserFavorite.objects.all()
    serializer_class = UserFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserFavorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_favorites(self, request):
        favorites = UserFavorite.objects.filter(user=request.user)
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
            # Все активные скидки
            now = timezone.now()
            active_discounts = ServiceDiscount.objects.filter(
                start_date__lte=now,
                end_date__gte=now
            )

            # Если пользователь авторизован и владелец компании,
            # добавляем ЕГО скидки (даже неактивные)
            if user.is_authenticated:
                user_companies = SecurityCompany.objects.filter(user=user)
                if user_companies.exists():
                    user_services = Service.objects.filter(security_company__in=user_companies)
                    my_discounts = ServiceDiscount.objects.filter(service__in=user_services)
                    # Объединяем: активные скидки + мои скидки
                    return (active_discounts | my_discounts).distinct()

            return active_discounts

        user_companies = SecurityCompany.objects.filter(user=user)
        user_services = Service.objects.filter(security_company__in=user_companies)
        return ServiceDiscount.objects.filter(service__in=user_services)

    def perform_create(self, serializer):
        service = serializer.validated_data.get('service')

        # Проверяем, что пользователь - владелец компании услуги
        if not service.security_company.user == self.request.user:
            raise PermissionDenied("Вы не можете создавать скидки для чужих услуг")

        # Дополнительная проверка: даты скидки
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')

        if start_date >= end_date:
            raise ValidationError({"end_date": "Дата окончания должна быть позже даты начала"})

        serializer.save()


class AnalyticsView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AnalyticsSerializer

    def get(self, request):
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
    permission_classes = [IsAuthenticated]

    def get(self, request, company_id):
        try:
            company = SecurityCompany.objects.get(id=company_id)

            # Проверка прав доступа
            if not (request.user.is_staff or company.user == request.user):
                return Response(
                    {'error': 'Permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )

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
            return Response(
                {'error': 'Company not found'},
                status=status.HTTP_404_NOT_FOUND
            )