# Маршрутизация (Vue Router)

## Обзор

Маршрутизация реализована с помощью Vue Router 4. Конфигурация находится в `src/router/index.js`.

## Маршруты

### Публичные маршруты

#### `/login` - Страница входа

- **Компонент:** `LoginView.vue`
- **Мета:** `requiresGuest: true` - доступна только неавторизованным пользователям
- **Функциональность:**
  - Форма входа (email + пароль)
  - Валидация полей
  - Редирект на `/profile` после успешного входа
  - Ссылка на регистрацию

#### `/register` - Страница регистрации

- **Компонент:** `RegisterView.vue`
- **Мета:** `requiresGuest: true`
- **Функциональность:**
  - Форма регистрации (email, username, password, re_password)
  - Валидация полей
  - Автоматический вход после регистрации
  - Редирект на `/profile` после успешной регистрации
  - Ссылка на вход

### Защищенные маршруты

#### `/profile` - Профиль пользователя

- **Компонент:** `ProfileView.vue`
- **Мета:** `requiresAuth: true` - доступна только авторизованным пользователям
- **Функциональность:**
  - Просмотр профиля (display_name, bio, avatar, email, username)
  - Редактирование профиля (модальное окно)
  - Загрузка аватара
  - Отображение даты регистрации

#### `/settings` - Настройки аккаунта

- **Компонент:** `SettingsView.vue`
- **Мета:** `requiresAuth: true`
- **Функциональность:**
  - Вкладка "Аккаунт": изменение email и username
  - Вкладка "Пароль": изменение пароля
  - Валидация всех полей

### Служебные маршруты

#### `/` - Главная страница

- **Редирект:** на `/profile` (или `/login` если не авторизован)

## Гварды маршрутов (Route Guards)

### `beforeEach`

Глобальный guard, выполняющийся перед каждым переходом.

#### Логика работы:

1. **Для маршрутов с `requiresAuth: true`:**
   - Проверяет `authStore.isAuthenticated`
   - Если не авторизован:
     - Пытается восстановить сессию из localStorage (если есть токены)
     - Если восстановление не удалось - редирект на `/login` с параметром `redirect`
   - Если авторизован - разрешает переход

2. **Для маршрутов с `requiresGuest: true`:**
   - Если пользователь уже авторизован - редирект на `/profile`
   - Если не авторизован - разрешает переход

3. **Для остальных маршрутов:**
   - Разрешает переход без проверок

#### Пример кода:

```javascript
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      // Попытка восстановления сессии
      if (authStore.accessToken && authStore.refreshToken) {
        try {
          await authStore.loadUser()
          await authStore.loadProfile()
          if (authStore.isAuthenticated) {
            next()
            return
          }
        } catch (error) {
          authStore.logout()
        }
      }
      // Редирект на логин с сохранением целевого маршрута
      next({ name: 'login', query: { redirect: to.fullPath } })
      return
    }
    next()
    return
  }

  if (to.meta.requiresGuest) {
    if (authStore.isAuthenticated) {
      next({ name: 'profile' })
      return
    }
    next()
    return
  }

  next()
})
```

## Программная навигация

### После успешного входа

```javascript
// LoginView.vue
const result = await authStore.login(email.value, password.value)
if (result.success) {
  const redirect = route.query.redirect || '/profile'
  router.push(redirect)
}
```

### После выхода

```javascript
// App.vue
const handleLogout = () => {
  authStore.logout() // Внутри logout уже есть router.push('/login')
}
```

## История браузера

Используется `createWebHistory` для поддержки HTML5 History API:

```javascript
const router = createRouter({
  history: createWebHistory(),
  routes: [...]
})
```

Это позволяет использовать красивые URL без хэша (`/profile` вместо `/#/profile`).

## Динамические маршруты

В будущем можно добавить динамические маршруты, например:

```javascript
{
  path: '/users/:id',
  name: 'user-profile',
  component: () => import('@/views/UserProfileView.vue'),
  meta: { requiresAuth: true }
}
```

## Ленивая загрузка компонентов

Все компоненты маршрутов загружаются лениво (lazy loading) для оптимизации:

```javascript
component: () => import('@/views/LoginView.vue')
```

Это уменьшает размер начального бандла и ускоряет загрузку приложения.
