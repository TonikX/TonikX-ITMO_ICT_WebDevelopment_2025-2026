from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AuthorViewSet,
    BookViewSet,
    ReadingHallViewSet,
    ReaderViewSet,
    BookCopyViewSet,
    LoanViewSet,
    MonthlyReportView,
)

router = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"books", BookViewSet, basename="book")
router.register(r"halls", ReadingHallViewSet, basename="hall")
router.register(r"readers", ReaderViewSet, basename="reader")
router.register(r"copies", BookCopyViewSet, basename="copy")
router.register(r"loans", LoanViewSet, basename="loan")

urlpatterns = [
    path("", include(router.urls)),
    path("reports/monthly/", MonthlyReportView.as_view(), name="monthly-report"),
]
