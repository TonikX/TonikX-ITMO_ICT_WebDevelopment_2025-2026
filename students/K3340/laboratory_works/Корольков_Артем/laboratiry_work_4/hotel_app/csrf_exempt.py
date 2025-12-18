from django.utils.deprecation import MiddlewareMixin

class DisableCSRFOnAPI(MiddlewareMixin):
    def process_request(self, request):
        # Отключаем CSRF для API endpoints
        if request.path.startswith('/api/') or request.path.startswith('/auth/'):
            setattr(request, '_dont_enforce_csrf_checks', True)