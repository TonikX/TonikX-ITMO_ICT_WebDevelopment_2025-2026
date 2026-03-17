from datetime import date

from django.db.models import Count, F, Q
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Profession, EducationLevel, Applicant, Employer, Vacancy, BenefitPayment
from .serializers import (
    ProfessionSerializer, EducationLevelSerializer, ApplicantSerializer,
    EmployerSerializer, VacancySerializer, BenefitPaymentSerializer
)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class EducationLevelViewSet(viewsets.ModelViewSet):
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer


class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer


class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.select_related("employer", "profession", "education_required").all()
    serializer_class = VacancySerializer


class BenefitPaymentViewSet(viewsets.ModelViewSet):
    queryset = BenefitPayment.objects.select_related("applicant").all()
    serializer_class = BenefitPaymentSerializer


class AnalyticsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["get"], url_path="applicant-professions-not-in-vacancies")
    def applicant_professions_not_in_vacancies(self, request):
        # 1) Профессии соискателей, которых нет в вакансии
        vacancy_prof_ids = Vacancy.objects.values_list("profession_id", flat=True).distinct()
        profs = Profession.objects.filter(applicants__isnull=False).exclude(id__in=vacancy_prof_ids).distinct()
        return Response(ProfessionSerializer(profs, many=True).data)

    @action(detail=False, methods=["get"], url_path="vacancies-for-applicants")
    def vacancies_for_applicants(self, request):
        """
        2) Все возможные варианты вакансий для соискателей
        Ответ: список вида [{applicant: ..., vacancies: [...]}, ...]
        """
        result = []
        applicants = Applicant.objects.select_related("profession", "education_level").all()

        for a in applicants:
            qs = Vacancy.objects.select_related("employer", "profession", "education_required").filter(
                status=Vacancy.Status.OPEN,
                profession=a.profession,
                required_experience_years__lte=a.experience_years,
                required_grade__lte=a.grade,
                education_required__rank__lte=a.education_level.rank,
            )
            result.append({
                "applicant": ApplicantSerializer(a).data,
                "vacancies": VacancySerializer(qs, many=True).data
            })

        return Response(result)

    @action(detail=False, methods=["get"], url_path="open-vacancies-days-since-posted")
    def open_vacancies_days_since_posted(self, request):
        # 3) Кол-во дней с момента подачи вакансии для незакрытых (OPEN)
        today = now().date()
        qs = Vacancy.objects.filter(status=Vacancy.Status.OPEN).values(
            "id", "employer_id", "profession_id", "date_posted"
        )

        data = []
        for v in qs:
            days = (today - v["date_posted"]).days
            data.append({**v, "days_since_posted": days})

        return Response(data)

    @action(detail=False, methods=["get"], url_path="active-benefits-count")
    def active_benefits_count(self, request):
        # 4) Кол-во выплачиваемых пособий на текущий момент
        today = now().date()
        cnt = BenefitPayment.objects.filter(date_start__lte=today, date_end__gte=today).count()
        return Response({"active_benefits_count": cnt, "date": str(today)})

    @action(detail=False, methods=["get"], url_path="vacancies-count-high-edu-salary-range")
    def vacancies_count_high_edu_salary_range(self, request):
        """
        5) Кол-во вакансий с высшим образованием и зарплатой от 5000 до 60000
        Чуть безопаснее: считаем rank >= 3 как 'высшее'.
        """
        cnt = Vacancy.objects.filter(
            education_required__rank__gte=3,
            salary_from__gte=5000,
            salary_to__lte=60000,
        ).count()
        return Response({"vacancies_count": cnt})


class ReportsViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"], url_path="employers-open-vacancies")
    def employers_open_vacancies(self, request):
        # Отчёт: для каждого предприятия список открытых вакансий + их общее количество
        employers = Employer.objects.all()
        report = []

        for e in employers:
            open_vacancies = Vacancy.objects.filter(employer=e, status=Vacancy.Status.OPEN)
            report.append({
                "employer": EmployerSerializer(e).data,
                "open_vacancies_count": open_vacancies.count(),
                "open_vacancies": VacancySerializer(open_vacancies, many=True).data
            })

        return Response(report)