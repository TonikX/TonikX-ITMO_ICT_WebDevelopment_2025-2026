from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile


User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['display_name', 'bio', 'avatar', 'created_at', 'updated_at']
