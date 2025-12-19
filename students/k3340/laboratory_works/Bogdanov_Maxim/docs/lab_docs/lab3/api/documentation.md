# API Документация

## Базовая информация

- **Base URL**: `http://localhost:8080/api/v1`
- **Формат данных**: JSON
- **Аутентификация**: JWT Bearer tokens
- **Swagger UI**: `http://localhost:8080/swagger/`

## Аутентификация

### Регистрация

```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "admin",
  "email": "admin@school.com",
  "password": "admin123",
  "role": "admin"
}
```

### Вход

```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

Ответ содержит `access_token` и `refresh_token`.

### Использование токена

Все защищенные endpoints требуют заголовок:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Обновление токена

```bash
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "YOUR_REFRESH_TOKEN"
}
```

## Основные endpoints

### Учителя

- `GET /api/v1/teachers` - Список учителей
- `GET /api/v1/teachers/{id}` - Получить учителя
- `POST /api/v1/teachers` - Создать учителя (admin)
- `PUT /api/v1/teachers/{id}` - Обновить учителя (admin)
- `DELETE /api/v1/teachers/{id}` - Удалить учителя (admin)

### Ученики

- `GET /api/v1/students` - Список учеников
- `GET /api/v1/students/{id}` - Получить ученика
- `GET /api/v1/students/class/{classId}` - Список учеников класса
- `POST /api/v1/students` - Создать ученика (admin)
- `PUT /api/v1/students/{id}` - Обновить ученика (admin)
- `DELETE /api/v1/students/{id}` - Удалить ученика (admin)

### Классы

- `GET /api/v1/classes` - Список классов
- `GET /api/v1/classes/{id}` - Получить класс
- `POST /api/v1/classes` - Создать класс (admin)
- `PUT /api/v1/classes/{id}` - Обновить класс (admin)
- `DELETE /api/v1/classes/{id}` - Удалить класс (admin)

### Расписание

- `GET /api/v1/schedules` - Список расписаний
- `GET /api/v1/schedules/class/{classId}` - Расписание класса
- `POST /api/v1/schedules` - Создать урок (admin)
- `PUT /api/v1/schedules/{id}` - Обновить урок (admin)
- `DELETE /api/v1/schedules/{id}` - Удалить урок (admin)

### Оценки

- `GET /api/v1/grades` - Список оценок
- `GET /api/v1/grades/class/{classId}` - Оценки класса
- `POST /api/v1/grades` - Создать оценку (admin, teacher)
- `PUT /api/v1/grades/{id}` - Обновить оценку (admin, teacher)
- `DELETE /api/v1/grades/{id}` - Удалить оценку (admin, teacher)

### Справочные данные

- `GET /api/v1/reference/subjects` - Список предметов
- `GET /api/v1/reference/classrooms` - Список кабинетов
- `GET /api/v1/reference/academic-years` - Список учебных годов
- `GET /api/v1/reference/grading-periods` - Список периодов оценивания
- `GET /api/v1/reference/weekdays` - Список дней недели

### Статистика

- `GET /api/v1/info/teachers-count-by-subject` - Количество учителей по предметам
- `GET /api/v1/info/students-count-by-gender` - Количество учеников по полу
- `GET /api/v1/info/classrooms-count-by-type` - Количество кабинетов по типам

### Отчеты

- `GET /api/v1/reports/class-performance?classId={id}` - Отчет об успеваемости класса

## Роли и права доступа

- **admin** - полный доступ ко всем операциям
- **teacher** - может создавать и редактировать оценки
- **head_teacher** - расширенные права для учителей

