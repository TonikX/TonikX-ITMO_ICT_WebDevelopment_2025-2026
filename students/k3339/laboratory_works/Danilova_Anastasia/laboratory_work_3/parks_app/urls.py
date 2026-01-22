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
    path('plants/<int:plant_id>/plantwateringschedules/', PlantWateringScheduleByPlantAPIView.as_view()),

    path('workers/', WorkerListAPIView.as_view()),
    # path('workers/<int:pk>/', WorkerDetailAPIView.as_view()),
    path('workers/<int:pk>/', WorkerDetailFullAPIView.as_view()),

    path('workerassignments/', WorkerAssignmentListAPIView.as_view()),
    path('workerassignments/<int:pk>/', WorkerAssignmentDetailAPIView.as_view()),

    path('objectworkers/', ObjectWorkerListAPIView.as_view()),
    path('objectworkers/<int:pk>', ObjectWorkerDetailAPIView.as_view()),

]
