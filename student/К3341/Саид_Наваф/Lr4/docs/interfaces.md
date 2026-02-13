# Интерфейсы API (обновлённые)

Базовый префикс API: `/api/`

Аутентификация (Simple JWT)
- POST /api/token/  
  Тело: `{ "username": "<user>", "password": "<pass>" }`  
  Ответ: `{ "access": "...", "refresh": "..." }`
- POST /api/token/refresh/  
  Тело: `{ "refresh": "<token>" }`  
  Ответ: `{ "access": "..." }`

Основные ресурсы
- Owners
  - GET /api/owners/ — список владельцев (pagination если включён)
  - POST /api/owners/ — создать владельца
  - GET /api/owners/{id}/ — детальная информация (включает driver_license, contacts, ownerships)
  - PUT /api/owners/{id}/ — обновить
  - DELETE /api/owners/{id}/ — удалить

- OwnerContacts
  - GET /api/contacts/
  - POST /api/contacts/

- DriverLicense
  - GET /api/driverlicenses/ (если зарегистровано)  
  - GET /api/owners/{id}/ — driver_license вложён в OwnerDetail

- VehicleModel
  - GET /api/vehicle-models/
  - POST /api/vehicle-models/
  - GET /api/vehicle-models/{id}/

- Cars
  - GET /api/cars/
  - POST /api/cars/
  - GET /api/cars/{id}/ — детально (возможно без связанных списков)
  - Примеры фильтрации (реализуйте на сервере): `?vehicle_model=`, `?vin=`

- Ownerships
  - GET /api/ownerships/
  - POST /api/ownerships/ — тело: `{ "owner": id, "car": id, "date_start": "YYYY-MM-DD", "date_end": "YYYY-MM-DD" }`
  - При создании Ownership сервер выполняет валидацию перекрытия периодов (если периоды пересекаются — вернёт 400 с сообщением).

- InsurancePolicy
  - GET /api/insurance/
  - POST /api/insurance/ — поля: car, policy_number (unique), insurer, date_start, date_end, sum_insured

- ServiceRecord
  - GET /api/services/
  - POST /api/services/ — поля: car, date, mileage, description

- Registration
  - GET /api/registrations/
  - POST /api/registrations/ — поля: car, reg_number, authority, valid_from, valid_to

Поведение и форматы
- Для списков API может использовать DRF пагинацию — в этом случае ответ: `{ "count":.., "next":.., "previous":.., "results":[...] }`.
- Авторизация: для защищённых методов добавьте заголовок `Authorization: Bearer <access_token>`.
- Ошибки валидации возвращаются в формате DRF: HTTP 400 и тело с полями ошибок.

Примеры полезных запросов (SQL)
- Машины без действующей страховки (пример для SQL/постгрес):
  SELECT c.* FROM car c LEFT JOIN insurancepolicy ip ON ip.car_id=c.id AND (ip.date_end IS NULL OR ip.date_end >= CURRENT_DATE) WHERE ip.id IS NULL;
- Регистрации, истекающие в ближайшие 30 дней:
  SELECT r.* FROM registration r WHERE r.valid_to BETWEEN CURRENT_DATE AND CURRENT_DATE + interval '30 days';
- Средний возраст авто по производителю:
  SELECT vm.manufacturer, AVG(EXTRACT(YEAR FROM CURRENT_DATE) - c.year) AS avg_age FROM car c JOIN vehiclemodel vm ON c.vehicle_model_id=vm.id GROUP BY vm.manufacturer;
