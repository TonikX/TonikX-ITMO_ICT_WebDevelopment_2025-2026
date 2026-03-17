from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .auth_views import register, change_password

from .views import (
    ProfessionViewSet, EducationLevelViewSet, ApplicantViewSet,
    EmployerViewSet, VacancyViewSet, BenefitPaymentViewSet,
    AnalyticsViewSet, ReportsViewSet
)

router = DefaultRouter()
router.register("professions", ProfessionViewSet)
router.register("education-levels", EducationLevelViewSet)
router.register("applicants", ApplicantViewSet)
router.register("employers", EmployerViewSet)
router.register("vacancies", VacancyViewSet)
router.register("benefit-payments", BenefitPaymentViewSet)

router.register("analytics", AnalyticsViewSet, basename="analytics")
router.register("reports", ReportsViewSet, basename="reports")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(router.urls)),
    path("auth/login/", obtain_auth_token),
    path("auth/register/", register),
    path("auth/change-password/", change_password),
]
