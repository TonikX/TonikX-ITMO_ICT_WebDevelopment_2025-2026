from rest_framework import serializers
from .models import (
    Client, Passport, Deposit, DepositType, DepositSchedule, Currency,
    Credit, CreditType, CreditPaymentSchedule, EmployeePosition
)

class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        exclude = ('client',)

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('code', 'name')

class EmployeePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePosition
        fields = '__all__'

class DepositTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositType
        fields = '__all__'

class DepositScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositSchedule
        exclude = ('deposit',)

class CreditTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditType
        fields = '__all__'

class CreditPaymentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditPaymentSchedule
        exclude = ('credit',)

class ClientSerializer(serializers.ModelSerializer):
    passports = PassportSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

class DepositSerializer(serializers.ModelSerializer):
    deposit_type = DepositTypeSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)
    employee_position = EmployeePositionSerializer(read_only=True)
    schedule = DepositScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Deposit
        fields = '__all__'

class CreditSerializer(serializers.ModelSerializer):
    credit_type = CreditTypeSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)
    employee_position = EmployeePositionSerializer(read_only=True)
    payment_schedule = CreditPaymentScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Credit
        fields = '__all__'