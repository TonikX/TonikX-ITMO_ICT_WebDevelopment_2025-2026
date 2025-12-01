from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AuthorViewSet, BookViewSet, ContractViewSet,
    CustomerViewSet, OrderViewSet, BookAuthorViewSet,
    BookEditorViewSet, OrderItemViewSet
)

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)

router.register(r'book-authors', BookAuthorViewSet)
router.register(r'book-editors', BookEditorViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
