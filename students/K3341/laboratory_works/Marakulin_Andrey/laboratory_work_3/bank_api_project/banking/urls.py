from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'passports', PassportViewSet)
router.register(r'currencies', CurrencyViewSet)
router.register(r'exchange-rates', ExchangeRateViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'occupied-positions', OccupiedPositionViewSet)
router.register(r'deposit-types', DepositTypeViewSet)
router.register(r'deposits', DepositViewSet)
router.register(r'accrual-schedules', AccrualScheduleViewSet)
router.register(r'loan-types', LoanTypeViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'payout-schedules', PayoutScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]