# Отчет по лабораторной работе №3
### Тема: Разработка серверной части (API) банковского приложения

### Структура проекта

Проект представляет собой REST API приложение на Django + Django REST Framework. Реализована сложная структура базы данных и механизмы авторизации для дальнейшей интеграции с клиентской частью на Vue.js.

1.  **Проект `bank_api_project`**
    * `bank_api_project/settings.py` — основной файл настроек: подключение `rest_framework`, `djoser` (авторизация), `drf_yasg` (документация) и `corsheaders`.
    * `bank_api_project/urls.py` — глобальная маршрутизация, включая подключение эндпоинтов авторизации и Swagger-документации.

2.  **Приложение `banking`**
    * `models.py` — описывает структуру базы данных согласно варианту "Маракулин". Включает модели: `Client`, `Passport`, `Deposit`, `Loan`, `Employee` и справочники (`Currency`, `Position`).
    * `serializers.py` — отвечает за преобразование сложных типов данных (моделей Django) в JSON и обратно. Реализована поддержка вложенных структур (например, графики платежей внутри кредита).
    * `views.py` — содержит логику обработки запросов (API Views). Используются `ModelViewSet` для реализации полного CRUD функционала.
    * `urls.py` — определяет маршруты (Router) для ресурсов API (`/api/v1/...`).



## 1. Проектирование и реализация модели данных

Схема базы данных реализована с использованием Django ORM в строгом соответствии с выданным вариантом. Обеспечена целостность данных через использование `ForeignKey`, `PROTECT` и `CASCADE` ограничений.

Ключевые сущности:
- **`Client` / `Passport`**: Хранение персональных данных.
- **`Deposit` / `DepositType`**: Управление вкладами, включая типы вкладов и графики начислений.
- **`Loan` / `LoanType`**: Управление кредитами, графиками выплат и типами кредитования.
- **`Employee` / `Position`**: Кадровый учет, история должностей.

**Код:**

*banking/models.py (фрагмент):*
```python
from django.db import models

class Client(models.Model):
    fio = models.CharField(max_length=255, verbose_name="ФИО")
    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email", blank=True, null=True)

    def __str__(self):
        return self.fio

class Deposit(models.Model):
    deposit_type = models.ForeignKey('DepositType', on_delete=models.PROTECT, verbose_name="Тип вклада")
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT, verbose_name="Код валюты")
    passport = models.ForeignKey('Passport', on_delete=models.PROTECT, verbose_name="Паспорт")
    
    contract_number = models.CharField(max_length=50, verbose_name="Номер договора")
    deposit_sum = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Сумма вклада")
    deposit_date = models.DateField(verbose_name="Дата вклада")
    return_date = models.DateField(verbose_name="Дата возврата")

    class Meta:
        verbose_name = "Вклад"
```



## 2. Реализация логики API (Serializers & Views)

Для взаимодействия с клиентом используется Django REST Framework.
- **Сериализаторы (`Serializers`)**: Описывают правила валидации и формат выходных данных.
- **Представления (`ViewSets`)**: Обеспечивают стандартные методы API: `GET` (список/детально), `POST` (создание), `PUT`/`PATCH` (обновление), `DELETE` (удаление).

**Код:**

*banking/serializers.py (фрагмент):*
```python
from rest_framework import serializers
from .models import Deposit, AccrualSchedule

class AccrualScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccrualSchedule
        fields = '__all__'

class DepositSerializer(serializers.ModelSerializer):
    # Вложенный сериализатор для отображения графика начислений вместе с вкладом
    accruals = AccrualScheduleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Deposit
        fields = '__all__'
```

*banking/views.py (фрагмент):*
```python
from rest_framework import viewsets, permissions
from .models import Deposit
from .serializers import DepositSerializer

class DepositViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления вкладами
    """
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]
```



## 3. Аутентификация и Djoser

Для реализации системы регистрации и входа используется библиотека **Djoser**. Настроена аутентификация по токенам (`TokenAuthentication`), что позволяет безопасно взаимодействовать с API внешним клиентам (Vue.js).

Доступные эндпоинты:
- `/auth/users/` — регистрация.
- `/auth/token/login/` — получение токена.
- `/auth/users/me/` — получение данных текущего пользователя.

**Код:**

*settings.py (фрагмент):*
```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders', 
    'banking',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
```


### Выводы
В ходе выполнения лабораторной работы была разработана серверная часть веб-приложения (API).
- Спроектирована и реализована реляционная модель базы данных сложной структуры (более 10 таблиц).
- Настроен Django REST Framework для сериализации данных и обработки HTTP-запросов.
- Подключена система авторизации Djoser (Token Auth).