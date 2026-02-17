from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from api.extended_views import HotelStatisticsView, ClientStatisticsView, EmployeeScheduleView

router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'cleaning', views.CleaningScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('report/', views.ReportView.as_view(), name='report'),
    path('statistics/hotel/', HotelStatisticsView.as_view(), name='hotel-statistics'),
    path('statistics/clients/', ClientStatisticsView.as_view(), name='client-statistics'),
    path('employee-schedule/', EmployeeScheduleView.as_view(), name='employee-schedule'),
]
