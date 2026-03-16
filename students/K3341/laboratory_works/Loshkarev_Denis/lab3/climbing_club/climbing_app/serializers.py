from rest_framework import serializers
from .models import Club, Alpinist, Mountain, Route, Climb, Participation

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'

class AlpinistSerializer(serializers.ModelSerializer):
    # Показываем название клуба текстом 
    club_name = serializers.StringRelatedField(source='club', read_only=True)
    
    class Meta:
        model = Alpinist
        fields = '__all__'

class MountainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mountain
        fields = '__all__'

class ParticipationSerializer(serializers.ModelSerializer):
    alpinist_name = serializers.ReadOnlyField(source='alpinist.name')
    
    class Meta:
        model = Participation
        fields = ['alpinist_name', 'is_success', 'status', 'incident_details']

class ClimbSerializer(serializers.ModelSerializer):
    # Вложенные данные (Nested Serializer)
    route_details = serializers.ReadOnlyField(source='route.description')
    mountain_name = serializers.ReadOnlyField(source='route.mountain.name')
    # Список участников внутри восхождения
    details = ParticipationSerializer(many=True, read_only=True)

    class Meta:
        model = Climb
        fields = '__all__'


class ParticipantCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления участника при создании группы"""
    class Meta:
        model = Participation
        fields = ['alpinist', 'is_success', 'status', 'incident_details']

class ClimbCreateSerializer(serializers.ModelSerializer):
    # Поле для приема списка участников
    participants_data = ParticipantCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Climb
        fields = [
            'route', 'group_name', 'start_planned', 'end_planned', 
            'start_actual', 'end_actual', 'is_group_success', 
            'group_notes', 'participants_data'
        ]

    def create(self, validated_data):
        # Извлекаем данные участников из общего словаря
        participants_data = validated_data.pop('participants_data')
        
        # Создаем само восхождение
        climb = Climb.objects.create(**validated_data)
        
        # Создаем записи в промежуточной таблице Participation для каждого участника
        for p_data in participants_data:
            Participation.objects.create(climb=climb, **p_data)
            
        return climb