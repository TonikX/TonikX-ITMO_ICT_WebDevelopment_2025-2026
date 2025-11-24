from django.contrib import admin
from django.urls import path, include # Make sure 'include' is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project_first_app.urls')), # This includes all URLs from your app
]