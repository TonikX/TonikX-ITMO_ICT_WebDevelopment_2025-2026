# Vue.js Frontend для Django REST Framework

Frontend приложение на Vue 3 для работы с Django REST Framework бэкендом, использующим Djoser для аутентификации.

## Технологии

- **Vue 3** (Composition API)
- **Vue Router** - маршрутизация
- **Pinia** - управление состоянием
- **Axios** - HTTP клиент
- **Vuetify 3** - UI компоненты
- **Vite** - сборщик проекта

## Установка

```bash
npm install
```

## Разработка

```bash
npm run dev
```

Приложение будет доступно по адресу `http://localhost:5173`

## Сборка для продакшена

```bash
npm run build
```

Собранные файлы будут в папке `dist/`

## Настройка

### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### Настройка CORS на бэкенде

Убедитесь, что в Django settings.py настроен CORS:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

## Структура проекта

```
src/
├── api/              # API модули
│   ├── axios.js      # Настройка Axios с interceptors
│   ├── auth.js       # API методы для аутентификации
│   └── profile.js    # API методы для профиля
├── stores/           # Pinia stores
│   └── authStore.js  # Store для аутентификации
├── router/           # Vue Router
│   └── index.js     # Конфигурация маршрутов
├── views/            # Страницы
│   ├── LoginView.vue
│   ├── RegisterView.vue
│   ├── ProfileView.vue
│   └── SettingsView.vue
├── plugins/          # Плагины
│   └── vuetify.js   # Конфигурация Vuetify
├── App.vue           # Главный компонент
└── main.js           # Точка входа
```

## Функциональность

### Аутентификация

- **Вход** (`/login`) - вход по email или username и паролю
- **Регистрация** (`/register`) - создание нового аккаунта
- **Профиль** (`/profile`) - просмотр и редактирование профиля
- **Настройки** (`/settings`) - изменение email, username, пароля

### Особенности

- Автоматическое добавление JWT токена к запросам
- Автоматическое обновление токена при истечении
- Защита маршрутов (только для авторизованных пользователей)
- Сохранение состояния в localStorage
- Адаптивный дизайн
- Валидация форм
- Уведомления через Snackbar

## API Endpoints

Приложение использует следующие endpoints бэкенда:

- `POST /auth/jwt/create/` - вход
- `POST /auth/users/` - регистрация
- `POST /auth/jwt/refresh/` - обновление токена
- `GET /auth/users/me/` - текущий пользователь
- `PATCH /auth/users/me/` - обновление пользователя
- `POST /auth/users/set_password/` - изменение пароля
- `GET /api/profile/` - профиль текущего пользователя
- `PATCH /api/profile/` - обновление профиля

## Документация

Подробная документация доступна в папке `docs/` (MkDocs).
