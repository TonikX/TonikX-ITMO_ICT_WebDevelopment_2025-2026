from rest_framework import serializers
from .models import *



class AccrualScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccrualSchedule
        fields = '__all__'


class PayoutScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutSchedule
        fields = '__all__'


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = '__all__'



class ClientSerializer(serializers.ModelSerializer):
    passports = PassportSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'fio', 'address', 'phone', 'email', 'passports']


class DepositSerializer(serializers.ModelSerializer):
    accruals = AccrualScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Deposit
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    payouts = PayoutScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Loan
        fields = '__all__'



class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class OccupiedPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccupiedPosition
        fields = '__all__'


class DepositTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositType
        fields = '__all__'


class LoanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanType
        fields = '__all__'