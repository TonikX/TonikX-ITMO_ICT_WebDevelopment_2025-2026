# Модели данных

## Общая структура

В лабораторной работе 4 используется следующая структура моделей данных для представления авиакомпании:

## Основные модели

### Airport (Аэропорт)
Представляет информацию об аэропорте.

Поля:
- `airport_code` (CharField) - Уникальный код аэропорта (первичный ключ)
- `country` (CharField) - Страна расположения
- `status` (CharField) - Статус аэропорта
- `city` (CharField) - Город расположения
- `name` (CharField) - Название аэропорта

### Company (Авиакомпания)
Представляет информацию о авиакомпании.

Поля:
- `name` (CharField) - Название авиакомпании
- `country` (CharField) - Страна регистрации

### Plane (Самолет)
Представляет информацию о самолете.

Поля:
- `company` (ForeignKey) - Ссылка на авиакомпанию
- `status` (CharField) - Текущий статус самолета
- `flight_duration` (IntegerField) - Продолжительность полета
- `mark` (CharField) - Модель самолета
- `last_technical_service` (DateTimeField) - Дата последнего технического обслуживания

### Flight (Рейс)
Представляет информацию о рейсе.

Поля:
- `plane` (ForeignKey) - Ссылка на самолет
- `status` (CharField) - Статус рейса
- `departure_airport` (ForeignKey) - Аэропорт отправления
- `destination_airport` (ForeignKey) - Аэропорт назначения
- `arrival_time` (DateTimeField) - Планируемое время прибытия
- `arrival_time_fact` (DateTimeField) - Фактическое время прибытия
- `departure_time` (DateTimeField) - Планируемое время отправления
- `departure_time_fact` (DateTimeField) - Фактическое время отправления

### Seat (Место)
Представляет информацию о месте в самолете.

Поля:
- `flight` (ForeignKey) - Ссылка на рейс
- `seat_number` (CharField) - Номер места
- `seat_type` (CharField) - Тип места
- `base_price` (FloatField) - Базовая цена
- `is_booked` (BooleanField) - Забронировано ли место

### Passenger (Пассажир)
Представляет информацию о пассажире.

Поля:
- `full_name` (CharField) - Полное имя
- `passport_serial` (CharField) - Серия паспорта
- `passport_number` (CharField) - Номер паспорта
- `passport_region` (CharField) - Регион выдачи паспорта
- `birth_date` (DateField) - Дата рождения
- `phone_number` (CharField) - Номер телефона
- `email` (CharField) - Электронная почта

### Ticket (Билет)
Представляет информацию о билете.

Поля:
- `flight` (ForeignKey) - Ссылка на рейс
- `passenger` (ForeignKey) - Ссылка на пассажира
- `seat` (ForeignKey) - Ссылка на место
- `sale_channel` (CharField) - Канал продажи
- `status` (CharField) - Статус билета
- `additional_fee` (FloatField) - Дополнительная плата

### CrewMember (Член экипажа)
Представляет информацию о члене экипажа.

Поля:
- `company` (ForeignKey) - Ссылка на авиакомпанию
- `full_name` (CharField) - Полное имя
- `email` (CharField) - Электронная почта
- `phone_number` (CharField) - Номер телефона
- `passport_serial` (CharField) - Серия паспорта
- `passport_number` (CharField) - Номер паспорта
- `passport_region` (CharField) - Регион выдачи паспорта
- `role` (CharField) - Роль в экипаже

### Crew (Экипаж)
Представляет информацию о назначении члена экипажа на рейс.

Поля:
- `member` (ForeignKey) - Ссылка на члена экипажа
- `role` (CharField) - Роль в конкретном рейсе
- `medical_check_date` (DateTimeField) - Дата медицинского осмотра
- `medical_status` (CharField) - Медицинский статус
- `medical_reason` (CharField) - Причина медицинского статуса (необязательно)
- `flight` (ForeignKey) - Ссылка на рейс