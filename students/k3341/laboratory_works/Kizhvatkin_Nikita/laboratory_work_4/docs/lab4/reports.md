# Запросы и отчёты

Страница собирает кастомные действия (DRF `@action`) и выводит результат.

## Реализовано
- Самый частый тип самолёта на маршруте: `GET /flights/popular_aircraft_on_route/?departure=...&arrival=...` (запрос 1 из ЛР №3)
- Маршруты с низкой загрузкой: `GET /flights/low_load_routes/?threshold=...` (запрос 2 из ЛР №3)
- Самолёты в ремонте: `GET /aircrafts/in_repair_count/` (запрос 4 из ЛР №3)
- Количество сотрудников компании: `GET /employees/company_employees_count/?company_id=...` (запрос 5 из ЛР №3)
- Отчёт по бортам компании: `GET /aircrafts/company_aircrafts_report/?company_id=...` (финальный запрос из ЛР №3)
