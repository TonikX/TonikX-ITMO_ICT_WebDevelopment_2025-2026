from django.core.exceptions import ValidationError
from rest_framework import serializers

from clients.models import Client
from rooms.models import Room
from .models import Stay


class StaySerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())

    class Meta:
        model = Stay
        fields = ['id', 'client', 'room', 'check_in', 'check_out', 'status', 'total_cost']
        read_only_fields = ['status', 'total_cost']

    def validate(self, attrs):
        instance = Stay(**attrs)
        if self.instance:
            for attr, value in attrs.items():
                setattr(self.instance, attr, value)
            instance = self.instance
        try:
            instance.clean()
        except ValidationError as exc:
            raise serializers.ValidationError(exc.message_dict or exc.messages)
        return attrs

