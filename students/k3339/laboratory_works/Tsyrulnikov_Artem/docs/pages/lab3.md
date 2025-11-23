## Лабораторная работа: REST API для рекламного агентства

В третьей лабораторной работе реализовано REST API для отдела маркетинга рекламного агентства на Django REST Framework. Проект включает модели базы данных, сериализаторы, ViewSets с кастомными действиями для отчетов и авторизацию по токенам через Djoser.

## Вариант задания

- Реализовать модель базы данных средствами Django ORM для рекламного агентства «Луч».
- Создать API средствами Django REST Framework с сериализацией данных.
- Подключить регистрацию/авторизацию по токенам через Djoser.
- Реализовать учет заявок клиентов (рекламодателей), прайс-лист услуг, платежные поручения.
- Обеспечить запросы: список выполненных работ, платежные поручения за период, номенклатура услуг по видам, заявки по заказчику, нагрузка сотрудников.
- Отчет об объеме работ исполнителей за последний квартал.

## Ход выполнения

## Задание 1: Модели базы данных

_Модели_

- `apps/agency/models.py`: реализованы 6 моделей для предметной области рекламного агентства.
- **Client** — заказчик с полями: название компании, контактное лицо, телефон, email.
- **Employee** — сотрудник агентства, связан с `User` через `OneToOneField`. Хранит ФИО, телефон, email, должность.
- **ServiceCategory** — категория рекламных услуг (вид услуги).
- **Service** — услуга из прайс-листа: категория (FK), наименование, цена, единица измерения, материалы.
- **Order** — заявка клиента: ссылки на клиента, услугу и исполнителя, количество, стоимость, статус (`new`/`in_progress`/`completed`), дата создания.
- **PaymentOrder** — платежное поручение: связь с заявкой (OneToOne), дата выставления, дата оплаты, флаг оплаты.

_База данных_

- `config/settings.py`: подключение к SQLite (по умолчанию), легко переключается на PostgreSQL через переменные окружения.

## Задание 2: Сериализаторы DRF

_Основные сериализаторы_

- `apps/agency/serializers.py`: для каждой модели создан `ModelSerializer` с полями `__all__`.
- **ServiceSerializer** — добавлено read-only поле `category_name` через `source="category.name"`.
- **OrderSerializer** — read-only поля: `client_name`, `service_name`, `executor_name` (с кастомным методом), `status_display` для отображения статуса.
- **PaymentOrderSerializer** — read-only поля: `order_id`, `client_name`, `service_name`.

_Сериализаторы для отчетов_

- **CompletedWorkSerializer** — дата оплаты, заказчик, код услуги, исполнитель.
- **EmployeeWorkloadSerializer** — имя исполнителя и количество заявок.
- **QuarterReportSerializer** — исполнитель и суммарная стоимость работ.

## Задание 3: API Views и ViewSets

_ViewSets_

- `apps/agency/views.py`: 6 ViewSets на базе `ModelViewSet` с `IsAuthenticated` permission.
- **ClientViewSet** — CRUD + кастомный action `orders` для получения заявок клиента с фильтрацией по дате (`date_from`, `date_to`).
- **EmployeeViewSet** — CRUD + action `workload` для расчета нагрузки сотрудников (количество заявок за период).
- **ServiceCategoryViewSet** — стандартный CRUD для категорий услуг.
- **ServiceViewSet** — CRUD + action `by_category` для фильтрации услуг по категории.
- **OrderViewSet** — CRUD для заявок с select_related для оптимизации запросов.
- **PaymentOrderViewSet** — CRUD + actions: `completed_works`, `by_period`, `quarter_report`.

_URL маршрутизация_

- `apps/agency/urls.py`: используется `DefaultRouter` для автоматической генерации маршрутов.
- Эндпоинты: `/api/clients/`, `/api/employees/`, `/api/categories/`, `/api/services/`, `/api/orders/`, `/api/payments/`.

## Задание 4: Авторизация через Djoser

_Настройка_

- `config/urls.py`: подключены маршруты Djoser — `/api/auth/` для регистрации/авторизации.
- Используется `djangorestframework-simplejwt` для JWT токенов.
- `djoser` обеспечивает эндпоинты: создание пользователя, получение токена, информация о текущем пользователе (`/api/auth/users/me/`).

_Зависимости_

- `pyproject.toml`: django, djangorestframework, djoser, djangorestframework-simplejwt, drf-spectacular.

## Задание 5: Специальные запросы и отчеты

_Список выполненных работ_

- `PaymentOrderViewSet.completed_works`: возвращает оплаченные платежные поручения с датой оплаты, заказчиком, кодом услуги, исполнителем.

_Платежные поручения за период_

- `PaymentOrderViewSet.by_period`: фильтрация по параметрам `date_from`/`date_to` с информацией о заказчике, услуге, статусе оплаты.

_Номенклатура услуг по видам_

- `ServiceViewSet.by_category`: фильтрация услуг по ID категории.

_Заявки клиента за период_

- `ClientViewSet.orders`: получение заявок конкретного клиента с фильтрацией по дате.

_Нагрузка сотрудников_

- `EmployeeViewSet.workload`: агрегация количества заявок по исполнителям за указанный период через `annotate(Count)`.

_Отчет за квартал_

- `PaymentOrderViewSet.quarter_report`: агрегация стоимости работ по исполнителям за последние 3 месяца через `Sum`.

_Swagger документация_

- Подключен `drf-spectacular`: схема API доступна по `/api/schema/`, интерактивная документация — `/api/docs/`.

## Выводы

В работе освоил разработку REST API на Django REST Framework: создание моделей предметной области, сериализацию с вложенными полями, ViewSets с кастомными actions для отчетов, JWT-авторизацию через Djoser. Реализованы все требуемые запросы к базе данных — от списков заявок до агрегированных отчетов по исполнителям.
