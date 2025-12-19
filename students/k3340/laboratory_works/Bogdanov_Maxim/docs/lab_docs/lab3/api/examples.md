# Примеры использования API

## Создание учителя

```bash
curl -X POST http://localhost:8080/api/v1/teachers \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Иван",
    "last_name": "Иванов",
    "middle_name": "Иванович",
    "classroom_id": 1
  }'
```

## Создание ученика

```bash
curl -X POST http://localhost:8080/api/v1/students \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Петр",
    "last_name": "Петров",
    "middle_name": "Петрович",
    "gender_id": 1,
    "class_id": 1
  }'
```

## Получение расписания класса

```bash
curl -X GET http://localhost:8080/api/v1/schedules/class/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Создание оценки

```bash
curl -X POST http://localhost:8080/api/v1/grades \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "subject_id": 1,
    "grading_period_id": 1,
    "grade": 5
  }'
```

## Получение отчета об успеваемости

```bash
curl -X GET "http://localhost:8080/api/v1/reports/class-performance?classId=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

