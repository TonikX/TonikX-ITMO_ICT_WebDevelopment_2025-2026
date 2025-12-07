# ЖК Коннект - Frontend

Веб-приложение для управления жилым комплексом, разработанное на Vue.js 3 с использованием Vuetify.

## Технологии

- **Vue.js 3** - прогрессивный JavaScript фреймворк
- **Vuetify 3** - Material Design компоненты для Vue.js
- **Vue Router 4** - официальный роутер для Vue.js
- **Pinia** - стейт-менеджер для Vue.js
- **Axios** - HTTP клиент для работы с API
- **Vite** - инструмент сборки

## Установка

1. Установите зависимости:
```bash
npm install
```

2. Создайте файл `.env` (опционально) для настройки API:
```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

3. Запустите сервер разработки:
```bash
npm run dev
```

Приложение будет доступно по адресу `http://localhost:5173`

## Сборка для production

```bash
npm run build
```

Собранные файлы будут в папке `dist/`

## Структура проекта

```
src/
├── assets/          # Статические ресурсы (CSS, изображения)
├── components/       # Переиспользуемые компоненты
│   ├── CategorySelect.vue
│   ├── ApartmentSelect.vue
│   ├── BuildingSelect.vue
│   ├── WorkerSelect.vue
│   ├── StatusChip.vue
│   ├── PriorityChip.vue
│   ├── StatisticsCard.vue
│   └── DataTable.vue
├── plugins/         # Плагины (Vuetify)
├── router/          # Конфигурация роутера
├── services/        # API сервисы
│   ├── api.js
│   ├── authService.js
│   ├── buildingsService.js
│   ├── apartmentsService.js
│   ├── categoriesService.js
│   ├── serviceRequestsService.js
│   └── meterReadingsService.js
├── stores/          # Pinia stores (состояние приложения)
│   └── auth.js
├── utils/           # Утилиты
│   ├── roleUtils.js
│   ├── dateUtils.js
│   └── statusUtils.js
├── views/           # Страницы приложения
│   ├── Home.vue
│   ├── Login.vue
│   ├── Register.vue
│   ├── Profile.vue
│   ├── ServiceRequestsList.vue
│   ├── ServiceRequestForm.vue
│   ├── ServiceRequestDetail.vue
│   ├── MyRequests.vue
│   ├── AssignedRequests.vue
│   ├── ServiceRequestsStatistics.vue
│   ├── MeterReadingsList.vue
│   ├── MeterReadingForm.vue
│   ├── MeterReadingDetail.vue
│   ├── MeterReadingsStatistics.vue
│   ├── ApartmentsList.vue
│   ├── ApartmentForm.vue
│   ├── ApartmentDetail.vue
│   ├── BuildingsList.vue
│   ├── BuildingForm.vue
│   ├── BuildingDetail.vue
│   └── BuildingsStatistics.vue
├── App.vue          # Корневой компонент
└── main.js          # Точка входа
```

## Функциональность

### Аутентификация
- **Вход** (`/login`) - авторизация пользователя
- **Регистрация** (`/register`) - создание нового аккаунта
- **Профиль** (`/profile`) - просмотр и редактирование данных пользователя
- **Смена пароля** - изменение пароля в профиле

### Заявки на обслуживание
- Список заявок с фильтрацией и поиском
- Создание заявок
- Детальная информация с возможностью управления
- Мои заявки (для жильца)
- Назначенные мне (для мастера)
- Статистика по заявкам

### Показания счетчиков
- Подача показаний
- Просмотр истории показаний
- Статистика потребления

### Квартиры
- Просмотр квартир (для жильцов - только свои)
- Создание и редактирование (для диспетчера)
- Детальная информация

### Дома (только для диспетчера)
- Управление домами
- Статистика по домам и квартирам

### Dashboard
- Виджеты со статистикой
- Быстрые действия
- Последние заявки/показания

## Роли пользователей
- **Жилец** (`resident`) - основной пользователь системы
- **Мастер** (`master`) - специалист по обслуживанию
- **Диспетчер** (`dispatcher`) - администратор системы

## API Интеграция

Приложение взаимодействует с Django REST Framework бэкендом через следующие эндпоинты:

- `POST /api/auth/users/` - регистрация
- `POST /api/auth/token/login/` - вход
- `POST /api/auth/token/logout/` - выход
- `GET /api/auth/users/me/` - получение текущего пользователя
- `PATCH /api/auth/users/me/` - обновление профиля
- `POST /api/auth/users/set_password/` - смена пароля
- И многие другие эндпоинты для работы с заявками, показаниями, квартирами и домами

## Документация

Подробная документация доступна в папке `docs/`. Для просмотра:

```bash
# Используя mkdocs из виртуального окружения бэкенда
/путь/к/Lr3/ResidentalConnect/venv/bin/mkdocs serve --dev-addr=127.0.0.1:8001
```

Документация будет доступна по адресу `http://127.0.0.1:8001`

## Разработка

### Добавление новых компонентов

1. Создайте компонент в `src/components/`
2. Импортируйте и используйте в нужном view

### Добавление новых страниц

1. Создайте view в `src/views/`
2. Добавьте маршрут в `src/router/index.js`

### Работа с API

Используйте сервисы из `src/services/` для взаимодействия с бэкендом.

## Лицензия

Проект создан в рамках учебной программы.
