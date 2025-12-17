# Отчет по лабораторной работе №3
### Тема: Разработка серверной части (API) банковского приложения

### Структура проекта

Проект представляет собой REST API приложение на Django + Django REST Framework. Реализована сложная структура базы данных и механизмы авторизации для дальнейшей интеграции с клиентской частью.

1.  **Проект `bank_api_project`**
    * `bank_api_project/settings.py` — основной файл настроек: подключение `rest_framework`, `djoser` (авторизация), `drf_yasg` (документация) и `corsheaders`.
    * `bank_api_project/urls.py` — глобальная маршрутизация, включая подключение эндпоинтов авторизации и Swagger-документации.

2.  **Приложение `banking`**
    * `models.py` — описывает структуру базы данных согласно варианту "Маракулин". Включает модели: `Client`, `Passport`, `Deposit`, `Loan`, `Employee` и справочники (`Currency`, `Position`).
    * `serializers.py` — отвечает за преобразование сложных типов данных (моделей Django) в JSON и обратно. Реализована поддержка вложенных структур (например, графики платежей внутри кредита).
    * `views.py` — содержит логику обработки запросов (API Views). Используются `ModelViewSet` для реализации полного CRUD функционала, а также кастомные `@action` для аналитики.
    * `urls.py` — определяет маршруты (Router) для ресурсов API (`/api/v1/...`).
    * `admin.py` — конфигурация административной панели для управления всеми сущностями системы.



## 1. Проектирование и реализация модели данных

Схема базы данных реализована с использованием Django ORM. Обеспечена целостность данных через использование `ForeignKey`, `PROTECT` и `CASCADE` ограничений.

Ключевые сущности:
-   **`Client` / `Passport`**: Хранение персональных данных. Реализована связь один-ко-многим.
-   **`Deposit` / `DepositType`**: Управление вкладами, включая типы вкладов и графики начислений (`AccrualSchedule`).
-   **`Loan` / `LoanType`**: Управление кредитами, графиками выплат (`PayoutSchedule`) и типами кредитования.
-   **`Employee` / `Position`**: Кадровый учет, история занимаемых должностей (`OccupiedPosition`).

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
    
    #...
```



## 2. Реализация логики API (Serializers & Views)

Для взаимодействия с клиентом используется Django REST Framework.
-   **Сериализаторы (`Serializers`)**: Описывают правила валидации и формат выходных данных. Реализована **вложенная сериализация** (Criterion 3): при запросе клиента отдаются его паспорта, при запросе кредита — график платежей.
-   **Представления (`ViewSets`)**: Обеспечивают стандартные методы API: `GET`, `POST`, `PUT`, `DELETE`.

**Код:**

*banking/serializers.py (фрагмент):*
```python
from rest_framework import serializers
from .models import Deposit, AccrualSchedule, Loan, PayoutSchedule

class DepositSerializer(serializers.ModelSerializer):
    accruals = AccrualScheduleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Deposit
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    payouts = PayoutScheduleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Loan
        fields = '__all__'
```



## 3. Аутентификация и Djoser

Для реализации системы регистрации и входа используется библиотека **Djoser**. Настроена аутентификация по токенам (`TokenAuthentication`), что позволяет безопасно взаимодействовать с API внешним клиентам.

Доступные эндпоинты:
-   `/auth/users/` — регистрация.
-   `/auth/token/login/` — получение токена.
-   `/auth/users/me/` — получение данных текущего пользователя.

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



## 4. Аналитика и Агрегация данных

В соответствии с требованиями (Criterion 4), реализованы дополнительные endpoints с аналитикой, использующие агрегационные функции SQL (`Sum`, `Count`, `Avg`, `Min`, `Max`).

Реализованы действия:
1.  **Портфель клиента**: Расчет общей суммы вкладов и долгов по кредитам.
2.  **KPI сотрудника**: Подсчет количества и объема оформленных сотрудником договоров.
3.  **Статистика валют**: Анализ колебаний курса (мин/макс/среднее).

**Код:**

*banking/views.py (фрагмент):*
```python
class ClientViewSet(BaseViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=True, methods=['get'])
    def portfolio(self, request, pk=None):
        """
        Агрегационный запрос: Считает общую сумму вкладов и кредитов клиента.
        """
        client = self.get_object()
        
        total_deposits = Deposit.objects.filter(
            passport__client=client
        ).aggregate(total=Sum('deposit_sum'))['total'] or 0

        total_loans = Loan.objects.filter(
            passport__client=client
        ).aggregate(total=Sum('sum_credit'))['total'] or 0

        return Response({
            'client': client.fio,
            'total_deposits_amount': total_deposits,
            'total_loans_amount': total_loans,
            'net_balance': total_deposits - total_loans
        })
```



## 5. Документирование API (Swagger)

Для автоматической генерации документации подключена библиотека `drf-yasg`. Это позволяет тестировать запросы и просматривать структуру ответов через веб-интерфейс без написания внешней документации вручную.

Доступные интерфейсы:
-   **Swagger UI**: `/swagger/`
-   **ReDoc**: `/redoc/`

**Код:**

*bank_api_project/urls.py (фрагмент):*
```python
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Bank API",
      default_version='v1',
      description="API для банковской системы (Лабораторная №3)",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # ...
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
]
```

### Выводы
В ходе выполнения лабораторной работы была разработана серверная часть веб-приложения (API).

-   Спроектирована и реализована реляционная модель базы данных сложной структуры (более 10 таблиц).

-   Настроен Django REST Framework для сериализации данных, включая работу с вложенными объектами.

-   Реализованы сложные агрегационные запросы для бизнес-аналитики.

-   Подключена система авторизации Djoser (Token Auth).

-   Реализована автодокументация API через Swagger.

-   Произведена настройка CORS для будущей интеграции с Vue.js.