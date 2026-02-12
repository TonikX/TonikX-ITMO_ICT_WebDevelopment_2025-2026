# Модели данных

Описание структуры базы данных и связей между моделями.

## Диаграмма связей

```
RoomType (1) ──< (N) Room
Floor (1) ──< (N) Room
Floor (1) ──< (N) CleaningSchedule
Guest (1) ──< (N) Stay
Room (1) ──< (N) Stay
Employee (1) ──< (N) CleaningSchedule
```

## RoomType (Тип номера)

Описание типа номера отеля.

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | Integer | Уникальный идентификатор | Primary Key, Auto |
| `name` | CharField | Название типа номера | max_length=100, NOT NULL |
| `capacity` | PositiveInteger | Вместимость номера | NOT NULL |
| `price_per_day` | DecimalField | Цена за день | max_digits=10, decimal_places=2, NOT NULL |

**Связи:**
- Один ко многим с `Room` (один тип может иметь много номеров)

## Floor (Этаж)

Этаж отеля.

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | Integer | Уникальный идентификатор | Primary Key, Auto |
| `number` | PositiveInteger | Номер этажа | NOT NULL |

**Связи:**
- Один ко многим с `Room` (один этаж может иметь много номеров)
- Один ко многим с `CleaningSchedule` (один этаж может иметь много записей в расписании)

## Room (Номер)

Номер отеля.

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | Integer | Уникальный идентификатор | Primary Key, Auto |
| `number` | CharField | Номер комнаты | max_length=10, NOT NULL |
| `phone` | CharField | Телефон в номере | max_length=20, blank=True |
| `type` | ForeignKey | Тип номера | FK to RoomType, CASCADE |
| `floor` | ForeignKey | Этаж | FK to Floor, CASCADE |

**Связи:**
- Многие к одному с `RoomType` (много номеров одного типа)
- Многие к одному с `Floor` (много номеров на одном этаже)
- Один ко многим с `Stay` (один номер может иметь много проживаний)

## Guest (Гость)

Гость отеля.

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | Integer | Уникальный идентификатор | Primary Key, Auto |
| `passport_number` | CharField | Номер паспорта | max_length=50, unique=True, NOT NULL |
| `last_name` | CharField | Фамилия | max_length=100, NOT NULL |
| `first_name` | CharField | Имя | max_length=100, NOT NULL |
| `middle_name` | CharField | Отчество | max_length=100, blank=True |
| `city` | CharField | Город | max_length=100, NOT NULL |

**Связи:**
- Один ко многим с `Stay` (один гость может иметь много проживаний)

**Особенности:**
- `passport_number` должен быть уникальным

## Stay (Проживание)

Запись о проживании гостя в номере.

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | Integer | Уникальный идентификатор | Primary Key, Auto |
| `check_in` | DateField | Дата заселения | NOT NULL |
| `check_out` | DateField | Дата выселения | NOT NULL |
| `guest` | ForeignKey | Гость | FK to Guest, CASCADE |
| `room` | ForeignKey | Номер | FK to Room, CASCADE |

**Связи:**
- Многие к одному с `Guest` (много проживаний одного гостя)
- Многие к одному с `Room` (много проживаний в одном номере)

## Employee (Сотрудник)

Сотрудник отеля.

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | Integer | Уникальный идентификатор | Primary Key, Auto |
| `last_name` | CharField | Фамилия | max_length=100, NOT NULL |
| `first_name` | CharField | Имя | max_length=100, NOT NULL |
| `middle_name` | CharField | Отчество | max_length=100, blank=True |
| `employed` | BooleanField | Статус работы | default=True |

**Связи:**
- Один ко многим с `CleaningSchedule` (один сотрудник может иметь много записей в расписании)

**Особенности:**
- `employed` по умолчанию `True`

## CleaningSchedule (Расписание уборки)

Расписание уборки этажей сотрудниками.

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | Integer | Уникальный идентификатор | Primary Key, Auto |
| `weekday` | CharField | День недели | max_length=20, NOT NULL |
| `employee` | ForeignKey | Сотрудник | FK to Employee, CASCADE |
| `floor` | ForeignKey | Этаж | FK to Floor, CASCADE |

**Связи:**
- Многие к одному с `Employee` (много записей расписания для одного сотрудника)
- Многие к одному с `Floor` (много записей расписания для одного этажа)

## Типы данных

- **CharField** - строковое поле с ограничением длины
- **PositiveIntegerField** - положительное целое число
- **DecimalField** - десятичное число с фиксированной точностью
- **DateField** - дата (без времени)
- **BooleanField** - логическое значение (True/False)
- **ForeignKey** - внешний ключ (связь с другой моделью)

## Каскадные удаления

Все внешние ключи используют `on_delete=models.CASCADE`, что означает:
- При удалении родительской записи автоматически удаляются все связанные дочерние записи
- Например, при удалении `RoomType` удаляются все связанные `Room`
- При удалении `Guest` удаляются все связанные `Stay`






