from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Client
        fields = [
            'id',
            'passport_number',
            'last_name',
            'first_name',
            'middle_name',
            'city',
            'phone',
            'email',
            'notes',
            'full_name',
        ]

