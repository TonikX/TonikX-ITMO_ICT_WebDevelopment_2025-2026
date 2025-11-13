# Маршрутизация (Vue Router)

Настройка и использование Vue Router в приложении.

## Конфигурация Router

### Файл router/index.js

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Lazy loading компонентов
const Login = () => import('@/views/Login.vue')
const Dashboard = () => import('@/views/Dashboard.vue')
const ReadingRooms = () => import('@/views/ReadingRooms.vue')
const Readers = () => import('@/views/Readers.vue')
const Reservations = () => import('@/views/Reservations.vue')
const Librarians = () => import('@/views/Librarians.vue')
const Reports = () => import('@/views/Reports.vue')

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/reading-rooms',
    name: 'ReadingRooms',
    component: ReadingRooms,
    meta: { requiresAuth: true }
  },
  {
    path: '/readers',
    name: 'Readers',
    component: Readers,
    meta: { requiresAuth: true }
  },
  {
    path: '/reservations',
    name: 'Reservations',
    component: Reservations,
    meta: { requiresAuth: true }
  },
  {
    path: '/librarians',
    name: 'Librarians',
    component: Librarians,
    meta: { requiresAuth: true }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/')
  } else if (to.path === '/' && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
```

---

## Карта маршрутов

| Path | Component | Auth Required | Description |
|------|-----------|---------------|-------------|
| `/` | Login.vue | ❌ | Вход и регистрация |
| `/dashboard` | Dashboard.vue | ✅ | Главная панель |
| `/reading-rooms` | ReadingRooms.vue | ✅ | Управление залами |
| `/readers` | Readers.vue | ✅ | Управление читателями |
| `/reservations` | Reservations.vue | ✅ | Управление бронированиями |
| `/librarians` | Librarians.vue | ✅ | Управление библиотекарями |
| `/reports` | Reports.vue | ✅ | Отчеты |

---

## Navigation Guards

### Global Guard (beforeEach)

**Проверка аутентификации:**

```javascript
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Защищенный маршрут + не авторизован → редирект на /
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/')
  }
  // Публичный маршрут + авторизован → редирект на /dashboard
  else if (to.path === '/' && authStore.isAuthenticated) {
    next('/dashboard')
  }
  // Разрешить переход
  else {
    next()
  }
})
```

### Component Guard (beforeRouteEnter)

```javascript
// В компоненте
beforeRouteEnter(to, from, next) {
  // Выполнить до входа в компонент
  next(vm => {
    vm.loadData()
  })
}
```

### Component Guard (beforeRouteLeave)

```javascript
beforeRouteLeave(to, from, next) {
  // Подтверждение перед уходом
  if (this.hasUnsavedChanges) {
    const answer = confirm('Есть несохраненные изменения. Покинуть страницу?')
    if (answer) {
      next()
    } else {
      next(false)
    }
  } else {
    next()
  }
}
```

---

## Программная навигация

### router.push()

```javascript
import { useRouter } from 'vue-router'

const router = useRouter()

// По пути
router.push('/dashboard')

// По имени маршрута
router.push({ name: 'Dashboard' })

// С параметрами
router.push({
  name: 'ReadingRooms',
  query: { floor: 2 }
})
```

### router.replace()

Заменить текущую запись в истории:

```javascript
router.replace('/login')
```

### router.go()

```javascript
router.go(-1) // Назад
router.go(1)  // Вперед
```

---

## router-link

### Базовое использование

```vue
<router-link to="/dashboard">Dashboard</router-link>
```

### С именем маршрута

```vue
<router-link :to="{ name: 'Dashboard' }">
  Dashboard
</router-link>
```

### Active класс

```vue
<router-link
  to="/dashboard"
  active-class="active"
  exact-active-class="exact-active"
>
  Dashboard
</router-link>
```

---

## Параметры маршрута

### Query Parameters

**Передача:**
```javascript
router.push({
  path: '/reading-rooms',
  query: { floor: 2, type: 'small' }
})
// URL: /reading-rooms?floor=2&type=small
```

**Получение:**
```javascript
import { useRoute } from 'vue-router'

const route = useRoute()
const floor = route.query.floor    // '2'
const type = route.query.type      // 'small'
```

### Path Parameters

**Определение маршрута:**
```javascript
{
  path: '/reading-rooms/:id',
  component: ReadingRoomDetail
}
```

**Переход:**
```javascript
router.push({ name: 'RoomDetail', params: { id: 123 } })
```

**Получение:**
```javascript
const route = useRoute()
const id = route.params.id  // '123'
```

---

## Lazy Loading

### Преимущества

- Уменьшение размера начального bundle
- Быстрая загрузка приложения
- Загрузка компонентов по требованию

### Реализация

```javascript
// Вместо
import Dashboard from '@/views/Dashboard.vue'

// Используем
const Dashboard = () => import('@/views/Dashboard.vue')
```

### С комментариями webpack

```javascript
const Dashboard = () => import(
  /* webpackChunkName: "dashboard" */
  '@/views/Dashboard.vue'
)
```

---

## Redirect и Alias

### Redirect

```javascript
{
  path: '/home',
  redirect: '/dashboard'
}

// Или с функцией
{
  path: '/old-path/:id',
  redirect: to => {
    return { name: 'NewPath', params: { id: to.params.id } }
  }
}
```

### Alias

```javascript
{
  path: '/dashboard',
  component: Dashboard,
  alias: '/home'
}
// Оба /dashboard и /home откроют Dashboard
```

---

## Navigation в компонентах

### Composition API (setup)

```vue
<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const goToDashboard = () => {
  router.push('/dashboard')
}

const currentPath = route.path
</script>
```

### Options API

```vue
<script>
export default {
  methods: {
    goToDashboard() {
      this.$router.push('/dashboard')
    }
  },
  computed: {
    currentPath() {
      return this.$route.path
    }
  }
}
</script>
```

---

## Навигация в Vuetify

### v-list с router-link

```vue
<v-list>
  <v-list-item
    to="/dashboard"
    prepend-icon="mdi-view-dashboard"
  >
    <v-list-item-title>Dashboard</v-list-item-title>
  </v-list-item>
  
  <v-list-item
    to="/reading-rooms"
    prepend-icon="mdi-door"
  >
    <v-list-item-title>Читальные залы</v-list-item-title>
  </v-list-item>
</v-list>
```

### v-btn с router

```vue
<v-btn to="/dashboard">Dashboard</v-btn>

<!-- Или -->
<v-btn @click="router.push('/dashboard')">Dashboard</v-btn>
```

---

## Scroll Behavior

### Настройка

```javascript
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})
```

---

## 404 Not Found

### Catch-all маршрут

```javascript
{
  path: '/:pathMatch(.*)*',
  name: 'NotFound',
  component: () => import('@/views/NotFound.vue')
}
```

### Компонент NotFound.vue

```vue
<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" class="text-center">
        <h1>404</h1>
        <p>Страница не найдена</p>
        <v-btn to="/dashboard">На главную</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
```

---

## Best Practices

### 1. Именованные маршруты

```javascript
// ✅ Правильно
router.push({ name: 'Dashboard' })

// ❌ Неправильно
router.push('/dashboard')
```

### 2. Meta поля

```javascript
{
  path: '/admin',
  meta: {
    requiresAuth: true,
    requiresAdmin: true,
    title: 'Admin Panel'
  }
}
```

### 3. Navigation Guards

```javascript
// Используйте глобальные guards для общей логики
router.beforeEach((to, from, next) => {
  // Проверка аутентификации
  // Логирование
  // Analytics
  next()
})
```

---

## Отладка

### Vue DevTools

1. Откройте DevTools (F12)
2. Вкладка "Vue"
3. "Routing" - просмотр текущего маршрута

### Console Logging

```javascript
router.beforeEach((to, from, next) => {
  console.log('Navigating from:', from.path)
  console.log('Navigating to:', to.path)
  next()
})
```

---

## Следующие шаги

- [State Management (Pinia)](state.md)
- [API Integration](api-integration.md)
- [Компоненты](components.md)

