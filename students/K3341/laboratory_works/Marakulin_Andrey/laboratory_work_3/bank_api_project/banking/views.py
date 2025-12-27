from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg, Min, Max
from .models import *
from .serializers import *


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]


class ClientViewSet(BaseViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=True, methods=['get'])
    def portfolio(self, request, pk=None):
        client = self.get_object()

        total_deposits = Deposit.objects.filter(
            passport__client=client
        ).aggregate(total=Sum('deposit_sum'))['total'] or 0

        total_loans = Loan.objects.filter(
            passport__client=client
        ).aggregate(total=Sum('sum_credit'))['total'] or 0

        balance = total_deposits - total_loans

        return Response({
            'client': client.fio,
            'total_deposits_amount': total_deposits,
            'total_loans_amount': total_loans,
            'net_balance': balance
        })


class PassportViewSet(BaseViewSet):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer


class CurrencyViewSet(BaseViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        currency = self.get_object()
        stats = ExchangeRate.objects.filter(currency=currency).aggregate(
            min_sell=Min('sell_price'),
            max_sell=Max('sell_price'),
            avg_sell=Avg('sell_price')
        )

        return Response({
            'currency': currency.code,
            'stats': stats
        })


class ExchangeRateViewSet(BaseViewSet):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer


class EmployeeViewSet(BaseViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=True, methods=['get'])
    def kpi(self, request, pk=None):
        employee = self.get_object()

        positions_ids = OccupiedPosition.objects.filter(employee=employee).values_list('id', flat=True)

        deposits_count = Deposit.objects.filter(processed_by__in=positions_ids).count()
        deposits_sum = Deposit.objects.filter(processed_by__in=positions_ids).aggregate(Sum('deposit_sum'))[
                           'deposit_sum__sum'] or 0

        loans_count = Loan.objects.filter(processed_by__in=positions_ids).count()
        loans_sum = Loan.objects.filter(processed_by__in=positions_ids).aggregate(Sum('sum_credit'))[
                        'sum_credit__sum'] or 0

        return Response({
            'employee': employee.fio,
            'processed_deposits': {
                'count': deposits_count,
                'total_volume': deposits_sum
            },
            'processed_loans': {
                'count': loans_count,
                'total_volume': loans_sum
            },
            'total_operations': deposits_count + loans_count
        })


class PositionViewSet(BaseViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


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