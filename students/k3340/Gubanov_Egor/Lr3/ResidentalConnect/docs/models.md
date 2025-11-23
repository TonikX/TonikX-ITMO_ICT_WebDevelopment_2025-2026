# Модели данных

## Обзор

Проект использует Django ORM для работы с базой данных. Все модели определены в файле `residential_app/models.py`.

## CustomUser (Пользователь)

### Описание
Расширенная модель пользователя Django с добавлением роли и номера телефона.

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | AutoField | Первичный ключ | Автоматически |
| `username` | CharField | Имя пользователя | Уникальное, из AbstractUser |
| `email` | EmailField | Email | Из AbstractUser |
| `first_name` | CharField | Имя | Из AbstractUser |
| `last_name` | CharField | Фамилия | Из AbstractUser |
| `role` | CharField | Роль | Выбор: resident/master/dispatcher |
| `phone_number` | CharField | Номер телефона | Необязательное |
| `password` | CharField | Пароль | Хешируется, из AbstractUser |
| `is_active` | BooleanField | Активен | Из AbstractUser |
| `date_joined` | DateTimeField | Дата регистрации | Автоматически |

### Роли
- `resident` — Жилец
- `master` — Мастер
- `dispatcher` — Диспетчер

## Building (Дом)

### Описание
Модель для хранения информации о жилых домах.

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | AutoField | Первичный ключ | Автоматически |
| `address` | CharField | Адрес дома | max_length=255 |
| `total_floors` | PositiveIntegerField | Количество этажей | - |
| `description` | TextField | Описание | Необязательное |
| `created_at` | DateTimeField | Дата создания | auto_now_add |
| `updated_at` | DateTimeField | Дата обновления | auto_now |

### Связи
- **One-to-Many** с `Apartment` (один дом содержит много квартир)

## Apartment (Квартира)

### Описание
Модель для хранения информации о квартирах.

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | AutoField | Первичный ключ | Автоматически |
| `building` | ForeignKey | Дом | CASCADE, связь с Building |
| `number` | CharField | Номер квартиры | max_length=10 |
| `floor` | PositiveIntegerField | Этаж | - |
| `area` | DecimalField | Площадь (кв.м) | max_digits=6, decimal_places=2 |
| `balance` | DecimalField | Баланс счета | max_digits=10, decimal_places=2, default=0 |
| `owner` | ForeignKey | Владелец | SET_NULL, связь с CustomUser |
| `created_at` | DateTimeField | Дата создания | auto_now_add |
| `updated_at` | DateTimeField | Дата обновления | auto_now |

### Связи
- **Many-to-One** с `Building` (много квартир принадлежат одному дому)
- **Many-to-One** с `CustomUser` (много квартир могут принадлежать одному владельцу)

### Ограничения
- Уникальная комбинация `building` и `number`

## ServiceCategory (Категория услуг)

### Описание
Справочник категорий заявок на обслуживание.

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | AutoField | Первичный ключ | Автоматически |
| `name` | CharField | Название категории | max_length=100 |
| `description` | TextField | Описание | Необязательное |

### Связи
- **One-to-Many** с `ServiceRequest` (одна категория может содержать много заявок)

## ServiceRequest (Заявка)

### Описание
Модель заявки на обслуживание (тикет).

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | AutoField | Первичный ключ | Автоматически |
| `title` | CharField | Тема обращения | max_length=200 |
| `description` | TextField | Описание проблемы | - |
| `status` | CharField | Статус | Выбор: new/in_progress/done/canceled |
| `created_at` | DateTimeField | Дата создания | auto_now_add |
| `updated_at` | DateTimeField | Дата обновления | auto_now |
| `resolved_at` | DateTimeField | Дата решения | Необязательное |
| `worker_comment` | TextField | Комментарий мастера | Необязательное |
| `category` | ForeignKey | Категория | SET_NULL, связь с ServiceCategory |
| `apartment` | ForeignKey | Квартира | CASCADE, связь с Apartment |
| `requester` | ForeignKey | Заявитель | CASCADE, связь с CustomUser |
| `worker` | ForeignKey | Мастер-исполнитель | SET_NULL, связь с CustomUser |

### Статусы
- `new` — Новая
- `in_progress` — В работе
- `done` — Выполнено
- `canceled` — Отменена

### Связи
- **Many-to-One** с `ServiceCategory`
- **Many-to-One** с `Apartment`
- **Many-to-One** с `CustomUser` (requester — кто создал)
- **Many-to-One** с `CustomUser` (worker — кто исполняет)

## MeterReading (Показания счетчика)

### Описание
Модель для хранения показаний счетчиков (вода, электричество, газ).

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | AutoField | Первичный ключ | Автоматически |
| `apartment` | ForeignKey | Квартира | CASCADE, связь с Apartment |
| `meter_type` | CharField | Тип счетчика | Выбор: hot_water/cold_water/electricity/gas |
| `value` | DecimalField | Показания | max_digits=10, decimal_places=3 |
| `date_recorded` | DateField | Дата подачи | auto_now_add |
| `created_at` | DateTimeField | Дата создания | auto_now_add |

### Типы счетчиков
- `hot_water` — Горячая вода
- `cold_water` — Холодная вода
- `electricity` — Электричество
- `gas` — Газ

### Связи
- **Many-to-One** с `Apartment` (много показаний принадлежат одной квартире)

