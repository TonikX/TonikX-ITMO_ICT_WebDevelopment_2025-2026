from rest_framework import viewsets, permissions
from .models import *
from .serializers import *

class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

class ClientViewSet(BaseViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class PassportViewSet(BaseViewSet):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer

class CurrencyViewSet(BaseViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class ExchangeRateViewSet(BaseViewSet):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer

class PositionViewSet(BaseViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class EmployeeViewSet(BaseViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class OccupiedPositionViewSet(BaseViewSet):
    queryset = OccupiedPosition.objects.all()
    serializer_class = OccupiedPositionSerializer

class DepositTypeViewSet(BaseViewSet):
    queryset = DepositType.objects.all()
    serializer_class = DepositTypeSerializer

class DepositViewSet(BaseViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer

class AccrualScheduleViewSet(BaseViewSet):
    queryset = AccrualSchedule.objects.all()
    serializer_class = AccrualScheduleSerializer

class LoanTypeViewSet(BaseViewSet):
    queryset = LoanType.objects.all()
    serializer_class = LoanTypeSerializer

class LoanViewSet(BaseViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class PayoutScheduleViewSet(BaseViewSet):
    queryset = PayoutSchedule.objects.all()
    serializer_class = PayoutScheduleSerializer