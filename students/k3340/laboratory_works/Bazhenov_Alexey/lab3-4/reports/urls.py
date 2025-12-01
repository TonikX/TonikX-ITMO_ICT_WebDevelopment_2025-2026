from django.urls import path

from .views import QuarterlyReportView

urlpatterns = [
    path('reports/quarterly/', QuarterlyReportView.as_view(), name='reports-quarterly'),
]

