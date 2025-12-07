# Аутентификация

## Обзор

Приложение использует **Token-based аутентификацию** через Django REST Framework и Djoser. Токены хранятся в `localStorage` и автоматически добавляются к каждому API запросу.

## Архитектура

### Компоненты системы

1. **Auth Service** (`src/services/authService.js`) - методы для работы с API
2. **Auth Store** (`src/stores/auth.js`) - управление состоянием аутентификации
3. **Router Guards** (`src/router/index.js`) - защита маршрутов
4. **API Interceptors** (`src/services/api.js`) - автоматическое добавление токенов

## Процесс аутентификации

### Регистрация

1. Пользователь заполняет форму регистрации
2. Данные отправляются на `POST /api/auth/users/`
3. После успешной регистрации автоматически выполняется вход
4. Токен сохраняется в `localStorage`
5. Данные пользователя загружаются и сохраняются

```javascript
// В Register.vue
const result = await authStore.register(formData)
if (result.success) {
  // Автоматический вход выполнен
  this.$router.push('/')
}
```

### Вход

1. Пользователь вводит username и password
2. Данные отправляются на `POST /api/auth/token/login/`
3. Сервер возвращает `auth_token`
4. Токен сохраняется в `localStorage`
5. Загружаются данные пользователя через `GET /api/auth/users/me/`
6. Пользователь перенаправляется на главную страницу

```javascript
// В Login.vue
const result = await authStore.login(username, password)
if (result.success) {
  const redirect = this.$route.query.redirect || '/'
  this.$router.push(redirect)
}
```

### Выход

1. Отправляется запрос `POST /api/auth/token/logout/`
2. Токен удаляется из `localStorage`
3. Данные пользователя очищаются из store
4. Пользователь перенаправляется на страницу входа

```javascript
// В App.vue
async logout() {
  await authStore.logout()
  this.$router.push('/login')
}
```

## Хранение данных

### localStorage

- `auth_token` - токен авторизации
- `user` - JSON строка с данными пользователя

### Pinia Store

Состояние в `auth` store:

```javascript
{
  token: string | null,
  user: object | null,
  loading: boolean,
  error: string | null
}
```

## Защита маршрутов

Роутер автоматически проверяет статус аутентификации:

```javascript
router.beforeEach((to, from, next) => {
  const isAuthenticated = useAuthStore().isAuthenticated
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next({ name: 'Home' })
  } else {
    next()
  }
})
```

## Автоматическое добавление токена

API interceptor автоматически добавляет токен к каждому запросу:

```javascript
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})
```

## Обработка истечения токена

Если токен недействителен (401 ошибка):

1. Токен удаляется из `localStorage`
2. Данные пользователя очищаются
3. Пользователь перенаправляется на `/login`

```javascript
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

## Роли пользователей

Система поддерживает три роли:

- **resident** (Жилец) - основной пользователь
- **master** (Мастер) - специалист по обслуживанию
- **dispatcher** (Диспетчер) - администратор

Роль устанавливается при регистрации и не может быть изменена пользователем.

## Обновление профиля

Пользователь может обновить свои данные через `PATCH /api/auth/users/me/`:

```javascript
// В Profile.vue
const result = await authStore.updateProfile(formData)
if (result.success) {
  // Профиль обновлён, данные перезагружены
}
```

**Доступные поля для обновления:**
- email
- first_name
- last_name
- phone_number
- address
- birth_date

**Недоступные поля:**
- username (нельзя изменить)
- role (нельзя изменить)
- password (используйте отдельный метод)

## Смена пароля

Отдельный метод для смены пароля:

```javascript
// В Profile.vue
const result = await authStore.changePassword(
  currentPassword,
  newPassword
)
```

**Endpoint:** `POST /api/auth/users/set_password/`

**Требования:**
- Текущий пароль
- Новый пароль

## Проверка статуса аутентификации

В компонентах:

```javascript
import { useAuthStore } from '@/stores/auth'

export default {
  computed: {
    isAuthenticated() {
      return useAuthStore().isAuthenticated
    },
    user() {
      return useAuthStore().user
    },
    userRole() {
      return useAuthStore().userRole
    }
  }
}
```

## Обработка ошибок

### Ошибки входа/регистрации

Store возвращает объект с результатом:

```javascript
{
  success: boolean,
  error: string | null
}
```

Пример обработки:

```javascript
const result = await authStore.login(username, password)
if (!result.success) {
  this.errorMessage = result.error
}
```

### Валидация форм

Ошибки валидации отображаются под соответствующими полями:

```vue
<v-text-field
  v-model="username"
  :error-messages="errors.username"
></v-text-field>
```

## Безопасность

### Рекомендации

1. **HTTPS в production** - всегда используйте HTTPS для передачи токенов
2. **HttpOnly cookies** - рассмотрите использование cookies вместо localStorage (требует изменений на бэкенде)
3. **Таймаут токенов** - настройте автоматическое истечение токенов на бэкенде
4. **Refresh tokens** - для production рассмотрите использование refresh tokens

### Текущая реализация

- Токены хранятся в `localStorage` (доступны для JavaScript)
- Токены не имеют срока действия (настраивается на бэкенде)
- При 401 ошибке происходит автоматический logout

