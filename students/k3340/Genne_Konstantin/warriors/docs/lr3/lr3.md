# Лабораторная работа №3. Реализация серверной части на Django REST Framework

**Цель**: овладеть практическими навыками и умениями реализации web-сервисов
средствами Django.  

В данном отчёте представлены модели базы данных и описание API.

---

## Модели базы данных

### 1. **Breed (Порода)**

Представляет породу кур.

- **`name`** (`CharField`) — название породы (уникальное, макс. 80 символов).
- **`efficiency`** (`PositiveIntegerField`) — среднее количество яиц в месяц.
- **`mean_weight`** (`PositiveIntegerField`) — средний вес курицы в граммах.
- **`diets`** (`ManyToManyField` через `BreedDiet`) — связь с диетами по сезонам.

**Связи:**
- Связана с моделью `Diet` через промежуточную модель `BreedDiet`.
- Используется в модели `Hen`.

---

### 2. **Diet (Диета)**

Описывает рацион питания кур.

- **`number`** (`IntegerField`) — уникальный номер диеты.
- **`structure`** (`TextField`) — описание состава диеты.

**Связи:**
- Связана с `Breed` через `BreedDiet`.

---

### 3. **BreedDiet (Диета породы)**

Промежуточная модель для связи породы, диеты и сезона.

- **`breed`** (`ForeignKey` → `Breed`) — порода.
- **`diet`** (`ForeignKey` → `Diet`) — диета.
- **`season`** (`CharField` с выбором из: `winter`, `spring`, `summer`, `autumn`) — сезон.

**Особенности:**
- Уникальность по тройке: `(breed, diet, season)`.

---

### 4. **Hen (Курица)**

Отдельная особь курицы.

- **`breed`** (`ForeignKey` → `Breed`, `on_delete=PROTECT`) — порода.
- **`weight`** (`PositiveIntegerField`) — текущий вес в граммах.
- **`birth_date`** (`DateTimeField`) — дата рождения.
- **`death_date`** (`DateTimeField`, опционально) — дата смерти.
- **`cages`** (`ManyToManyField` через `HenCage`) — история размещения по клеткам.

**Связи:**
- Связана с `Cage` через `HenCage`.
- Используется в `HenEggs`.

---

### 5. **HenEggs (Яйценоскость)**

Фиксирует количество снесённых яиц конкретной курицей в определённую дату.

- **`hen`** (`ForeignKey` → `Hen`) — курица.
- **`count_eggs`** (`PositiveIntegerField`) — количество яиц.
- **`date`** (`DateField`) — дата сбора яиц.

**Особенности:**
- Уникальность по паре: `(hen, date)`.

---

### 6. **Cage (Клетка)**

Описывает физическое расположение клетки.

- **`workshop_number`** (`PositiveIntegerField`) — номер цеха.
- **`row_number`** (`PositiveIntegerField`) — номер ряда.
- **`in_row_number`** (`PositiveIntegerField`) — номер клетки в ряду.

**Особенности:**
- Уникальность по тройке: `(workshop_number, row_number, in_row_number)`.

**Связи:**
- Используется в `HenCage` и `EmployeeCage`.

---

### 7. **HenCage (Размещение курицы)**

Промежуточная модель, отслеживающая, когда и куда заселялась курица.

- **`hen`** (`ForeignKey` → `Hen`) — курица.
- **`cage`** (`ForeignKey` → `Cage`) — клетка.
- **`date_start`** (`DateField`) — дата заселения.
- **`date_end`** (`DateField`, опционально) — дата выселения.

---

### 8. **Employee (Работник)**

Информация о сотруднике.

- **`full_name`** (`CharField`) — ФИО.
- **`passport_series`** (`CharField`, 4 цифры, валидация регулярным выражением).
- **`passport_number`** (`CharField`, 6 цифр, валидация регулярным выражением).
- **`cages`** (`ManyToManyField` через `EmployeeCage`) — история закрепления за клетками.

**Связи:**
- Связана с `Cage` через `EmployeeCage`.
- Используется в `Employment`.

---

### 9. **EmployeeCage (Закрепление клетки за работником)**

Промежуточная модель для отслеживания, за какими клетками закреплён работник.

- **`employee`** (`ForeignKey` → `Employee`) — работник.
- **`cage`** (`ForeignKey` → `Cage`) — клетка.
- **`date_start`** (`DateField`) — дата начала закрепления.
- **`date_end`** (`DateField`, опционально) — дата окончания закрепления.

---

### 10. **Employment (Трудоустройство)**

Информация о трудовом договоре и должности сотрудника.

- **`employee`** (`ForeignKey` → `Employee`) — работник.
- **`position`** (`CharField`) — должность.
- **`contract`** (`CharField`, уникальный) — номер трудового договора.
- **`salary_rub`** (`DecimalField`) — зарплата (до 10 цифр, 2 знака после запятой).
- **`date_start`** (`DateField`) — дата начала работы.
- **`date_end`** (`DateField`, опционально) — дата увольнения.
- **`termination_reason`** (`CharField` с выбором из предопределённых причин, опционально).
- **`termination_order_num`** (`CharField`, опционально) — номер приказа об увольнении.

---

## Аутентификация

Токены необходимо передавать в заголовке запроса:
```
Authorization: Token <access_token>
```

### 1. Регистрация пользователя
**Endpoint:** `/auth/users/`  
**Метод:** POST  
**Права доступа:** Любой пользователь
```json
{
    "username": "first_name",
    "password": "jkhfcgxxx5366",
    "email": "first_user@mail.ru",
    "first_name": "Ivan",
    "last_name": "Ivanov"
}
```

### 2. Получение токена

**Endpoint:** `/auth/token/login/`  
**Метод:** POST  
**Права доступа:** Любой пользователь

**Запрос:**
```json
{
    "username": "first_name",
    "password": "jkhfcgxxx5366"
}
```

**Ответ (200 OK):**
```json
{
    "auth_token": "88a66ce54788bb36773548ee613250954a3cb909"
}
```

**Коды ответов:**
| Код | Описание |
|-----|----------|
| 200 | Успешная аутентификация |
| 401 | Неверные учетные данные |



### 3. Текущий пользователь

**Endpoint:** `/auth/users/me/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
{
    "email": "first_user@mail.ru",
    "id": 1,
    "username": "first_user"
}
```

**Коды ответов:**
| Код | Описание |
|-----|----------|
| 200 | Информация о пользователе получена |
| 401 | Необходима аутентификация |

---

## CRUD операции

### 1. Породы (Breeds)

#### Получение списка пород
**Endpoint:** `/api/breeds/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
[
    {
        "id": 1,
        "name": "Леггорн",
        "efficiency": 300,
        "mean_weight": 1000
    },
    {
        "id": 2,
        "name": "Род-Айленд",
        "efficiency": 280,
        "mean_weight": 988
    }
]
```

#### Создание новой породы
**Endpoint:** `/api/breeds/`  
**Метод:** POST  
**Права доступа:** Аутентифицированный пользователь

**Запрос:**
```json
{
    "name": "Хайсекс",
    "efficiency": 310,
    "mean_weight": 2005
}
```

**Ответ (201 Created):**
```json
{
    "id": 3,
    "name": "Хайсекс",
    "efficiency": 310,
    "mean_weight": 2005
}
```

#### Изменение породы
**Endpoint:** `/api/breeds/<id>/`  
**Метод:** PATCH  
**Права доступа:** Аутентифицированный пользователь

**Запрос:**
```json
{
    "efficiency": 315
}
```

**Ответ (200 OK):**
```json
{
    "id": 3,
    "name": "Хайсекс",
    "efficiency": 315,
    "mean_weight": 2005
}
```

#### Удаление породы
**Endpoint:** `/api/breeds/<id>/`  
**Метод:** DELETE  
**Права доступа:** Аутентифицированный пользователь

**Ответ (204 No Content):** Пустой ответ

**Ошибка при удалении породы с привязанными курами (400 Bad Request):**
```json
{
    "error": "Нельзя удалить породу, к которой привязаны куры"
}
```

### 2. Куры (Hens)

#### Получение списка кур
**Endpoint:** `/api/hens/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
[
    {
        "id": 1,
        "breed": 1,
        "weight": 2000,
        "birth_date": "2025-01-26T00:00:00Z",
        "death_date": null,
        "breed_name": "Леггорн"
    },
    {
        "id": 2,
        "breed": 1,
        "weight": 2050,
        "birth_date": "2025-01-16T00:00:00Z",
        "death_date": null,
        "breed_name": "Леггорн"
    }
]
```

#### Обновление характеристик курицы
**Endpoint:** `/api/hens/<id>/`  
**Метод:** PATCH  
**Права доступа:** Аутентифицированный пользователь

**Запрос:**
```json
{
    "weight": 2100
}
```

**Ответ (200 OK):**
```json
{
    "id": 1,
    "breed": 1,
    "weight": 2100,
    "birth_date": "2025-01-26T00:00:00Z",
    "death_date": null,
    "breed_name": "Леггорн"
}
```

Разрешено менять только: weight (масса), death_date (дата и время смерти).

**Ошибка при попытке изменить запрещенное поле (400 Bad Request):**
```json
{
    "error": "Обновление полей breed запрещено."
}
```

#### Детальная информация о курице
**Endpoint:** `/api/hens/<id>/detail/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
{
    "id": 1,
    "breed": {
        "id": 1,
        "name": "Леггорн",
        "efficiency": 300,
        "mean_weight": 988
    },
    "weight": 2100,
    "birth_date": "2024-05-31T00:00:00Z",
    "death_date": null,
    "current_cage": {
        "id": 5,
        "workshop_number": 2,
        "row_number": 3,
        "in_row_number": 4,
        "date_start": "2025-06-01",
        "date_end": null
    }
}
```

### 3. Клетки (Cages)

#### Детальная информация о клетке
**Endpoint:** `/api/cages/<id>/detail/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
{
    "id": 5,
    "workshop_number": 2,
    "row_number": 3,
    "in_row_number": 4,
    "current_hens": [
        {
            "id": 1,
            "breed_name": "Леггорн",
            "weight": 2100,
            "birth_date": "2025-06-01",
            "date_start": "2025-06-01",
            "date_end": null
        },
        {
            "id": 2,
            "breed_name": "Леггорн",
            "weight": 2050,
            "birth_date": "2025-06-05",
            "date_start": "2025-06-05",
            "date_end": null
        }
    ]
}
```

### 4. Диеты (Diets)

#### Получение списка диет
**Endpoint:** `/api/diets/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
[
    {
        "id": 1,
        "number": 2,
        "structure": "Летняя: комбикорм 60%, трава 30%, минералы 10%"
    },
    {
        "id": 2,
        "number": 3,
        "structure": "Универсальная: зерно 40%, бобовые 30%, витамины 30%"
    }
]
```

#### Создание новой диеты
**Endpoint:** `/api/diets/`  
**Метод:** POST  
**Права доступа:** Аутентифицированный пользователь

**Запрос:**
```json
{
    "number": 4,
    "structure": "Зеленые корма + зерносмесь + ракушка"
}
```

**Ответ (201 Created):**
```json
{
    "id": 4,
    "number": 4,
    "structure": "Зеленые корма + зерносмесь + ракушка"
}
```

#### Изменение диеты
**Endpoint:** `/api/diets/<id>/`  
**Метод:** PATCH  
**Права доступа:** Аутентифицированный пользователь

**Запрос:**
```json
{
    "structure": "Зерносмесь 50%, шрот 30%, минералы 20%"
}
```

**Ответ (200 OK):**
```json
{
    "id": 4,
    "number": 4,
    "structure": "Зерносмесь 50%, шрот 30%, минералы 20%"
}
```

#### Удаление диеты
**Endpoint:** `/api/diets/<id>/`  
**Метод:** DELETE  
**Права доступа:** Аутентифицированный пользователь

**Ответ (204 No Content):** Пустой ответ

**Ошибка при удалении диеты с привязанными породами (400 Bad Request):**
```json
{
    "error": "Нельзя удалить диету, к которой привязаны породы"
}
```

### 5. Сезонные диеты для пород (BreedDiets)

#### Получение списка сезонных диет
**Endpoint:** `/api/breed-diets/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
[
    {
        "id": 1,
        "breed": 1,
        "diet": 1,
        "season": "winter",
        "breed_name": "Леггорн",
        "diet_number": 1
    },
    {
        "id": 2,
        "breed": 1,
        "diet": 2,
        "season": "spring",
        "breed_name": "Леггорн",
        "diet_number": 2
    }
]
```

#### Фильтрация по породе
**Endpoint:** `/api/breed-diets/?breed_id=1`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
[
    {
        "id": 1,
        "breed": 1,
        "diet_id": 1,
        "season": "Зима",
        "breed_name": "Леггорн",
        "diet_number": 1
    },
    {
        "id": 2,
        "breed": 1,
        "diet_id": 2,
        "season": "Лето",
        "breed_name": "Леггорн",
        "diet_number": 2
    },
]
```

#### Создание сезонной диеты
**Endpoint:** `/api/breed-diets/`  
**Метод:** POST  
**Права доступа:** Аутентифицированный пользователь

**Запрос:**
```json
{
    "breed": 1,
    "diet": 3,
    "season": "summer"
}
```

**Ответ (201 Created):**
```json
{
    "id": 3,
    "breed": 1,
    "diet": 3,
    "season": "summer",
    "breed_name": "Леггорн",
    "diet_number": 3
}
```

#### Обновление сезонной диеты
**Endpoint:** `/api/breed-diets/<id>/`  
**Метод:** PATCH  
**Права доступа:** Аутентифицированный пользователь

**Запрос:**
```json
{
    "diet": 4
}
```

**Ответ (200 OK):**
```json
{
    "id": 3,
    "breed": 1,
    "diet": 4,
    "season": "summer",
    "breed_name": "Леггорн",
    "diet_number": 4
}
```

#### Удаление сезонной диеты
**Endpoint:** `/api/breed-diets/<id>/`  
**Метод:** DELETE  
**Права доступа:** Аутентифицированный пользователь

**Ответ (204 No Content):** Пустой ответ

**Коды ответов:**
| Код | Описание |
|-----|----------|
| 204 | Сезонная диета успешно удалена |
| 404 | Сезонная диета не найдена |

### 6. Яйценоскость (HenEggs)

#### Получение записей яйценоскости
**Endpoint:** `/api/hen-eggs/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Параметры фильтрации:**
- `hen_id` - ID курицы
- `date_from` - начальная дата (формат YYYY-MM-DD)
- `date_to` - конечная дата (формат YYYY-MM-DD)

**Пример:** `/api/hen-eggs/?hen=1&date_from=2025-11-01&date_to=2025-11-30`

**Ответ (200 OK):**
```json
[
    {
        "id": 1,
        "hen": 1,
        "count_eggs": 28,
        "date": "2025-11-01"
    },
    {
        "id": 2,
        "hen": 1,
        "count_eggs": 30,
        "date": "2025-11-02"
    }
]
```

#### Создание записи яйценоскости
**Endpoint:** `/api/hen-eggs/`  
**Метод:** POST  
**Права доступа:** Аутентифицированный пользователь

**Запрос:**
```json
{
    "hen": 1,
    "count_eggs": 29,
    "date": "2025-12-01"
}
```

**Ответ (201 Created):**
```json
{
    "id": 3,
    "hen": 1,
    "count_eggs": 29,
    "date": "2025-12-01"
}
```

Если уже существует запись для этой курицы и даты:  
**Ответ (400 Bad Request):**
```json
{
    "non_field_errors": [
        "The fields hen, date must make a unique set."
    ]
}
```

#### Обновление записи яйценоскости
**Endpoint:** `/api/hen-eggs/<id>/`  
**Метод:** PATCH  
**Права доступа:** Аутентифицированный пользователь

**Запрос:**
```json
{
    "count_eggs": 31
}
```

**Ответ (200 OK):**
```json
{
    "id": 3,
    "hen_id": 1,
    "count_eggs": 31,
    "date": "2025-12-01"
}
```

#### Удаление записи яйценоскости
**Endpoint:** `/api/hen-eggs/<id>/`  
**Метод:** DELETE  
**Права доступа:** Аутентифицированный пользователь

**Ограничение:** Удаление разрешено только в течение 24 часов после создания

**Ответ (204 No Content):** Пустой ответ

**Ошибка при попытке удаления старой записи (403 Forbidden):**
```json
{
    "error": "Удаление записей о яйценоскости разрешено только в течение 24 часов"
}
```

### 7. Работники (Employees)

#### Получение списка работников
**Endpoint:** `/api/employees/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
[
    {
        "id": 1,
        "full_name": "Иванов Иван Иванович",
        "passport_series": "1234",
        "passport_number": "567890"
    },
    {
        "id": 2,
        "full_name": "Петров Петр Петрович",
        "passport_series": "2345",
        "passport_number": "678901"
    }
]
```

#### Создание работника
**Endpoint:** `/api/employees/`  
**Метод:** POST  
**Права доступа:** Аутентифицированный пользователь

**Запрос:**
```json
{
    "full_name": "Сидоров Сидор Сидорович",
    "passport_series": "3456",
    "passport_number": "789012"
}
```

**Ответ (201 Created):**
```json
{
    "id": 3,
    "full_name": "Сидоров Сидор Сидорович",
    "passport_series": "3456",
    "passport_number": "789012"
}
```

#### Обновление работника
**Endpoint:** `/api/employees/<id>/`  
**Метод:** PATCH  
**Права доступа:** Аутентифицированный пользователь

**Запрос:**
```json
{
    "full_name": "Сидоров С.С."
}
```

**Ответ (200 OK):**
```json
{
    "id": 3,
    "full_name": "Сидоров С.С.",
    "passport_series": "3456",
    "passport_number": "789012"
}
```

#### Удаление работника
**Endpoint:** `/api/employees/<id>/`  
**Метод:** DELETE  
**Права доступа:** Запрещено

**Ответ (405 Method Not Allowed):**
```json
{
    "error": "Удаление сотрудников запрещено. Используйте увольнение через Employment"
}
```

### 8. Закрепление работников за клетками (EmployeeCages)

#### Получение списка закреплений
**Endpoint:** `/api/employee-cages/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Параметры фильтрации:**
- `employee` - ID работника
- `cage` - ID клетки
- `active` - только текущие закрепления (true/false)

**Пример:** `/api/employee-cages/?employee=1&active=true`

**Ответ (200 OK):**
```json
[
    {
        "id": 1,
        "employee": 1,
        "cage": 5,
        "date_start": "2025-06-01",
        "date_end": null,
        "employee_details": {
            "id": 1,
            "full_name": "Иванов Иван Иванович",
            "passport_series": "1234",
            "passport_number": "567890"
        },
        "cage_details": {
            "id": 5,
            "workshop_number": 2,
            "row_number": 3,
            "in_row_number": 4
        }
    }
]
```

#### Создание закрепления
**Endpoint:** `/api/employee-cages/`  
**Метод:** POST  
**Права доступа:** Аутентифицированный пользователь

**Запрос:**
```json
{
    "employee": 1,
    "cage": 6,
    "date_start": "2025-12-01",
    "date_end": null
}
```

**Ответ (201 Created):**
```json
{
    "id": 2,
    "employee": 1,
    "cage": 6,
    "date_start": "2025-12-01",
    "date_end": "2026-12-01",
    "employee_details": {
        "id": 1,
        "full_name": "Иванов Иван Иванович",
        "passport_series": "1234",
        "passport_number": "567890"
    },
    "cage_details": {
        "id": 6,
        "workshop_number": 2,
        "row_number": 3,
        "in_row_number": 5
    }
}
```

#### Обновление закрепления
**Endpoint:** `/api/employee-cages/<id>/`  
**Метод:** PATCH  
**Права доступа:** Аутентифицированный пользователь

**Запрос (открепление работника):**
```json
{
    "date_end": "2025-12-15"
}
```

**Ответ (200 OK):**
```json
{
    "id": 2,
    "employee": 1,
    "cage": 6,
    "date_start": "2025-12-01",
    "date_end": "2025-12-15",
    "employee_details": {
        "id": 1,
        "full_name": "Иванов Иван Иванович",
        "passport_series": "1234",
        "passport_number": "567890"
    },
    "cage_details": {
        "id": 6,
        "workshop_number": 2,
        "row_number": 3,
        "in_row_number": 5
    }
}
```

#### Удаление закрепления
**Endpoint:** `/api/employee-cages/<id>/`  
**Метод:** DELETE  
**Права доступа:** Запрещено

**Ответ (405 Method Not Allowed):**
```json
{
    "error": "Удаление записей о закреплении запрещено. Используйте обновление даты открепления"
}
```

### 9. Трудоустройство (Employments)

#### Получение списка трудоустройств
**Endpoint:** `/api/employments/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Параметры фильтрации:**
- `employee_id` - ID работника
- `active` - только текущие трудоустройства (true/false)

**Пример:** `/api/employments/?employee_id=1&active=true`

**Ответ (200 OK):**
```json
[

    {
        "id": 3,
        "employee": 2,
        "position": "Старший птицевод",
        "contract": "ДОГ-2023-020",
        "salary_rub": "48000.00",
        "date_start": "2025-06-06",
        "date_end": null,
        "termination_reason": null,
        "termination_order_num": null,
        "employee_details": {
            "id": 2,
            "full_name": "Петрова Анна Сергеевна",
            "passport_series": "4502",
            "passport_number": "234567"
        }
    }
]
```

#### Создание трудоустройства
**Endpoint:** `/api/employments/`  
**Метод:** POST  
**Права доступа:** Аутентифицированный пользователь

```json
{
    "employee": 3,
    "position": "Птицевод",
    "contract": "DOGOVOR-003",
    "salary_rub": "75000.00",
    "date_start": "2025-12-01"
}
```

**Ответ (201 Created):**
```json
{
    "id": 3,
    "employee": 3,
    "position": "Ветеринар",
    "contract": "DOGOVOR-003",
    "salary_rub": "75000.00",
    "date_start": "2025-12-01",
    "date_end": null,
    "termination_reason": null,
    "termination_order_num": null,
    "employee_details": {
        "id": 3,
        "full_name": "Сидоров С.С.",
        "passport_series": "3456",
        "passport_number": "789012"
    }
}
```


#### Обновление трудоустройства
**Endpoint:** `/api/employments/<id>/`  
**Метод:** PATCH  
**Права доступа:** Аутентифицированный пользователь

**Запрос (изменение зарплаты):**
```json
{
    "salary_rub": "80000.00"
}
```

**Запрос (увольнение):**
```json
{
    "date_end": "2025-12-15",
    "termination_reason": "employee_initiative",
    "termination_order_num": "PRIKAZ-001"
}
```

**Ответ (200 OK):**
```json
{
    "id": 3,
    "employee": 3,
    "position": "Ветеринар",
    "contract": "DOGOVOR-003",
    "salary_rub": "80000.00",
    "date_start": "2025-12-01",
    "date_end": "2025-12-15",
    "termination_reason": "employee_initiative",
    "termination_order_num": "PRIKAZ-001",
    "employee_details": {
        "id": 3,
        "full_name": "Сидоров С.С.",
        "passport_series": "3456",
        "passport_number": "789012"
    }
}
```

#### Удаление трудоустройства
**Endpoint:** `/api/employments/<id>/`  
**Метод:** DELETE  
**Права доступа:** Запрещено

**Ответ (405 Method Not Allowed):**
```json
{
    "error": "Удаление записей о трудоустройстве запрещено. Используйте пометку об увольнении"
}
```

### 10. Заселение кур в клетки (HenCages)

#### Получение списка заселений
**Endpoint:** `/api/hen-cages/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Параметры фильтрации:**
- `hen_id` - ID курицы
- `cage_id` - ID клетки
- `active` - только текущие заселения (true/false)

**Пример:** `/api/hen-cages/?hen_id=1&active=true`

**Ответ (200 OK):**
```json
[
    {
        "id": 1,
        "hen": 1,
        "cage": 5,
        "date_start": "2025-06-01",
        "date_end": null,
        "hen_details": {
            "id": 1,
            "breed": 1,
            "weight": 2000,
            "birth_date": "2025-06-01",
            "death_date": null,
            "breed_name": "Леггорн"
        },
        "cage_details": {
            "id": 5,
            "workshop_number": 2,
            "row_number": 3,
            "in_row_number": 4
        }
    }
]
```

#### Создание заселения
**Endpoint:** `/api/hen-cages/`  
**Метод:** POST  
**Права доступа:** Аутентифицированный пользователь

**Запрос:**
```json
{
    "hen": 2,
    "cage": 5,
    "date_start": "2025-12-01"
}
```

**Ответ (201 Created):**
```json
{
    "id": 2,
    "hen": 2,
    "cage": 5,
    "date_start": "2025-12-01",
    "date_end": null,
    "hen_details": {
        "id": 2,
        "breed": 1,
        "weight": 2050,
        "birth_date": "2025-06-05",
        "death_date": null,
        "breed_name": "Леггорн"
    },
    "cage_details": {
        "id": 5,
        "workshop_number": 2,
        "row_number": 3,
        "in_row_number": 4
    }
}
```

#### Обновление заселения
**Endpoint:** `/api/hen-cages/<id>/`  
**Метод:** PATCH  
**Права доступа:** Аутентифицированный пользователь

**Запрос (выселение курицы):**
```json
{
    "date_end": "2025-12-15"
}
```

**Ответ (200 OK):**
```json
{
    "id": 2,
    "hen": 2,
    "cage": 5,
    "date_start": "2025-12-01",
    "date_end": "2025-12-15",
    "hen_details": {
        "id": 2,
        "breed": 1,
        "weight": 2050,
        "birth_date": "2025-06-05",
        "death_date": null,
        "breed_name": "Леггорн"
    },
    "cage_details": {
        "id": 5,
        "workshop_number": 2,
        "row_number": 3,
        "in_row_number": 4
    }
}
```

#### Удаление заселения
**Endpoint:** `/api/hen-cages/<id>/`  
**Метод:** DELETE  
**Права доступа:** Запрещено

**Ответ (405 Method Not Allowed):**
```json
{
    "error": "Удаление записей о заселении запрещено. Используйте обновление даты выселения"
}
```

### 11. Клетки (Cages)

#### Получение списка клеток
**Endpoint:** `/api/cages/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
[
    {
        "id": 5,
        "workshop_number": 2,
        "row_number": 3,
        "in_row_number": 4
    },
    {
        "id": 6,
        "workshop_number": 2,
        "row_number": 3,
        "in_row_number": 5
    }
]
```

#### Создание клетки
**Endpoint:** `/api/cages/`  
**Метод:** POST  
**Права доступа:** Аутентифицированный пользователь

**Запрос:**
```json
{
    "workshop_number": 3,
    "row_number": 1,
    "in_row_number": 1
}
```

**Ответ (201 Created):**
```json
{
    "id": 7,
    "workshop_number": 3,
    "row_number": 1,
    "in_row_number": 1
}
```

#### Обновление клетки
**Endpoint:** `/api/cages/<id>/`  
**Метод:** PATCH  
**Права доступа:** Запрещено

**Ответ (405 Method Not Allowed):**
```json
{
    "error": "Обновление параметров клетки запрещено"
}
```

#### Удаление клетки
**Endpoint:** `/api/cages/<id>/`  
**Метод:** DELETE  
**Права доступа:** Аутентифицированный пользователь

**Ограничение:** Удаление разрешено только для пустых клеток

**Ответ (204 No Content):** Пустой ответ

**Ошибка при удалении непустой клетки (400 Bad Request):**
```json
{
    "error": "Нельзя удалить клетку, в которой есть куры или за которой закреплены работники"
}
```

---

## Отчеты

### 1. Яйценоскость по характеристикам курицы

**Endpoint:** `/api/reports/eggs-by-characteristics/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
[
    {
        "hen_id": 1,
        "breed_name": "Леггорн",
        "weight": 1106.0,
        "age_months": 10.4,
        "birth_date": "2025-01-26",
        "avg_eggs": 1.17
    },
    {
        "hen_id": 2,
        "breed_name": "Леггорн",
        "weight": 1820.0,
        "age_months": 10.7,
        "birth_date": "2025-01-16",
        "avg_eggs": 1.0
    }
]
```

Обладает параметрами: `breed`, `weight_category`, `age_category`.

Доступные возрастные категории `weight_category`:
* 'до_6_месяцев'
* '6-12_месяцев'
* 'старше_года'

Доступные весовые категории `age_category`:
* 'до_1.5_кг'
* '1.5-2.0_кг'
* 'свыше_2.0_кг'

**Endpoint:** `/api/reports/eggs-by-characteristics/?breed=Леггорн` 
```json
[
    {
        "hen_id": 2,
        "breed_name": "Леггорн",
        "weight": 1820.0,
        "age_months": 10.7,
        "birth_date": "2025-01-16",
        "avg_eggs": 1.0
    },
    {
        "hen_id": 3,
        "breed_name": "Леггорн",
        "weight": 1830.0,
        "age_months": 11.0,
        "birth_date": "2025-01-06",
        "avg_eggs": 1.0
    },
]
```

### 2. Цех с наибольшим количеством кур определенной породы

**Endpoint:** `/api/reports/top-workshop/<breed_name>/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Пример:** `/api/reports/top-workshop/Леггорн/`

**Ответ (200 OK):**
```json
[
    {
        "workshop_number": 2,
        "breed_count": 48
    }
]
```

### 3. Среднее количество яиц на работника в день

**Endpoint:** `/api/reports/employee-average-eggs/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
[
    {
        "employee_name": "Иванов И.И.",
        "avg_eggs_per_day": 95.3
    },
    {
        "employee_name": "Петров П.П.",
        "avg_eggs_per_day": 112.7
    },
]
```

### 4. Распределение пород кур по цехам

**Endpoint:** `/api/reports/breed-distribution/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
[
    {
        "workshop_number": 1,
        "breed_name": "Леггорн",
        "count": 5
    },
    {
        "workshop_number": 1,
        "breed_name": "Плимутрок",
        "count": 2
    },
    {
        "workshop_number": 1,
        "breed_name": "Род-Айленд",
        "count": 4
    }
]
```

### 5. Разница эффективности породы и среднего по фабрике

**Endpoint:** `/api/reports/breed-efficiency-difference/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
[
    {
        "breed_name": "Леггорн",
        "breed_efficiency": 28,
        "factory_avg": 1.11,
        "difference": -0.04
    },
    {
        "breed_name": "Род-Айленд",
        "breed_efficiency": 20,
        "factory_avg": 1.11,
        "difference": 0.12
    },
    {
        "breed_name": "Плимутрок",
        "breed_efficiency": 16,
        "factory_avg": 1.11,
        "difference": -0.05
    }
]
```

### 6. Ежемесячный отчет

**Endpoint:** `/api/reports/monthly/`  
**Метод:** GET  
**Права доступа:** Аутентифицированный пользователь

**Ответ (200 OK):**
```json
{
    "period": "2025-11-01 - 2025-11-30",
    "total_hens": 30,
    "total_eggs": 363,
    "workshops": [
        {
            "workshop_number": 1,
            "total_hens": 11,
            "total_eggs": 165,
            "breeds": [
                {
                    "breed_name": "Леггорн",
                    "count": 5,
                    "eggs": 100
                },
                {
                    "breed_name": "Плимутрок",
                    "count": 2,
                    "eggs": 19
                },
                {
                    "breed_name": "Род-Айленд",
                    "count": 4,
                    "eggs": 46
                }
            ]
        },
        {
            "workshop_number": 2,
            "total_hens": 9,
            "total_eggs": 69,
            "breeds": [
                {
                    "breed_name": "Леггорн",
                    "count": 1,
                    "eggs": 16
                },
                {
                    "breed_name": "Плимутрок",
                    "count": 4,
                    "eggs": 23
                },
                {
                    "breed_name": "Род-Айленд",
                    "count": 4,
                    "eggs": 30
                }
            ]
        },
        {
            "workshop_number": 3,
            "total_hens": 10,
            "total_eggs": 129,
            "breeds": [
                {
                    "breed_name": "Леггорн",
                    "count": 4,
                    "eggs": 64
                },
                {
                    "breed_name": "Плимутрок",
                    "count": 4,
                    "eggs": 39
                },
                {
                    "breed_name": "Род-Айленд",
                    "count": 2,
                    "eggs": 26
                }
            ]
        }
    ]
}
```