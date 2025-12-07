# Управление состоянием (Pinia)

## Обзор

Управление состоянием приложения реализовано с помощью Pinia - официальной библиотеки управления состоянием для Vue 3.

## Auth Store

Основной store для управления аутентификацией находится в `src/stores/authStore.js`.

### Состояние (State)

```javascript
{
  accessToken: null,      // JWT access токен
  refreshToken: null,      // JWT refresh токен
  user: null,             // Данные текущего пользователя
  profile: null,          // Профиль текущего пользователя
  isLoading: false,       // Флаг загрузки
}
```

### Геттеры (Getters)

#### `isAuthenticated`

Проверяет, авторизован ли пользователь.

```javascript
const authStore = useAuthStore()
if (authStore.isAuthenticated) {
  // Пользователь авторизован
}
```

#### `displayName`

Возвращает отображаемое имя пользователя (приоритет: display_name → username → email → 'Пользователь').

```javascript
const name = authStore.displayName
```

### Действия (Actions)

#### `login(usernameOrEmail, password)`

Вход пользователя в систему.

**Параметры:**
- `usernameOrEmail` (string) - Username или email пользователя
- `password` (string) - Пароль

**Возвращает:** `{ success: boolean, error?: string }`

**Пример:**
```javascript
const result = await authStore.login('user@example.com', 'password')
// или
const result = await authStore.login('username', 'password')
if (result.success) {
  // Успешный вход
} else {
  // Ошибка: result.error
}
```

После успешного входа автоматически:
- Сохраняются токены
- Загружаются данные пользователя
- Загружается профиль

#### `register(email, username, password, rePassword)`

Регистрация нового пользователя.

**Параметры:**
- `email` (string) - Email
- `username` (string, optional) - Имя пользователя
- `password` (string) - Пароль
- `rePassword` (string) - Подтверждение пароля

**Возвращает:** `{ success: boolean, error?: string }`

После успешной регистрации автоматически выполняется вход.

#### `refresh()`

Обновление JWT access токена.

**Возвращает:** `{ success: boolean }`

Вызывается автоматически через Axios interceptor при получении 401 ошибки.

#### `loadUser()`

Загрузка данных текущего пользователя.

**Возвращает:** Promise с данными пользователя

#### `loadProfile()`

Загрузка профиля текущего пользователя.

**Возвращает:** Promise с данными профиля

Если профиль не существует (404), возвращает `null` (это нормально).

#### `updateUser(userData)`

Обновление данных пользователя.

**Параметры:**
- `userData` (object) - Объект с полями для обновления (email, username)

**Возвращает:** `{ success: boolean, error?: string, data?: object }`

**Пример:**
```javascript
const result = await authStore.updateUser({
  email: 'newemail@example.com',
  username: 'newusername'
})
```

#### `logout()`

Выход пользователя из системы.

Очищает все данные аутентификации и перенаправляет на страницу входа.

## Персистентность

Store использует плагин `pinia-plugin-persistedstate` для сохранения состояния в localStorage.

**Сохранение:**
- `accessToken`
- `refreshToken`
- `user`
- `profile`

При перезагрузке страницы состояние автоматически восстанавливается из localStorage.

## Использование в компонентах

### Composition API

```vue
<script setup>
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()

// Использование геттеров
const isAuth = authStore.isAuthenticated
const name = authStore.displayName

// Вызов действий
const handleLogin = async () => {
  const result = await authStore.login(email.value, password.value)
  if (result.success) {
    // Успех
  }
}
</script>
```

### Options API

```vue
<script>
import { useAuthStore } from '@/stores/authStore'

export default {
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  computed: {
    isAuthenticated() {
      return this.authStore.isAuthenticated
    }
  }
}
</script>
```

## Интеграция с Router

Store интегрирован с Vue Router для защиты маршрутов:

```javascript
// router/index.js
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Пытаемся восстановить сессию
    if (authStore.accessToken) {
      await authStore.loadUser()
    }
    // Редирект на логин если не удалось
  }
})
```

## Интеграция с Axios

Store используется в Axios interceptors для автоматического добавления токенов и обработки ошибок:

```javascript
// api/axios.js
apiClient.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.accessToken) {
    config.headers.Authorization = `Bearer ${authStore.accessToken}`
  }
  return config
})
```
