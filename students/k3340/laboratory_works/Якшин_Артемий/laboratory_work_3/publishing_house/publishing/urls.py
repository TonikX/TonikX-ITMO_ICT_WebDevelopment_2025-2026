from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet, AuthorViewSet, BookViewSet, ContractViewSet,
    CustomerViewSet, OrderViewSet, BookAuthorViewSet, BookEditorViewSet,
    OrderItemViewSet,
    BooksByAuthorReportView, ChiefEditorsReportView, EditorsPerBookReportView,
    ContractsByMonthReportView, TopManagersReportView, QuarterlyContractsReportView
)

app_name = 'publishing'

# Router для CRUD ViewSets
router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')
router.register(r'contracts', ContractViewSet, basename='contract')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'book-authors', BookAuthorViewSet, basename='book-author')
router.register(r'book-editors', BookEditorViewSet, basename='book-editor')
router.register(r'order-items', OrderItemViewSet, basename='order-item')

# URL patterns
urlpatterns = [
    # CRUD endpoints
    path('', include(router.urls)),

    # Report endpoints
    path('reports/books-by-author/', BooksByAuthorReportView.as_view(), name='books-by-author-report'),
    path('reports/chief-editors/', ChiefEditorsReportView.as_view(), name='chief-editors-report'),
    path('reports/editors-per-book/', EditorsPerBookReportView.as_view(), name='editors-per-book-report'),
    path('reports/contracts-by-month/', ContractsByMonthReportView.as_view(), name='contracts-by-month-report'),
    path('reports/top-managers/', TopManagersReportView.as_view(), name='top-managers-report'),
    path('reports/quarterly-contracts/', QuarterlyContractsReportView.as_view(), name='quarterly-contracts-report'),
]
