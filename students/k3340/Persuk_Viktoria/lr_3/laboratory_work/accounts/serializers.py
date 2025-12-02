from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import Profile


User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Кастомный сериализатор для создания пользователя.
    Автоматически генерирует username из email, если username не указан.
    """

    def _generate_username(self, email):
        """Генерирует уникальный username из email"""
        base_username = email.split('@')[0]
        # Очищаем username от недопустимых символов
        base_username = ''.join(c for c in base_username if c.isalnum() or c in ['_', '-'])
        if not base_username:
            base_username = 'user'
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        return username

    def validate(self, attrs):
        # КРИТИЧНО: Устанавливаем username ДО вызова родительского validate
        # Если username не указан или пустой, генерируем его из email
        if 'username' not in attrs or not attrs.get('username'):
            email = attrs.get('email', '')
            if email:
                attrs['username'] = self._generate_username(email)
            else:
                # Если email тоже нет, генерируем случайный username
                import random
                attrs['username'] = f"user_{random.randint(1000, 9999)}"
        
        # Теперь вызываем родительский validate с уже установленным username
        attrs = super().validate(attrs)
        return attrs
    
    def perform_create(self, validated_data):
        """
        Переопределяем perform_create из Djoser, чтобы гарантировать установку username.
        Этот метод вызывается напрямую из Djoser.
        """
        # Дополнительная проверка на случай, если username потерялся
        if 'username' not in validated_data or not validated_data.get('username'):
            email = validated_data.get('email', '')
            if email:
                validated_data['username'] = self._generate_username(email)
            else:
                import random
                validated_data['username'] = f"user_{random.randint(1000, 9999)}"
        
        # Вызываем родительский метод с гарантированно установленным username
        return super().perform_create(validated_data)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password']


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'display_name', 'bio', 'avatar', 'created_at', 'updated_at']
