from rest_framework import serializers
from .models import Club, Alpinist, Mountain, Route, Climb, Participation


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'


class AlpinistSerializer(serializers.ModelSerializer):
    club_names = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Alpinist
        fields = ['id', 'name', 'address', 'clubs', 'club_names']

    def get_club_names(self, obj):
        return [c.name for c in obj.clubs.all()]


class MountainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mountain
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    mountain_name = serializers.ReadOnlyField(source='mountain.name')

    class Meta:
        model = Route
        fields = ['id', 'mountain', 'mountain_name', 'description', 'expected_duration']


class ParticipationSerializer(serializers.ModelSerializer):
    alpinist_name = serializers.ReadOnlyField(source='alpinist.name')

    class Meta:
        model = Participation
        fields = ['alpinist_name', 'is_success', 'status', 'incident_details']


class ClimbSerializer(serializers.ModelSerializer):
    route_details = serializers.ReadOnlyField(source='route.description')
    mountain_name = serializers.ReadOnlyField(source='route.mountain.name')
    details = ParticipationSerializer(many=True, read_only=True)

    class Meta:
        model = Climb
        fields = '__all__'


class ParticipantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ['alpinist', 'is_success', 'status', 'incident_details']


class ClimbCreateSerializer(serializers.ModelSerializer):
    participants_data = ParticipantCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Climb
        fields = [
            'route', 'group_name', 'start_planned', 'end_planned',
            'start_actual', 'end_actual', 'is_group_success',
            'group_notes', 'participants_data'
        ]

    def create(self, validated_data):
        participants_data = validated_data.pop('participants_data')
        climb = Climb.objects.create(**validated_data)
        for p_data in participants_data:
            Participation.objects.create(climb=climb, **p_data)
        return climb