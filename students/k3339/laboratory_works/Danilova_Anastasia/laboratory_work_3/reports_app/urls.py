from django.urls import path
from .views import *

app_name = 'reports_app'
urlpatterns = [
    path('objects-statistics/', ObjectStatusReportView.as_view()),
    path('plants-by-life-form/', PlantsByLifeFormReportView.as_view(),),
    path('workers-with-objects-count/', WorkerObjectCountView.as_view()),
    path('worker-colleagues/<int:pk>/', WorkerColleaguesListAPIView.as_view()),
    path('most-planted-species-per-object/', MostPlantedSpeciesPerObjectView.as_view()),
    path('worker-plants-per-object-over-period/', WorkerPlantsPerObjectView.as_view()), # ?date_from=2024-05-01&date_to=2024-05-31
]
