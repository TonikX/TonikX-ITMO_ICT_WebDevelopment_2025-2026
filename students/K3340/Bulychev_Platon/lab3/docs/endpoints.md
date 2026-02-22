# API Endpoints

## CRUD ресурсы

Все CRUD-ресурсы поддерживают `GET` (list/detail), `POST`, `PUT`, `PATCH`, `DELETE`.

### Bus Types

```
/api/bus-types/
/api/bus-types/{id}/
```

Поля: `name`, `capacity`

### Buses

```
/api/buses/
/api/buses/{id}/
```

Поля: `reg_number`, `bus_type`

Фильтр: `?bus_type=1`

### Routes

```
/api/routes/
/api/routes/{id}/
```

Поля: `number`, `start_point`, `end_point`, `start_time`, `end_time`, `interval_minutes`, `duration_minutes`

### Drivers

```
/api/drivers/
/api/drivers/{id}/
```

Поля: `first_name`, `last_name`, `passport`, `driver_class`, `experience_years`, `salary`, `bus`, `route`

Фильтры: `?driver_class=1`, `?route=1`, `?bus=1`

### Schedules

```
/api/schedules/
/api/schedules/{id}/
```

Поля: `driver`, `bus`, `route`, `date`, `shift_start`, `shift_end`

Фильтры: `?driver=1`, `?route=1`, `?date=2025-01-15`

### Absences

```
/api/absences/
/api/absences/{id}/
```

Поля: `bus`, `date`, `reason`, `note`

Фильтры: `?date=2025-01-15`, `?reason=breakdown`

---

## Аналитические эндпоинты

### Водители на маршруте

```
GET /api/drivers-on-route/{route_id}/
```

Список водителей на определенном маршруте с графиком работы.

### Время начала/конца движения

```
GET /api/route-times/
```

Когда начинается и заканчивается движение автобусов на каждом маршруте.

### Общая протяженность маршрутов

```
GET /api/total-route-length/
```

Response:

```json
{
    "total_duration_minutes": 450
}
```

### Автобусы, не вышедшие на линию

```
GET /api/absent-buses/?date=2025-01-15
```

Какие автобусы не вышли на линию и по какой причине.

### Водители по классам

```
GET /api/drivers-by-class/
```

Response:

```json
[
    {"driver_class": "1", "count": 5},
    {"driver_class": "2", "count": 8},
    {"driver_class": "3", "count": 3}
]
```

### Отчет по автопарку

```
GET /api/fleet-report/
```

Отчет, сгруппированный по типам автобусов, с маршрутами, автобусами, водителями и суммарной статистикой.
