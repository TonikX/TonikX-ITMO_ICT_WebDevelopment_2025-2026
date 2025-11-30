"""
URL configuration for library API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema
from .views import (
    AuthorViewSet, PublisherViewSet, BookSectionViewSet, BookViewSet,
    HallViewSet, ReaderViewSet, BookCopyViewSet, BookIssueViewSet,
    HallBookStockViewSet, StaffViewSet
)
from .auth_views import StaffTokenObtainPairView


# Декоратор для refresh токена
class TokenRefreshViewWithDocs(TokenRefreshView):
    """View для обновления JWT токена. Не требует аутентификации."""
    permission_classes = [AllowAny]  # Явно указываем, что не требуется аутентификация
    @extend_schema(
        summary='Обновить JWT токен',
        description='Обновить access токен используя refresh токен. Возвращает новый access токен. Аутентификация не требуется.',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'refresh': {
                        'type': 'string',
                        'description': 'Refresh токен для обновления access токена',
                        'example': 'eyJ0eXAiOiJKV1QiLCJhbGc...'
                    }
                },
                'required': ['refresh']
            }
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'access': {
                        'type': 'string',
                        'description': 'Новый JWT access токен',
                        'example': 'eyJ0eXAiOiJKV1QiLCJhbGc...'
                    }
                }
            },
            401: {
                'type': 'object',
                'description': 'Неверный или истёкший refresh токен'
            }
        },
        tags=['Authentication'],
        operation_id='refresh_token',
        auth=[],  # Явно исключаем из DEFAULT_SECURITY
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'publishers', PublisherViewSet, basename='publisher')
router.register(r'book-sections', BookSectionViewSet, basename='book-section')
router.register(r'books', BookViewSet, basename='book')
router.register(r'halls', HallViewSet, basename='hall')
router.register(r'readers', ReaderViewSet, basename='reader')
router.register(r'book-copies', BookCopyViewSet, basename='book-copy')
router.register(r'book-issues', BookIssueViewSet, basename='book-issue')
router.register(r'hall-book-stocks', HallBookStockViewSet, basename='hall-book-stock')
router.register(r'staff', StaffViewSet, basename='staff')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', StaffTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshViewWithDocs.as_view(), name='token_refresh'),
]

