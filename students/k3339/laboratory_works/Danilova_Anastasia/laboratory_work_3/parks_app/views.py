from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics

from .serializers import *


# Create your views here.

@extend_schema(tags=['Enterprise'])
class EnterpriseListAPIView(generics.ListCreateAPIView):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer

@extend_schema(tags=['Enterprise'])
class EnterpriseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer

@extend_schema(tags=['Service'])
class ServiceListAPIView(generics.ListCreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer

@extend_schema(tags=['Service'])
class ServiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer

@extend_schema(tags=['Objects'])
class ObjectListAPIView(generics.ListCreateAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer

@extend_schema(tags=['Objects'])
class ObjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer

@extend_schema(tags=['Contract'])
class ContractListAPIView(generics.ListCreateAPIView):
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['object']  # или 'object_id'

    def get_queryset(self):
        queryset = Contract.objects.all()

        # Фильтрация по параметрам запроса
        object_id = self.request.query_params.get('object')
        enterprise_id = self.request.query_params.get('enterprise')

        if object_id:
            queryset = queryset.filter(object_id=object_id)
        if enterprise_id:
            queryset = queryset.filter(enterprise_id=enterprise_id)

        return queryset

@extend_schema(tags=['Contract'])
class ContractDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

@extend_schema(tags=['Decorator'])
class DecoratorListAPIView(generics.ListCreateAPIView):
    queryset = Decorator.objects.all()
    serializer_class = DecoratorSerializer


@extend_schema(tags=['Decorator'])
class DecoratorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Decorator.objects.all()
    serializer_class = DecoratorSerializer


@extend_schema(tags=['ObjectZone'])
class ObjectZoneListAPIView(generics.ListCreateAPIView):
    queryset = ObjectZone.objects.all()
    serializer_class = ObjectZoneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['object']


@extend_schema(tags=['ObjectZone'])
class ObjectZoneDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ObjectZone.objects.all()
    serializer_class = ObjectZoneSerializer

@extend_schema(tags=['Plant'])
class PlantListAPIView(generics.ListCreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer  # Используем PlantSerializer для создания

    def get_queryset(self):
        queryset = Plant.objects.all()

        object_id = self.request.query_params.get("object_id")
        if object_id:
            queryset = queryset.filter(
                placements__zone__object_id=object_id
            ).distinct()

        return queryset

@extend_schema(tags=['Plant'])
class PlantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


@extend_schema(tags=['PlantPlacement'])
class PlantPlacementListAPIView(generics.ListCreateAPIView):
    queryset = PlantPlacement.objects.all()
    serializer_class = PlantPlacementFullSerializer  # Используйте FullSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        object_id = self.request.query_params.get('object_id')
        if object_id:
            queryset = queryset.filter(zone__object_id=object_id)
        return queryset


@extend_schema(tags=['PlantPlacement'])
class PlantPlacementListAPIView(generics.ListCreateAPIView):
    queryset = PlantPlacement.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PlantPlacementCreateSerializer
        return PlantPlacementFullSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        object_id = self.request.query_params.get('object_id')
        if object_id:
            queryset = queryset.filter(zone__object_id=object_id)
        return queryset

@extend_schema(tags=['PlantPlacement'])
class PlantPlacementDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlantPlacement.objects.all()
    serializer_class = PlantPlacementFullSerializer

@extend_schema(tags=['LifeForm'])
class LifeFormListAPIView(generics.ListCreateAPIView):
    queryset = LifeForm.objects.all()
    serializer_class = LifeFormSerializer

@extend_schema(tags=['LifeForm'])
class LifeFormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LifeForm.objects.all()
    serializer_class = LifeFormSerializer

@extend_schema(tags=['Species'])
class SpeciesListAPIView(generics.ListCreateAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

@extend_schema(tags=['Species'])
class SpeciesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

@extend_schema(tags=['PlantWateringSchedule'])
class PlantWateringScheduleListAPIView(generics.ListCreateAPIView):
    serializer_class = PlantWateringScheduleSerializer

    def get_queryset(self):
        queryset = PlantWateringSchedule.objects.all()

        object_id = self.request.query_params.get("object_id")
        if object_id:
            queryset = queryset.filter(
                plant__placements__zone__object_id=object_id
            ).distinct()

        return queryset


@extend_schema(tags=['PlantWateringSchedule'])
class PlantWateringScheduleByPlantAPIView(generics.RetrieveAPIView):
    serializer_class = PlantWateringScheduleSerializer

    def get_object(self):
        plant_id = self.kwargs.get('plant_id')
        try:
            return PlantWateringSchedule.objects.get(plant_id=plant_id)
        except PlantWateringSchedule.DoesNotExist:
            raise Http404("No watering schedule found for this plant")

@extend_schema(tags=['PlantWateringSchedule'])
class PlantWateringScheduleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlantWateringSchedule.objects.all()
    serializer_class = PlantWateringScheduleSerializer

@extend_schema(tags=['Worker'])
class WorkerListAPIView(generics.ListCreateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerFullSerializer

@extend_schema(tags=['Worker'])
class WorkerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

@extend_schema(tags=['Worker'])
class WorkerDetailFullAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerFullSerializer


@extend_schema(tags=['WorkerAssignment'])
class WorkerAssignmentListAPIView(generics.ListCreateAPIView):
    queryset = PlantWorkerAssignment.objects.all()
    serializer_class = PlantWorkerAssignmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'plant': ['exact'],
        'worker': ['exact'],
        'plant__placements__zone__object': ['exact'],  # Это может мешать
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        plant_id = self.request.query_params.get('plant')
        if plant_id:
            queryset = queryset.filter(plant_id=plant_id)
        return queryset

@extend_schema(tags=['WorkerAssignment'])
class WorkerAssignmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlantWorkerAssignment.objects.all()
    serializer_class = PlantWorkerAssignmentSerializer

@extend_schema(tags=['ObjectWorker'])
class ObjectWorkerListAPIView(generics.ListCreateAPIView):
    queryset = ObjectWorkerAssignment.objects.all()
    serializer_class = ObjectWorkerAssignmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['object', 'worker']

@extend_schema(tags=['ObjectWorker'])
class ObjectWorkerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ObjectWorkerAssignment.objects.all()
    serializer_class = ObjectWorkerAssignmentSerializer
