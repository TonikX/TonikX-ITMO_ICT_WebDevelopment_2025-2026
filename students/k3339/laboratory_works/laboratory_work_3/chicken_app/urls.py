from django.urls import path

from chicken_app.views import EmployeeAPIView, EmployeeDetailsAPIView, ResponsibleEmployeeAPIView, DietAPIView, \
    DietDetailsAPIView, BreedAPIView, BreedDetailsAPIView, ChickenAPIView, ChickenDetailsAPIView, LaborContractsAPIView, \
    LaborContractDetailsAPIView, CellAPIView, WorkshopWithMostBreedAPIView, EggPerformanceByWeightBreedAgeAPIView, \
    AverageEggsPerEmployeeAPIView, ChickenCountByBreedWorkshopAPIView, BreedPerformanceDifferenceAPIView, \
    MonthlyReportAPIView, ResponsibleEmployeeDetailsAPIView

urlpatterns = [
    path('employees/', EmployeeAPIView.as_view()),
    path('employees/<int:pk>/', EmployeeDetailsAPIView.as_view()),
    path('employees/cells/', ResponsibleEmployeeAPIView.as_view()),
    path('employees/cells/<int:pk>/', ResponsibleEmployeeDetailsAPIView.as_view()),
    path('diets/', DietAPIView.as_view()),
    path('diets/<int:pk>/', DietDetailsAPIView.as_view()),
    path('breeds/', BreedAPIView.as_view()),
    path('breeds/<int:pk>/', BreedDetailsAPIView.as_view()),
    path('chicken/', ChickenAPIView.as_view()),
    path('chicken/<int:pk>/', ChickenDetailsAPIView.as_view()),
    path('employees/contracts/', LaborContractsAPIView.as_view()),
    path('employees/contracts/<int:pk>/', LaborContractDetailsAPIView.as_view()),
    path('cells/', CellAPIView.as_view()),
    path('workshop/breeds/', WorkshopWithMostBreedAPIView.as_view()),
    path('egg/performance/breed/', EggPerformanceByWeightBreedAgeAPIView.as_view()),
    path('employees/eggs/', AverageEggsPerEmployeeAPIView.as_view()),
    path('workshop/breeds/count/', ChickenCountByBreedWorkshopAPIView.as_view()),
    path('breeds/difference/', BreedPerformanceDifferenceAPIView.as_view()),
    path('reports/', MonthlyReportAPIView.as_view())
]
