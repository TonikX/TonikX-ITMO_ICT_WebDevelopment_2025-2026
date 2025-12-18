"""
URL configuration for school_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="School Management API",
        default_version='v1',
        description="""
## API для системы управления школой

Данный API предоставляет полный функционал для управления школьной системой:

### Основные сущности:
- **Предметы (Subjects)** - учебные дисциплины
- **Кабинеты (Classrooms)** - учебные помещения
- **Учителя (Teachers)** - преподаватели школы
- **Классы (Classes)** - школьные классы
- **Ученики (Students)** - учащиеся
- **Четверти (Quarters)** - учебные периоды
- **Назначения (Teaching Assignments)** - назначения учителей на предметы в классах
- **Расписание (Schedule)** - расписание уроков
- **Оценки (Grades)** - оценки учеников

### Аутентификация:
Используется Token-based аутентификация. Получите токен через `/api/auth/token/login/`
и передавайте его в заголовке: `Authorization: Token <ваш_токен>`
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@school.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Swagger/OpenAPI documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API школьной системы
    path('api/', include('school.urls')),
    
    # Djoser авторизация
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
