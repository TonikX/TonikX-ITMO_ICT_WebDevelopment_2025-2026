from rest_framework import serializers
from datetime import date
from django.core.validators import RegexValidator
from django.db.models import Q
from poultry_farm_app.models import (
    Breed, Diet, Hen, HenEggs,
    Cage, HenCage, Employee, EmployeeCage, Employment, BreedDiet
)

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name', 'efficiency', 'mean_weight']
        read_only_fields = ['id']
        
    def validate_name(self, value):
        if Breed.objects.filter(name=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Порода с таким названием уже существует")
        return value


class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = ['id', 'number', 'structure']
        read_only_fields = ['id']
        
    def validate_number(self, value):
        if Diet.objects.filter(number=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Диета с таким номером уже существует")
        return value


class BreedDietSerializer(serializers.ModelSerializer):
    breed_name = serializers.CharField(source='breed.name', read_only=True)
    diet_number = serializers.IntegerField(source='diet.number', read_only=True)
    
    class Meta:
        model = BreedDiet
        fields = ['id', 'breed', 'diet_id', 'season', 'breed_name', 'diet_number']
        read_only_fields = ['id']


class HenSerializer(serializers.ModelSerializer):
    breed_name = serializers.CharField(source='breed.name', read_only=True)
    
    class Meta:
        model = Hen
        fields = ['id', 'breed', 'weight', 'birth_date', 'death_date', 'breed_name']
        read_only_fields = ['id', 'birth_date']
        extra_kwargs = {
            'death_date': {'required': False}
        }


class HenEggsSerializer(serializers.ModelSerializer):
    hen = serializers.PrimaryKeyRelatedField(queryset=Hen.objects.filter(death_date__isnull=True))
    
    class Meta:
        model = HenEggs
        fields = ['id', 'hen', 'count_eggs', 'date']
        read_only_fields = ['id']
        
    def validate(self, data):
        if data['hen'].death_date and data['hen'].death_date < data['date']:
            raise serializers.ValidationError("Нельзя добавить яйценоскость для мертвой курицы")
        return data


class CageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cage
        fields = ['id', 'workshop_number', 'row_number', 'in_row_number']
        read_only_fields = ['id']
        
    def validate(self, data):
        if Cage.objects.filter(
            workshop_number=data['workshop_number'],
            row_number=data['row_number'],
            in_row_number=data['in_row_number']
        ).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Клетка с такими координатами уже существует")
        return data


class HenCageSerializer(serializers.ModelSerializer):
    hen_details = HenSerializer(source='hen', read_only=True)
    cage_details = CageSerializer(source='cage', read_only=True)
    
    class Meta:
        model = HenCage
        fields = ['id', 'hen', 'cage', 'date_start', 'date_end', 'hen_details', 'cage_details']
        read_only_fields = ['id']
        
    def validate(self, data):
        if data['date_end'] < data['date_start']:
            raise serializers.ValidationError("Дата выселения не может быть раньше даты заселения")
        
        if HenCage.objects.filter(
            hen=data['hen'],
            date_start__lt=data['date_end'],
            date_end__gt=data['date_start']
        ).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Курица уже заселена в другую клетку в этот период")
        
        return data


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'passport_series', 'passport_number']
        read_only_fields = ['id']
        extra_kwargs = {
            'passport_series': {
                'validators': [RegexValidator(regex=r'^\d{4}$', message='Серия паспорта должна содержать ровно 4 цифры')]
            },
            'passport_number': {
                'validators': [RegexValidator(regex=r'^\d{6}$', message='Номер паспорта должен содержать ровно 6 цифр')]
            }
        }
        
    def validate(self, data):
        if Employee.objects.filter(
            passport_series=data['passport_series'],
            passport_number=data['passport_number']
        ).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Сотрудник с таким паспортом уже существует")
        return data


class EmployeeCageSerializer(serializers.ModelSerializer):
    employee_details = EmployeeSerializer(source='employee', read_only=True)
    cage_details = CageSerializer(source='cage', read_only=True)
    
    class Meta:
        model = EmployeeCage
        fields = ['id', 'employee', 'cage', 'date_start', 'date_end', 'employee_details', 'cage_details']
        read_only_fields = ['id']
        
    def validate(self, data):
        if data['date_end'] < data['date_start']:
            raise serializers.ValidationError("Дата открепления не может быть раньше даты закрепления")
        
        if EmployeeCage.objects.filter(
            employee=data['employee'],
            date_start__lt=data['date_end'],
            date_end__gt=data['date_start']
        ).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Работник уже закреплен за другой клеткой в этот период")
        
        return data


class EmploymentSerializer(serializers.ModelSerializer):
    employee_details = EmployeeSerializer(source='employee', read_only=True)
    
    class Meta:
        model = Employment
        fields = [
            'id', 'employee', 'position', 'contract', 'salary_rub', 
            'date_start', 'date_end', 'termination_reason', 
            'termination_order_num', 'employee_details'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'date_end': {'required': False},
            'termination_reason': {'required': False},
            'termination_order_num': {'required': False}
        }
        
    def validate(self, data):
        if data.get('date_end') and not self.instance:
            if not data.get('termination_reason') or not data.get('termination_order_num'):
                raise serializers.ValidationError(
                    "При указании даты увольнения необходимо указать причину и номер приказа"
                )
        
        if Employment.objects.filter(
            contract=data['contract']
        ).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Трудовой договор с таким номером уже существует")
        
        return data


class DietDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = ['id', 'number', 'structure']


class BreedDietSeasonSerializer(serializers.ModelSerializer):
    diet = DietDetailSerializer(read_only=True)
    
    class Meta:
        model = BreedDiet
        fields = ['id', 'season', 'diet']


class HenWithBreedSerializer(serializers.ModelSerializer):
    breed = BreedSerializer(read_only=True)
    current_cage = serializers.SerializerMethodField()
    
    class Meta:
        model = Hen
        fields = ['id', 'breed', 'weight', 'birth_date', 'death_date', 'current_cage']
    
    def get_current_cage(self, obj):
        today = date.today()
        try:
            cage_assignment = obj.hen_cages.filter(
                date_start__lte=today,
            ).filter(
                Q(date_end__gte=today) | Q(date_end__isnull=True)
            ).select_related('cage').latest('date_start')
            
            return {
                'id': cage_assignment.cage.id,
                'workshop_number': cage_assignment.cage.workshop_number,
                'row_number': cage_assignment.cage.row_number,
                'in_row_number': cage_assignment.cage.in_row_number,
                'date_start': cage_assignment.date_start,
                'date_end': cage_assignment.date_end
            }
        except HenCage.DoesNotExist:
            return None
        except HenCage.MultipleObjectsReturned:
            cage_assignment = obj.hen_cages.filter(
                date_start__lte=today,
            ).filter(
                Q(date_end__gte=today) | Q(date_end__isnull=True)
            ).select_related('cage').order_by('-date_start').first()
            return {
                'id': cage_assignment.cage.id,
                'workshop_number': cage_assignment.cage.workshop_number,
                'row_number': cage_assignment.cage.row_number,
                'in_row_number': cage_assignment.cage.in_row_number,
                'date_start': cage_assignment.date_start,
                'date_end': cage_assignment.date_end
            }


class EmployeeWithCagesSerializer(serializers.ModelSerializer):
    current_cages = serializers.SerializerMethodField()
    current_position = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'passport_series', 'passport_number', 'current_cages', 'current_position']
    
    def get_current_cages(self, obj):
        today = date.today()
        cage_assignments = obj.employeecage_set.filter(
            date_start__lte=today,
            date_end__gte=today
        ).select_related('cage')
        
        return [{
            'cage_id': assignment.cage.id,
            'workshop_number': assignment.cage.workshop_number,
            'row_number': assignment.cage.row_number,
            'in_row_number': assignment.cage.in_row_number,
            'date_start': assignment.date_start
        } for assignment in cage_assignments]
    
    def get_current_position(self, obj):
        try:
            employment = obj.employments.filter(
                date_end__isnull=True
            ).latest('date_start')
            return {
                'position': employment.position,
                'salary_rub': employment.salary_rub,
                'contract': employment.contract
            }
        except Employment.DoesNotExist:
            return None


class CageWithHensSerializer(serializers.ModelSerializer):
    current_hens = serializers.SerializerMethodField()
    
    class Meta:
        model = Cage
        fields = ['id', 'workshop_number', 'row_number', 'in_row_number', 'current_hens']
    
    def get_current_hens(self, obj):
        today = date.today()
        hen_assignments = obj.cage_hens.filter(
            date_start__lte=today,
        ).filter(
            Q(date_end__gte=today) | Q(date_end__isnull=True)
        ).select_related('hen__breed')
        
        return [{
            'id': assignment.hen.id,
            'breed_name': assignment.hen.breed.name,
            'weight': assignment.hen.weight,
            'birth_date': assignment.hen.birth_date,
            'date_start': assignment.date_start,
            'date_end': assignment.date_end
        } for assignment in hen_assignments]


class EggsByCharacteristicsSerializer(serializers.Serializer):
    hen_id = serializers.IntegerField()
    breed_name = serializers.CharField()
    weight = serializers.FloatField()
    age_months = serializers.FloatField()
    birth_date = serializers.DateField()
    avg_eggs = serializers.FloatField()


class TopWorkshopSerializer(serializers.Serializer):
    workshop_number = serializers.IntegerField()
    breed_count = serializers.IntegerField()


class EmployeeAvgEggsSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    employee_name = serializers.CharField()
    avg_eggs_per_day = serializers.FloatField()


class BreedDistributionSerializer(serializers.Serializer):
    workshop_number = serializers.IntegerField()
    breed_name = serializers.CharField()
    count = serializers.IntegerField()


class BreedEfficiencyDiffSerializer(serializers.Serializer):
    breed_name = serializers.CharField()
    breed_efficiency = serializers.IntegerField()
    factory_avg = serializers.FloatField()
    difference = serializers.FloatField()


class MonthlyReportSerializer(serializers.Serializer):

    class WorkshopSerializer(serializers.Serializer):

        class BreedDataSerializer(serializers.Serializer):
            breed_name = serializers.CharField()
            count = serializers.IntegerField()
            eggs = serializers.IntegerField()

        workshop_number = serializers.IntegerField()
        total_hens = serializers.IntegerField()
        total_eggs = serializers.IntegerField()
        breeds = serializers.ListField(
            child=BreedDataSerializer()
        )

    period = serializers.CharField()
    total_hens = serializers.IntegerField()
    total_eggs = serializers.IntegerField()
    workshops = serializers.ListField(
        child=WorkshopSerializer()
    )