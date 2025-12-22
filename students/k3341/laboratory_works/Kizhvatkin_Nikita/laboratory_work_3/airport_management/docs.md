Основные CRUD операции:
/api/companies/                    - компании
/api/aircrafts/                    - самолеты
/api/airports/                     - аэропорты
/api/employees/                    - сотрудники
/api/crews/                        - экипажи
/api/crew-members/                 - члены экипажа
/api/flights/                      - рейсы
/api/transit-stops/                - транзитные остановки

Специальные запросы (кастомные actions):
/api/aircrafts/in_repair_count/    - самолеты в ремонте (запрос 4)
/api/aircrafts/company_aircrafts_report/?company_id=1 - отчет
/api/employees/company_employees_count/?company_id=1  - сотрудники (запрос 5)
/api/flights/popular_aircraft_on_route/?departure=SVO&arrival=JFK (запрос 1)
/api/flights/low_load_routes/?threshold=50            (запрос 2)
/api/flights/{id}/available_seats/                    (запрос 3)

Аутентификация:
/api/auth/users/                   - регистрация
/api/auth/token/login/             - получение токена
/api/auth/token/logout/            - удаление токена
/api/auth/users/me/                - информация о пользователе
/api/current-user/                 - альтернативная информация

Админка:
/admin/                            - Django Admin