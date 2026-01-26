# API эндпоинты

Базовый путь: `/api/`

## Ключевые блоки кода

### Регистрация маршрутов (router + Djoser)

```python
router = DefaultRouter()
router.register(r"teachers", views.TeacherViewSet)
router.register(r"students", views.StudentViewSet)
router.register(r"schoolclasses", views.SchoolClassViewSet)
router.register(r"subjects", views.SubjectViewSet)
router.register(r"classrooms", views.ClassroomViewSet)
router.register(r"grades", views.GradeViewSet)
router.register(r"schedule", views.ScheduleViewSet)
router.register(r"assignments", views.TeachingAssignmentViewSet)
router.register(r"reports", views.ReportViewSet, basename="reports")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
```

### Пример бизнес-отчета

```python
@action(detail=False, methods=["get"])
def class_performance_report(self, request):
    class_id = request.query_params.get("class_id")
    quarter = request.query_params.get("quarter")
    school_year = request.query_params.get("school_year")
    if not class_id or not quarter or not school_year:
        return Response(
            {"error": "Необходимы параметры: class_id, quarter, school_year"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    school_class = get_object_or_404(SchoolClass, pk=class_id)
    students = school_class.students.all()
    subjects = Subject.objects.filter(
        teachingassignment__school_class=school_class
    ).distinct()
    # Далее формируется агрегированный отчет
```

### Валидация расписания (контроль назначения учителя)

```python
def validate(self, attrs):
    teacher = attrs.get("teacher", getattr(self.instance, "teacher", None))
    subject = attrs.get("subject", getattr(self.instance, "subject", None))
    school_class = attrs.get(
        "school_class", getattr(self.instance, "school_class", None)
    )
    if teacher and subject and school_class:
        has_assignment = TeachingAssignment.objects.filter(
            teacher=teacher,
            subject=subject,
            school_class=school_class,
        ).exists()
        if not has_assignment:
            raise serializers.ValidationError(
                "Нельзя поставить в расписание: учитель не назначен на предмет для этого класса."
            )
    return attrs
```

## CRUD-эндпоинты

Стандартные действия DRF:
- `GET /` — список
- `POST /` — создание
- `GET /{id}/` — детальная запись
- `PUT/PATCH /{id}/` — обновление
- `DELETE /{id}/` — удаление

Ресурсы:
- `/api/teachers/` — учителя
- `/api/students/` — ученики
- `/api/schoolclasses/` — классы
- `/api/subjects/` — предметы
- `/api/classrooms/` — кабинеты
- `/api/grades/` — оценки
- `/api/schedule/` — расписание
- `/api/assignments/` — назначения учителей

## Отчеты и аналитика

### Предмет в расписании
`GET /api/reports/subject_for_class/?class_id=1&day=1&lesson=2`

### Сколько учителей на каждый предмет
`GET /api/reports/teachers_per_subject/`

### Учителя, ведущие те же предметы, что и учитель информатики
`GET /api/reports/same_subject_teachers/?class_id=1`

### Количество мальчиков и девочек в каждом классе
`GET /api/reports/gender_count_per_class/`

### Статистика кабинетов
`GET /api/reports/classroom_stats/`

### Отчет об успеваемости класса
`GET /api/reports/class_performance_report/?class_id=1&quarter=1&school_year=2023-2024`

## Аутентификация и пользователи (Djoser)

Базовый путь: `/api/auth/`

Ключевые эндпоинты:
- `POST /api/auth/users/` — регистрация
- `POST /api/auth/token/login/` — получение токена
- `POST /api/auth/token/logout/` — отзыв токена
- `GET /api/auth/users/me/` — текущий пользователь

Токен в заголовке:
```
Authorization: Token <your_token>
```

## Полный список используемых endpoint-ов

### Учителя
- `GET /api/teachers/`
- `POST /api/teachers/`
- `GET /api/teachers/{id}/`
- `PUT /api/teachers/{id}/`
- `PATCH /api/teachers/{id}/`
- `DELETE /api/teachers/{id}/`

### Ученики
- `GET /api/students/`
- `POST /api/students/`
- `GET /api/students/{id}/`
- `PUT /api/students/{id}/`
- `PATCH /api/students/{id}/`
- `DELETE /api/students/{id}/`

### Классы
- `GET /api/schoolclasses/`
- `POST /api/schoolclasses/`
- `GET /api/schoolclasses/{id}/`
- `PUT /api/schoolclasses/{id}/`
- `PATCH /api/schoolclasses/{id}/`
- `DELETE /api/schoolclasses/{id}/`

### Предметы
- `GET /api/subjects/`
- `POST /api/subjects/`
- `GET /api/subjects/{id}/`
- `PUT /api/subjects/{id}/`
- `PATCH /api/subjects/{id}/`
- `DELETE /api/subjects/{id}/`

### Кабинеты
- `GET /api/classrooms/`
- `POST /api/classrooms/`
- `GET /api/classrooms/{id}/`
- `PUT /api/classrooms/{id}/`
- `PATCH /api/classrooms/{id}/`
- `DELETE /api/classrooms/{id}/`

### Оценки
- `GET /api/grades/`
- `POST /api/grades/`
- `GET /api/grades/{id}/`
- `PUT /api/grades/{id}/`
- `PATCH /api/grades/{id}/`
- `DELETE /api/grades/{id}/`

### Расписание
- `GET /api/schedule/`
- `POST /api/schedule/`
- `GET /api/schedule/{id}/`
- `PUT /api/schedule/{id}/`
- `PATCH /api/schedule/{id}/`
- `DELETE /api/schedule/{id}/`

### Назначения учителей
- `GET /api/assignments/`
- `POST /api/assignments/`
- `GET /api/assignments/{id}/`
- `PUT /api/assignments/{id}/`
- `PATCH /api/assignments/{id}/`
- `DELETE /api/assignments/{id}/`

### Отчеты
- `GET /api/reports/subject_for_class/?class_id=1&day=1&lesson=1`
- `GET /api/reports/teachers_per_subject/`
- `GET /api/reports/same_subject_teachers/?class_id=1`
- `GET /api/reports/gender_count_per_class/`
- `GET /api/reports/classroom_stats/`
- `GET /api/reports/class_performance_report/?class_id=1&quarter=1&school_year=2025-2026`

### Auth (Djoser)
- `POST /api/auth/users/`
- `POST /api/auth/token/login/`
- `POST /api/auth/token/logout/`
- `GET /api/auth/users/me/`

### Swagger
- `GET /swagger/`
- `GET /redoc/`
