# Роутинг

## Обзор

Приложение использует **Vue Router 4** для навигации между страницами. Роутер настроен с защитой маршрутов на основе статуса аутентификации.

## Конфигурация

Файл конфигурации: `src/router/index.js`

### Маршруты

| Путь | Компонент | Описание | Требования |
|------|-----------|----------|------------|
| `/` | `Home.vue` | Главная страница | Аутентификация |
| `/login` | `Login.vue` | Страница входа | Гость |
| `/register` | `Register.vue` | Страница регистрации | Гость |
| `/profile` | `Profile.vue` | Профиль пользователя | Аутентификация |

## Защита маршрутов

Роутер использует навигационные guards для защиты маршрутов:

```javascript
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated

  if (to.meta.requiresAuth && !isAuthenticated) {
    // Редирект на логин, если требуется аутентификация
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresGuest && isAuthenticated) {
    // Редирект на главную, если пользователь уже авторизован
    next({ name: 'Home' })
  } else {
    next()
  }
})
```

### Мета-поля маршрутов

- `requiresAuth: true` - маршрут доступен только авторизованным пользователям
- `requiresGuest: true` - маршрут доступен только неавторизованным пользователям

## Навигация

### Программная навигация

Использование в компонентах:

```javascript
// Переход на другую страницу
this.$router.push('/profile')

// Переход с параметрами
this.$router.push({ name: 'Profile' })

// Переход с сохранением истории
this.$router.push({ path: '/login', query: { redirect: '/profile' } })
```

### Навигация через шаблоны

Использование `router-link`:

```vue
<router-link to="/profile">Профиль</router-link>
```

Или через Vuetify компоненты:

```vue
<v-btn to="/profile">Профиль</v-btn>
```

## Редиректы

### После входа

После успешного входа пользователь перенаправляется:
- На страницу, указанную в `redirect` query параметре
- Или на главную страницу (`/`)

Пример:
```javascript
// В Login.vue после успешного входа
const redirect = this.$route.query.redirect || '/'
this.$router.push(redirect)
```

### Защищённые маршруты

Если неавторизованный пользователь пытается зайти на защищённый маршрут:
1. Сохраняется исходный путь в `redirect` параметре
2. Происходит редирект на `/login`
3. После входа пользователь возвращается на исходную страницу

## История навигации

Роутер использует `createWebHistory()` для HTML5 History API:

```javascript
const router = createRouter({
  history: createWebHistory(),
  routes,
})
```

Это означает:
- Чистые URL без `#`
- Поддержка браузерной истории (кнопки назад/вперёд)
- Требуется настройка сервера для production (fallback на `index.html`)

## Добавление нового маршрута

1. Создайте компонент view в `src/views/`
2. Добавьте маршрут в `src/router/index.js`:

```javascript
{
  path: '/new-page',
  name: 'NewPage',
  component: () => import('@/views/NewPage.vue'),
  meta: { requiresAuth: true }, // опционально
}
```

3. Используйте в навигации:

```vue
<v-btn to="/new-page">Новая страница</v-btn>
```

## Динамические маршруты

Для маршрутов с параметрами:

```javascript
{
  path: '/apartment/:id',
  name: 'Apartment',
  component: () => import('@/views/Apartment.vue'),
}
```

Доступ к параметру в компоненте:

```javascript
this.$route.params.id
```

## Query параметры

Использование query параметров:

```javascript
// Переход с query параметрами
this.$router.push({ 
  path: '/search', 
  query: { q: 'apartment' } 
})

// Чтение query параметров
this.$route.query.q
```

