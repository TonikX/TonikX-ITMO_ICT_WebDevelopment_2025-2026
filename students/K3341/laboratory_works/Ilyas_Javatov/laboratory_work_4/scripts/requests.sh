#!/bin/bash

docker compose exec web python manage.py migrate

docker compose exec web python manage.py seed_data


curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"javatov_ilyas","password":"JAVATOV_2005","re_password":"JAVATOV_2005","email":"a@a.ru"}'

curl -X POST http://localhost:8000/api/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"javatov_ilyas","password":"JAVATOV_2005"}'

TOKEN=...

curl http://localhost:8000/api/classrooms/ \
  -H "Authorization: Token $TOKEN"

curl "http://localhost:8000/api/reports/teachers_per_subject/" \
  -H "Authorization: Token $TOKEN"

curl "http://localhost:8000/api/reports/class_performance_report/?class_id=1&quarter=1&school_year=2023-2024" \
  -H "Authorization: Token $TOKEN"

CLASS_ID=1
DAY=1
LESSON=1

# Какой предмет будет в заданном классе, в заданный день недели на заданном уроке?
curl "http://127.0.0.1:8000/api/reports/subject_for_class/?class_id=${CLASS_ID}&day=${DAY}&lesson=${LESSON}" \
  -H "Authorization: Token ${TOKEN}"

# Сколько учителей преподает каждую дисциплину
curl "http://127.0.0.1:8000/api/reports/teachers_per_subject/" \
  -H "Authorization: Token ${TOKEN}"

# Учителя, ведущие те же предметы, что и учитель информатики в классе
curl "http://127.0.0.1:8000/api/reports/same_subject_teachers/?class_id=${CLASS_ID}" \
  -H "Authorization: Token ${TOKEN}"

# Сколько мальчиков и девочек в каждом классе
curl "http://127.0.0.1:8000/api/reports/gender_count_per_class/" \
  -H "Authorization: Token ${TOKEN}"

# Сколько кабинетов для базовых и профильных дисциплин
curl "http://127.0.0.1:8000/api/reports/classroom_stats/" \
  -H "Authorization: Token ${TOKEN}"
