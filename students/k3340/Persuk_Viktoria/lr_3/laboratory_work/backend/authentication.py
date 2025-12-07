"""
Кастомная аутентификация, которая не блокирует запросы без токена
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.authentication import get_authorization_header


class OptionalJWTAuthentication(JWTAuthentication):
    """
    JWT аутентификация, которая не блокирует запросы без токена.
    Если токен не передан или неверен, просто не аутентифицирует пользователя,
    позволяя permissions проверить, разрешен ли доступ.
    """

    def authenticate(self, request):
        header = get_authorization_header(request).split()

        if not header or len(header) != 2:
            # Нет токена или неверный формат - не аутентифицируем, но не блокируем запрос
            return None

        if header[0].lower() != b'bearer':
            # Неверный формат - не блокируем
            return None

        try:
            # Пытаемся аутентифицировать
            raw_token = header[1].decode('utf-8')
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except (InvalidToken, TokenError, UnicodeError, Exception):
            # Токен неверный или ошибка - не блокируем, просто не аутентифицируем
            return None
