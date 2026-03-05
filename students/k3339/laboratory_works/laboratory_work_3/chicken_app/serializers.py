from rest_framework import serializers

from .models import Workshop, Cell, Employee, ResponsibleEmployee, Breed, Chicken, Diet, LaborContract


class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'


class CellSerializer(serializers.ModelSerializer):
    workshop = WorkshopSerializer(read_only=True)

    class Meta:
        model = Cell
        fields = '__all__'


class CellWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    responsible_cells = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'passport', 'first_name', 'second_name', 'patronymic', 'responsible_cells']

    def get_responsible_cells(self, obj):
        responsible_cells = ResponsibleEmployee.objects.filter(employee=obj).values_list('cell', flat=True)
        cells = Cell.objects.filter(cell_code__in=responsible_cells)
        return CellSerializer(cells, many=True).data


class ResponsibleEmployeeSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = ResponsibleEmployee
        fields = '__all__'


class ResponsibleEmployeeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleEmployee
        fields = '__all__'


class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = '__all__'


class BreedSerializer(serializers.ModelSerializer):
    diet_number = DietSerializer(read_only=True)

    class Meta:
        model = Breed
        fields = '__all__'


class BreedWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'


class ChickenSerializer(serializers.ModelSerializer):
    breed = BreedSerializer(read_only=True)
    cell = CellSerializer(read_only=True)

    class Meta:
        model = Chicken
        fields = '__all__'


class ChickenWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chicken
        fields = '__all__'


class LaborContractSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = LaborContract
        fields = '__all__'


class LaborContractWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaborContract
        fields = '__all__'
