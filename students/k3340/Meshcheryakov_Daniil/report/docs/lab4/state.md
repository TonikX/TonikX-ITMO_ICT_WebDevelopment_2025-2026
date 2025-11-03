# State Management (Pinia)

Управление состоянием приложения с использованием Pinia.

## Что такое Pinia?

**Pinia** - официальное state management решение для Vue.js 3, замена Vuex.

### Преимущества

- ✅ Простой и интуитивный API
- ✅ TypeScript support из коробки
- ✅ Devtools интеграция
- ✅ Модульность
- ✅ Composition API first

---

## Установка и настройка

### main.js

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.mount('#app')
```

---

## Auth Store

### stores/auth.js

Основной store для управления аутентификацией.

```javascript
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  // State
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
  }),

  // Getters
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    currentUser: (state) => state.user,
  },

  // Actions
  actions: {
    // Вход
    async login(credentials) {
      try {
        const response = await axios.post(
          'http://localhost:8000/api/auth/jwt/create/',
          credentials
        )

        this.accessToken = response.data.access
        this.refreshToken = response.data.refresh

        // Сохранение в localStorage
        localStorage.setItem('access_token', this.accessToken)
        localStorage.setItem('refresh_token', this.refreshToken)

        // Получение данных пользователя
        await this.fetchUser()

        return { success: true }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data?.detail || 'Ошибка входа'
        }
      }
    },

    // Регистрация
    async register(userData) {
      try {
        await axios.post(
          'http://localhost:8000/api/auth/users/',
          userData
        )
        return { success: true }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data || 'Ошибка регистрации'
        }
      }
    },

    // Получение данных пользователя
    async fetchUser() {
      try {
        const response = await axios.get(
          'http://localhost:8000/api/auth/users/me/',
          {
            headers: {
              Authorization: `Bearer ${this.accessToken}`
            }
          }
        )
        this.user = response.data
      } catch (error) {
        console.error('Failed to fetch user:', error)
      }
    },

    // Обновление токена
    async refreshAccessToken() {
      try {
        const response = await axios.post(
          'http://localhost:8000/api/auth/jwt/refresh/',
          { refresh: this.refreshToken }
        )

        this.accessToken = response.data.access
        localStorage.setItem('access_token', this.accessToken)

        return true
      } catch (error) {
        this.logout()
        return false
      }
    },

    // Выход
    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },
  },
})
```

---

## Использование Store

### В компоненте (setup)

```vue
<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Доступ к state
console.log(authStore.user)
console.log(authStore.isAuthenticated)

// Вызов actions
const handleLogin = async () => {
  const result = await authStore.login({
    username: 'admin',
    password: 'admin123'
  })

  if (result.success) {
    console.log('Успешный вход!')
  }
}

const handleLogout = () => {
  authStore.logout()
}
</script>
```

### В Options API

```vue
<script>
import { mapState, mapActions } from 'pinia'
import { useAuthStore } from '@/stores/auth'

export default {
  computed: {
    ...mapState(useAuthStore, ['user', 'isAuthenticated'])
  },
  methods: {
    ...mapActions(useAuthStore, ['login', 'logout'])
  }
}
</script>
```

---

## Дополнительные Stores

### Пример: Reading Rooms Store

```javascript
// stores/readingRooms.js
import { defineStore } from 'pinia'
import api from '@/services/api'

export const useReadingRoomsStore = defineStore('readingRooms', {
  state: () => ({
    rooms: [],
    loading: false,
    error: null,
  }),

  getters: {
    getRoomById: (state) => (id) => {
      return state.rooms.find(room => room.id === id)
    },

    roomsByFloor: (state) => (floor) => {
      return state.rooms.filter(room => room.floor === floor)
    },

    totalRooms: (state) => state.rooms.length,
  },

  actions: {
    async fetchRooms() {
      this.loading = true
      try {
        const response = await api.get('/reading-rooms/')
        this.rooms = response.data
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async createRoom(roomData) {
      try {
        const response = await api.post('/reading-rooms/', roomData)
        this.rooms.push(response.data)
        return { success: true, data: response.data }
      } catch (error) {
        return { success: false, error: error.message }
      }
    },

    async updateRoom(id, roomData) {
      try {
        const response = await api.put(`/reading-rooms/${id}/`, roomData)
        const index = this.rooms.findIndex(r => r.id === id)
        if (index !== -1) {
          this.rooms[index] = response.data
        }
        return { success: true }
      } catch (error) {
        return { success: false, error: error.message }
      }
    },

    async deleteRoom(id) {
      try {
        await api.delete(`/reading-rooms/${id}/`)
        this.rooms = this.rooms.filter(r => r.id !== id)
        return { success: true }
      } catch (error) {
        return { success: false, error: error.message }
      }
    },
  },
})
```

---

## Composition Utilities

### storeToRefs

Сохраняет реактивность при деструктуризации:

```vue
<script setup>
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const { user, isAuthenticated } = storeToRefs(authStore)

// Теперь user и isAuthenticated реактивны!
</script>

<template>
  <div v-if="isAuthenticated">
    Welcome, {{ user.username }}!
  </div>
</template>
```

**Важно:**

```javascript
// ❌ Неправильно - теряется реактивность
const { user } = authStore

// ✅ Правильно - реактивность сохранена
const { user } = storeToRefs(authStore)

// ✅ Actions можно деструктурировать напрямую
const { login, logout } = authStore
```

---

## Plugins

### Persist State Plugin

Автоматическое сохранение state в localStorage:

```javascript
// plugins/persistState.js
export function persistStatePlugin({ store }) {
  // Восстановление из localStorage при загрузке
  const savedState = localStorage.getItem(`pinia-${store.$id}`)
  if (savedState) {
    store.$patch(JSON.parse(savedState))
  }

  // Сохранение при изменении state
  store.$subscribe((mutation, state) => {
    localStorage.setItem(
      `pinia-${store.$id}`,
      JSON.stringify(state)
    )
  })
}

// main.js
const pinia = createPinia()
pinia.use(persistStatePlugin)
```

---

## Devtools

### Просмотр состояния

1. Откройте Vue DevTools
2. Вкладка "Pinia"
3. Выберите store
4. Просмотр state, getters, actions

### Time Travel Debugging

- Просмотр истории изменений
- Возврат к предыдущему состоянию
- Replay actions

---

## Best Practices

### 1. Модульные Stores

```javascript
// ✅ Правильно - отдельный store для каждой сущности
stores/
  auth.js
  readingRooms.js
  readers.js
  reservations.js

// ❌ Неправильно - один огромный store
stores/
  index.js  // все в одном файле
```

### 2. Async Actions

```javascript
// ✅ Правильно
async fetchData() {
  this.loading = true
  try {
    const response = await api.get('/data/')
    this.data = response.data
  } catch (error) {
    this.error = error
  } finally {
    this.loading = false
  }
}
```

### 3. Immutability

```javascript
// ✅ Правильно
this.rooms = [...this.rooms, newRoom]

// ❌ Неправильно
this.rooms.push(newRoom)  // Работает, но менее предсказуемо
```

### 4. Error Handling

```javascript
async fetchData() {
  try {
    // ...
  } catch (error) {
    this.error = {
      message: error.message,
      code: error.response?.status,
      details: error.response?.data
    }
  }
}
```

---

## Тестирование

### Unit тест

```javascript
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should login successfully', async () => {
    const store = useAuthStore()
    const result = await store.login({
      username: 'test',
      password: 'test123'
    })

    expect(result.success).toBe(true)
    expect(store.isAuthenticated).toBe(true)
  })

  it('should logout', () => {
    const store = useAuthStore()
    store.accessToken = 'test-token'
    
    store.logout()
    
    expect(store.accessToken).toBe(null)
    expect(store.isAuthenticated).toBe(false)
  })
})
```

---

## Сравнение с Vuex

| Feature | Pinia | Vuex |
|---------|-------|------|
| API | Простой | Сложный |
| TypeScript | ✅ Отлично | ⚠️ Требует настройки |
| Mutations | ❌ Не нужны | ✅ Обязательны |
| Modules | ✅ Автоматически | ⚠️ Вручную |
| Composition API | ✅ Native | ⚠️ Helpers |
| Bundle Size | 📦 Меньше | 📦 Больше |

---

## Следующие шаги

- [API Integration](api-integration.md)
- [Компоненты](components.md)
- [Маршрутизация](routing.md)

