from rest_framework import serializers
from djoser.serializers import UserSerializer as DjoserUserSerializer
from django.contrib.auth.models import Group

class UserSerializer(DjoserUserSerializer):
    role = serializers.SerializerMethodField()

    class Meta(DjoserUserSerializer.Meta):
        fields = DjoserUserSerializer.Meta.fields + ('role',)

    def get_role(self, obj):
        groups = obj.groups.values_list('name', flat=True)
        # Предполагается, что у пользователя только одна роль
        return groups[0] if groups else None