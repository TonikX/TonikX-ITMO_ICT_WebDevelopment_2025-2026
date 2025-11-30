from drf_spectacular.extensions import OpenApiAuthenticationExtension


class StaffJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    """OpenAPI схема для JWT аутентификации Staff"""
    target_class = 'library.authentication.StaffJWTAuthentication'
    name = 'BearerAuth'
    
    def get_security_definition(self, auto_schema):
        """Возвращает определение безопасности для OpenAPI."""
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'description': (
                'JWT токен авторизации для сотрудников библиотеки. '
                'Получите токен через POST /api/token/ используя login и password. '
                'Используйте формат заголовка: Authorization: Bearer <access_token>'
            )
        }
