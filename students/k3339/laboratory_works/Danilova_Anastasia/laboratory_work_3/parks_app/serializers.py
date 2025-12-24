from rest_framework import serializers
from .models import Services, Enterprise, Object, Contract, Decorator, ObjectZone, Plant, \
    PlantPlacement, LifeForm, Species, PlantWateringSchedule, Worker, PlantWorkerAssignment

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

class ObjectZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectZone
        fields = "__all__"

class PlantSerializer(serializers.ModelSerializer):
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

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = "__all__"

class PlantWateringScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantWateringSchedule
        fields = "__all__"

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = "__all__"

class PlantWorkerAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantWorkerAssignment
        fields = "__all__"
