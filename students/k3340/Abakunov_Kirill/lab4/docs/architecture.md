# Архитектура приложения

## Общая структура

Приложение построено на основе Vue.js 3 с использованием Composition API и следует модульной архитектуре.

```
src/
├── api/           # Слой работы с API
├── plugins/       # Конфигурация плагинов
├── router/        # Маршрутизация
├── stores/        # Управление состоянием
├── views/         # Страницы приложения
├── App.vue        # Корневой компонент
└── main.js        # Точка входа
```

## Слой API

### api/index.js

Централизованный модуль для работы с REST API. Использует Axios с настроенными interceptors.

```javascript
// Автоматическое добавление токена к запросам
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

// Обработка ошибок авторизации
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Редирект на страницу входа
    }
    return Promise.reject(error)
  }
)
```

### API модули

- `authAPI` — авторизация, регистрация, профиль
- `roomsAPI` — CRUD номеров, свободные номера, история
- `guestsAPI` — CRUD гостей, заселение/выселение
- `staffAPI` — CRUD персонала, найм/увольнение
- `schedulesAPI` — CRUD расписаний уборки
- `reportsAPI` — квартальные отчёты

## Управление состоянием (Pinia)

### stores/auth.js

Хранит состояние авторизации пользователя.

**State:**
- `user` — данные текущего пользователя
- `token` — токен авторизации
- `loading` — состояние загрузки
- `error` — ошибки

**Actions:**
- `login(credentials)` — вход в систему
- `register(userData)` — регистрация
- `logout()` — выход
- `updateUser(data)` — обновление профиля
- `changePassword(data)` — смена пароля

## Маршрутизация (Vue Router)

### Защита маршрутов

```javascript
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login' })
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next({ name: 'Home' })
  } else {
    next()
  }
})
```

### Маршруты

| Путь | Компонент | Требует авторизации |
|------|-----------|---------------------|
| `/` | HomeView | Нет |
| `/login` | LoginView | Гостевой |
| `/register` | RegisterView | Гостевой |
| `/profile` | ProfileView | Да |
| `/rooms` | RoomsView | Нет |
| `/rooms/:id` | RoomDetailView | Нет |
| `/guests` | GuestsView | Нет |
| `/guests/:id` | GuestDetailView | Нет |
| `/staff` | StaffView | Нет |
| `/schedules` | SchedulesView | Нет |
| `/reports` | ReportsView | Да |

## UI Framework (Vuetify)

### Конфигурация темы

```javascript
export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1976D2',
          secondary: '#424242',
          // ...
        }
      }
    }
  }
})
```

### Используемые компоненты

- `v-app-bar` — верхняя панель навигации
- `v-navigation-drawer` — боковое меню
- `v-card` — карточки контента
- `v-data-table` — таблицы данных
- `v-form` — формы с валидацией
- `v-dialog` — модальные окна
- `v-snackbar` — уведомления

## Паттерны

### Provide/Inject для уведомлений

```javascript
// App.vue
const showSnackbar = (text, color) => {
  snackbar.text = text
  snackbar.color = color
  snackbar.show = true
}
provide('showSnackbar', showSnackbar)

// В компонентах
const showSnackbar = inject('showSnackbar')
showSnackbar('Успешно!', 'success')
```

### Реактивные формы

```javascript
const form = reactive({
  field1: '',
  field2: ''
})

const rules = {
  required: (v) => !!v || 'Обязательное поле'
}
```
