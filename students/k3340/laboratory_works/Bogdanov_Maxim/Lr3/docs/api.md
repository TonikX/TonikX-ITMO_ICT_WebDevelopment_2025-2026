# API документация

## Базовая информация

- **Base URL**: `http://localhost:8080/api/v1`
- **Формат**: JSON
- **Аутентификация**: JWT Bearer tokens
- **Swagger UI**: `http://localhost:8080/swagger/`

## Аутентификация

### Получение токена

```bash
# Регистрация
POST /api/v1/auth/register
{
  "username": "admin",
  "email": "admin@school.com",
  "password": "admin123",
  "role": "admin"
}

# Вход
POST /api/v1/auth/login
{
  "username": "admin",
  "password": "admin123"
}
```

### Использование токена

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Обновление токена

```bash
POST /api/v1/auth/refresh
{
  "refresh_token": "YOUR_REFRESH_TOKEN"
}
```

## Основные endpoints

### Учителя

```bash
POST   /api/v1/teachers           # Создать (admin)
GET    /api/v1/teachers           # Список
GET    /api/v1/teachers/:id       # Получить
PUT    /api/v1/teachers/:id       # Обновить (admin)
DELETE /api/v1/teachers/:id       # Удалить (admin)
```

### Ученики

```bash
POST   /api/v1/students           # Создать (admin)
GET    /api/v1/students           # Список
GET    /api/v1/students/:id       # Получить
PUT    /api/v1/students/:id       # Обновить (admin)
DELETE /api/v1/students/:id       # Удалить (admin)
GET    /api/v1/students/by-class/:classId  # По классу
```

### Классы

```bash
POST   /api/v1/classes            # Создать (admin)
GET    /api/v1/classes            # Список
GET    /api/v1/classes/:id        # Получить
PUT    /api/v1/classes/:id        # Обновить (admin)
DELETE /api/v1/classes/:id        # Удалить (admin)
```

### Расписание

```bash
POST   /api/v1/schedules          # Создать (admin)
GET    /api/v1/schedules          # Список
GET    /api/v1/schedules/by-class/:classId  # По классу
```

### Оценки

```bash
POST   /api/v1/grades             # Создать (admin, teacher)
GET    /api/v1/grades             # Список
GET    /api/v1/grades/by-student/:studentId  # По ученику
GET    /api/v1/grades/by-class/:classId      # По классу
```

### Отчеты

```bash
GET    /api/v1/reports/class-performance/:classId  # Успеваемость класса
GET    /api/v1/info/teachers-count-by-subject      # Статистика учителей
GET    /api/v1/info/students-count-by-gender       # Статистика учеников
```

## Примеры

### Полный сценарий

```bash
# 1. Регистрация
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","email":"admin@school.com","password":"admin123","role":"admin"}'

# 2. Создание класса
curl -X POST http://localhost:8080/api/v1/classes \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"class_number":10,"class_letter":"А","academic_year":"2023-2024"}'

# 3. Создание учителя
curl -X POST http://localhost:8080/api/v1/teachers \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Иван","last_name":"Петров","subject_name":"Математика"}'

# 4. Создание ученика
curl -X POST http://localhost:8080/api/v1/students \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Алексей","last_name":"Иванов","class_id":1,"gender":"male"}'
```

## Роли и права доступа

### admin
- Полный доступ ко всем операциям
- CREATE/UPDATE/DELETE для teachers, students, classes, schedules
- CREATE/UPDATE/DELETE для grades
- Все GET запросы

### teacher
- Все GET запросы (чтение)
- CREATE/UPDATE/DELETE для grades (управление оценками)

### Любой аутентифицированный пользователь
- Все GET запросы (просмотр данных)
- Информационные endpoints (info, reports)

## HTTP статусы

- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Интерактивная документация

Используйте Swagger UI для тестирования API: `http://localhost:8080/swagger/`

