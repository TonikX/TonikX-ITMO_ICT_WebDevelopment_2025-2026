# Модели данных Printing House

## Обзор

Система Printing House использует следующие модели данных для управления газетами, типографиями и почтовыми отделениями.

## Модели

### Newspaper (Газета)

Модель для представления газеты.

**Поля:**
- `id` - уникальный идентификатор (автоматически)
- `title` - название газеты (CharField, max_length=200)
- `publication_index` - индекс издания (CharField, max_length=20, unique=True)
- `editor_first_name` - имя редактора (CharField, max_length=100)
- `editor_last_name` - фамилия редактора (CharField, max_length=100)
- `editor_middle_name` - отчество редактора (CharField, max_length=100, blank=True, null=True)
- `price_per_copy` - цена экземпляра (DecimalField, max_digits=10, decimal_places=2)

**Свойства:**
- `editor_full_name` - полное имя редактора (property)

**Связи:**
- One-to-Many с PrintingRun (газета может иметь много тиражей)
- One-to-Many с Distribution (газета может иметь много распределений)

**Пример:**
```python
{
    "id": 1,
    "title": "Городские вести",
    "publication_index": "GV-001",
    "editor_first_name": "Иван",
    "editor_last_name": "Иванов",
    "editor_middle_name": "Иванович",
    "price_per_copy": "25.00"
}
```

### PrintingHouse (Типография)

Модель для представления типографии.

**Поля:**
- `id` - уникальный идентификатор (автоматически)
- `name` - название типографии (CharField, max_length=200)
- `address` - адрес типографии (TextField)
- `is_active` - статус активности (BooleanField, default=True)

**Связи:**
- One-to-Many с PrintingRun (типография может иметь много тиражей)
- One-to-Many с Distribution (типография может отправлять газеты в много почтовых отделений)

**Пример:**
```python
{
    "id": 1,
    "name": "Типография \"Печатный дом\"",
    "address": "г. Москва, ул. Промышленная, д. 15",
    "is_active": true
}
```

### PostOffice (Почтовое отделение)

Модель для представления почтового отделения.

**Поля:**
- `id` - уникальный идентификатор (автоматически)
- `number` - номер почтового отделения (CharField, max_length=20, unique=True)
- `address` - адрес почтового отделения (TextField)

**Связи:**
- One-to-Many с Distribution (почтовое отделение может получать много распределений)

**Пример:**
```python
{
    "id": 1,
    "number": "101001",
    "address": "г. Москва, ул. Тверская, д. 1"
}
```

### PrintingRun (Тираж)

Промежуточная модель для связи типографии и газеты с указанием тиража.

**Поля:**
- `id` - уникальный идентификатор (автоматически)
- `printing_house` - типография (ForeignKey -> PrintingHouse)
- `newspaper` - газета (ForeignKey -> Newspaper)
- `circulation` - размер тиража (IntegerField)

**Ограничения:**
- Уникальная комбинация printing_house и newspaper (unique_together)

**Пример:**
```python
{
    "id": 1,
    "printing_house": 1,
    "newspaper": 1,
    "circulation": 10000
}
```

### Distribution (Распределение)

Промежуточная модель для связи почтового отделения, газеты и типографии с количеством экземпляров.

**Поля:**
- `id` - уникальный идентификатор (автоматически)
- `post_office` - почтовое отделение (ForeignKey -> PostOffice)
- `newspaper` - газета (ForeignKey -> Newspaper)
- `printing_house` - типография (ForeignKey -> PrintingHouse)
- `quantity` - количество экземпляров (IntegerField)

**Ограничения:**
- Уникальная комбинация post_office, newspaper и printing_house (unique_together)

**Пример:**
```python
{
    "id": 1,
    "post_office": 1,
    "newspaper": 1,
    "printing_house": 1,
    "quantity": 500
}
```

## Типы связей

### One-to-Many (один-ко-многим)

1. **PrintingHouse -> PrintingRun**
   - Одна типография может иметь много тиражей разных газет
   - Реализовано через ForeignKey в PrintingRun

2. **PostOffice -> Distribution**
   - Одно почтовое отделение может получать много распределений
   - Реализовано через ForeignKey в Distribution

3. **Newspaper -> PrintingRun**
   - Одна газета может печататься в разных типографиях
   - Реализовано через ForeignKey в PrintingRun

4. **Newspaper -> Distribution**
   - Одна газета может распределяться в разные почтовые отделения
   - Реализовано через ForeignKey в Distribution

### Many-to-Many (многие-ко-многим)

1. **Newspaper <-> PrintingHouse** (через PrintingRun)
   - Многие газеты могут печататься во многих типографиях
   - Реализовано через промежуточную модель PrintingRun

2. **Newspaper <-> PostOffice** (через Distribution)
   - Многие газеты могут распределяться во многие почтовые отделения
   - Реализовано через промежуточную модель Distribution

3. **PrintingHouse <-> PostOffice** (через Distribution)
   - Многие типографии могут отправлять газеты во многие почтовые отделения
   - Реализовано через промежуточную модель Distribution

## Особенности реализации

### Уникальные ограничения

- `publication_index` в Newspaper - уникальный индекс издания
- `number` в PostOffice - уникальный номер почтового отделения
- `unique_together` в PrintingRun - уникальная комбинация типографии и газеты
- `unique_together` в Distribution - уникальная комбинация почтового отделения, газеты и типографии

### Сортировка

- Newspaper: по названию (title)
- PrintingHouse: по названию (name)
- PostOffice: по номеру (number)
- PrintingRun: по тиражу в порядке убывания (circulation DESC)
- Distribution: по почтовому отделению и газете

### Управление статусом типографии

Поле `is_active` в модели PrintingHouse позволяет отслеживать статус типографии (активна или закрыта). При закрытии типографии можно скорректировать работу других типографий с учетом потребностей почтовых отделений.

