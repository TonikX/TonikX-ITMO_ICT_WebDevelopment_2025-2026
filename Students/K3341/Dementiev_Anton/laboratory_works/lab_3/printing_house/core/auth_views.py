from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль', format='password'),
        },
    ),
    responses={
        200: openapi.Response(
            description='Успешная авторизация',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'auth_token': openapi.Schema(type=openapi.TYPE_STRING, description='Токен аутентификации'),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID пользователя'),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя'),
                }
            )
        ),
        400: openapi.Response('Ошибка: неверные данные'),
        401: openapi.Response('Ошибка: неверные учетные данные'),
    },
    operation_summary="Получить токен аутентификации",
    operation_description="Авторизуйтесь с помощью username и password, чтобы получить токен. "
                          "Используйте этот токен в заголовке Authorization: Token <your_token> для доступа к API."
)
@api_view(['POST'])
@permission_classes([AllowAny])
def get_auth_token(request):
    """
    Получить токен аутентификации для использования в API.
    
    Использование:
    1. Отправьте POST запрос с username и password
    2. Получите токен из ответа
    3. Используйте токен в заголовке: Authorization: Token <your_token>
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Необходимо указать username и password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response(
            {'error': 'Неверные учетные данные'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'auth_token': token.key,
        'user_id': user.id,
        'username': user.username,
    })

