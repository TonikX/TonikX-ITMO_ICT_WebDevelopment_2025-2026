from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class IndividualClient(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField()
    passport = models.CharField(max_length=10)


class Agent(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    passport = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)


class IndividualContract(models.Model):
    contract_statuses = (
        ('a', 'active'),
        ('p', 'paused'),
        ('e', 'expired')
    )

    contract_types = (
        ('m', 'medical'),
        ('l', 'life-property'),
        ('a', 'accident'),
    )
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    client = models.ForeignKey(IndividualClient, on_delete=models.CASCADE)
    sign_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=1, choices=contract_statuses)
    type = models.CharField(max_length=1, choices=contract_types)


class LaborContract(models.Model):
    contract_statuses = (
        ('a', 'active'),
        ('p', 'paused'),
        ('f', 'fired'),
        ('e', 'expired')
    )

    contract_types = (
        ('f', 'full-time'),
        ('p', 'part-time'),
        ('d', 'deal')
    )

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=contract_types)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=1, choices=contract_statuses)


class Organization(models.Model):
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100)
    address = models.TextField()
    bank_code = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)


class CollectiveContract(models.Model):
    contract_statuses = (
        ('a', 'active'),
        ('p', 'paused'),
        ('e', 'expired')
    )

    contract_types = (
        ('m', 'medical'),
        ('l', 'life-property'),
        ('a', 'accident'),
        ('g', 'mortgage'),
    )

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    sign_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=1, choices=contract_statuses)
    type = models.CharField(max_length=1, choices=contract_types)


class RiskCategory(models.Model):
    title = models.CharField(max_length=100)
    payment_amount = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(10000000)])


class InsuredEmployee(models.Model):
    client = models.ForeignKey(IndividualClient, on_delete=models.CASCADE)
    risk_category = models.ForeignKey(RiskCategory, on_delete=models.CASCADE)
    collective_contract = models.ForeignKey(CollectiveContract, on_delete=models.CASCADE, related_name='insured_employees')


class InsuredEventIndividual(models.Model):
    date = models.DateField()
    cause = models.TextField()
    contract = models.ForeignKey(IndividualContract, on_delete=models.CASCADE)
    decision = models.CharField(max_length=50)


class IndividualPayment(models.Model):
    date = models.DateField()
    amount = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(10000000)])
    event = models.ForeignKey(InsuredEventIndividual, on_delete=models.CASCADE)


class InsuredEventEmployee(models.Model):
    date = models.DateField()
    cause = models.TextField()
    employee = models.ForeignKey(InsuredEmployee, on_delete=models.CASCADE)
    decision = models.CharField(max_length=50)


class EmployeePayment(models.Model):
    date = models.DateField()
    amount = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(10000000)])
    event = models.ForeignKey(InsuredEventEmployee, on_delete=models.CASCADE)
