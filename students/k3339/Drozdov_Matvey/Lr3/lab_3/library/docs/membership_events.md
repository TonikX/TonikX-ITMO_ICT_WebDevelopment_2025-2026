# Членство

GET `/api/membership-events/`

POST `/api/membership-events/`

POST тело:
```json
{ "reader": 1, "event_type": "enroll", "event_date": "2025-12-01", "comment": "Первичная запись" }
```