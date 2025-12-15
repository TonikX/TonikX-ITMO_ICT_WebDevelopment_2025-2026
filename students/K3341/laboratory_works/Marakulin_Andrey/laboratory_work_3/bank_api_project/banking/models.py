from django.db import models


class Client(models.Model):
    """Клиент"""
    fio = models.CharField(max_length=255, verbose_name="ФИО")
    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email", blank=True, null=True)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Passport(models.Model):
    """Паспорт"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='passports', verbose_name="Клиент")
    series = models.CharField(max_length=10, verbose_name="Серия")
    number = models.CharField(max_length=10, verbose_name="Номер")
    date_issue = models.DateField(verbose_name="Дата выдачи")
    issuer = models.CharField(max_length=255, verbose_name="Кем выдан")
    fio = models.CharField(max_length=255, verbose_name="ФИО в паспорте", blank=True)

    def __str__(self):
        return f"{self.series} {self.number}"

    class Meta:
        verbose_name = "Паспорт"
        verbose_name_plural = "Паспорта"


class Currency(models.Model):
    """Валюта"""
    code = models.CharField(max_length=3, unique=True, verbose_name="Код валюты")
    name = models.CharField(max_length=50, verbose_name="Наименование валюты")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"


class ExchangeRate(models.Model):
    """Курсы валют"""
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name="Код валюты")
    date = models.DateTimeField(verbose_name="Дата")
    buy_price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Стоимость покупки")
    sell_price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Стоимость продажи")
    multiplicity = models.IntegerField(default=1, verbose_name="Кратность")

    class Meta:
        verbose_name = "Курс валют"
        verbose_name_plural = "Курсы валют"


class Position(models.Model):
    """Должности"""
    name = models.CharField(max_length=100, verbose_name="Наименование")
    salary = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Оклад")
    vacancies_count = models.IntegerField(verbose_name="Количество вакансий")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class Employee(models.Model):
    """Сотрудник"""
    fio = models.CharField(max_length=255, verbose_name="ФИО")
    dob = models.DateField(verbose_name="Дата рождения")
    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    passport_data = models.TextField(verbose_name="Паспортные данные")
    salary = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Оклад")

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class OccupiedPosition(models.Model):
    """Занимаемая должность"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Должность")
    start_date = models.DateField(verbose_name="Дата вступления")
    end_date = models.DateField(verbose_name="Дата окончания", null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - {self.position}"

    class Meta:
        verbose_name = "Занимаемая должность"
        verbose_name_plural = "Занимаемые должности"


class DepositType(models.Model):
    """Тип вклада"""
    name = models.CharField(max_length=100, verbose_name="Наименование вклада")
    description = models.TextField(verbose_name="Описание вклада")
    min_term = models.IntegerField(verbose_name="Минимальный срок (мес)")
    min_sum = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Минимальная сумма")
    term = models.IntegerField(verbose_name="Срок")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процентная ставка")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип вклада"
        verbose_name_plural = "Типы вкладов"


class Deposit(models.Model):
    """Вклад"""
    deposit_type = models.ForeignKey(DepositType, on_delete=models.PROTECT, verbose_name="Тип вклада")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name="Код валюты")
    passport = models.ForeignKey(Passport, on_delete=models.PROTECT,
                                 verbose_name="Паспорт")
    processed_by = models.ForeignKey(OccupiedPosition, on_delete=models.PROTECT, verbose_name="Оформил сотрудник")

    contract_number = models.CharField(max_length=50, verbose_name="Номер договора")
    contract_data = models.TextField(verbose_name="Данные договора")
    deposit_data = models.TextField(verbose_name="Данные вклада", blank=True)

    deposit_sum = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Сумма вклада")
    return_sum = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Сумма возврата", null=True,
                                     blank=True)
    deposit_date = models.DateField(verbose_name="Дата вклада")
    return_date = models.DateField(verbose_name="Дата возврата")
    fact_return_date = models.DateField(verbose_name="Фактическая дата возврата", null=True, blank=True)

    class Meta:
        verbose_name = "Вклад"
        verbose_name_plural = "Вклады"


class AccrualSchedule(models.Model):
    """График начислений (для вклада)"""
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, related_name='accruals', verbose_name="Вклад")
    date = models.DateField(verbose_name="Дата начисления")
    sum = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Сумма начисления")
    number = models.IntegerField(verbose_name="Номер")

    class Meta:
        verbose_name = "График начислений"
        verbose_name_plural = "Графики начислений"


class LoanType(models.Model):
    """Тип кредита"""
    name = models.CharField(max_length=100, verbose_name="Название")
    loan_type = models.CharField(max_length=100, verbose_name="Тип")
    term = models.IntegerField(verbose_name="Срок")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процентная ставка")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип кредита"
        verbose_name_plural = "Типы кредитов"


class Loan(models.Model):
    """Кредит"""
    loan_type = models.ForeignKey(LoanType, on_delete=models.PROTECT, verbose_name="Тип кредита")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name="Код валюты")
    passport = models.ForeignKey(Passport, on_delete=models.PROTECT, verbose_name="Паспорт")
    processed_by = models.ForeignKey(OccupiedPosition, on_delete=models.PROTECT, verbose_name="Оформил сотрудник")

    contract_number = models.CharField(max_length=50, verbose_name="Номер договора")
    contract_data = models.TextField(verbose_name="Данные договора")
    loan_data = models.TextField(verbose_name="Данные кредита", blank=True)
    trusted_person = models.CharField(max_length=255, verbose_name="Доверенное лицо", blank=True)

    date_issue = models.DateField(verbose_name="Дата кредита")
    sum_credit = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Сумма кредита")
    payout_count = models.IntegerField(verbose_name="Число выплат")
    monthly_payment = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Ежемесячная сумма")

    close_date = models.DateField(verbose_name="Дата закрытия")
    fact_close_date = models.DateField(verbose_name="Фактическая дата закрытия", null=True, blank=True)

    class Meta:
        verbose_name = "Кредит"
        verbose_name_plural = "Кредиты"


class PayoutSchedule(models.Model):
    """График выплат (по кредиту)"""
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payouts', verbose_name="Кредит")
    date_payout = models.DateField(verbose_name="Дата выплаты")
    sum_payout = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Сумма выплаты")
    sum_interest = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Сумма выплаты по процентам")
    remainder = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Остаток")
    fact_date_payout = models.DateField(verbose_name="Дата фактической выплаты", null=True, blank=True)
    number = models.IntegerField(verbose_name="Номер")

    class Meta:
        verbose_name = "График выплат"
        verbose_name_plural = "Графики выплат"