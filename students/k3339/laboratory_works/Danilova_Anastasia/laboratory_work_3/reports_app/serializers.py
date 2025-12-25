from rest_framework import serializers

from parks_app.models import Worker


class WorkerWithObjectsSerializer(serializers.ModelSerializer):
    active_objects_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Worker
        fields = ["id", "first_name", "last_name", "middle_name", "phone_number", "address", "active_objects_count"]

    def get_active_objects_count(self, obj):
        return obj.object_assignments.filter(
            end_date__isnull=True
        ).count()

class MostPlantedSpeciesPerObjectSerializer(serializers.Serializer):
    object_id = serializers.IntegerField()
    object_name = serializers.CharField()
    most_planted_species = serializers.CharField()
    most_planted_species_count = serializers.IntegerField()

class WorkerObjectPlantCountSerializer(serializers.Serializer):
    worker_id = serializers.IntegerField()
    worker_name = serializers.CharField()
    object_id = serializers.IntegerField()
    object_name = serializers.CharField()
    plants_count = serializers.IntegerField()

class SpeciesReportSerializer(serializers.Serializer):
    species = serializers.CharField()
    count = serializers.IntegerField()


class LifeFormReportSerializer(serializers.Serializer):
    life_form = serializers.CharField()
    life_form_total = serializers.IntegerField()
    species = SpeciesReportSerializer(many=True)


class ObjectPlantReportSerializer(serializers.Serializer):
    object_id = serializers.IntegerField()
    object_name = serializers.CharField()
    object_total = serializers.IntegerField()
    life_forms = LifeFormReportSerializer(many=True)


class PlantsSummaryReportSerializer(serializers.Serializer):
    total_plants = serializers.IntegerField()
    objects = ObjectPlantReportSerializer(many=True)