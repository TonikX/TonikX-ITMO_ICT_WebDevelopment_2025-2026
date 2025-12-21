# API

## Аутентификация (Djoser)

- `POST /api/auth/users/` — регистрация пользователя.
- `POST /api/auth/token/login/` — получение токена.
- `POST /api/auth/token/logout/` — отзыв токена.
- `GET /api/auth/users/me/` — текущий пользователь.

Все остальные запросы требуют заголовок `Authorization: Token <token>`.

## CRUD-эндпоинты

| Ресурс | Базовый путь | Описание |
| --- | --- | --- |
| Учителя | `/api/teachers/` | Справочник учителей, их кабинетов, предметов |
| Ученики | `/api/students/` | Сведения об учениках и их принадлежности к классу |
| Классы | `/api/classes/` | Сведения о классах и классных руководителях |
| Предметы | `/api/subjects/` | Набор дисциплин с типами (базовый/профильный) |
| Кабинеты | `/api/classrooms/` | Закрепление кабинетов и их категорий |
| Преподавания | `/api/teacher-subjects/` | Связь учителя и предмета по периодам |
| Назначения | `/api/teaching-assignments/` | Привязка учителя+предмета к классу |
| Расписание | `/api/schedule/` | Уроки с указанием дня, номера, кабинета |
| Оценки | `/api/grades/` | Четвертные оценки учеников |

Каждый ресурс поддерживает стандартные методы `GET/POST/PUT/PATCH/DELETE`, фильтры (`?school_class=1` и т.д.), поиск по имени и сортировку.

### Пример: добавление ученика

```http
POST /api/students/
{
  "first_name": "Иван",
  "last_name": "Петров",
  "gender": "male",
  "school_class": 1,
  "date_of_birth": "2011-05-12"
}
```

## Аналитика

- `GET /api/analytics/schedule/lookup/?class_id=1&weekday=1&lesson_number=3` — какой предмет и учитель стоят у класса N в заданный день/урок.
- `GET /api/analytics/subjects/teacher-count/` — сколько преподавателей ведёт каждую дисциплину.
- `GET /api/analytics/classes/{id}/subject-peers/?subject_code=INF` — список учителей, преподающих те же предметы, что и учитель информатики в классе.
- `GET /api/analytics/classes/gender-distribution/` — распределение мальчиков и девочек по классам.
- `GET /api/analytics/classrooms/categories/` — количество кабинетов базовых/профильных дисциплин.

## Оценки и отчёты

- `GET /api/reports/classes/{id}/?quarter=1` — JSON-отчёт по успеваемости класса: средние баллы по предметам, куратора, общее число учеников, средний балл по классу.
- `GET /api/reports/classes/{id}/download/?quarter=1` — тот же отчёт в PDF-формате (подходит для выдачи завучу).

Структура JSON-ответа:

```json
{
  "class_id": 1,
  "class_title": "10А",
  "quarter": 1,
  "students_total": 25,
  "homeroom_teacher": {"id": 3, "full_name": "Сидорова Н.В."},
  "subjects": [
    {
      "subject_id": 2,
      "subject_name": "Математика",
      "average_grade": 4.3,
      "grades": [
        {"student_id": 5, "student_name": "Петров И.", "value": 5, "quarter": 1}
      ]
    }
  ],
  "class_average": 4.1
}
```

## Документация схемы

- Swagger UI: `http://127.0.0.1:8000/api/schema/swagger-ui/`
- Redoc: `http://127.0.0.1:8000/api/schema/redoc/`

Схема генерируется автоматически пакетом **drf-spectacular**.

