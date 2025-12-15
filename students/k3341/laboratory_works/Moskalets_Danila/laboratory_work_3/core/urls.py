from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'companies', views.SecurityCompanyViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'requests', views.ServiceRequestViewSet, basename='request')
router.register(r'reviews', views.ReviewViewSet)
router.register(r'favorites', views.UserFavoriteViewSet, basename='favorite')
router.register(r'discounts', views.ServiceDiscountViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Аналитика
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('analytics/companies/<int:company_id>/', views.CompanyAnalyticsView.as_view(), name='company-analytics'),
]