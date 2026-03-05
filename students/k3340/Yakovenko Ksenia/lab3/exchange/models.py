from django.db import models


class Profession(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.name


class EducationLevel(models.Model):
    """
    rank: чем больше — тем выше уровень
    Например: 1=Среднее, 2=Среднее спец, 3=Высшее
    """
    name = models.CharField(max_length=120, unique=True)
    rank = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["rank"]

    def __str__(self) -> str:
        return self.name


class Applicant(models.Model):
    full_name = models.CharField(max_length=200)
    profession = models.ForeignKey(Profession, on_delete=models.PROTECT, related_name="applicants")
    education_level = models.ForeignKey(EducationLevel, on_delete=models.PROTECT, related_name="applicants")
    experience_years = models.PositiveSmallIntegerField(default=0)
    grade = models.PositiveSmallIntegerField(default=1)  # разряд
    last_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.full_name


class Employer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=300, blank=True)
    contact_person = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self) -> str:
        return self.name


class Vacancy(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        CLOSED = "CLOSED", "Closed"

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name="vacancies")
    profession = models.ForeignKey(Profession, on_delete=models.PROTECT, related_name="vacancies")
    education_required = models.ForeignKey(EducationLevel, on_delete=models.PROTECT, related_name="vacancies_required")
    required_experience_years = models.PositiveSmallIntegerField(default=0)
    required_grade = models.PositiveSmallIntegerField(default=1)
    salary_from = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    salary_to = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_posted = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)

    additional_info = models.TextField(blank=True)

    class Meta:
        ordering = ["-date_posted"]

    def __str__(self) -> str:
        return f"{self.employer.name}: {self.profession.name} ({self.status})"


class BenefitPayment(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name="benefits")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date_start = models.DateField()
    date_end = models.DateField()

    class Meta:
        ordering = ["-date_start"]

    def __str__(self) -> str:
        return f"{self.applicant.full_name}: {self.amount} ({self.date_start}..{self.date_end})"