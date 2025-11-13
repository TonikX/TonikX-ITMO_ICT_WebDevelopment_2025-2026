from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view

User = get_user_model()


@extend_schema_view(
    list=extend_schema(summary="Список пользователей", description="Получить список всех пользователей (только для администраторов)"),
    create=extend_schema(summary="Регистрация", description="Создать нового пользователя"),
    retrieve=extend_schema(summary="Детали пользователя", description="Получить информацию о пользователе"),
    update=extend_schema(summary="Обновить пользователя", description="Обновить информацию о пользователе"),
    destroy=extend_schema(summary="Удалить пользователя", description="Удалить пользователя (только для администраторов)"),
)
class CustomUserViewSet(viewsets.ModelViewSet):
    """
    Кастомный ViewSet для пользователей с ограниченным набором действий
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Для регистрации нужен AllowAny
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        """
        Устанавливаем права доступа в зависимости от действия
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['list', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    @extend_schema(summary="Текущий пользователь", description="Получить информацию о текущем аутентифицированном пользователе")
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Получить информацию о текущем пользователе
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

