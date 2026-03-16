# Документация для API-эндпоинтов

## Базовые API-эндпоинты

### `GET /bus-depot/bus-types/`

Тело запроса не требуется.

Формат ответа:

```json
[
    {
        "id": <id>,
        "name": <название>,
        "capacity": <вместимость>
    },
    <...>
]
```

### `POST /bus-depot/bus-types/`

Формат тела запроса:

```json
{
    "name": <название>,
    "capacity": <вместимость>
}
```

### `GET /bus-depot/bus-types/<id>/`

Тело запроса не требуется.

Формат ответа:

```json
{
    "id": <id>,
    "name": <название>,
    "capacity": <вместимость>
}
```

### `PUT /bus-depot/bus-types/<id>/`

Формат тела запроса:

```json
{
    "name": <название>,
    "capacity": <вместимость>
}
```

### `PATCH /bus-depot/bus-types/<id>/`

Формат тела запроса:

```json
{
    "name": <название>,
    "capacity": <вместимость>
}
```

### `DELETE /bus-depot/bus-types/<id>/`

Тело запроса не требуется.

### `GET /bus-depot/buses/`

Тело запроса не требуется.

Формат ответа:

```json
[
    {
        "id": <id>,
        "license_plate": <номер>,
        "is_active": <действующий>,
        "purchase_date": <дата_приобретения>,
        "bus_type": <тип_автобуса>
    },
    <...>
]
```

### `POST /bus-depot/buses/`

Формат тела запроса:

```json
{
    "license_plate": <номер>,
    "is_active": <действующий>,
    "purchase_date": <дата_приобретения>,
    "bus_type": <тип_автобуса>
}
```

### `GET /bus-depot/buses/<id>/`

Тело запроса не требуется.

Формат ответа:

```json
{
    "id": <id>,
    "license_plate": <номер>,
    "is_active": <действующий>,
    "purchase_date": <дата_приобретения>,
    "bus_type": <тип_автобуса>
}
```

### `PUT /bus-depot/buses/<id>/`

Формат тела запроса:

```json
{
    "license_plate": <номер>,
    "is_active": <действующий>,
    "purchase_date": <дата_приобретения>,
    "bus_type": <тип_автобуса>
}
```

### `PATCH /bus-depot/buses/<id>/`

Формат тела запроса:

```json
{
    "license_plate": <номер>,
    "is_active": <действующий>,
    "purchase_date": <дата_приобретения>,
    "bus_type": <тип_автобуса>
}
```

### `DELETE /bus-depot/buses/<id>/`

Тело запроса не требуется.

### `GET /bus-depot/routes/`

Тело запроса не требуется.

Формат ответа:

```json
[
    {
        "id": <id>,
        "number": <номер>,
        "start_point": <начальный_пункт>,
        "end_point": <конечный_пункт>,
        "start_time": <время_начала>,
        "end_time": <время_окончания>,
        "interval": <интервал_движения_мин>,
        "duration": <протяжённость_мин>
    },
    <...>
]
```

### `POST /bus-depot/routes/`

Формат тела запроса:

```json
{
    "number": <номер>,
    "start_point": <начальный_пункт>,
    "end_point": <конечный_пункт>,
    "start_time": <время_начала>,
    "end_time": <время_окончания>,
    "interval": <интервал_движения_мин>,
    "duration": <протяжённость_мин>
}
```

### `GET /bus-depot/routes/<id>/`

Тело запроса не требуется.

Формат ответа:

```json
{
    "id": <id>,
    "number": <номер>,
    "start_point": <начальный_пункт>,
    "end_point": <конечный_пункт>,
    "start_time": <время_начала>,
    "end_time": <время_окончания>,
    "interval": <интервал_движения_мин>,
    "duration": <протяжённость_мин>
}
```

### `PUT /bus-depot/routes/<id>/`

Формат тела запроса:

```json
{
    "number": <номер>,
    "start_point": <начальный_пункт>,
    "end_point": <конечный_пункт>,
    "start_time": <время_начала>,
    "end_time": <время_окончания>,
    "interval": <интервал_движения_мин>,
    "duration": <протяжённость_мин>
}
```

### `PATCH /bus-depot/routes/<id>/`

Формат тела запроса:

```json
{
    "number": <номер>,
    "start_point": <начальный_пункт>,
    "end_point": <конечный_пункт>,
    "start_time": <время_начала>,
    "end_time": <время_окончания>,
    "interval": <интервал_движения_мин>,
    "duration": <протяжённость_мин>
}
```

### `DELETE /bus-depot/routes/<id>/`

Тело запроса не требуется.

### `GET /bus-depot/drivers/`

Тело запроса не требуется.

Формат ответа:

```json
[
    {
        "id": <id>,
        "full_name": <фио>,
        "passport": <номер_паспорта>,
        "birth_date": <дата_рождения>,
        "driver_class": <класс_водителя>,
        "experience": <опыт_лет>,
        "salary": <зарплата>,
        "main_bus": <основной_автобус>,
        "main_route": <основной_маршрут>
    },
    <...>
]
```

### `POST /bus-depot/drivers/`

Формат тела запроса:

```json
{
    "full_name": <фио>,
    "passport": <номер_паспорта>,
    "birth_date": <дата_рождения>,
    "driver_class": <класс_водителя>,
    "experience": <опыт_лет>,
    "salary": <зарплата>,
    "main_bus": <основной_автобус>,
    "main_route": <основной_маршрут>
}
```

### `GET /bus-depot/drivers/<id>/`

Тело запроса не требуется.

Формат ответа:

```json
{
    "id": <id>,
    "full_name": <фио>,
    "passport": <номер_паспорта>,
    "birth_date": <дата_рождения>,
    "driver_class": <класс_водителя>,
    "experience": <опыт_лет>,
    "salary": <зарплата>,
    "main_bus": <основной_автобус>,
    "main_route": <основной_маршрут>
}
```

### `PUT /bus-depot/drivers/<id>/`

Формат тела запроса:

```json
{
    "full_name": <фио>,
    "passport": <номер_паспорта>,
    "birth_date": <дата_рождения>,
    "driver_class": <класс_водителя>,
    "experience": <опыт_лет>,
    "salary": <зарплата>,
    "main_bus": <основной_автобус>,
    "main_route": <основной_маршрут>
}
```

### `PATCH /bus-depot/drivers/<id>/`

Формат тела запроса:

```json
{
    "full_name": <фио>,
    "passport": <номер_паспорта>,
    "birth_date": <дата_рождения>,
    "driver_class": <класс_водителя>,
    "experience": <опыт_лет>,
    "salary": <зарплата>,
    "main_bus": <основной_автобус>,
    "main_route": <основной_маршрут>
}
```

### `DELETE /bus-depot/drivers/<id>/`

Тело запроса не требуется.

### `GET /bus-depot/driver-assignments/`

Тело запроса не требуется.

Формат ответа:

```json
[
    {
        "id": <id>,
        "date": <дата>,
        "start_time": <время_начала_смены>,
        "end_time": <время_окончания_смены>,
        "driver": <водитель>,
        "bus": <автобус>,
        "route": <маршрут>
    },
    <...>
]
```

### `POST /bus-depot/driver-assignments/`

Формат тела запроса:

```json
{
    "date": <дата>,
    "start_time": <время_начала_смены>,
    "end_time": <время_окончания_смены>,
    "driver": <водитель>,
    "bus": <автобус>,
    "route": <маршрут>
}
```

### `GET /bus-depot/driver-assignments/<id>/`

Тело запроса не требуется.

Формат ответа:

```json
{
    "id": <id>,
    "date": <дата>,
    "start_time": <время_начала_смены>,
    "end_time": <время_окончания_смены>,
    "driver": <водитель>,
    "bus": <автобус>,
    "route": <маршрут>
}
```

### `PUT /bus-depot/driver-assignments/<id>/`

Формат тела запроса:

```json
{
    "date": <дата>,
    "start_time": <время_начала_смены>,
    "end_time": <время_окончания_смены>,
    "driver": <водитель>,
    "bus": <автобус>,
    "route": <маршрут>
}
```

### `PATCH /bus-depot/driver-assignments/<id>/`

Формат тела запроса:

```json
{
    "date": <дата>,
    "start_time": <время_начала_смены>,
    "end_time": <время_окончания_смены>,
    "driver": <водитель>,
    "bus": <автобус>,
    "route": <маршрут>
}
```

### `DELETE /bus-depot/driver-assignments/<id>/`

Тело запроса не требуется.

### `GET /bus-depot/bus-statuses/`

Тело запроса не требуется.

Формат ответа:

```json
[
    {
        "id": <id>,
        "date": <дата>,
        "status": <статус>,
        "reason": <причина>,
        "bus": <автобус>
    },
    <...>
]
```

### `POST /bus-depot/bus-statuses/`

Формат тела запроса:

```json
{
    "date": <дата>,
    "status": <статус>,
    "reason": <причина>,
    "bus": <автобус>
}
```

### `GET /bus-depot/bus-statuses/<id>/`

Тело запроса не требуется.

Формат ответа:

```json
{
    "id": <id>,
    "date": <дата>,
    "status": <статус>,
    "reason": <причина>,
    "bus": <автобус>
}
```

### `PUT /bus-depot/bus-statuses/<id>/`

Формат тела запроса:

```json
{
    "date": <дата>,
    "status": <статус>,
    "reason": <причина>,
    "bus": <автобус>
}
```

### `PATCH /bus-depot/bus-statuses/<id>/`

Формат тела запроса:

```json
{
    "date": <дата>,
    "status": <статус>,
    "reason": <причина>,
    "bus": <автобус>
}
```

### `DELETE /bus-depot/bus-statuses/<id>/`

Тело запроса не требуется.

## Специализированные API-эндпоинты

### `GET /bus-depot/routes/<id>/drivers/`

Формат ответа:

```json
{
    "route": {
        "id": <id>,
        "number": <number>,
        "start_point": <start_point>,
        "end_point": <end_point>,
        "start_time": <start_time>,
        "end_time": <end_time>,
        "interval": <interval>,
        "duration": <duration>
    },
    "drivers": [
        {
            "id": <id>,
            "assignments": [
                {
                    "id": <id>,
                    "date": <date>,
                    "start_time": <start_time>,
                    "end_time": <end_time>,
                    "driver": <driver>,
                    "bus": <bus>,
                    "route": <route>
                },
                <...>
            ],
            "full_name": <full_name>,
            "passport": <passport>,
            "birth_date": <birth_date>,
            "driver_class": <driver_class>,
            "experience": <experience>,
            "salary": <salary>,
            "main_bus": <main_bus>,
            "main_route": <main_route>
        },
        <...>
    ]
}
```

### `GET /bus-depot/routes/total-length/`

Формат ответа:

```json
{
    "total_length": <total_length>,
    "routes_count": <routes_count>,
    "average_length": <average_length>
}
```

### `GET /bus-depot/buses/not-active/?date=<дата>`

Формат ответа:

```json
[
    {
        "id": <id>,
        "bus": {
            "id": <id>,
            "license_plate": <license_plate>,
            "is_active": <is_active>,
            "purchase_date": <purchase_date>,
            "bus_type": <bus_type>
        },
        "date": <date>,
        "status": <status>,
        "reason": <reason>
    },
    <...>
]
```

### `GET /bus-depot/drivers/class-stats`

Формат ответа:

```json
[
    {
        "driver_class": <driver_class>,
        "driver_class_display": <driver_class_display>,
        "count": <count>
    },
    <...>
]
```

## API-эндпоинт с отчётом по автобусному парку

### `GET /bus-depot/report/`

Формат ответа:

```json
{
    "summary": {
        "total_routes": <всего_маршрутов>,
        "total_route_length_minutes": <общая_протяжённость_маршрутов_мин>,
        "total_bus_types": <число_типов_автобусов>,
        "bus_type_distribution": {
            <тип_автобуса>: <число_автобусов_данного_типа>,
            <остальные_типы_автобусов...>
        },
        "total_buses": <общее_число_автобусов>,
        "total_drivers": <общее_число_водителей>,
        "drivers_average_experience": <средний_опыт_водителя>,
        "drivers_class_distribution": {
            "1": <число_водителей_первого_класса>,
            "2": <число_водителей_второго_класса>,
            "3": <число_водителей_третьего_класса>
        }
    },
    "routes": [
        {
            "id": <id_маршрута>,
            "number": <номер_маршрута>,
            "start_point": <начало_маршрута>,
            "end_point": <конец_маршрута>,
            "start_time": <время_начала_работы_маршрута>,
            "end_time": <время_конца_работы_маршрута>,
            "interval": <интервал_между_автобусами_на_маршруте_мин>,
            "duration": <протяжённость_маршрута_мин>,
            "bus_types": [
                {
                    "id": <id_типа_автобуса>,
                    "name": <название_типа_автобуса>,
                    "capacity": <вместимость_типа_автобуса>,
                    "buses": [
                        {
                            "id": <id_автобуса>,
                            "license_plate": <номер_автобуса>,
                            "is_active": <действует_ли_автобус>,
                            "purchase_date": <дата_покупки_автобуса>,
                            "drivers": [
                                {
                                    "id": <id_водителя>,
                                    "full_name": <фио_водителя>,
                                    "passport": <номер_паспорта_водителя>,
                                    "birth_date": <дата_рождения_водителя>,
                                    "driver_class": <класс_водителя>,
                                    "experience": <стаж_водителя_лет>,
                                    "salary": <зарплата_водителя>
                                },
                                <остальные_водители_данного_автобуса...>
                            ]
                        },
                        <остальные_автобусы_данного_типа_на_данном_маршруте...>
                    ]
                },
                <остальные_типы_автобусов_на_данном_маршруте...>
            ]
        },
        <остальные_маршруты...>
    ]
}
```
