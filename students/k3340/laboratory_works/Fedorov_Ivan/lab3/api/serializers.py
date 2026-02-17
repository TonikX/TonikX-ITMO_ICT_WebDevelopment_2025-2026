from rest_framework import serializers
from django.contrib.auth.models import User
from hotel.models import Room, Client, Employee, CleaningSchedule


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source='room.number', read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

    def validate(self, attrs):
        """
        Нельзя заселять в занятый номер, если клиент заселяется check_out_date = None"""
        room = attrs.get('room') or getattr(self.instance, 'room', None)
        check_out_date = attrs.get('check_out_date', getattr(self.instance, 'check_out_date', None))

        # если пытаемся создать/обновить "текущего" клиента (не выселен)
        if room and check_out_date is None:
            # при update допускаем, что клиент уже в этом номере
            if not room.is_available:
                # если это update и комната та же и клиент тот же — ок
                if not self.instance or self.instance.room_id != room.id:
                    raise serializers.ValidationError(
                        {'room': 'Номер занят. Нельзя поселить клиента в занятый номер.'}
                    )
        return attrs


class EmployeeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True, required=False)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        user_id = validated_data.pop('user_id', None)
        employee = Employee.objects.create(**validated_data)

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                employee.user = user
                employee.save()
            except User.DoesNotExist:
                pass

        return employee


class CleaningScheduleSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.__str__', read_only=True)

    class Meta:
        model = CleaningSchedule
        fields = '__all__'


# Специальные сериализаторы для запросов
class RoomClientsPeriodSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class ClientSamePeriodSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
