from rest_framework import serializers
from .models import *
from datetime import date


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

    def validate_date_issue(self, value):
        if value > date.today():
            raise serializers.ValidationError("Дата выдачи паспорта не может быть в будущем!")
        return value



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

    def validate(self, data):
        deposit_type = data.get('deposit_type')
        deposit_sum = data.get('deposit_sum')
        start_date = data.get('deposit_date')
        end_date = data.get('return_date')

        if deposit_type and deposit_sum:
            if deposit_sum < deposit_type.min_sum:
                raise serializers.ValidationError({
                    "deposit_sum": f"Сумма меньше минимальной ({deposit_type.min_sum}) для тарифа '{deposit_type.name}'"
                })

        if start_date and end_date:
            if end_date <= start_date:
                raise serializers.ValidationError({
                    "return_date": "Дата возврата должна быть позже даты открытия вклада."
                })

        return data


class LoanSerializer(serializers.ModelSerializer):
    payouts = PayoutScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Loan
        fields = '__all__'

    def validate(self, data):
        date_issue = data.get('date_issue')
        close_date = data.get('close_date')
        sum_credit = data.get('sum_credit')
        monthly_payment = data.get('monthly_payment')

        if date_issue and close_date:
            if close_date <= date_issue:
                raise serializers.ValidationError({
                    "close_date": "Дата закрытия кредита должна быть строго позже даты выдачи."
                })

        if sum_credit and monthly_payment:
            if monthly_payment > sum_credit:
                raise serializers.ValidationError({
                    "monthly_payment": "Ежемесячный платеж не может превышать сумму кредита."
                })

        return data



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