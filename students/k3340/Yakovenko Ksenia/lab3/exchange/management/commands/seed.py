import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.apps import apps


APP_LABEL = "exchange"  # <-- если у тебя приложение называется иначе, поменяй


class Command(BaseCommand):
    help = "Seed database with test data for Lab3/Lab4"

    @transaction.atomic
    def handle(self, *args, **options):
        # models
        Profession = apps.get_model(APP_LABEL, "Profession")
        EducationLevel = apps.get_model(APP_LABEL, "EducationLevel")
        Employer = apps.get_model(APP_LABEL, "Employer")
        Applicant = apps.get_model(APP_LABEL, "Applicant")
        Vacancy = apps.get_model(APP_LABEL, "Vacancy")


        # --- clear old data (optional but convenient for labs)
        Vacancy.objects.all().delete()
        Applicant.objects.all().delete()
        Employer.objects.all().delete()
        Profession.objects.all().delete()
        EducationLevel.objects.all().delete()

        self.stdout.write("Old data cleared.")

        # --- education levels
        edu_names = [
            ("Secondary", 1),
            ("College", 2),
            ("Bachelor", 3),
            ("Master", 4),
        ]
        edus = []
        for name, rank in edu_names:
            edus.append(EducationLevel.objects.create(name=name, rank=rank))
        self.stdout.write(f"EducationLevels: {len(edus)}")

        # --- professions (make many)
        prof_titles = [
            "Android Developer", "Backend Developer", "QA Engineer", "Data Analyst", "DevOps Engineer",
            "Project Manager", "UI/UX Designer", "Sales Manager", "HR Specialist", "Accountant",
            "System Administrator", "Support Engineer", "Marketing Specialist", "Business Analyst",
            "Mobile Tester", "Java Developer", "Python Developer", "Frontend Developer"
        ]
        # ensure unique names
        professions = [Profession.objects.create(name=t) for t in prof_titles]
        # add extra generic professions
        for i in range(1, 21):
            professions.append(Profession.objects.create(name=f"Profession {i}"))

        self.stdout.write(f"Professions: {len(professions)}")

        # --- employers
        employers = []
        for i in range(1, 11):
            employers.append(
                Employer.objects.create(
                    name=f"Company {i}",
                    address=f"City, Street {i}",
                    contact_person=f"Contact {i}",
                    phone=f"+1-555-01{i:02d}",
                    email=f"hr{i}@company.com",
                )
            )
        self.stdout.write(f"Employers: {len(employers)}")

        # --- split professions: some will have NO vacancies at all
        random.shuffle(professions)
        profs_with_vacancies = professions[: int(len(professions) * 0.7)]  # 70% have vacancies
        profs_without_vacancies = professions[int(len(professions) * 0.7) :]  # 30% without

        # --- vacancies (only for profs_with_vacancies)
        vacancies = []
        for _ in range(60):
            prof = random.choice(profs_with_vacancies)
            emp = random.choice(employers)
            edu_req = random.choice(edus)
            exp = random.randint(0, 5)
            grade = random.randint(1, 5)
            s_from = random.randint(20000, 90000)
            s_to = s_from + random.randint(5000, 60000)

            v = Vacancy.objects.create(
                employer=emp,
                profession=prof,
                education_required=edu_req,
                required_experience_years=exp,
                required_grade=grade,
                salary_from=s_from,
                salary_to=s_to,
                status=Vacancy.Status.OPEN if random.random() < 0.75 else Vacancy.Status.CLOSED,
                date_posted=(timezone.now().date() - timedelta(days=random.randint(0, 60))),
            )
            vacancies.append(v)

        self.stdout.write(f"Vacancies: {len(vacancies)}")

        # --- applicants
        applicants = []
        for i in range(1, 51):
            # force some applicants into professions WITHOUT vacancies
            if i <= 12:
                prof = random.choice(profs_without_vacancies) if profs_without_vacancies else random.choice(professions)
            else:
                prof = random.choice(professions)

            edu = random.choice(edus)
            exp = random.randint(0, 8)
            grade = random.randint(1, 5)
            last_salary = random.randint(15000, 120000)

            a = Applicant.objects.create(
                full_name=f"Applicant {i}",
                profession=prof,
                education_level=edu,
                experience_years=exp,
                grade=grade,
                last_salary=last_salary,
            )
            applicants.append(a)

        self.stdout.write(f"Applicants: {len(applicants)}")

        self.stdout.write(self.style.SUCCESS("Seed completed ✅"))
        self.stdout.write(
            self.style.WARNING(
                f"Professions without vacancies: {len(profs_without_vacancies)} (analytics #1 should NOT be empty now)"
            )
        )