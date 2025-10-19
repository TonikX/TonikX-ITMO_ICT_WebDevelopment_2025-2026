"""
URL configuration for task1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Маршруты для владельцев (function-based views)
    path("owners/", views.owners_list, name="owners_list"),
    path("owner/<int:owner_id>/", views.owner_detail, name="owner_detail"),
    path("owner/create/", views.create_owner, name="create_owner"),
    # Маршруты для автомобилей (class-based views)
    path("cars/", views.CarListView.as_view(), name="cars_list"),
    path("car/<int:car_id>/", views.CarDetailView.as_view(), name="car_detail"),
    path("car/create/", views.CarCreateView.as_view(), name="create_car"),
    path("car/<int:car_id>/update/", views.CarUpdateView.as_view(), name="update_car"),
    path("car/<int:car_id>/delete/", views.CarDeleteView.as_view(), name="delete_car"),
]
