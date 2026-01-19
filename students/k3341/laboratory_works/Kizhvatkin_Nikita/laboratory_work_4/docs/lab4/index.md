# Airline Admin UI

Клиентская часть на **Vue 3 + Vuetify**, которая работает с сервером на **Django REST Framework**.

## Реализовано
- Авторизация через Djoser + страница профиля (через эндпоинт `current-user`)
- CRUD-интерфейсы для моделей:
  - Company, Aircraft, Airport, Employee, Crew, CrewMember, Flight, TransitStop
- Отдельная страница «Запросы/отчёты» для кастомных действий:
  - `flights/popular_aircraft_on_route/?departure=...&arrival=...` (запрос 1 из ЛР №3)
  - `flights/low_load_routes/?threshold=...` (запрос 2 из ЛР №3)
  - `flights/{id}/available_seats/` (запрос 3 из ЛР №3)
  - `aircrafts/in_repair_count/` (запрос 4 из ЛР №3)
  - `employees/company_employees_count/?company_id=...` (запрос 5 из ЛР №3)
  - `aircrafts/company_aircrafts_report/?company_id=...` (финальный запрос из ЛР №3)

## Запуск
```bash
npm i
npm run build
npm run preview
```
