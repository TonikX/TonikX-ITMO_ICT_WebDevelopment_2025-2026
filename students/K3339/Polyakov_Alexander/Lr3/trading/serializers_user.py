from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers

from .models import Broker


class UserSerializer(DjoserUserSerializer):
    broker_id = serializers.SerializerMethodField()

    class Meta(DjoserUserSerializer.Meta):
        model = get_user_model()
        fields = tuple(DjoserUserSerializer.Meta.fields) + ("is_staff", "broker_id")

    def get_broker_id(self, obj):
        try:
            return obj.broker_profile.id
        except Broker.DoesNotExist:
            return None
        except AttributeError:
            return None

