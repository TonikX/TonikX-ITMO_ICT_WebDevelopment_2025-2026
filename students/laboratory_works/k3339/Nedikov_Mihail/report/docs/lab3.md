# Лабораторная работа №3. Реализация серверной части на django rest. Документирование API.

В рамках лабораторной работы было необходимо реализовать REST API приложение, используя Django Rest Framework

Также было необходимо подключить работу с пользователями через djoser и создать документацию


## Выполнение работы

### Models
Мною был выбран вариант сервиса для лизинга авто. Для этого была создана база данных,
основными сущностями в которой являются администратор (сотрудник), клиент (компания), 
автомобиль, характеристики, автопарк, договор лизинга, заявка.

Как и в прошлой лабораторной работе, модели были описаны в файле **leasing_app/models**.

Были применены таблицы связей many-many, one-many через внешние ключи.


### Djoser 

Для подключения djoser была расширена стандартная модель пользователя:

```
class AdminUser(AbstractUser):
    """ Сотрудник """
    phone = models.CharField("Телефон", max_length=50, blank=True)
    position = models.CharField("Должность", max_length=100, blank=True)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.username
```

Таким образом, для подключения регистрации / авторизации по токенам и вывод информации о текущем пользователе
было необходимо:

1) установить и добавить соответствующие приложения в настройках:
2) настроить модель авторизации и сам djoser
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'leasing_app',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_spectacular',
    'drf_spectacular_sidecar',
]

AUTH_USER_MODEL = "leasing_app.AdminUser"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

DJOSER = {
    "HIDE_USERS": True,
    "USER_ID_FIELD": "id",

    "USER_CREATE_PASSWORD_RETYPE": False,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": False,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": False,
    "SEND_ACTIVATION_EMAIL": False,
    "SEND_CONFIRMATION_EMAIL": False,

    "SERIALIZERS": {
        "user_create": "leasing_app.serializers.UserCreateSerializer",
        "user": "leasing_app.serializers.UserSerializer",
        "current_user": "leasing_app.serializers.UserSerializer",
    },

    "LOGIN_FIELD": "username",
}
```

3) добавить новые пути в urls

```
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
```

Таким образом, имеем готовую логику для авторизации и аутентификации сотрудников.

### Serializers

Далее были созданы сериализаторы для корректной работы с данными при вводе/выводе. 
Для некоторых запросов также использовались и вложенные сериализаторы.
Пример:

```
class CarFleetSerializer(serializers.ModelSerializer):
    fleet = serializers.PrimaryKeyRelatedField(
        queryset=Fleet.objects.all()
    )
    car = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all()
    )

    class Meta:
        model = CarFleet
        fields = ["id", "car", "fleet", "assigned_at"]
        read_only_fields = ["id"]
```

### views

Представления были созданы как классы для всех потенциальных интерфейсов. 
Были использованы как стандартные APIView, так и CreateAPIView и serializer_class
в необходимых местах для корректности работы DRF и последующей генерации динамической документации

```
class CarSpecificationsListAPIView(APIView):
    serializer_class = CarSpecificationSerializer

    def get(self, request, id):
        car = get_object_or_404(Car, id=id)
        specs = CarSpecification.objects.filter(car=car).order_by("id")
        serializer = self.serializer_class(specs, many=True)
        return Response({"specifications": serializer.data})
```

### urls

Также была продумана и реализована структура путей, которая позволила обеспечить 
понятные логические связи между разделами. Ниже приведен список путей, разделенных на группы:

```
urlpatterns = [

    # admin — cars
    path("admin/cars/", AdminCarListAPIView.as_view(), name="admin-car-list"),
    path("admin/cars/create/", AdminCarCreateAPIView.as_view(), name="admin-car-create"),
    path("admin/cars/<int:pk>/", AdminCarDetailAPIView.as_view(), name="admin-car-detail"),

    # admin — maintenance companies
    path("admin/maintenance_companies/", MaintenanceCompanyListCreateAPIView.as_view(), name="admin-maintenance-company-list"),
    path("admin/maintenance_companies/<int:id>/", MaintenanceCompanyDetailAPIView.as_view(), name="admin-maintenance-company-detail"),

    # admin — car maintenance
    path("admin/cars/<int:id>/maintenance/", CarMaintenanceAPIView.as_view(), name="admin_car_maintenance"),

    # admin — lease applications
    path("admin/lease_applications/", LeaseApplicationAPIView.as_view(), name="admin_lease_applications"),
    path("admin/lease_applications/<int:id>/", LeaseApplicationAPIView.as_view(), name="admin_lease_application_detail"),
    path("admin/lease_applications/<int:id>/approve/", LeaseApplicationAPIView.as_view(), name="admin_lease_application_approve"),

    # admin — leases
    path("admin/leases/", LeaseAPIView.as_view(), name="admin_leases"),
    path("admin/leases/<int:id>/", LeaseAPIView.as_view(), name="admin_lease_detail"),

    # admin — clients
    path("admin/clients/", ClientAPIView.as_view(), name="admin_clients"),
    path("admin/clients/<int:id>/", ClientAPIView.as_view(), name="admin_client_detail"),

    # public — cars
    path("cars/", CarsListAPIView.as_view(), name="cars_list"),
    path("cars/<int:id>/", CarDetailAPIView.as_view(), name="car_detail"),
    path("cars/<int:id>/application/", CarApplicationAPIView.as_view(), name="car_application"),

    # admin — car specifications & fleet
    path("admin/car_specifications/", AdminCarSpecificationAPIView.as_view()),
    path("admin/fleets/", AdminFleetAPIView.as_view()),
    path("admin/car_fleets/", AdminCarFleetAPIView.as_view()),

    # admin — nested: car leasings
    path("admin/cars/<int:id>/leasings/", CarLeasingsListAPIView.as_view(), name="car-leasings-list"),

    # admin — nested: car specifications
    path("admin/cars/<int:id>/specifications/", CarSpecificationsListAPIView.as_view(), name="car-specifications-list"),
    path("admin/cars/<int:id>/specifications/create/", CarSpecificationCreateAPIView2.as_view(), name="car-specifications-create"),
]

```

### drf_spectacular

Для удобства при тестировании и наглядности была создана динамическая документация на основе **drf_spectacular**

Для этого было необходимо установить нужные модули и добавить их в настройки и пути:

```
INSTALLED_APPS += [
    'drf_spectacular',
    'drf_spectacular_sidecar',
]
```

```
urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
```

Получилась простая и удобная документация с возможностью быстро тестировать проект:

![swagger.png](assets/swagger.png)


## Вывод

В ходе лабораторной работы получилось создать полноценное REST API на базе Django с использованием всех полученных знаний

