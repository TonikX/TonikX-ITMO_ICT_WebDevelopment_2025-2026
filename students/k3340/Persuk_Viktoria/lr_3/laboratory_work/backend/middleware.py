"""
Middleware для отключения CSRF для API endpoints
"""


class DisableCSRFForAPI:
    """
    Middleware для отключения CSRF проверки для API endpoints
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Отключаем CSRF для API endpoints
        if request.path.startswith('/auth/') or request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)
