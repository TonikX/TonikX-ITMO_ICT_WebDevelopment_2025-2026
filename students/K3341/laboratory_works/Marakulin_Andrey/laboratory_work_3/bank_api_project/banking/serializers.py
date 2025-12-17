from rest_framework import serializers
from .models import *


# --- Вспомогательные сериализаторы ---

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


# --- Основные сериализаторы с вложенностью ---

class ClientSerializer(serializers.ModelSerializer):
    # Вложенность: Один Клиент -> Много Паспортов
    # read_only=True значит, что мы показываем паспорта при чтении,
    # но при создании клиента не обязаны сразу передавать паспорта.
    passports = PassportSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'fio', 'address', 'phone', 'email', 'passports']


class DepositSerializer(serializers.ModelSerializer):
    # Вложенность: Один Вклад -> Много Начислений
    accruals = AccrualScheduleSerializer(many=True, read_only=True, source='accruals')

    class Meta:
        model = Deposit
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    # Вложенность: Один Кредит -> Много Выплат
    payouts = PayoutScheduleSerializer(many=True, read_only=True, source='payouts')

    class Meta:
        model = Loan
        fields = '__all__'


# --- Обычные сериализаторы для остальных справочников ---

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