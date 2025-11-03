# API Integration

Интеграция фронтенда с backend API через Axios.

## Конфигурация Axios

### services/api.js

Основной файл конфигурации HTTP клиента.

```javascript
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

// Создание instance
const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request Interceptor - добавление токена
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response Interceptor - обработка ошибок
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // 401 Unauthorized - обновление токена
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const authStore = useAuthStore()
      const success = await authStore.refreshAccessToken()

      if (success) {
        // Повтор оригинального запроса с новым токеном
        const token = localStorage.getItem('access_token')
        originalRequest.headers.Authorization = `Bearer ${token}`
        return api(originalRequest)
      }
    }

    return Promise.reject(error)
  }
)

export default api
```

---

## Использование в компонентах

### Базовый пример

```vue
<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const items = ref([])
const loading = ref(false)
const error = ref(null)

const fetchItems = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await api.get('/reading-rooms/')
    items.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка загрузки'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchItems()
})
</script>

<template>
  <div v-if="loading">Загрузка...</div>
  <div v-else-if="error">{{ error }}</div>
  <div v-else>
    <!-- Отображение items -->
  </div>
</template>
```

---

## CRUD операции

### Create (POST)

```javascript
const createRoom = async (roomData) => {
  try {
    const response = await api.post('/reading-rooms/', roomData)
    console.log('Created:', response.data)
    return { success: true, data: response.data }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data || 'Ошибка создания'
    }
  }
}

// Использование
const newRoom = {
  number: 101,
  floor: 1,
  room_type: 'small',
  capacity: 20,
  hourly_rate: '150.00',
  description: 'Тихий зал'
}

const result = await createRoom(newRoom)
if (result.success) {
  console.log('Зал создан!')
}
```

### Read (GET)

```javascript
// Список
const fetchRooms = async () => {
  const response = await api.get('/reading-rooms/')
  return response.data
}

// Детали
const fetchRoom = async (id) => {
  const response = await api.get(`/reading-rooms/${id}/`)
  return response.data
}

// С параметрами
const fetchFreeRooms = async (datetime) => {
  const response = await api.get('/reading-rooms/free/', {
    params: { on: datetime }
  })
  return response.data
}
```

### Update (PUT/PATCH)

```javascript
// Полное обновление (PUT)
const updateRoom = async (id, roomData) => {
  try {
    const response = await api.put(`/reading-rooms/${id}/`, roomData)
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: error.response?.data }
  }
}

// Частичное обновление (PATCH)
const patchRoom = async (id, updates) => {
  try {
    const response = await api.patch(`/reading-rooms/${id}/`, updates)
    return { success: true, data: response.data }
  } catch (error) {
    return { success: false, error: error.response?.data }
  }
}

// Использование
await patchRoom(1, { hourly_rate: '175.00' })
```

### Delete (DELETE)

```javascript
const deleteRoom = async (id) => {
  try {
    await api.delete(`/reading-rooms/${id}/`)
    return { success: true }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data || 'Ошибка удаления'
    }
  }
}
```

---

## Обработка ошибок

### Типы ошибок

```javascript
try {
  const response = await api.get('/reading-rooms/')
} catch (error) {
  // Network error
  if (!error.response) {
    console.error('Network error:', error.message)
  }
  
  // HTTP error
  else {
    const status = error.response.status
    const data = error.response.data
    
    switch (status) {
      case 400:
        console.error('Bad Request:', data)
        break
      case 401:
        console.error('Unauthorized')
        break
      case 403:
        console.error('Forbidden')
        break
      case 404:
        console.error('Not Found')
        break
      case 500:
        console.error('Server Error')
        break
      default:
        console.error('Error:', status, data)
    }
  }
}
```

### Centralized Error Handler

```javascript
// services/errorHandler.js
export const handleApiError = (error) => {
  if (!error.response) {
    return 'Ошибка сети. Проверьте подключение к интернету.'
  }

  const status = error.response.status
  const data = error.response.data

  switch (status) {
    case 400:
      return data.detail || 'Неверные данные'
    case 401:
      return 'Требуется авторизация'
    case 403:
      return 'Доступ запрещен'
    case 404:
      return 'Ресурс не найден'
    case 500:
      return 'Ошибка сервера. Попробуйте позже.'
    default:
      return data.detail || 'Произошла ошибка'
  }
}

// Использование
import { handleApiError } from '@/services/errorHandler'

try {
  await api.get('/reading-rooms/')
} catch (error) {
  errorMessage.value = handleApiError(error)
}
```

---

## API Service Layer

### Организация кода

Создайте отдельный сервис для каждой сущности:

```javascript
// services/readingRoomsService.js
import api from './api'

export const readingRoomsService = {
  // Список залов
  getAll() {
    return api.get('/reading-rooms/')
  },

  // Детали зала
  getById(id) {
    return api.get(`/reading-rooms/${id}/`)
  },

  // Создание
  create(data) {
    return api.post('/reading-rooms/', data)
  },

  // Обновление
  update(id, data) {
    return api.put(`/reading-rooms/${id}/`, data)
  },

  // Частичное обновление
  patch(id, data) {
    return api.patch(`/reading-rooms/${id}/`, data)
  },

  // Удаление
  delete(id) {
    return api.delete(`/reading-rooms/${id}/`)
  },

  // Custom endpoints
  getFree(datetime) {
    return api.get('/reading-rooms/free/', {
      params: { on: datetime }
    })
  },

  getReaders(id, start, end) {
    return api.get(`/reading-rooms/${id}/readers/`, {
      params: { start, end }
    })
  },
}
```

### Использование в компоненте

```vue
<script setup>
import { readingRoomsService } from '@/services/readingRoomsService'

const loadRooms = async () => {
  try {
    const response = await readingRoomsService.getAll()
    rooms.value = response.data
  } catch (error) {
    console.error(error)
  }
}

const loadFreeRooms = async (datetime) => {
  const response = await readingRoomsService.getFree(datetime)
  freeRooms.value = response.data
}
</script>
```

---

## Loading States

### Управление состоянием загрузки

```vue
<script setup>
import { ref } from 'vue'

const loading = ref(false)
const data = ref([])

const loadData = async () => {
  loading.value = true
  try {
    const response = await api.get('/data/')
    data.value = response.data
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-btn @click="loadData" :loading="loading">
    Загрузить
  </v-btn>
  
  <v-progress-circular v-if="loading" indeterminate />
  
  <div v-else>
    <!-- Данные -->
  </div>
</template>
```

---

## Composables

### useApi Composable

```javascript
// composables/useApi.js
import { ref } from 'vue'
import api from '@/services/api'

export function useApi() {
  const loading = ref(false)
  const error = ref(null)

  const execute = async (apiCall) => {
    loading.value = true
    error.value = null

    try {
      const response = await apiCall()
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  return { loading, error, execute }
}
```

### Использование

```vue
<script setup>
import { ref } from 'vue'
import { useApi } from '@/composables/useApi'
import api from '@/services/api'

const rooms = ref([])
const { loading, error, execute } = useApi()

const loadRooms = async () => {
  const result = await execute(() => api.get('/reading-rooms/'))
  if (result.success) {
    rooms.value = result.data
  }
}
</script>

<template>
  <v-progress-circular v-if="loading" />
  <v-alert v-if="error" type="error">{{ error }}</v-alert>
  <v-data-table v-else :items="rooms" />
</template>
```

---

## FormData для файлов

### Загрузка файлов

```javascript
const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('name', 'Document')

  try {
    const response = await api.post('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        const progress = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        )
        console.log(`Upload progress: ${progress}%`)
      }
    })
    
    return response.data
  } catch (error) {
    console.error('Upload failed:', error)
  }
}
```

---

## Cancellation Tokens

### Отмена запросов

```javascript
import { ref, onUnmounted } from 'vue'
import axios from 'axios'

const controller = new AbortController()

const loadData = async () => {
  try {
    const response = await api.get('/data/', {
      signal: controller.signal
    })
    data.value = response.data
  } catch (error) {
    if (axios.isCancel(error)) {
      console.log('Request cancelled')
    }
  }
}

// Отмена при размонтировании
onUnmounted(() => {
  controller.abort()
})
```

---

## Retry Logic

### Автоматический retry при ошибках

```javascript
const apiWithRetry = async (apiCall, maxRetries = 3) => {
  let lastError

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await apiCall()
    } catch (error) {
      lastError = error
      
      // Не retry для клиентских ошибок
      if (error.response?.status < 500) {
        throw error
      }
      
      // Ждем перед retry
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)))
    }
  }

  throw lastError
}

// Использование
const data = await apiWithRetry(() => api.get('/data/'))
```

---

## Environment Variables

### Конфигурация URL

```javascript
// .env.development
VITE_API_BASE_URL=http://localhost:8000/api/

// .env.production
VITE_API_BASE_URL=https://api.production.com/api/
```

```javascript
// services/api.js
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  // ...
})
```

---

## Best Practices

### 1. Используйте Service Layer

```javascript
// ✅ Правильно
import { roomsService } from '@/services/roomsService'
const rooms = await roomsService.getAll()

// ❌ Неправильно
const rooms = await api.get('/reading-rooms/')
```

### 2. Обрабатывайте все ошибки

```javascript
// ✅ Правильно
try {
  const data = await api.get('/data/')
} catch (error) {
  handleError(error)
}

// ❌ Неправильно
const data = await api.get('/data/')  // Может упасть
```

### 3. Используйте async/await

```javascript
// ✅ Правильно
const data = await api.get('/data/')

// ❌ Неправильно
api.get('/data/').then(r => data.value = r.data)
```

### 4. Типизация (если используете TypeScript)

```typescript
interface Room {
  id: number
  number: number
  floor: number
  // ...
}

const rooms = ref<Room[]>([])
```

---

## Debugging

### Логирование запросов

```javascript
api.interceptors.request.use(config => {
  console.log('Request:', config.method?.toUpperCase(), config.url)
  console.log('Data:', config.data)
  return config
})

api.interceptors.response.use(response => {
  console.log('Response:', response.status, response.data)
  return response
})
```

### Network Tab

1. Откройте DevTools (F12)
2. Вкладка "Network"
3. Фильтр "XHR"
4. Просмотр всех API запросов

---

## Заключение

API интеграция настроена и готова к использованию! 🎉

### Полный стек технологий:

- ✅ **Vue.js 3** - фронтенд фреймворк
- ✅ **Vuetify 3** - UI компоненты
- ✅ **Pinia** - state management
- ✅ **Vue Router** - маршрутизация
- ✅ **Axios** - HTTP клиент
- ✅ **Django + DRF** - backend API
- ✅ **JWT** - аутентификация

---

## Навигация по документации

- [Главная Lab 4](index.md)
- [Установка](installation.md)
- [Компоненты](components.md)
- [Маршрутизация](routing.md)
- [State Management](state.md)

---

**Студент:** Мещеряков Даниил  
**Группа:** K3340  
**Курс:** Web-программирование  
**Университет:** ИТМО

