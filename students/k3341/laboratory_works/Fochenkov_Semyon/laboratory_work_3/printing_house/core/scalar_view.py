from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
import json


@xframe_options_exempt
@csrf_exempt
@require_http_methods(["GET"])
def scalar_ui(request):
    """
    Кастомный view для Scalar UI - современного интерфейса для OpenAPI документации.
    
    Scalar предоставляет красивый и современный интерфейс для просмотра и тестирования API.
    """
    schema_url = request.build_absolute_uri('/swagger.json')
    base_url = request.build_absolute_uri('/')[:-1]
    
    # Конфигурация для Scalar с поддержкой авторизации
    # Scalar автоматически читает security из OpenAPI схемы,
    # но мы можем добавить дополнительную конфигурацию
    config = {
        "theme": "purple",
        "layout": "modern",
        "darkMode": True,
        "defaultHttpClient": {
            "targetKey": "javascript",
            "clientKey": "fetch"
        },
        "proxy": base_url,
    }
    
    html_content = f"""<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Printing House API - Scalar Documentation</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
        }}
    </style>
</head>
<body>
    <noscript>
        Scalar требует включенного JavaScript для работы. Пожалуйста, включите его для просмотра документации.
    </noscript>
    <script
        id="api-reference"
        data-url="{schema_url}"
        data-configuration='{json.dumps(config, ensure_ascii=False)}'
    ></script>
    <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference@1.26.0/dist/browser/standalone.js"></script>
    <script>
        // Отладка: проверка загрузки схемы
        console.log('Scalar UI загружен');
        console.log('Schema URL:', '{schema_url}');
        
        // Проверка доступности схемы
        fetch('{schema_url}')
            .then(response => {{
                console.log('Schema response status:', response.status);
                return response.json();
            }})
            .then(data => {{
                console.log('Schema loaded successfully:', data.info?.title || 'Unknown');
                console.log('Security definitions:', data.components?.securitySchemes || 'Not found');
            }})
            .catch(error => {{
                console.error('Error loading schema:', error);
            }});
    </script>
</body>
</html>"""
    
    return HttpResponse(html_content)

