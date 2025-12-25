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

class ContractListAPIView(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

class ContractDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

class DecoratorListAPIView(generics.ListCreateAPIView):
    queryset = Decorator.objects.all()
    serializer_class = DecoratorSerializer

class DecoratorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Decorator.objects.all()
    serializer_class = DecoratorSerializer

class ObjectZoneListAPIView(generics.ListCreateAPIView):
    queryset = ObjectZone.objects.all()
    serializer_class = ObjectZoneSerializer

class ObjectZoneDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ObjectZone.objects.all()
    serializer_class = ObjectZoneSerializer

class PlantListAPIView(generics.ListCreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

class PlantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

class PlantPlacementListAPIView(generics.ListCreateAPIView):
    queryset = PlantPlacement.objects.all()
    serializer_class = PlantPlacementSerializer

class PlantPlacementDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlantPlacement.objects.all()
    serializer_class = PlantPlacementSerializer

class LifeFormListAPIView(generics.ListCreateAPIView):
    queryset = LifeForm.objects.all()
    serializer_class = LifeFormSerializer

class LifeFormDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LifeForm.objects.all()
    serializer_class = LifeFormSerializer

class SpeciesListAPIView(generics.ListCreateAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

class SpeciesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

class PlantWateringScheduleListAPIView(generics.ListCreateAPIView):
    queryset = PlantWateringSchedule.objects.all()
    serializer_class = PlantWateringScheduleSerializer

class PlantWateringScheduleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlantWateringSchedule.objects.all()
    serializer_class = PlantWateringScheduleSerializer

class WorkerListAPIView(generics.ListCreateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerFullSerializer

class WorkerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

class WorkerDetailFullAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerFullSerializer



class WorkerAssignmentListAPIView(generics.ListCreateAPIView):
    queryset = PlantWorkerAssignment.objects.all()
    serializer_class = PlantWorkerAssignmentSerializer

class WorkerAssignmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlantWorkerAssignment.objects.all()
    serializer_class = PlantWorkerAssignmentSerializer

class ObjectWorkerListAPIView(generics.ListCreateAPIView):
    queryset = ObjectWorkerAssignment.objects.all()
    serializer_class = ObjectWorkerAssignmentSerializer

class ObjectWorkerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ObjectWorkerAssignment.objects.all()
    serializer_class = ObjectWorkerAssignmentSerializer

