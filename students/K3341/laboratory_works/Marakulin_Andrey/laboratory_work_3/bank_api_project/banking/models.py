from django.db import models


class Position(models.Model):
    id_position = models.AutoField(primary_key=True, verbose_name='ID Должности')
    title = models.CharField(max_length=100, verbose_name='Наименование')
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Оклад')
    vacancies_count = models.IntegerField(verbose_name='Количество вакансий')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.title


class Employee(models.Model):
    id_employee = models.AutoField(primary_key=True, verbose_name='ID Сотрудника')
    fio = models.CharField(max_length=255, verbose_name='ФИО')
    birth_date = models.DateField(verbose_name='Дата рождения')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    passport_data = models.CharField(max_length=50, verbose_name='Паспортные данные')
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Оклад')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.fio


class EmployeePosition(models.Model):
    id_employee_position = models.AutoField(primary_key=True, verbose_name='ID Занимаемой должности')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник',
                                 related_name='positions_history')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Должность')
    start_date = models.DateField(verbose_name='Дата вступления в должность')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания должности')

    class Meta:
        verbose_name = 'Занимаемая должность'
        verbose_name_plural = 'Занимаемые должности'

    def __str__(self):
        return f"{self.employee.fio} - {self.position.title}"


class Client(models.Model):
    id_client = models.AutoField(primary_key=True, verbose_name='ID Клиента')
    fio = models.CharField(max_length=255, verbose_name='ФИО')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.fio


class Passport(models.Model):
    id_passport = models.AutoField(primary_key=True, verbose_name='ID Паспорта')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент', related_name='passports')
    series = models.CharField(max_length=4, verbose_name='Серия')
    number = models.CharField(max_length=6, verbose_name='Номер')
    issue_date = models.DateField(verbose_name='Дата выдачи')
    issued_by = models.CharField(max_length=255, verbose_name='Кем выдан')
    fio_on_passport = models.CharField(max_length=255, verbose_name='ФИО в паспорте')

    class Meta:
        verbose_name = 'Паспорт'
        verbose_name_plural = 'Паспорта'

    def __str__(self):
        return f"Паспорт {self.series} {self.number} ({self.client.fio})"


class Currency(models.Model):
    code = models.CharField(max_length=3, primary_key=True, verbose_name='Код валюты')
    name = models.CharField(max_length=50, verbose_name='Наименование валюты')

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self):
        return self.code


class ExchangeRate(models.Model):
    id_rate = models.AutoField(primary_key=True, verbose_name='ID Курса')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name='Код валюты', related_name='rates')
    multiplier = models.IntegerField(verbose_name='Кратность')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='Стоимость покупки')
    sale_price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='Стоимость продажи')
    date = models.DateField(verbose_name='Дата')

    class Meta:
        verbose_name = 'Курс валют'
        verbose_name_plural = 'Курсы валют'

    def __str__(self):
        return f"{self.currency.code} ({self.date})"


class DepositType(models.Model):
    id_deposit_type = models.AutoField(primary_key=True, verbose_name='ID Типа вклада')
    name = models.CharField(max_length=100, verbose_name='Наименование вклада')
    description = models.TextField(verbose_name='Описание вклада')
    min_term = models.IntegerField(verbose_name='Минимальный срок вклада')
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Минимальная сумма вклада')
    term = models.IntegerField(verbose_name='Срок (в днях/месяцах)')
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Процентная ставка')

    class Meta:
        verbose_name = 'Тип вклада'
        verbose_name_plural = 'Типы вкладов'

    def __str__(self):
        return self.name


class Deposit(models.Model):
    id_deposit = models.AutoField(primary_key=True, verbose_name='ID Вклада')
    deposit_type = models.ForeignKey(DepositType, on_delete=models.CASCADE, verbose_name='Тип вклада')
    contract_data = models.CharField(max_length=255, verbose_name='Данные договора')
    contract_number = models.CharField(max_length=50, verbose_name='Номер договора')
    deposit_date = models.DateField(verbose_name='Дата вклада')
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма вклада')
    return_date = models.DateField(verbose_name='Дата возврата')
    return_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма возврата')
    actual_return_date = models.DateField(null=True, blank=True, verbose_name='Фактическая дата возврата')

    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name='Код валюты')
    employee_position = models.ForeignKey(EmployeePosition, on_delete=models.SET_NULL, null=True, blank=True,
                                          verbose_name='Занимаемая должность сотрудника')

    class Meta:
        verbose_name = 'Вклад'
        verbose_name_plural = 'Вклады'

    def __str__(self):
        return f"Вклад №{self.id_deposit} ({self.deposit_type.name})"


class DepositSchedule(models.Model):
    id_schedule = models.AutoField(primary_key=True, verbose_name='ID Графика начислений')
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, verbose_name='ID Вклада', related_name='schedule')
    charge_date = models.DateField(verbose_name='Дата начисления')
    charge_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма начисления')
    number = models.IntegerField(verbose_name='Номер начисления')

    class Meta:
        verbose_name = 'График начислений'
        verbose_name_plural = 'Графики начислений'

    def __str__(self):
        return f"Начисление {self.number} по вкладу {self.deposit.id_deposit}"


class CreditType(models.Model):
    id_credit_type = models.AutoField(primary_key=True, verbose_name='ID Типа кредита')
    name = models.CharField(max_length=100, verbose_name='Название')
    type = models.CharField(max_length=50, verbose_name='Тип')
    term = models.IntegerField(verbose_name='Срок')
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Процентная ставка')
    balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Остаток')

    class Meta:
        verbose_name = 'Тип кредита'
        verbose_name_plural = 'Типы кредитов'

    def __str__(self):
        return self.name


class Credit(models.Model):
    id_credit = models.AutoField(primary_key=True, verbose_name='ID Кредита')
    credit_type = models.ForeignKey(CreditType, on_delete=models.CASCADE, verbose_name='Тип кредита')
    contract_data = models.CharField(max_length=255, verbose_name='Данные договора')
    contract_number = models.CharField(max_length=50, verbose_name='Номер договора')
    credit_date = models.DateField(verbose_name='Дата кредита')
    credit_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма кредита')
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ежемесячная сумма')
    payment_count = models.IntegerField(verbose_name='Число выплаты')
    authorized_person = models.CharField(max_length=255, verbose_name='Доверенное лицо')
    closing_date = models.DateField(verbose_name='Дата закрытия')
    actual_closing_date = models.DateField(null=True, blank=True, verbose_name='Фактическая дата закрытия')

    passport = models.ForeignKey(Passport, on_delete=models.CASCADE, verbose_name='Паспорт')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name='Код валюты')
    employee_position = models.ForeignKey(EmployeePosition, on_delete=models.SET_NULL, null=True, blank=True,
                                          verbose_name='Занимаемая должность сотрудника')

    class Meta:
        verbose_name = 'Кредит'
        verbose_name_plural = 'Кредиты'

    def __str__(self):
        return f"Кредит №{self.id_credit} ({self.credit_type.name})"


class CreditPaymentSchedule(models.Model):
    id_schedule = models.AutoField(primary_key=True, verbose_name='ID Графика выплат')
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, verbose_name='ID Кредита',
                               related_name='payment_schedule')
    payment_date = models.DateField(verbose_name='Дата выплаты')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма выплаты')
    balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Остаток')
    actual_payment_date = models.DateField(null=True, blank=True, verbose_name='Дата фактической выплаты')
    interest_payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма выплаты по процентам')
    number = models.IntegerField(verbose_name='Номер выплаты')

    class Meta:
        verbose_name = 'График выплат по кредиту'
        verbose_name_plural = 'Графики выплат по кредиту'

    def __str__(self):
        return f"Выплата {self.number} по кредиту {self.credit.id_credit}"