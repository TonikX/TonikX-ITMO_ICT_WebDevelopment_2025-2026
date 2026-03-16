# Лабораторная работа №2

## Описание варианта работы

> В качестве варианта работы было выбрано `Задание 9` из ["Основы баз данных"](https://drive.google.com/file/d/174gPjJ7AOHfzteYcobPY0x7sFBTkN1Xx/view?usp=sharing).

Создать программную систему, предназначенную для диспетчера автобусного парка частной транспортной фирмы. Фима обслуживает несколько коммерческих маршрутов. Такая система должна обеспечивать хранение сведений о водителях, о маршрутах и характеристиках автобусов.

Каждый водитель характеризуется паспортными данными, классом, стажем работы и окладом, причем оклад зависит от класса и стажа работы.

Маршрут автобуса характеризуется номером маршрута, названием начального и конечного пункта движения, временем начала и конца движения, интервалом движения и протяженностью в минутах (время движения от кольца до кольца). Характеристиками автобуса являются: номер государственной регистрации автобуса, его тип и вместимость, причем вместимость автобуса зависит от его типа.

Каждый водитель закреплен за определенным автобусом и работает на определенном маршруте, но в случае поломки своего автобуса или болезни другого водителя может пересесть на другую машину.

В базе должен храниться график работы водителей.

Необходимо предусмотреть возможность корректировки БД в случаях поступления на работу нового водителя, списания старого автобуса, введения нового маршрута или изменения старого и т.п.

Диспетчеру автопарка могут потребоваться следующие сведения:

- Список водителей, работающих на определенном маршруте с указанием графика их работы?
- Когда начинается и заканчивается движение автобусов на каждом маршруте?
- Какова общая протяженность маршрутов, обслуживаемых автопарком?
- Какие автобусы не вышли на линию в заданный день и по какой причине (неисправность, отсутствие водителя)?
- Сколько водителей каждого класса работает в автопарке?

Необходимо предусмотреть возможность выдачи отчета по автопарку, сгруппированного по типам автобусов, с указанием маршрутов, обслуживаемых автобусами каждого типа. Для маршрутов должны быть указаны все характеристики, включая списки автобусов и водителей, обслуживающих каждый маршрут. Отчёт должен содержать сведения о суммарной протяжённости обслуживаемых маршрутов, о количестве имеющихся в автопарке автобусов каждого типа, о количестве водителей, их среднем возрасте и стаже.

## Выполнение работы

### Реализация модели базы данных средствами DjangoORM

Основываясь на требованиях задания, была разработана следующая модель базы данных средствами DjangoORM:

```python title="bus_depot_project/bus_depot_app/models.py"
class BusType(models.Model):
    """
    Тип автобуса.
    """
    name = models.CharField(max_length=50, verbose_name="Название")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость")

    class Meta:
        verbose_name = "Тип автобуса"
        verbose_name_plural = "Типы автобусов"
    
    def __str__(self):
        return f"{self.name} (число мест: {self.capacity})"


class Bus(models.Model):
    """
    Автобус.
    """
    license_plate = models.CharField(
        max_length=10, 
        unique=True,
        verbose_name="Номер"
    )
    bus_type = models.ForeignKey(
        BusType,
        on_delete=models.CASCADE,
        related_name='buses',
        verbose_name="Тип автобуса"
    )
    is_active = models.BooleanField(verbose_name="Действующий")
    purchase_date = models.DateField(verbose_name="Дата приобретения")

    class Meta:
        verbose_name = "Автобус"
        verbose_name_plural = "Автобусы"
    
    def __str__(self):
        return f"{self.license_plate} ({self.bus_type.name})"


class Route(models.Model):
    """
    Маршрут.
    """
    number = models.CharField(max_length=10, unique=True, verbose_name="Номер маршрута")
    start_point = models.CharField(max_length=100, verbose_name="Начальный пункт")
    end_point = models.CharField(max_length=100, verbose_name="Конечный пункт")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    interval = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Интервал движения (мин)"
    )
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Протяженность (мин)"
    )

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"
    
    def __str__(self):
        return f"{self.number} ({self.start_point} - {self.end_point})"


class Driver(models.Model):
    """
    Водитель.
    """
    CLASS_CHOICES = [
        ('1', 'Первый класс'),
        ('2', 'Второй класс'),
        ('3', 'Третий класс'),
    ]

    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    passport = models.CharField(
        max_length=10, 
        unique=True, 
        verbose_name="Серия и номер паспорта"
    )
    birth_date = models.DateField(verbose_name="Дата рождения")
    driver_class = models.CharField(
        max_length=1,
        choices=CLASS_CHOICES,
        verbose_name="Класс водителя"
    )
    experience = models.PositiveIntegerField(
        verbose_name="Стаж (лет)"
    )
    salary = models.PositiveIntegerField(
        verbose_name="Оклад"
    )
    main_bus = models.ForeignKey(
        Bus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='main_drivers',
        verbose_name="Основной автобус"
    )
    main_route = models.ForeignKey(
        Route,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='main_drivers',
        verbose_name="Основной маршрут"
    )

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"
    
    def __str__(self):
        return f"{self.full_name} (автобус: {self.main_bus.license_plate}, маршрут: {self.main_route.number})"


class DriverAssignment(models.Model):
    """
    Назначение водителя.
    """
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name="Водитель"
    )
    bus = models.ForeignKey(
        Bus,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name="Автобус"
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name="Маршрут"
    )
    date = models.DateField(verbose_name="Дата работы")
    start_time = models.TimeField(verbose_name="Время начала смены")
    end_time = models.TimeField(verbose_name="Время окончания смены")

    class Meta:
        verbose_name = "Назначение водителя"
        verbose_name_plural = "График работы водителей"
    
    def __str__(self):
        return f"{self.driver} на {self.bus} ({self.date})"


class BusStatus(models.Model):
    """
    Статус автобуса.
    """
    STATUS_CHOICES = [
        ('active', 'На линии'),
        ('not_active', 'Не на линии'),
        ('broken', 'Неисправность'),
        ('no_driver', 'Отсутствие водителя'),
    ]

    bus = models.ForeignKey(
        Bus,
        on_delete=models.CASCADE,
        related_name='statuses',
        verbose_name="Автобус"
    )
    date = models.DateField(verbose_name="Дата")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name="Статус"
    )
    reason = models.TextField(
        blank=True,
        verbose_name="Причина отсутствия"
    )

    class Meta:
        verbose_name = "Статус автобуса"
        verbose_name_plural = "Статусы автобусов"
        unique_together = ['bus', 'date']

    def __str__(self):
        return f"{self.bus} - {self.status} ({self.date})"
```

### Реализация логики работы API средствами Django REST Framework (используя методы сериализации)

#### Реализация базовых CRUD-операций

В первую очередь для каждой модели из `models.py` были реализованы базовые CRUD-ы. Для этого для каждой модели бал создан базовый сериализатор:

```python title="bus_depot_project/bus_depot_app/serializers.py"
class BusTypeSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для типа автобуса.
    """
    class Meta:
        model = BusType
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для автобуса.
    """
    class Meta:
        model = Bus
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для маршрута.
    """
    class Meta:
        model = Route
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для водителя.
    """
    class Meta:
        model = Driver
        fields = '__all__'


class DriverAssignmentSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для назначения водителя.
    """
    class Meta:
        model = DriverAssignment
        fields = '__all__'


class BusStatusSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для статуса автобуса.
    """
    class Meta:
        model = BusStatus
        fields = '__all__'
```

Используя созданные сериализаторы были реализованы представления на основе ViewSet для основных CRUD-операций:

```python title="bus_depot_project/bus_depot_app/views.py"
class BusTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для типа автобуса.
    """
    serializer_class = BusTypeSerializer
    queryset = BusType.objects.all()


class BusViewSet(viewsets.ModelViewSet):
    """
    ViewSet для автобуса.
    """
    serializer_class = BusSerializer
    queryset = Bus.objects.all()


class RouteViewSet(viewsets.ModelViewSet):
    """
    ViewSet для маршрута.
    """
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class DriverViewSet(viewsets.ModelViewSet):
    """
    ViewSet для водителя.
    """
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


class DriverAssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для назначения водителя.
    """
    serializer_class = DriverAssignmentSerializer
    queryset = DriverAssignment.objects.all()


class BusStatusViewSet(viewsets.ModelViewSet):
    """
    ViewSet для статуса автобуса.
    """
    serializer_class = BusStatusSerializer
    queryset = BusStatus.objects.all()
```

Далее эти представления были зарегистрированы в URLs:

```python title="bus_depot_project/bus_depot_app/urls.py"
router = DefaultRouter()
router.register('bus-types', BusTypeViewSet)
router.register('buses', BusViewSet)
router.register('routes', RouteViewSet)
router.register('drivers', DriverViewSet)
router.register('driver-assignments', DriverAssignmentViewSet)
router.register('bus-statuses', BusStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

В результате были реализованы базовые API-эндпоинты для создания, получения, изменения и удаления всех моделей.

#### Реализация специальных API-эндпоинтов

Помимо базовых CRUD-операций, в задании требовалось написать несколько специальных API-эндпоинтов, которые реализуют более сложную механику. В результате были реализованы следующие специальные эндпоинты:

##### Список водителей, работающих на определённом маршруте с указанием графика их работы

Сериализаторы:

```python title="bus_depot_project/bus_depot_app/serializers.py"
class DriverWithAssignmentsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для водителя с его назначениями.
    """
    assignments = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = '__all__'
    
    def get_assignments(self, obj):
        assignments = DriverAssignment.objects.filter(driver=obj)
        return DriverAssignmentSerializer(assignments, many=True).data


class RouteDriversSerializer(serializers.Serializer):
    """
    Сериализатор для маршрута с водителями и их графиком работы.
    """
    route = RouteSerializer()
    drivers = DriverWithAssignmentsSerializer(many=True)
```

Представление:

```python title="bus_depot_project/bus_depot_app/views.py"
class RouteDriversAPIView(APIView):
    """
    Список водителей, работающих на определённом маршруте с указанием графика их работы.
    """
    def get(self, request, route_id):
        # Получаем маршрут
        try:
            route = Route.objects.get(pk=route_id)
        except Route.DoesNotExist:
            return Response(
                {"error": "Маршрут не найден"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем всех водителей, для которых этот маршрут является основным
        drivers = Driver.objects.filter(main_route=route).distinct()

        # Преобразуем данные в JSON
        serializer = RouteDriversSerializer({
            'route': route,
            'drivers': drivers
        })

        # Возвращаем данные
        return Response(serializer.data)
```

URLs:

```python title="bus_depot_project/bus_depot_app/urls.py"
urlpatterns = [
    # ...
    path('routes/<int:route_id>/drivers/', RouteDriversAPIView.as_view()),
    # ...
]
```

Пример запроса:

```
GET /bus-depot/routes/1/drivers/
```

Пример ответа:

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "route": {
        "id": 1,
        "number": "R1",
        "start_point": "ул. Дзержинского, 18",
        "end_point": "ул. Полевая, 24",
        "start_time": "08:00:00",
        "end_time": "20:00:00",
        "interval": 15,
        "duration": 50
    },
    "drivers": [
        {
            "id": 1,
            "assignments": [
                {
                    "id": 1,
                    "date": "2025-01-01",
                    "start_time": "08:00:00",
                    "end_time": "16:00:00",
                    "driver": 1,
                    "bus": 1,
                    "route": 1
                }
            ],
            "full_name": "Фролов Олег Николаевич",
            "passport": "2365898564",
            "birth_date": "1980-05-02",
            "driver_class": "1",
            "experience": 5,
            "salary": 80000,
            "main_bus": 1,
            "main_route": 1
        },
        {
            "id": 2,
            "assignments": [
                {
                    "id": 2,
                    "date": "2024-09-06",
                    "start_time": "10:00:00",
                    "end_time": "18:00:00",
                    "driver": 2,
                    "bus": 2,
                    "route": 1
                },
                {
                    "id": 3,
                    "date": "2024-10-06",
                    "start_time": "10:00:00",
                    "end_time": "18:00:00",
                    "driver": 2,
                    "bus": 2,
                    "route": 2
                }
            ],
            "full_name": "Кузнецов Николай Егорович",
            "passport": "5236956324",
            "birth_date": "1996-07-02",
            "driver_class": "2",
            "experience": 3,
            "salary": 70000,
            "main_bus": 2,
            "main_route": 1
        }
    ]
}
```

##### Когда начинается и заканчивается движение автобусов на каждом маршруте?

Данную задачу выполняет базовый эндпоинт для просмотра всех маршрутов, так как каждый маршрут содержит поля с временем начала и окончания движения автобусов.

Пример запроса:

```
GET /bus-depot/routes/
```

Пример ответа:

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "number": "R1",
        "start_point": "ул. Дзержинского, 18",
        "end_point": "ул. Полевая, 24",
        "start_time": "08:00:00",
        "end_time": "20:00:00",
        "interval": 15,
        "duration": 50
    },
    {
        "id": 2,
        "number": "R2",
        "start_point": "ул. Больничная, 48",
        "end_point": "ул. Фрунзе, 35",
        "start_time": "09:00:00",
        "end_time": "21:00:00",
        "interval": 30,
        "duration": 120
    }
]
```

##### Какова общая протяженность маршрутов, обслуживаемых автопарком?

Сериализатор:

```python title="bus_depot_project/bus_depot_app/serializers.py"
class TotalRouteLengthSerializer(serializers.Serializer):
    """
    Сериализатор для общей протяжённости маршрутов.
    """
    total_length = serializers.IntegerField()
    routes_count = serializers.IntegerField()
    average_length = serializers.FloatField()
```

Представление:

```python title="bus_depot_project/bus_depot_app/views.py"
class TotalRouteLengthAPIView(APIView):
    """
    Общая протяжённость всех маршрутов.
    """
    def get(self, request):
        aggregation = Route.objects.aggregate(
            total_length=Sum('duration'),
            routes_count=Count('id'),
            average_length=Avg('duration')
        )
        if aggregation['total_length'] is None:
            aggregation['total_length'] = 0
            aggregation['routes_count'] = 0
            aggregation['average_length'] = 0
        serializer = TotalRouteLengthSerializer(aggregation)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

URLs:

```python title="bus_depot_project/bus_depot_app/urls.py"
urlpatterns = [
    # ...
    path('routes/total-length/', TotalRouteLengthAPIView.as_view()),
    # ...
]
```

Пример запроса:

```
GET /bus-depot/routes/total-length/
```

Пример ответа:

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "total_length": 170,
    "routes_count": 2,
    "average_length": 85.0
}
```

##### Какие автобусы не вышли на линию в заданный день и по какой причине (неисправность, отсутствие водителя)?

Сериализатор:

```python title="bus_depot_project/bus_depot_app/serializers.py"
class BusStatusDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для статуса автобуса с детальной информацией об автобусе.
    """
    bus = BusSerializer(read_only=True)
    class Meta:
        model = BusStatus
        fields = '__all__'
```

Представление:

```python title=""
class NotActiveBusesAPIView(APIView):
    """
    Информация об автобусах, не вышедших на линию в заданную дату.
    (Дата задаётся в URL: .../?date=YYYY-MM-DD)
    """
    def get(self, request):
        date = request.query_params.get('date')
        if not date:
            return Response(
                {"error": "Параметр 'date' обязателен (формат: YYYY-MM-DD)"},
                status=status.HTTP_400_BAD_REQUEST
            )
        not_active_statuses = BusStatus.objects.filter(
            date=date
        ).exclude(
            status='active'
        ).select_related('bus')
        serializer = BusStatusDetailSerializer(not_active_statuses, many=True)
        return Response(serializer.data)
```

URLs:

```python title="bus_depot_project/bus_depot_app/urls.py"
urlpatterns = [
    # ...
    path('buses/not-active/', NotActiveBusesAPIView.as_view()),
    # ...
]
```

Пример запроса:

```
GET /bus-depot/buses/not-active/?date=2020-01-01
```

Пример ответа:

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 2,
        "bus": {
            "id": 1,
            "license_plate": "B1",
            "is_active": true,
            "purchase_date": "2020-01-01",
            "bus_type": 1
        },
        "date": "2020-01-01",
        "status": "no_driver",
        "reason": ""
    },
    {
        "id": 3,
        "bus": {
            "id": 2,
            "license_plate": "B2",
            "is_active": true,
            "purchase_date": "2020-01-02",
            "bus_type": 2
        },
        "date": "2020-01-01",
        "status": "broken",
        "reason": ""
    },
    {
        "id": 4,
        "bus": {
            "id": 3,
            "license_plate": "B3",
            "is_active": true,
            "purchase_date": "2020-01-03",
            "bus_type": 3
        },
        "date": "2020-01-01",
        "status": "not_active",
        "reason": "Плановое обслуживание"
    }
]
```

##### Сколько водителей каждого класса работает в автопарке?

Сериализатор:

```python title="bus_depot_app/serializers.py"
class DriverClassStatsSerializer(serializers.Serializer):
    """
    Сериализатор для статистики по классам водителей.
    """
    driver_class = serializers.CharField()
    driver_class_display = serializers.CharField()
    count = serializers.IntegerField()
```

Представление:

```python title="bus_depot_project/bus_depot_app/views.py"
class DriverClassStatsAPIView(APIView):
    """
    API для получения статистики по количеству водителей каждого класса.
    """
    def get(self, request):
        stats = (
            Driver.objects.values('driver_class')
            .annotate(count=Count('id'))
            .order_by('driver_class')
        )
        for stat in stats:
            stat['driver_class_display'] = dict(Driver.CLASS_CHOICES).get(stat['driver_class'],
                                                                              'Неизвестный класс')
        serializer = DriverClassStatsSerializer(stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

URLs:

```python title="bus_depot_project/bus_depot_app/urls.py"
urlpatterns = [
    # ...
    path('drivers/class-stats', DriverClassStatsAPIView.as_view()),
    # ...
]
```

Пример запроса:

```
GET /bus-depot/drivers/class-stats
```

Пример ответа:

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "driver_class": "1",
        "driver_class_display": "Первый класс",
        "count": 2
    },
    {
        "driver_class": "2",
        "driver_class_display": "Второй класс",
        "count": 1
    }
]
```

#### Реализация отчёта

Также в рамках работы требовалось создать API-эндпоинт для генерации сложного отчёта по автобусному парку. Я реализовал отчёт, который предоставляет общую информацию по автопарку, а также данные по всем обслуживаемым маршрутам с развёрнутой структурой вида "маршрут - типы автобусов на этом маршруте - конкретные автобусы этих типов - водители, приписанные к этим автобусам". Реализация получилась следующая:

Сериализаторы:

```python title="bus_depot_project/bus_depot_app/serializers.py"
class ReportDriverSerializer(serializers.ModelSerializer):
    """
    Сериализатор для водителей для отчёта.
    """
    class Meta:
        model = Driver
        fields = [
            'id', 'full_name', 'passport', 'birth_date',
            'driver_class', 'experience', 'salary'
        ]


class ReportBusSerializer(serializers.ModelSerializer):
    """
    Сериализатор для автобусов для отчёта.
    """
    drivers = ReportDriverSerializer(many=True)
    class Meta:
        model = Bus
        fields = [
            'id', 'license_plate', 'is_active', 'purchase_date',
            'drivers'
        ]


class ReportBusTypeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для типов автобуса для отчёта.
    """
    buses = ReportBusSerializer(many=True)
    class Meta:
        model = BusType
        fields = [
            'id', 'name', 'capacity',
            'buses'
        ]


class ReportRouterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для маршрутов для отчёта.
    """
    bus_types = ReportBusTypeSerializer(many=True)
    class Meta:
        model = Route
        fields = [
            'id', 'number', 'start_point', 'end_point',
            'start_time', 'end_time', 'interval', 'duration',
            'bus_types'
        ]


class ReportSummarySerializer(serializers.Serializer):
    """
    Сериализатор для общей статистики для отчёта.
    """
    total_routes = serializers.IntegerField()
    total_route_length_minutes = serializers.IntegerField()
    total_bus_types = serializers.IntegerField()
    bus_type_distribution = serializers.DictField()
    total_buses = serializers.IntegerField()
    total_drivers = serializers.IntegerField()
    drivers_average_experience = serializers.FloatField()
    drivers_class_distribution = serializers.DictField()


class ReportSerializer(serializers.Serializer):
    """
    Главный сериализатор для полного отчёта.
    """
    summary = ReportSummarySerializer()
    routes = ReportRouterSerializer(many=True)
```

Представление:

```python title="bus_depot_project/bus_depot_app/views.py"
class ReportAPIView(APIView):
    """
    API для получения отчёта по автобусному парку.
    """
    def get(self, request):
        # Получаем общую статистику
        summary_data = self.get_summary_data()

        # Получаем данные по маршрутам
        routes_data = self.get_routes_data()

        # Преобразуем полученные данные с помощью сериализатора и возвращаем
        report_data = {
            'summary': summary_data,
            'routes': routes_data
        }
        serializer = ReportSerializer(report_data)
        return Response(serializer.data)

    def get_summary_data(self):
        """
        Формирование общей статистики.
        """
        # Рассчитываем различные total-значения
        total_routes = Route.objects.count()
        total_route_length_minutes = Route.objects.aggregate(
            total=Sum('duration')
        )['total'] or 0
        total_bus_types = BusType.objects.count()
        total_buses = Bus.objects.count()
        total_drivers = Driver.objects.count()

        # Рассчитываем распределение типов автобусов
        bus_type_distribution = {}
        for bus_type in BusType.objects.all():
            count = Bus.objects.filter(bus_type=bus_type).count()
            bus_type_distribution[bus_type.name] = count
        
        # Рассчитываем средний стаж водителя
        drivers_avg_experience = Driver.objects.aggregate(
            avg_exp=Avg('experience')
        )['avg_exp'] or 0

        # Рассчитываем распределение водителей по классам
        drivers_class_distribution = {
            '1': Driver.objects.filter(driver_class='1').count(),
            '2': Driver.objects.filter(driver_class='2').count(),
            '3': Driver.objects.filter(driver_class='3').count()
        }

        # Возвращаем полученные данные
        return {
            'total_routes': total_routes,
            'total_route_length_minutes': total_route_length_minutes,
            'total_bus_types': total_bus_types,
            'bus_type_distribution': bus_type_distribution,
            'total_buses': total_buses,
            'total_drivers': total_drivers,
            'drivers_average_experience': round(drivers_avg_experience, 1),
            'drivers_class_distribution': drivers_class_distribution
        }

    def get_routes_data(self):
        """
        Сбор данных для всех маршрутов.
        """
        # Перебираем все маршруты, для каждого маршрута получаем данные
        # и возвращаем полученные результаты
        routes_data = []
        for route in Route.objects.all():
            route_data = self.get_route_data(route)
            routes_data.append(route_data)
        return routes_data

    def get_route_data(self, route):
        """
        Получение данных для конкретного маршрута.
        """
        # Требуемые данные маршрута
        route_data = {
            'id': route.id,
            'number': route.number,
            'start_point': route.start_point,
            'end_point': route.end_point,
            'start_time': route.start_time,
            'end_time': route.end_time,
            'interval': route.interval,
            'duration': route.duration,
            'bus_types': []
        }

        # Получаем всех водителей для данного маршрута
        route_drivers = Driver.objects.filter(main_route=route)

        # Словарь для данных по типам автобусов на данном маршруте
        bus_types_data = {}

        # Перебираем всех водителей
        for driver in route_drivers:
            # Если у водителя нет главного автобуса, то пропускаем итерацию
            if driver.main_bus is None:
                continue

            # Получаем главный автобус водителя и тип этого автобуса 
            bus = driver.main_bus
            bus_type = bus.bus_type

            # Если этого типа нет в словаре типов автобусов, то добавляем
            if bus_type.id not in bus_types_data:
                bus_types_data[bus_type.id] = {
                    'id': bus_type.id,
                    'name': bus_type.name,
                    'capacity': bus_type.capacity,
                    'buses': {}
                }
            
            # Если автобус не добавлен в словарь автобусов данного типа, то добавляем
            if bus.id not in bus_types_data[bus_type.id]['buses']:
                bus_types_data[bus_type.id]['buses'][bus.id] = {
                    'id': bus.id,
                    'license_plate': bus.license_plate,
                    'is_active': bus.is_active,
                    'purchase_date': bus.purchase_date,
                    'drivers': []
                }
            
            # Формируем данные для водителя и добавляем в список водителей данного автобуса
            driver_data = {
                'id': driver.id,
                'full_name': driver.full_name,
                'passport': driver.passport,
                'birth_date': driver.birth_date,
                'driver_class': driver.driver_class,
                'experience': driver.experience,
                'salary': driver.salary
            }
            bus_types_data[bus_type.id]['buses'][bus.id]['drivers'].append(driver_data)

        # Преобразуем словари в списки и добавляем к данным маршрута
        for bus_type_id, bus_type_data in bus_types_data.items():
            buses_list = list(bus_type_data['buses'].values())
            route_data['bus_types'].append({
                'id': bus_type_data['id'],
                'name': bus_type_data['name'],
                'capacity': bus_type_data['capacity'],
                'buses': buses_list
            })

        # Возвращаем данные маршрута
        return route_data
```

URLs:

```python title="bus_depot_project/bus_depot_app/urls.py"
urlpatterns = [
    # ...
    path('report/', ReportAPIView.as_view()),
    # ...
]
```

Пример запроса:

```
GET /bus-depot/report/
```

Пример ответа:

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "summary": {
        "total_routes": 2,
        "total_route_length_minutes": 170,
        "total_bus_types": 3,
        "bus_type_distribution": {
            "Маленький автобус": 1,
            "Средний автобус": 1,
            "Большой автобус": 1
        },
        "total_buses": 3,
        "total_drivers": 3,
        "drivers_average_experience": 7.7,
        "drivers_class_distribution": {
            "1": 2,
            "2": 1,
            "3": 0
        }
    },
    "routes": [
        {
            "id": 1,
            "number": "R1",
            "start_point": "ул. Дзержинского, 18",
            "end_point": "ул. Полевая, 24",
            "start_time": "08:00:00",
            "end_time": "20:00:00",
            "interval": 15,
            "duration": 50,
            "bus_types": [
                {
                    "id": 1,
                    "name": "Маленький автобус",
                    "capacity": 10,
                    "buses": [
                        {
                            "id": 1,
                            "license_plate": "B1",
                            "is_active": true,
                            "purchase_date": "2020-01-01",
                            "drivers": [
                                {
                                    "id": 1,
                                    "full_name": "Фролов Олег Николаевич",
                                    "passport": "2365898564",
                                    "birth_date": "1980-05-02",
                                    "driver_class": "1",
                                    "experience": 5,
                                    "salary": 80000
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 2,
                    "name": "Средний автобус",
                    "capacity": 20,
                    "buses": [
                        {
                            "id": 2,
                            "license_plate": "B2",
                            "is_active": true,
                            "purchase_date": "2020-01-02",
                            "drivers": [
                                {
                                    "id": 2,
                                    "full_name": "Кузнецов Николай Егорович",
                                    "passport": "5236956324",
                                    "birth_date": "1996-07-02",
                                    "driver_class": "2",
                                    "experience": 3,
                                    "salary": 70000
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "id": 2,
            "number": "R2",
            "start_point": "ул. Больничная, 48",
            "end_point": "ул. Фрунзе, 35",
            "start_time": "09:00:00",
            "end_time": "21:00:00",
            "interval": 30,
            "duration": 120,
            "bus_types": [
                {
                    "id": 3,
                    "name": "Большой автобус",
                    "capacity": 40,
                    "buses": [
                        {
                            "id": 3,
                            "license_plate": "B3",
                            "is_active": true,
                            "purchase_date": "2020-01-03",
                            "drivers": [
                                {
                                    "id": 3,
                                    "full_name": "Архипов Сергей Ильич",
                                    "passport": "7859652345",
                                    "birth_date": "1978-09-07",
                                    "driver_class": "1",
                                    "experience": 15,
                                    "salary": 90000
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}
```

### Подключение регистрации / авторизации по токенам / вывод информации о текущем пользователе средствами Djoser

Установим Djoser:

```
pip install djoser
```

Добавим Djoser в приложения проекта:

```python title="bus_depot_project/bus_depot_project/settings.py"
INSTALLED_APPS = [
    # ...
    'djoser',
    # ...
]
```

Настроим проект для работы с Djoser:

```python title="bus_depot_project/bus_depot_project/settings.py"
# Настройки REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Настройки Djoser
DJOSER = {
    'LOGIN_FIELD': 'username',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SERIALIZERS': {
        'user_create': 'djoser.serializers.UserCreateSerializer',
        'user': 'djoser.serializers.UserSerializer',
        'current_user': 'djoser.serializers.UserSerializer',
    }
}
```

Добавим Djoser в URLs:

```python title="bus_depot_project/bus_depot_project/urls.py"
urlpatterns = [
    # ...
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # ...
]
```

Сделаем миграцию:

```
python manage.py migrate
```

Теперь проверим, что Djoser работает корректно. Запустим сервер и выполним следующие запросы:

Пробуем получить доступ к API без токена:

``` title="Запрос"
curl -X GET http://127.0.0.1:8000/bus-depot/routes/1/  \
    -H "Content-Type: application/json"
```

``` title="Ответ"
{"detail":"Authentication credentials were not provided."}
```

Видим, что теперь без токена доступа получить доступ к API нельзя.

Регистрируем пользователя:

``` title="Запрос"
curl -X POST http://127.0.0.1:8000/auth/users/ \
    -H "Content-Type: application/json" \
    -d '{"username": "user1", "password": "eJ8871QTGR", "re_password": "eJ8871QTGR"}'
```

``` title="Ответ"
{"email":"","username":"user1","id":2}
```

Видим, что нам успешно удалось зарегистрировать нового пользователя.

Теперь попробуем получить токен доступа:

``` title="Запрос"
curl -X POST http://127.0.0.1:8000/auth/token/login/ \
    -H "Content-Type: application/json" \
    -d '{"username": "user1", "password": "eJ8871QTGR"}'
```

``` title="Ответ"
{"auth_token":"3dd319d5d99c90f5e7cbb6c116bc38c4d7e1faed"}
```

Видим, что нам был выдан токен.

Теперь попробуем с помощью этого токена получить доступ к API:

``` title="Запрос"
curl -X GET http://127.0.0.1:8000/bus-depot/routes/1/ \
    -H "Authorization: Token 3dd319d5d99c90f5e7cbb6c116bc38c4d7e1faed"
```

``` title="Ответ"
{"id":1,"number":"R1","start_point":"ул. Дзержинского, 18","end_point":"ул. Полевая, 24","start_time":"08:00:00","end_time":"20:00:00","interval":15,"duration":50}
```

Видим, что при наличии токена доступ к API получить удаётся.

Теперь попробуем вывести информацию о текущем пользователе:

``` title="Запрос"
curl -X GET http://127.0.0.1:8000/auth/users/me/ \
    -H "Authorization: Token 3dd319d5d99c90f5e7cbb6c116bc38c4d7e1faed"
```

``` title="Ответ"
{"email":"","id":2,"username":"user1"}
```

Видим, что удалось получить информацию о текущем пользователе.

Теперь попробуем выйти из аккаунта (удалить токен) и после этого получить доступ к API:

``` title="Запрос"
curl -X POST http://127.0.0.1:8000/auth/token/logout/ \
    -H "Authorization: Token 3dd319d5d99c90f5e7cbb6c116bc38c4d7e1faed"
```

(Данный запрос ничего не возвращает.)

``` title="Запрос"
curl -X GET http://127.0.0.1:8000/bus-depot/routes/1/ \
    -H "Authorization: Token 3dd319d5d99c90f5e7cbb6c116bc38c4d7e1faed"
```

``` title="Ответ"
{"detail":"Invalid token."}
```

Видим, что после выхода из аккаунта старый токен считается недействительным.

### Реализация документации, описывающую работу всех используемых endpoint-ов средствами MkDocs

Документация для созданных API-эндпоинтов содержится в соответствующем разделе документации к данной лабораторной работе.
