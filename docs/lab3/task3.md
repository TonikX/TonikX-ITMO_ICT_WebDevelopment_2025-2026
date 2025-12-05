# Часть 3: Система для завуча школы

## Описание системы

Программная система для завуча школы, обеспечивающая:

- Хранение сведений об учителях (ФИО, классное руководство, преподаваемые предметы, закрепленный кабинет)
- Хранение сведений об учениках (ФИО, класс, пол, оценки)
- Управление расписанием занятий
- Управление четвертными оценками
- Формирование отчетов об успеваемости

---

## Запуск проекта

### 1. Активация виртуального окружения

=== "Linux / macOS"

    ```bash
    cd teachers_system
    source project-env/bin/activate
    ```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Применение миграций

```bash
python manage.py migrate
```

### 4. Заполнение базы данных тестовыми данными

```bash
python populate_db.py
```

### 5. Запуск сервера

```bash
python manage.py runserver
```

### 6. Доступ к системе

| Ресурс | URL |
|--------|-----|
| Admin панель | http://localhost:8000/admin/ |
| API | http://localhost:8000/api/ |

Учётные данные

- **Логин:** `admin`  
- **Пароль:** `admin123`

---

## API Endpoints

### Авторизация (Djoser)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/auth/users/` | Регистрация нового пользователя |
| POST | `/api/auth/token/login/` | Получение токена авторизации |
| POST | `/api/auth/token/logout/` | Выход (удаление токена) |
| GET | `/api/auth/users/me/` | Информация о текущем пользователе |

---

### Предметы (Subjects)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/subjects/` | Список всех предметов |
| POST | `/api/subjects/` | Создать предмет |
| GET | `/api/subjects/{id}/` | Получить предмет |
| PUT | `/api/subjects/{id}/` | Обновить предмет |
| DELETE | `/api/subjects/{id}/` | Удалить предмет |
| **GET** | **`/api/subjects/teacher_count/`** | **Сколько учителей преподает каждую дисциплину** |

---

### Кабинеты (Classrooms)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/classrooms/` | Список всех кабинетов |
| POST | `/api/classrooms/` | Создать кабинет |
| GET | `/api/classrooms/{id}/` | Получить кабинет |
| PUT | `/api/classrooms/{id}/` | Обновить кабинет |
| DELETE | `/api/classrooms/{id}/` | Удалить кабинет |
| **GET** | **`/api/classrooms/type_count/`** | **Сколько кабинетов для базовых/профильных дисциплин** |

---

### Учителя (Teachers)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/teachers/` | Список всех учителей |
| POST | `/api/teachers/` | Добавить учителя |
| GET | `/api/teachers/{id}/` | Получить учителя (детально с предметами) |
| PUT | `/api/teachers/{id}/` | Обновить данные учителя |
| DELETE | `/api/teachers/{id}/` | Удалить учителя |
| **GET** | **`/api/teachers/same_subjects_as_informatics_teacher/?class_id={id}`** | **Список учителей с теми же предметами, что у учителя информатики** |

---

### Классы (Classes)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/classes/` | Список всех классов |
| POST | `/api/classes/` | Создать класс |
| GET | `/api/classes/{id}/` | Получить класс (детально) |
| PUT | `/api/classes/{id}/` | Обновить класс |
| DELETE | `/api/classes/{id}/` | Удалить класс |
| **GET** | **`/api/classes/gender_stats/`** | **Сколько мальчиков и девочек в каждом классе** |
| **GET** | **`/api/classes/{id}/performance_report/?quarter_id={id}`** | **Отчет об успеваемости класса** |

---

### Ученики (Students)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/students/` | Список всех учеников |
| GET | `/api/students/?school_class={id}` | Фильтр по классу |
| POST | `/api/students/` | Добавить ученика |
| GET | `/api/students/{id}/` | Получить ученика (с оценками) |
| PUT | `/api/students/{id}/` | Обновить данные ученика |
| DELETE | `/api/students/{id}/` | Удалить ученика |

---

### Четверти (Quarters)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/quarters/` | Список всех четвертей |
| POST | `/api/quarters/` | Создать четверть |
| GET | `/api/quarters/{id}/` | Получить четверть |
| PUT | `/api/quarters/{id}/` | Обновить четверть |
| DELETE | `/api/quarters/{id}/` | Удалить четверть |
| **GET** | **`/api/quarters/current/`** | **Получить текущую четверть** |

---

### Назначения преподавания (Teaching Assignments)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/teaching-assignments/` | Список всех назначений |
| GET | `/api/teaching-assignments/?teacher={id}` | Фильтр по учителю |
| GET | `/api/teaching-assignments/?school_class={id}` | Фильтр по классу |
| GET | `/api/teaching-assignments/?quarter={id}` | Фильтр по четверти |
| POST | `/api/teaching-assignments/` | Создать назначение |
| GET | `/api/teaching-assignments/{id}/` | Получить назначение (детально) |
| PUT | `/api/teaching-assignments/{id}/` | Обновить назначение |
| DELETE | `/api/teaching-assignments/{id}/` | Удалить назначение |

---

### Расписание (Schedule)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/schedule/` | Список всего расписания |
| GET | `/api/schedule/?school_class={id}` | Фильтр по классу |
| GET | `/api/schedule/?day_of_week={1-6}` | Фильтр по дню недели |
| GET | `/api/schedule/?lesson_number={1-8}` | Фильтр по номеру урока |
| POST | `/api/schedule/` | Добавить запись в расписание |
| GET | `/api/schedule/{id}/` | Получить запись (детально) |
| PUT | `/api/schedule/{id}/` | Обновить запись |
| DELETE | `/api/schedule/{id}/` | Удалить запись |
| **GET** | **`/api/schedule/by_class_day_lesson/?school_class={id}&day_of_week={1-6}&lesson_number={1-8}`** | **Какой предмет будет в заданном классе, день, урок** |

---

### Оценки (Grades)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/grades/` | Список всех оценок |
| GET | `/api/grades/?student={id}` | Фильтр по ученику |
| GET | `/api/grades/?subject={id}` | Фильтр по предмету |
| GET | `/api/grades/?quarter={id}` | Фильтр по четверти |
| GET | `/api/grades/?school_class={id}` | Фильтр по классу |
| POST | `/api/grades/` | Добавить оценку |
| GET | `/api/grades/{id}/` | Получить оценку |
| PUT | `/api/grades/{id}/` | Изменить оценку |
| DELETE | `/api/grades/{id}/` | Удалить оценку |

---

## Аналитические запросы

### 1. Какой предмет будет в заданном классе, в заданный день недели на заданном уроке?

```bash
GET /api/schedule/by_class_day_lesson/?school_class=1&day_of_week=1&lesson_number=1
```

??? example "Пример ответа"

    ```json
    {
        "id": 1,
        "teaching_assignment": {
            "id": 1,
            "teacher": {...},
            "subject": {"id": 1, "name": "Математика", ...},
            "school_class": {"id": 1, "name": "5А", ...},
            "quarter": {...}
        },
        "day_of_week": 1,
        "day_of_week_display": "Понедельник",
        "lesson_number": 1,
        "lesson_number_display": "1 урок",
        "classroom": {"id": 10, "number": "304", ...}
    }
    ```

---

### 2. Сколько учителей преподает каждую из дисциплин в школе?

```bash
GET /api/subjects/teacher_count/
```

??? example "Пример ответа"

    ```json
    [
        {"subject": "Математика", "teachers_count": 2},
        {"subject": "Русский язык", "teachers_count": 2},
        {"subject": "Информатика", "teachers_count": 2}
    ]
    ```

---

### 3. Список учителей, преподающих те же предметы, что и учитель информатики

```bash
GET /api/teachers/same_subjects_as_informatics_teacher/?class_id=1
```

??? example "Пример ответа"

    ```json
    {
        "informatics_teacher": {
            "id": 1,
            "full_name": "Иванов Иван Иванович",
            "subjects": [...]
        },
        "teachers_with_same_subjects": [...]
    }
    ```

---

### 4. Сколько мальчиков и девочек в каждом классе?

```bash
GET /api/classes/gender_stats/
```

??? example "Пример ответа"

    ```json
    [
        {"school_class": "5А", "boys_count": 12, "girls_count": 13, "total": 25},
        {"school_class": "5Б", "boys_count": 10, "girls_count": 14, "total": 24}
    ]
    ```

---

### 5. Сколько кабинетов в школе для базовых и профильных дисциплин?

```bash
GET /api/classrooms/type_count/
```

??? example "Пример ответа"

    ```json
    [
        {"classroom_type": "Для базовых дисциплин", "count": 9},
        {"classroom_type": "Для профильных дисциплин", "count": 4}
    ]
    ```

---

### 6. Отчет об успеваемости класса

```bash
GET /api/classes/1/performance_report/?quarter_id=2
```

??? example "Пример ответа"

    ```json
    {
        "school_class": "5А",
        "class_teacher": "Иванов Иван Иванович",
        "students_count": 25,
        "subjects": ["Математика", "Русский язык", "Английский язык"],
        "average_by_subject": {
            "Математика": 4.12,
            "Русский язык": 3.96,
            "Английский язык": 4.24
        },
        "class_average": 4.05,
        "quarter": "II четверть (2024-2025)"
    }
    ```

---

## Связи моделей

### Один-ко-многим (1:N)

- **Student → SchoolClass**: Ученики в классе
- **Grade → Student**: Оценки ученика
- **TeachingAssignment → Teacher**: Назначения учителя
- **Schedule → TeachingAssignment**: Записи расписания

### Многие-ко-многим (M:N)

- **Teacher ↔ Subject** (через TeacherSubject): Учителя и их предметы

### Один-к-одному (1:1)

- **Teacher → Classroom**: Закрепленный кабинет (опционально)
- **SchoolClass → Teacher**: Классный руководитель
