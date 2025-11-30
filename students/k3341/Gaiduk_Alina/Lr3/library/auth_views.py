"""
Custom authentication views for JWT tokens with Staff model.
"""
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from .models import Staff
from .serializers import StaffSerializer


class StaffTokenObtainPairSerializer(serializers.Serializer):
    """Сериализатор для получения JWT токенов для Staff."""
    login = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        """Валидация логина и пароля сотрудника."""
        login = attrs.get('login')
        password = attrs.get('password')
        
        try:
            staff = Staff.objects.get(login=login)
        except Staff.DoesNotExist:
            raise serializers.ValidationError(
                'Неверный логин или пароль.',
                code='authorization'
            )
        
        if not check_password(password, staff.password_hash):
            raise serializers.ValidationError(
                'Неверный логин или пароль.',
                code='authorization'
            )
        
        attrs['staff'] = staff
        return attrs


class StaffTokenObtainPairView(APIView):
    """View для получения JWT токенов для Staff."""
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary='Получить JWT токены',
        description='Получить access и refresh токены для авторизации сотрудника библиотеки. Используйте access токен в заголовке Authorization: Bearer <token> для доступа к защищённым эндпоинтам. Аутентификация не требуется.',
        request=StaffTokenObtainPairSerializer,
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'access': {
                        'type': 'string',
                        'description': 'JWT access токен для авторизации запросов',
                        'example': 'eyJ0eXAiOiJKV1QiLCJhbGc...'
                    },
                    'refresh': {
                        'type': 'string',
                        'description': 'JWT refresh токен для обновления access токена',
                        'example': 'eyJ0eXAiOiJKV1QiLCJhbGc...'
                    }
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'login': {'type': 'array', 'items': {'type': 'string'}},
                    'password': {'type': 'array', 'items': {'type': 'string'}},
                    'non_field_errors': {'type': 'array', 'items': {'type': 'string'}}
                },
                'description': 'Ошибка валидации или неверные учётные данные'
            }
        },
        tags=['Authentication'],
        operation_id='obtain_token_pair',
        auth=[],  # Явно исключаем из DEFAULT_SECURITY
    )
    def post(self, request):
        """Получить JWT токены по логину и паролю."""
        serializer = StaffTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        staff = serializer.validated_data['staff']
        
        # Создаём токены
        refresh = RefreshToken()
        refresh['staff_id'] = staff.staff_id
        refresh['login'] = staff.login
        
        # Добавляем staff_id в access токен тоже
        refresh.access_token['staff_id'] = staff.staff_id
        refresh.access_token['login'] = staff.login
        
        # Не сохраняем refresh токен в БД - он не нужен там, токены валидируются по подписи
        # Сохраняем только время истечения для информации
        from datetime import timedelta
        from django.utils import timezone
        staff.refresh_token_expires_at = timezone.now() + timedelta(days=7)
        staff.save(update_fields=['refresh_token_expires_at'])
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)


