from rest_framework import serializers

from .models import (
    IndividualClient, Agent, IndividualContract, LaborContract,
    Organization, CollectiveContract, RiskCategory, InsuredEmployee,
    InsuredEventIndividual, IndividualPayment, InsuredEventEmployee, EmployeePayment
)


class IndividualClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualClient
        fields = '__all__'


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'


class IndividualContractSerializer(serializers.ModelSerializer):
    agent = AgentSerializer(read_only=True)
    client = IndividualClientSerializer(read_only=True)

    class Meta:
        model = IndividualContract
        fields = '__all__'


class IndividualContractWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualContract
        fields = '__all__'


class LaborContractSerializer(serializers.ModelSerializer):
    agent = AgentSerializer(read_only=True)

    class Meta:
        model = LaborContract
        fields = '__all__'


class LaborContractWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaborContract
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class CollectiveContractSerializer(serializers.ModelSerializer):
    agent = AgentSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    insured_employees = serializers.SerializerMethodField()

    class Meta:
        model = CollectiveContract
        fields = '__all__'

    def get_insured_employees(self, obj):
        insured_employees = obj.insured_employees.all()
        return InsuredEmployeeSerializer(insured_employees, many=True).data


class CollectiveContractWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectiveContract
        fields = '__all__'


class RiskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskCategory
        fields = '__all__'


class InsuredEmployeeSerializer(serializers.ModelSerializer):
    client = IndividualClientSerializer(read_only=True)
    risk_category = RiskCategorySerializer(read_only=True)

    class Meta:
        model = InsuredEmployee
        fields = '__all__'


class InsuredEmployeeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuredEmployee
        fields = '__all__'


class InsuredEventIndividualSerializer(serializers.ModelSerializer):
    contract = IndividualContractSerializer(read_only=True)

    class Meta:
        model = InsuredEventIndividual
        fields = '__all__'


class InsuredEventIndividualWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuredEventIndividual
        fields = '__all__'


class IndividualPaymentSerializer(serializers.ModelSerializer):
    event = InsuredEventIndividualSerializer(read_only=True)

    class Meta:
        model = IndividualPayment
        fields = '__all__'


class IndividualPaymentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualPayment
        fields = '__all__'


class InsuredEventEmployeeSerializer(serializers.ModelSerializer):
    employee = InsuredEmployeeSerializer(read_only=True)

    class Meta:
        model = InsuredEventEmployee
        fields = '__all__'


class InsuredEventEmployeeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuredEventEmployee
        fields = '__all__'


class EmployeePaymentSerializer(serializers.ModelSerializer):
    event = InsuredEventEmployeeSerializer(read_only=True)

    class Meta:
        model = EmployeePayment
        fields = '__all__'


class EmployeePaymentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePayment
        fields = '__all__'
