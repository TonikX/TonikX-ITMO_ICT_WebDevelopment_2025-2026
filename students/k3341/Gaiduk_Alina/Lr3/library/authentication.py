"""
Custom JWT authentication for Staff model.
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from .models import Staff


class StaffJWTAuthentication(JWTAuthentication):
    """Кастомная JWT аутентификация для модели Staff."""
    
    def get_user(self, validated_token):
        """Получить пользователя (Staff) из токена."""
        try:
            staff_id = validated_token.get('staff_id')
            if not staff_id:
                raise InvalidToken('Токен не содержит staff_id.')
            
            staff = Staff.objects.get(staff_id=staff_id)
            return staff
        except Staff.DoesNotExist:
            raise InvalidToken('Сотрудник не найден.')
        except Exception as e:
            raise InvalidToken(f'Ошибка при получении сотрудника: {str(e)}')
    
    def authenticate(self, request):
        """Аутентификация по JWT токену."""
        header = self.get_header(request)
        if header is None:
            return None
        
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        
        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)
        
        return (user, validated_token)

