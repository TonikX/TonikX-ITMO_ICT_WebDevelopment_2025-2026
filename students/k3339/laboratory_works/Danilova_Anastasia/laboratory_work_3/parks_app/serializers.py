from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Services, Enterprise, Object, Contract, Decorator, ObjectZone, Plant, \
    PlantPlacement, LifeForm, Species, PlantWateringSchedule, Worker, PlantWorkerAssignment, ObjectWorkerAssignment

class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = "__all__"



class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = "__all__"


class ObjectSerializer(serializers.ModelSerializer):
    is_serviced = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Object
        fields = "__all__"

    def get_is_serviced(self, obj):
        return obj.is_serviced


class ObjectZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectZone
        fields = "__all__"


class ObjectReadSerializer(serializers.ModelSerializer):
    zones = ObjectZoneSerializer(many=True, read_only=True)

    class Meta:
        model = Object
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    enterprise = serializers.PrimaryKeyRelatedField(
        queryset=Enterprise.objects.all(),

    )

    enterprise_details = EnterpriseSerializer(source='enterprise', read_only=True)

    object = serializers.PrimaryKeyRelatedField(
        queryset=Object.objects.all()
    )
    object_details = serializers.CharField(source='object.name', read_only=True)

    class Meta:
        model = Contract
        fields = [
            'id', 'contract_number', 'contract_date', 'description',
            'is_active', 'enterprise', 'enterprise_details',
            'object', 'object_details'
        ]


class DecoratorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Decorator
        fields = "__all__"

    def get_full_name(self, obj):
        return obj.full_name

class LifeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeForm
        fields = "__all__"

class SpeciesSerializer(serializers.ModelSerializer):
    life_form = LifeFormSerializer(read_only=True)

    class Meta:
        model = Species
        fields = "__all__"


class PlantSerializer(serializers.ModelSerializer):
    has_watering_schedule = serializers.SerializerMethodField()

    species = serializers.PrimaryKeyRelatedField(
        queryset=Species.objects.all()
    )
    species_details = SpeciesSerializer(source='species', read_only=True)
    current_age = serializers.ReadOnlyField()

    class Meta:
        model = Plant
        fields = ['id', 'species', 'species_details', 'initial_age', 'current_age', 'description', 'has_watering_schedule']

    def get_has_watering_schedule(self, obj):
        try:
            return obj.watering_schedule is not None
        except PlantWateringSchedule.DoesNotExist:
            return False


class PlantReadSerializer(serializers.ModelSerializer):
    current_age = serializers.ReadOnlyField()
    species = SpeciesSerializer(read_only=True)

    class Meta:
        model = Plant
        fields = "__all__"


class PlantPlacementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantPlacement
        fields = "__all__"

class PlantPlacementFullSerializer(serializers.ModelSerializer):
    plant = PlantSerializer(read_only=True)
    zone_id = serializers.IntegerField(source='zone.id', read_only=True)
    zone_number = serializers.ReadOnlyField(source='zone.number', read_only=True)

    class Meta:
        model = PlantPlacement
        fields = ['id', 'unique_number', 'planted_date', 'plant', 'zone_id', 'zone_number']


class PlantWateringScheduleSerializer(serializers.ModelSerializer):
    current_water_norm_liters = serializers.ReadOnlyField()
    watering_time_period = serializers.ReadOnlyField()
    plant = serializers.PrimaryKeyRelatedField(
        queryset=Plant.objects.all()
    )

    class Meta:
        model = PlantWateringSchedule
        fields = "__all__"


class WorkerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Worker
        fields = ["id", "full_name", "phone_number", "address"]

    def get_full_name(self, obj):
        return obj.full_name


class WorkerFullSerializer(serializers.ModelSerializer):
    active_objects_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Worker
        fields = ["id", "first_name", "last_name", "middle_name", "phone_number", "address", "active_objects_count"]

    def get_active_objects_count(self, obj):
        return obj.object_assignments.filter(
            end_date__isnull=True
        ).count()


class PlantWorkerAssignmentSerializer(serializers.ModelSerializer):
    worker = WorkerSerializer(read_only=True)  # Добавьте это

    plant_id = serializers.PrimaryKeyRelatedField(
        queryset=Plant.objects.all(),
        source='plant',
        write_only=True
    )
    worker_id = serializers.PrimaryKeyRelatedField(
        queryset=Worker.objects.all(),
        source='worker',
        write_only=True
    )

    class Meta:
        model = PlantWorkerAssignment
        fields = ["id", "plant", "plant_id", "worker", "worker_id", "date"]
        read_only_fields = ['plant', 'worker']


class ObjectWorkerAssignmentSerializer(serializers.ModelSerializer):
    worker = WorkerSerializer(read_only=True)
    worker_id = serializers.PrimaryKeyRelatedField(
        queryset=Worker.objects.all(),
        source='worker',
        write_only=True,
        required=True
    )

    class Meta:
        model = ObjectWorkerAssignment
        fields = ["id", "object", "worker", "worker_id", "start_date", "end_date"]