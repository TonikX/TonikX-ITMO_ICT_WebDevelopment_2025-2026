# Схемы процессов обработки заявок

## Обзор

В этом разделе представлены визуальные схемы, описывающие процесс обработки заявок в системе "ЖК Коннект".

## Жизненный цикл заявки

### Статусы заявки

Заявка проходит через следующие статусы:

```mermaid
stateDiagram-v2
    [*] --> new: Жилец создает заявку
    new --> in_progress: Диспетчер назначает мастера
    in_progress --> done: Мастер завершает работу
    in_progress --> canceled: Диспетчер отменяет
    new --> canceled: Диспетчер отменяет
    done --> [*]
    canceled --> [*]
    
    note right of new
        Статус: Новая
        Может: Диспетчер, Жилец (свои)
    end note
    
    note right of in_progress
        Статус: В работе
        Может: Мастер, Диспетчер
    end note
    
    note right of done
        Статус: Выполнено
        Финальный статус
    end note
```

## Процесс обработки заявки (Workflow)

### Полный процесс от создания до завершения

```mermaid
flowchart TD
    Start([Жилец создает заявку]) --> Create[Создание заявки<br/>Статус: new]
    Create --> Dispatcher{Диспетчер<br/>проверяет заявку}
    
    Dispatcher -->|Одобряет| Assign[Назначение мастера<br/>Статус: in_progress<br/>assigned_at установлен]
    Dispatcher -->|Отклоняет| Cancel1[Отмена заявки<br/>Статус: canceled]
    
    Assign --> MasterStart[Мастер начинает работу<br/>started_at установлен]
    MasterStart --> Work[Выполнение работ]
    
    Work --> MasterComment{Мастер добавляет<br/>комментарий?}
    MasterComment -->|Да| AddComment[Добавление комментария<br/>worker_comment]
    MasterComment -->|Нет| CheckStatus
    AddComment --> CheckStatus{Проверка<br/>статуса}
    
    CheckStatus -->|Работа завершена| Complete[Завершение работы<br/>Статус: done<br/>resolved_at установлен]
    CheckStatus -->|Работа продолжается| Work
    CheckStatus -->|Проблема| Dispatcher
    
    Complete --> End([Заявка закрыта])
    Cancel1 --> End
    
    style Start fill:#e1f5ff
    style Create fill:#fff4e1
    style Assign fill:#e8f5e9
    style Work fill:#f3e5f5
    style Complete fill:#c8e6c9
    style End fill:#ffcdd2
```

## Роли и их действия

### Кто что может делать с заявкой

```mermaid
graph LR
    subgraph Жилец
        R1[Создать заявку] --> R2[Просмотреть свои заявки]
        R2 --> R3[Отслеживать статус]
    end
    
    subgraph Диспетчер
        D1[Просмотреть все заявки] --> D2[Назначить мастера]
        D2 --> D3[Изменить статус]
        D3 --> D4[Добавить комментарий]
        D4 --> D5[Отменить заявку]
    end
    
    subgraph Мастер
        M1[Просмотреть назначенные заявки] --> M2[Изменить статус]
        M2 --> M3[Добавить комментарий]
        M3 --> M4[Завершить работу]
    end
    
    style R1 fill:#e3f2fd
    style D1 fill:#fff3e0
    style M1 fill:#f1f8e9
```

## Временная линия обработки заявки

### Отслеживание дат и событий

```mermaid
gantt
    title Временная линия обработки заявки
    dateFormat YYYY-MM-DD
    section Создание
    Жилец создает заявку           :created_at, 2024-01-01, 1d
    section Назначение
    Диспетчер назначает мастера    :assigned_at, 2024-01-02, 1d
    section Работа
    Мастер начинает работу         :started_at, 2024-01-02, 1d
    Выполнение работ               :active, 2024-01-02, 3d
    section Завершение
    Заявка выполнена               :done, resolved_at, 2024-01-05, 1d
```

## Схема взаимодействия ролей

### Кто с кем взаимодействует

```mermaid
sequenceDiagram
    participant Ж as Жилец
    participant Д as Диспетчер
    participant М as Мастер
    participant С as Система
    
    Ж->>С: Создать заявку (POST)
    С-->>Ж: Заявка создана (status: new)
    
    Д->>С: Просмотреть заявки (GET)
    С-->>Д: Список всех заявок
    
    Д->>С: Назначить мастера (POST assign_worker)
    С->>С: Установить assigned_at
    С->>С: Изменить статус на in_progress
    С-->>Д: Мастер назначен
    
    М->>С: Просмотреть назначенные заявки (GET)
    С-->>М: Список назначенных заявок
    
    М->>С: Начать работу (POST change_status)
    С->>С: Установить started_at
    С-->>М: Статус изменен
    
    М->>С: Добавить комментарий (POST add_comment)
    С-->>М: Комментарий добавлен
    
    М->>С: Завершить работу (POST change_status: done)
    С->>С: Установить resolved_at
    С-->>М: Заявка завершена
    
    Ж->>С: Просмотреть свои заявки (GET)
    С-->>Ж: Список заявок со статусом
```

## Схема данных заявки

### Структура и связи

```mermaid
erDiagram
    ServiceRequest ||--o{ ServiceCategory : "имеет"
    ServiceRequest }o--|| Apartment : "принадлежит"
    ServiceRequest }o--|| CustomUser : "создал"
    ServiceRequest }o--o| CustomUser : "исполняет"
    Apartment }o--|| Building : "находится в"
    Apartment }o--o| CustomUser : "принадлежит"
    
    ServiceRequest {
        int id PK
        string title
        string description
        string status "new/in_progress/done/canceled"
        string priority "low/medium/high/urgent"
        datetime created_at
        datetime assigned_at
        datetime started_at
        datetime resolved_at
        text worker_comment
    }
    
    CustomUser {
        int id PK
        string username
        string role "resident/master/dispatcher"
    }
    
    Apartment {
        int id PK
        string number
        int floor
        decimal area
    }
    
    Building {
        int id PK
        string address
        int total_floors
    }
    
    ServiceCategory {
        int id PK
        string name
        string description
    }
```

## Приоритеты заявок

### Обработка по приоритетам

```mermaid
flowchart TD
    Create[Создание заявки] --> Priority{Определение<br/>приоритета}
    
    Priority -->|urgent| Urgent[Срочный<br/>Обработка немедленно]
    Priority -->|high| High[Высокий<br/>Обработка в течение дня]
    Priority -->|medium| Medium[Средний<br/>Обработка в течение недели]
    Priority -->|low| Low[Низкий<br/>Обработка по возможности]
    
    Urgent --> Assign1[Назначение мастера<br/>в течение часа]
    High --> Assign2[Назначение мастера<br/>в течение дня]
    Medium --> Assign3[Назначение мастера<br/>в течение недели]
    Low --> Assign4[Назначение мастера<br/>по возможности]
    
    Assign1 --> Work[Выполнение работ]
    Assign2 --> Work
    Assign3 --> Work
    Assign4 --> Work
    
    style Urgent fill:#ffcdd2
    style High fill:#ffe0b2
    style Medium fill:#fff9c4
    style Low fill:#e8f5e9
```

## API Endpoints для работы с заявками

### Какие endpoints использовать на каждом этапе

```mermaid
graph TD
    Start[Работа с заявками] --> Create[Создание заявки]
    Create --> A1["POST /api/service-requests/"]
    
    Start --> View[Просмотр заявок]
    View --> B1["GET /api/service-requests/"]
    View --> B2["GET /api/requests-with-apartment/"]
    View --> B3["GET /api/requests-with-category/"]
    View --> B4["GET /api/request-detail/id/"]
    
    Start --> Manage[Управление заявками]
    Manage --> C1["POST /api/service-requests/id/assign_worker/"]
    Manage --> C2["POST /api/service-requests/id/change_status/"]
    Manage --> C3["POST /api/service-requests/id/add_comment/"]
    Manage --> C4["PATCH /api/request-detail/id/"]
    
    Start --> Special[Специальные endpoints]
    Special --> D1["GET /api/service-requests/my_requests/"]
    Special --> D2["GET /api/service-requests/assigned_to_me/"]
    
    classDef createStyle fill:#e1f5ff
    classDef viewStyle fill:#fff4e1
    classDef manageStyle fill:#e8f5e9
    classDef specialStyle fill:#f3e5f5
    
    class A1 createStyle
    class B1,B2,B3,B4 viewStyle
    class C1,C2,C3,C4 manageStyle
    class D1,D2 specialStyle
```

## Права доступа по статусам

### Кто может что делать в зависимости от статуса

```mermaid
graph TB
    subgraph Статус: new
        N1[Жилец: просмотр]
        N2[Диспетчер: все действия]
        N3[Мастер: нет доступа]
    end
    
    subgraph Статус: in_progress
        I1[Жилец: просмотр]
        I2[Диспетчер: все действия]
        I3[Мастер: изменение статуса, комментарии]
    end
    
    subgraph Статус: done
        D1[Жилец: просмотр]
        D2[Диспетчер: просмотр]
        D3[Мастер: просмотр]
    end
    
    subgraph Статус: canceled
        C1[Жилец: просмотр]
        C2[Диспетчер: просмотр]
        C3[Мастер: нет доступа]
    end
    
    style N2 fill:#4caf50
    style I2 fill:#4caf50
    style I3 fill:#ff9800
```

## Примеры использования

### Типичные сценарии

#### Сценарий 1: Жилец создает заявку

```mermaid
sequenceDiagram
    participant Ж as Жилец
    participant API as API
    participant БД as База данных
    
    Ж->>API: POST /api/service-requests/
    Note over Ж,API: {title, description, apartment_id, category_id}
    API->>БД: Создать ServiceRequest
    БД->>API: Заявка создана (status: new)
    API-->>Ж: 201 Created
```

#### Сценарий 2: Диспетчер назначает мастера

```mermaid
sequenceDiagram
    participant Д as Диспетчер
    participant API as API
    participant БД as База данных
    
    Д->>API: POST /api/service-requests/1/assign_worker/
    Note over Д,API: {worker_id: 3}
    API->>БД: Обновить ServiceRequest
    БД->>БД: Установить worker, assigned_at
    БД->>БД: Изменить status на in_progress
    БД->>API: Заявка обновлена
    API-->>Д: 200 OK
```

#### Сценарий 3: Мастер завершает работу

```mermaid
sequenceDiagram
    participant М as Мастер
    participant API as API
    participant БД as База данных
    
    М->>API: POST /api/service-requests/1/change_status/
    Note over М,API: {status: "done"}
    API->>БД: Обновить ServiceRequest
    БД->>БД: Установить resolved_at
    БД->>БД: Изменить status на done
    БД->>API: Заявка обновлена
    API-->>М: 200 OK
```

---

## Резюме

Все схемы выше показывают:

1. **Жизненный цикл заявки** - какие статусы существуют и как они меняются
2. **Процесс обработки** - полный workflow от создания до завершения
3. **Роли и действия** - кто что может делать
4. **Временная линия** - отслеживание дат событий
5. **Взаимодействие ролей** - последовательность действий
6. **Схема данных** - структура и связи
7. **Приоритеты** - обработка по важности
8. **API Endpoints** - какие endpoints использовать
9. **Права доступа** - кто может что делать по статусам
10. **Примеры** - типичные сценарии использования

Эти схемы помогут понять, как работает система обработки заявок в "ЖК Коннект".


