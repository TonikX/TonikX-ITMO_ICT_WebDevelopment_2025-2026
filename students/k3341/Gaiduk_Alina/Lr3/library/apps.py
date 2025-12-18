from django.apps import AppConfig


class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'
    verbose_name = 'Библиотека'
    
    def ready(self):
        """Импортируем расширения OpenAPI при готовности приложения."""
        from . import openapi_extensions  # noqa

