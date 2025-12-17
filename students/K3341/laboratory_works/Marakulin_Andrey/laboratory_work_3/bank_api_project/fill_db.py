import os
import django
import random
from datetime import date, timedelta
from decimal import Decimal
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank_api_project.settings')
django.setup()

from banking.models import *


def run():
    print(" Очистка старых данных (на всякий случай) ")
    PayoutSchedule.objects.all().delete()
    AccrualSchedule.objects.all().delete()
    Loan.objects.all().delete()
    Deposit.objects.all().delete()
    Passport.objects.all().delete()
    Client.objects.all().delete()
    OccupiedPosition.objects.all().delete()
    Employee.objects.all().delete()
    Position.objects.all().delete()
    ExchangeRate.objects.all().delete()
    Currency.objects.all().delete()
    DepositType.objects.all().delete()
    LoanType.objects.all().delete()

    print(" Создание справочников ")

    rub = Currency.objects.create(code='RUB', name='Российский Рубль')
    usd = Currency.objects.create(code='USD', name='Доллар США')
    eur = Currency.objects.create(code='EUR', name='Евро')

    for i in range(5):
        d = date.today() - timedelta(days=i)
        ExchangeRate.objects.create(currency=usd, date=d, buy_price=90 + i, sell_price=95 + i, multiplicity=1)
        ExchangeRate.objects.create(currency=eur, date=d, buy_price=100 + i, sell_price=105 + i, multiplicity=1)

    pos_manager = Position.objects.create(name='Менеджер', salary=50000, vacancies_count=2)
    pos_boss = Position.objects.create(name='Начальник отдела', salary=100000, vacancies_count=1)

    emp1 = Employee.objects.create(
        fio='Смирнова Анна Ивановна', dob='1990-05-15', address='ул. Ленина 1',
        phone='89001112233', passport_data='4010 123123', salary=50000
    )
    emp2 = Employee.objects.create(
        fio='Козлов Борис Петрович', dob='1985-11-20', address='ул. Мира 5',
        phone='89005556677', passport_data='4011 987987', salary=100000
    )

    occ_emp1 = OccupiedPosition.objects.create(
        employee=emp1, position=pos_manager, start_date='2023-01-01'
    )
    occ_emp2 = OccupiedPosition.objects.create(
        employee=emp2, position=pos_boss, start_date='2022-01-01'
    )

    dt_vip = DepositType.objects.create(
        name='VIP Вклад', description='Для богатых', min_term=12, min_sum=1000000, term=12, interest_rate=15.5
    )
    dt_simple = DepositType.objects.create(
        name='Простой', description='Для всех', min_term=3, min_sum=1000, term=6, interest_rate=10.0
    )

    lt_mortgage = LoanType.objects.create(
        name='Ипотека', loan_type='Целевой', term=120, interest_rate=12.0
    )
    lt_cash = LoanType.objects.create(
        name='Наличными', loan_type='Потребительский', term=24, interest_rate=25.0
    )

    print(" Создание Клиентов и Паспортов ")

    clients_data = [
        ('Иванов Иван Иванович', '4020', '100100'),
        ('Петров Петр Петрович', '4020', '200200'),
        ('Сидоров Сидор Сидорович', '4020', '300300'),
    ]

    passports_list = []

    for fio, series, number in clients_data:
        client = Client.objects.create(
            fio=fio, address='г. Москва', phone=f'8900{random.randint(1000000, 9999999)}', email='test@mail.ru'
        )
        passport = Passport.objects.create(
            client=client, series=series, number=number,
            date_issue='2020-01-01', issuer='УФМС', fio=fio
        )
        passports_list.append(passport)

    print(" Создание Вкладов, Кредитов и Графиков ")

    for i, passport in enumerate(passports_list):

        dep = Deposit.objects.create(
            deposit_type=dt_simple,
            currency=rub,
            passport=passport,
            processed_by=occ_emp1,
            contract_number=f"DEP-{i + 1}",
            contract_data="Текст договора...",
            deposit_sum=Decimal(100000 * (i + 1)),
            deposit_date='2024-01-01',
            return_date='2024-06-01'
        )


        for m in range(1, 4):
            AccrualSchedule.objects.create(
                deposit=dep, date=date(2024, m, 15), sum=Decimal(1000 * (i + 1)), number=m
            )


        loan = Loan.objects.create(
            loan_type=lt_cash,
            currency=rub,
            passport=passport,
            processed_by=occ_emp1,
            contract_number=f"LOAN-{i + 1}",
            contract_data="Договор кредита...",
            sum_credit=Decimal(50000 * (i + 1)),
            payout_count=12,
            monthly_payment=Decimal(5000),
            date_issue='2024-02-01',
            close_date='2025-02-01'
        )


        for m in range(3, 6):
            PayoutSchedule.objects.create(
                loan=loan,
                date_payout=date(2024, m, 20),
                sum_payout=Decimal(5000),
                sum_interest=Decimal(1000),
                remainder=Decimal(50000 - (1000 * m)),
                number=m - 2
            )

    print(" Успешно! База наполнена данными ")


if __name__ == '__main__':
    run()