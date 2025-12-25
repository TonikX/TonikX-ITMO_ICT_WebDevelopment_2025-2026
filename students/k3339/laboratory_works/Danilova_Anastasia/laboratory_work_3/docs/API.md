## Схема сущностей

### Serializers.py

Для большинства моделей и их ендпоинтов был сделан один сериализатор на все CRUD операции, за исключением случаев, когда
нужны были какие-то особые методы.

```python
from rest_framework import serializers
from .models import Services, Enterprise, Object, Contract, Decorator, ObjectZone, Plant,
    PlantPlacement, LifeForm, Species, PlantWateringSchedule, Worker, PlantWorkerAssignment, ObjectWorkerAssignment


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = "__all__"


class EnterpriseDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = "__all__"


class ObjectSerializer(serializers.ModelSerializer):
    is_serviced = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Object
        fields = "__all__"

    def get_is_serviced(self, obj):
        return obj.is_serviced


class ObjectZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectZone
        fields = "__all__"


class ObjectReadSerializer(serializers.ModelSerializer):
    zones = ObjectZoneSerializer(many=True, read_only=True)

    class Meta:
        model = Object
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"


class DecoratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decorator
        fields = "__all__"


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = "__all__"


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = "__all__"


class PlantReadSerializer(serializers.ModelSerializer):
    current_age = serializers.ReadOnlyField()
    species = SpeciesSerializer(read_only=True)

    class Meta:
        model = Plant
        fields = "__all__"


class PlantPlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantPlacement
        fields = "__all__"


class LifeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeForm
        fields = "__all__"


class PlantWateringScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantWateringSchedule
        fields = "__all__"


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = "__all__"


class WorkerFullSerializer(serializers.ModelSerializer):
    active_objects_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Worker
        fields = ["id", "first_name", "last_name", "middle_name", "phone_number", "address", "active_objects_count"]

    def get_active_objects_count(self, obj):
        return obj.object_assignments.filter(
            end_date__isnull=True
        ).count()


class PlantWorkerAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantWorkerAssignment
        fields = "__all__"


class ObjectWorkerAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectWorkerAssignment
        fields = "__all__"

```

Таким образом, можно заметить, что отличия от стандартного сериалайзера есть у класса WorkerFullSerializer - это
дополнительный serializer, который помимо основных полей показывает, за сколькими активными объектами закреплен
сотрудник.

Также у класса объекта сделан метод для получения property is_serviced.


### Views.py 

Для вью было выбрано сочетать для get и post запроса реализацию generics.ListCreateAPIView метода, а для put, patch и delete использовать generics.RetrieveUpdateDestroyAPIView

```python
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Exists, OuterRef, Subquery
from .serializers import *


# Create your views here.

class EnterpriseListAPIView(generics.ListCreateAPIView):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer


class EnterpriseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer


class ServiceListAPIView(generics.ListCreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer


class ServiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer


class ObjectListAPIView(generics.ListCreateAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer


class ObjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer


 ...


class ObjectWorkerListAPIView(generics.ListCreateAPIView):
    queryset = ObjectWorkerAssignment.objects.all()
    serializer_class = ObjectWorkerAssignmentSerializer


class ObjectWorkerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ObjectWorkerAssignment.objects.all()
    serializer_class = ObjectWorkerAssignmentSerializer

```

### Endpoints

#### Urls.py
Кратко список основных ендпоинтов можно увидеть по урлам приложения:

```python
from django.urls import path
from .views import *

app_name = 'parks_app'
urlpatterns = [
    path('enterprises/', EnterpriseListAPIView.as_view()),
    path('enterprises/<int:pk>/', EnterpriseDetailAPIView.as_view()),

    path('services/', ServiceListAPIView.as_view()),
    path('services/<int:pk>/', ServiceDetailAPIView.as_view()),

    path('objects/', ObjectListAPIView.as_view()),
    path('objects/<int:pk>/', ObjectDetailAPIView.as_view()),

    path('contracts/', ContractListAPIView.as_view()),
    path('contracts/<int:pk>/', ContractDetailAPIView.as_view()),

    path('decorators/', DecoratorListAPIView.as_view()),
    path('decorators/<int:pk>/', DecoratorDetailAPIView.as_view()),

    path('objectzones/', ObjectZoneListAPIView.as_view()),
    path('objectzones/<int:pk>/', ObjectZoneDetailAPIView.as_view()),

    path('plants/', PlantListAPIView.as_view()),
    path('plants/<int:pk>/', PlantDetailAPIView.as_view()),

    path('plantplacements/', PlantPlacementListAPIView.as_view()),
    path('plantplacements/<int:pk>/', PlantPlacementDetailAPIView.as_view()),

    path('lifeforms/', LifeFormListAPIView.as_view()),
    path('lifeforms/<int:pk>/', LifeFormDetailAPIView.as_view()),

    path('species/', SpeciesListAPIView.as_view()),
    path('species/<int:pk>/', SpeciesDetailAPIView.as_view()),

    path('plantwateringschedules/', PlantWateringScheduleListAPIView.as_view()),
    path('plantwateringschedules/<int:pk>/', PlantWateringScheduleDetailAPIView.as_view()),

    path('workers/', WorkerListAPIView.as_view()),
    # path('workers/<int:pk>/', WorkerDetailAPIView.as_view()),
    path('workers/<int:pk>/', WorkerDetailFullAPIView.as_view()),

    path('workerassignments/', WorkerAssignmentListAPIView.as_view()),
    path('workerassignments/<int:pk>/', WorkerAssignmentDetailAPIView.as_view()),

    path('objectworkers/', ObjectWorkerListAPIView.as_view()),
    path('objectworkers/<int:pk>', ObjectWorkerDetailAPIView.as_view()),

]

```

#### Screenshots

Ниже продемонстрирована работа вышеперечисленных енпоинтов:


##### **enterprises**

```python
path('enterprises/', EnterpriseListAPIView.as_view()),
```

![img_11.png](img_11.png)
![img_13.png](img_13.png)

```python
    path('enterprises/<int:pk>/', EnterpriseDetailAPIView.as_view()),
```

![img_12.png](img_12.png)


##### **services**

```python
    path('services/', ServiceListAPIView.as_view()),
```

![img_14.png](img_14.png)

```python
    path('services/<int:pk>/', ServiceDetailAPIView.as_view()),
```

![img_15.png](img_15.png)


##### **objects**

```python
    path('objects/', ObjectListAPIView.as_view()),
```

![img_16.png](img_16.png)

```python
    path('objects/<int:pk>/', ObjectDetailAPIView.as_view()),
```

![img_17.png](img_17.png)


##### **contracts**

```python
    path('contracts/', ContractListAPIView.as_view()),
```

![img_18.png](img_18.png)

```python
    path('contracts/<int:pk>/', ContractDetailAPIView.as_view()),
```

![img_19.png](img_19.png)


##### **decorators**

```python
    path('decorators/', DecoratorListAPIView.as_view()),
```

![img_20.png](img_20.png)

```python
    path('decorators/<int:pk>/', DecoratorDetailAPIView.as_view()),
```

![img_21.png](img_21.png)


##### **objectzones**

```python
    path('objectzones/', ObjectZoneListAPIView.as_view()),
```

![img_22.png](img_22.png)

```python
    path('objectzones/<int:pk>/', ObjectZoneDetailAPIView.as_view()),
```

![img_23.png](img_23.png)


##### **plants**

```python
        path('plants/', PlantListAPIView.as_view()),
```

![img_24.png](img_24.png)

```python
    path('plants/<int:pk>/', PlantDetailAPIView.as_view()),
```

![img_25.png](img_25.png)


##### **plantplacements**

```python
    path('plantplacements/', PlantPlacementListAPIView.as_view()),
```

![img_26.png](img_26.png)

```python
    path('plantplacements/<int:pk>/', PlantPlacementDetailAPIView.as_view()),
```

![img_27.png](img_27.png)


##### **lifeforms**

```python
    path('lifeforms/', LifeFormListAPIView.as_view()),
```

![img_28.png](img_28.png)

```python
    path('lifeforms/<int:pk>/', LifeFormDetailAPIView.as_view()),
```

![img_29.png](img_29.png)


##### **species**

```python
    path('species/', SpeciesListAPIView.as_view()),
```

![img_30.png](img_30.png)

```python
    path('species/<int:pk>/', SpeciesDetailAPIView.as_view()),
```

![img_31.png](img_31.png)


##### **plantwateringschedules**

```python
    path('plantwateringschedules/', PlantWateringScheduleListAPIView.as_view()),
```

![img_32.png](img_32.png)

```python
    path('plantwateringschedules/<int:pk>/', PlantWateringScheduleDetailAPIView.as_view()),
```

![img_33.png](img_33.png)



##### **workers**

```python
    path('workers/', WorkerListAPIView.as_view()),
```

![img_34.png](img_34.png)

```python
    path('workers/<int:pk>/', WorkerDetailFullAPIView.as_view()),
```

![img_35.png](img_35.png)


##### **workerassignments**

```python
    path('workerassignments/', WorkerAssignmentListAPIView.as_view()),
```

![img_36.png](img_36.png)

```python
    path('workerassignments/<int:pk>/', WorkerAssignmentDetailAPIView.as_view()),
```

![img_37.png](img_37.png)


##### **objectworkers**

```python
    path('objectworkers/', ObjectWorkerListAPIView.as_view()),
```

![img_38.png](img_38.png)

```python
    path('objectworkers/<int:pk>', ObjectWorkerDetailAPIView.as_view()),
```

![img_39.png](img_39.png)   





