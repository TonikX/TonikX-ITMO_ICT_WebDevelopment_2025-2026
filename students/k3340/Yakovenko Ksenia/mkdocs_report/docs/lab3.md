# Lab3 — Backend на Django REST Framework

## Цель работы
Разработать backend-приложение с REST API для предметной области **“Биржа труда”**:
хранение соискателей и вакансий, пособий, формирование аналитических запросов и отчёта.

## Используемые технологии
- Python, Django
- Django REST Framework (DRF)
- SQLite (или другая БД, если используешь)

## Предметная область
ИС хранит данные:
- **Соискатели** (профессия, образование, стаж, разряд, последняя зарплата)
- **Работодатели** (контактные данные)
- **Вакансии** (требования, зарплата, дата подачи, статус)
- **Пособия** (размер, даты начала/окончания)

## Структура данных (модели)
Кратко описать сущности и связи:

- `Profession` — справочник профессий
- `EducationLevel` — справочник уровней образования (rank)
- `Applicant` → FK `Profession`, FK `EducationLevel`
- `Employer`
- `Vacancy` → FK `Employer`, FK `Profession`, FK `EducationLevel`, status OPEN/CLOSED
- `BenefitPayment` → FK `Applicant`



## Реализованное REST API

### CRUD endpoints
(через DRF ViewSet + Router)

- `GET/POST /api/professions/`
- `GET/POST /api/education-levels/`
- `GET/POST /api/applicants/`
- `GET/POST /api/employers/`
- `GET/POST /api/vacancies/`
- `GET/POST /api/benefit-payments/`

Также поддерживаются операции:
- `GET /api/<entity>/{id}/`
- `PUT/PATCH /api/<entity>/{id}/`
- `DELETE /api/<entity>/{id}/`

## Запросы к базе данных (аналитика)

### 1. Профессии соискателей, не представленные в таблице вакансий
Endpoint:
- `GET /api/analytics/applicant-professions-not-in-vacancies/`

Результат: список профессий.

### 2. Все возможные варианты вакансий для соискателей
Endpoint:
- `GET /api/analytics/vacancies-for-applicants/`

Логика подбора:
- профессия совпадает
- образование соискателя >= требуемого (по rank)
- стаж и разряд не ниже требований
- вакансия в статусе OPEN

### 3. Количество дней с момента предложения вакансии для незакрытых вакансий
Endpoint:
- `GET /api/analytics/open-vacancies-days-since-posted/`

Результат: список открытых вакансий + `days_since_posted`.

### 4. Количество выплачиваемых пособий на текущий момент
Endpoint:
- `GET /api/analytics/active-benefits-count/`

Логика: дата сегодня попадает в диапазон `[date_start, date_end]`.

### 5. Количество вакансий с высшим образованием и зарплатой 5000..60000
Endpoint:
- `GET /api/analytics/vacancies-count-high-edu-salary-range/`

## Отчёт

### Для каждого предприятия вывести список открытых вакансий с указанием общего количества
Endpoint:
- `GET /api/reports/employers-open-vacancies/`

Результат: работодатель + список его открытых вакансий + count.

## Генерация тестовых данных
Для наполнения БД реализована management-команда seed:

```bash
python manage.py seed
```

![vacancy list.png](images/screenshots3/vacancy%20list.png)
Результат выполнения запроса `GET /api/vacancies/`, который возвращает список всех вакансий, хранящихся в системе.
В ответе API отображаются основные характеристики вакансии: требуемый стаж `(required_experience_years)`,
разряд `(required_grade)`, диапазон заработной платы `(salary_from, salary_to)`,
дата публикации `(date_posted)`, статус вакансии `(status)`,
а также ссылки на связанные сущности — работодателя `(employer)`,
профессию `(profession)` и требуемый уровень образования `(education_required)`.
Данные возвращаются в формате JSON.

![open vacancies days since posted.png](images/screenshots3/open%20vacancies%20days%20since%20posted.png)
Результат выполнения аналитического запроса `GET /api/analytics/open-vacancies-days-since-posted/`.
Запрос выводит список открытых вакансий и количество дней, прошедших с момента их публикации.
Поле `days_since_posted` рассчитывается как разница между текущей датой и датой размещения вакансии `(date_posted)`.