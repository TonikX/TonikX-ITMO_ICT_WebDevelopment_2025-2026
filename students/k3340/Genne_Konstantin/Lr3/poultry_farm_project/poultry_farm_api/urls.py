from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .views import *


router = DefaultRouter()
router.register(r'breeds', BreedViewSet, basename='breed')
router.register(r'diets', DietViewSet, basename='diet')
router.register(r'breed-diets', BreedDietViewSet, basename='breed-diet')
router.register(r'hens', HenViewSet, basename='hen')
router.register(r'hen-eggs', HenEggsViewSet, basename='hen-eggs')
router.register(r'cages', CageViewSet, basename='cage')
router.register(r'hen-cages', HenCageViewSet, basename='hen-cage')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'employee-cages', EmployeeCageViewSet, basename='employee-cage')
router.register(r'employments', EmploymentViewSet, basename='employment')


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('', include(router.urls)),
    
    path('reports/eggs-by-characteristics/', EggsByCharacteristicsView.as_view(), name='eggs-by-characteristics'),
    path('reports/top-workshop/<str:breed_name>/', TopWorkshopByBreedView.as_view(), name='top-workshop-by-breed'),
    path('reports/employee-average-eggs/', EmployeeAvgEggsView.as_view(), name='employee-average-eggs'),
    path('reports/breed-distribution/', BreedDistributionView.as_view(), name='breed-distribution'),
    path('reports/breed-efficiency-difference/', BreedEfficiencyDiffView.as_view(), name='breed-efficiency-difference'),
    path('reports/monthly/', MonthlyReportView.as_view(), name='monthly-report'),

    path('hens/<int:id>/detail/', HenDetailView.as_view(), name='hen-detail'),
    path('cages/<int:id>/detail/', CageDetailView.as_view(), name='cage-detail'),
]