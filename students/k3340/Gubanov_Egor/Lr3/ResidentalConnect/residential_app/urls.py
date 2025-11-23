from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BuildingViewSet,
    ApartmentViewSet,
    ServiceCategoryViewSet,
    ServiceRequestViewSet,
    MeterReadingViewSet,
    # Generic-классы согласно ТЗ
    RequestListApartmentView,
    RequestListCategoryView,
    RequestDetailView
)

router = DefaultRouter()
router.register(r'buildings', BuildingViewSet, basename='building')
router.register(r'apartments', ApartmentViewSet, basename='apartment')
router.register(r'categories', ServiceCategoryViewSet, basename='category')
router.register(r'service-requests', ServiceRequestViewSet, basename='service-request')
router.register(r'meter-readings', MeterReadingViewSet, basename='meter-reading')

# URL-маршруты для Generic-классов согласно ТЗ
urlpatterns = [
    path('', include(router.urls)),
    # Эндпоинты для Generic-классов
    path('requests-with-apartment/', RequestListApartmentView.as_view(), name='request-list-apartment'),
    path('requests-with-category/', RequestListCategoryView.as_view(), name='request-list-category'),
    path('request-detail/<int:pk>/', RequestDetailView.as_view(), name='request-detail'),
]

