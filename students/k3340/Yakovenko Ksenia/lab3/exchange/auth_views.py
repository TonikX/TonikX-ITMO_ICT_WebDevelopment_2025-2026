from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import status


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate_password(self, value):
        validate_password(value)
        return value


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    s = RegisterSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    user = User.objects.create_user(
        username=s.validated_data["username"],
        password=s.validated_data["password"],
        email=s.validated_data.get("email", ""),
    )
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "username": user.username})


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    s = ChangePasswordSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    user = request.user
    if not user.check_password(s.validated_data["old_password"]):
        return Response({"detail": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(s.validated_data["new_password"])
    user.save()
    # можно оставить токен прежним; для простоты — оставим
    return Response({"detail": "Password changed"})

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    s = RegisterSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    try:
        user = User.objects.create_user(
            username=s.validated_data["username"],
            password=s.validated_data["password"],
            email=s.validated_data.get("email", ""),
        )
    except IntegrityError:
        return Response(
            {"detail": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "username": user.username})