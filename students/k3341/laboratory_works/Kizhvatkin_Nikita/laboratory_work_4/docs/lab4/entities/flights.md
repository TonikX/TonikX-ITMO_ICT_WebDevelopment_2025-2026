# Рейсы

## Возможности
- Таблица рейсов + переход в карточку рейса
- В карточке рейса:
  - список членов экипажа (`crew_members`)
  - транзитные остановки (`transit_stops`)
  - запрос свободных мест (`available_seats`)

## Поля формы
- `flight_number`
- `distance`
- `departure_airport`, `arrival_airport`
- `departure_datetime`, `arrival_datetime` (ISO-строка)
- `aircraft`
- `tickets_sold`
- `crew` (опционально)

## Бэкенд
- CRUD: `/flights/`
- Свободные места: `/flights/{id}/available_seats/`
- Низкая загрузка: `/flights/low_load_routes/?threshold=...`
- Популярная марка: `/flights/popular_aircraft_on_route/?departure=...&arrival=...`
