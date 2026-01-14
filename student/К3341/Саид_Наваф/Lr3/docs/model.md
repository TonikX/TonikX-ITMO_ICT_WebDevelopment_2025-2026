# Модель данных (обновлённая для ЛР3)

Ниже описаны основные сущности и их поля после обновления схемы.

![DB schema](images/db_schema.png)

Основные сущности

- Owner (владелец)
  - id : int (PK)
  - first_name, last_name : varchar
  - date_of_birth : date (nullable) — добавлено
  - city : varchar (nullable)
  - created_at, updated_at : datetime
  - Связи: 1 → * OwnerContact, 1 → 1 DriverLicense, 1 → * Ownership

- OwnerContact
  - id : int (PK)
  - owner : FK → Owner
  - type : varchar (phone/email/address)
  - value : varchar
  - is_primary : boolean

- DriverLicense
  - id : int (PK)
  - owner : OneToOne → Owner
  - license_number : varchar UNIQUE
  - license_type : varchar (nullable) — возможно добавлено
  - issue_date : date
  - issued_by, notes : text (nullable)

- VehicleModel
  - id : int (PK)
  - manufacturer : varchar
  - model : varchar
  - segment, year_from, year_to : optional

- Car
  - id : int (PK)
  - vehicle_model : FK → VehicleModel (nullable)
  - vin : varchar UNIQUE
  - registration_number : varchar (nullable)
  - color, year : optional
  - Примечание: предыдущие поля make/reg_number могли быть переименованы в vehicle_model.via и registration_number.

- Ownership
  - id : int (PK)
  - owner : FK → Owner
  - car : FK → Car
  - date_start : date
  - date_end : date (nullable)
  - notes : text (nullable)
  - Ограничение: UniqueConstraint(owner, car, date_start)
  - Валидация: периоды владения для одной пары (owner, car) не должны пересекаться. Реализовано в clean()/save() модели.

- InsurancePolicy
  - id : int (PK)
  - car : FK → Car
  - policy_number : varchar UNIQUE
  - insurer : varchar
  - date_start, date_end : date
  - sum_insured : decimal (nullable)

- ServiceRecord
  - id : int (PK)
  - car : FK → Car
  - date : date
  - mileage : int (nullable)
  - description : text

- Registration
  - id : int (PK)
  - car : FK → Car
  - reg_number : varchar
  - authority : varchar (nullable)
  - valid_from : date
  - valid_to : date (nullable)

