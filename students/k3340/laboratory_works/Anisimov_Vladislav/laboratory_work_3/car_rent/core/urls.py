from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "core"

router = DefaultRouter()
router.register(r'car_infos', CarInfoAPIViewSet)
router.register(r'cars', CarAPIViewSet)
router.register(r'car_instances', CarInstanceAPIViewSet)
router.register(r'fines', FineAPIViewSet)
router.register(r'car_crashes', CarCrashAPIViewSet)
router.register(r'clients', ClientAPIViewSet)
router.register(r'workers', WorkerAPIViewSet)
router.register(r'rent_contracts', RentContractAPIViewSet)
#router.register(r'users', UserAPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('users', UserListAPIView.as_view()),
    path('users/', UserListAPIViewSet.as_view()),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view()),
    path('times_rented', TimesRentedAPIView.as_view()),
    path('days_rented', DaysRentedAPIView.as_view()),
    path('profit_by_car', ProfitByCarAPIView.as_view()),
    path('fines_by_client', FinesByClientAPIView.as_view()),
]