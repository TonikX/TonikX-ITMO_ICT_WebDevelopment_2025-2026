from rest_framework import serializers
from .models import Services, Enterprise, Object, Contract, Decorator, ObjectZone, Plant, \
    PlantPlacement, LifeForm, Species, PlantWateringSchedule, Worker, PlantWorkerAssignment, ObjectWorkerAssignment


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = "__all__"


class EnterpriseDestroySerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Contract
        fields = "__all__"


class DecoratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decorator
        fields = "__all__"


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = "__all__"


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = "__all__"


class PlantReadSerializer(serializers.ModelSerializer):
    current_age = serializers.ReadOnlyField()
    species = SpeciesSerializer(read_only=True)

    class Meta:
        model = Plant
        fields = "__all__"


class PlantPlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantPlacement
        fields = "__all__"


class LifeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeForm
        fields = "__all__"


class PlantWateringScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantWateringSchedule
        fields = "__all__"


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = "__all__"


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
    class Meta:
        model = PlantWorkerAssignment
        fields = "__all__"


class ObjectWorkerAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectWorkerAssignment
        fields = "__all__"
