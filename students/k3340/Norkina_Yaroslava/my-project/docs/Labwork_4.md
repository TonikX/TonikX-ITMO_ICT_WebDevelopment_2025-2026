# Лабораторная работа 4. ДОКУМЕНТАЦИЯ ПРОЕКТА
## Сайт для продвижения личного бренда

**Цель работы:** Овладеть практическими навыками разработки клиентской части веб-приложений на базе фреймворка Vue 3. Настроить взаимодействие с серверной частью (Django REST Framework), реализовать динамический интерфейс с использованием библиотеки компонентов Vuetify, настроить систему роутинга и авторизации по токенам.

### Фронтенд-часть (Vue.js 3)
Frontend часть системы представляет собой современное одностраничное приложение (SPA) для управления сайтом для продвижения личного бренда. Приложение построено на Vue.js 3 с использованием Composition API и Vuetify 3 для создания профессионального пользовательского интерфейса. Система разделена на две части: публичный интерфейс для клиентов и административную панель для сотрудников компании.

---

## Обзор архитектуры фронтенда

Проект реализован по архитектуре **разделённого фронтенда и бэкенда** (decoupled frontend):

```
brand_manager/          # Бэкенд (Django)
├── brand_manager/      # Основной пакет Django
├── manager_services/   # Приложение с моделями и API
└── ...

frontend/               # Фронтенд (Vue.js)
├── brand_app/          # SPA приложение на Vue 3
│   ├── public/         # Статические файлы
│   ├── src/
│   │   ├── assets/     # Изображения, стили
│   │   ├── components/ # Переиспользуемые компоненты
│   │   ├── router/     # Настройка маршрутизации
│   │   ├── store/      # Vuex хранилище
│   │   ├── views/      # Страницы приложения
│   │   ├── App.vue     # Корневой компонент
│   │   └── main.js     # Точка входа
│   ├── package.json    # Зависимости фронтенда
│   └── vite.config.js  # Конфигурация сборки
└── ...
```

**Принцип работы:**
- Фронтенд — полностью независимое SPA-приложение на Vue.js
- Бэкенд предоставляет REST API через Django REST Framework
- Аутентификация реализована через JWT токены (Djoser + SimpleJWT)
- Все запросы к бэкенду выполняются через `axios`
- CORS настроен для разрешения кросс-доменных запросов

---

## Технологический стек

| Компонент | Технология | Версия |
|-----------|------------|--------|
| Фронтенд фреймворк | Vue.js | 3.x |
| Маршрутизация | Vue Router | 4.x |
| Управление состоянием | Vuex | 4.x |
| HTTP клиент | Axios | 1.x |
| UI компоненты | Vuetify | 3.x |
| Сборка | Vite | 4.x |
| Бэкенд | Django | 6.0 |
| REST Framework | Django REST Framework | 3.14 |
| Аутентификация | Djoser + SimpleJWT | 2.2 + 5.3 |

---
# Ход выполнения работы

---

## Установка и настройка проекта

### Установка зависимостей фронтенда

```bash
# Папка фронтенда
cd frontend/brand_app

# Установка зависимостей
npm install
# или
yarn install
```

**Содержимое `package.json`:**
```json
{
  "name": "brand-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.6.0",
    "vue": "^3.3.0",
    "vue-router": "^4.2.0",
    "vuex": "^4.1.0",
    "vuetify": "^3.3.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.2.0",
    "vite": "^4.4.0"
  }
}
```

### Шаг 2: Настройка прокси для разработки

Создан файл `vite.config.js` для настройки прокси к бэкенду:

```javascript
import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  }, // changed by author
   server: {
    port: 8080,
    proxy: {
      '/media': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false
      }
    }
  } // to this
})
```

### Настройка бэкенда для CORS

В `brand_manager/settings.py` настроены следующие параметры:

```python
# Установка пакета
pip install django-cors-headers

# settings.py
INSTALLED_APPS = [
    # ...
    'corsheaders',
    # ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ← Должен быть первым!
    # ...
]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:8080',
    'http://127.0.0.1:8080',
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
    'x-csrftoken',
    'accept',
    'origin',
    'user-agent',
]
```

---

## Структура проекта фронтенда

```
frontend/brand_app/
├── public/
│   └── index.html              # HTML шаблон
├── src/
│   ├── assets/
│   │   └── logo.png            # Логотип и другие ресурсы
│   ├── components/
│   │   └── ...                 # Переиспользуемые компоненты (опционально)
│   ├── router/
│   │   └── index.js            # Настройка маршрутизации
│   ├── store/
│   │   ├── index.js            # Vuex хранилище
│   │   └── modules/
│   │       └── auth.js         # Модуль аутентификации
│   ├── views/
│   │   ├── HomeView.vue        # Главная страница
│   │   ├── LoginView.vue       # Страница входа
│   │   ├── RegisterView.vue    # Страница регистрации
│   │   ├── ServicesView.vue    # Список услуг
│   │   ├── ServiceDetailView.vue # Детали услуги
│   │   ├── CreateOrderView.vue # Создание заявки
│   │   ├── ProfileView.vue     # Личный кабинет
│   │   ├── OrdersView.vue      # Мои заявки
│   │   ├── AdminServicesView.vue # Управление услугами (админ)
│   │   ├── AdminServiceDetailView.vue # Детали услуги (админ)
│   │   ├── AdminServiceEditView.vue # Редактирование услуги (админ)
│   │   ├── AdminOrdersView.vue # Управление заявками (админ)
│   │   └── AdminReviewsView.vue # Управление отзывами (админ)
│   ├── App.vue                 # Корневой компонент
│   └── main.js                 # Точка входа приложения
├── package.json
├── vite.config.js
└── README.md
```

---

## Настройка маршрутизации (Vue Router)

### Файл: `src/router/index.js`

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

// Импорт всех страниц
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ServicesView from '../views/ServicesView.vue'
import ProfileView from '../views/ProfileView.vue'
import ServiceDetailView from '../views/ServiceDetailView.vue'
import CreateOrderView from '../views/CreateOrderView.vue'
import AdminServicesView from '../views/AdminServicesView.vue'
import AdminServiceDetailView from '../views/AdminServiceDetailView.vue'
import AdminServiceEditView from '../views/AdminServiceEditView.vue'
import AdminOrdersView from '../views/AdminOrdersView.vue'
import AdminReviewsView from '../views/AdminReviewsView.vue'
import OrdersView from '../views/OrdersView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/services',
    name: 'Services',
    component: ServicesView
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { guestOnly: true }  // Только для неавторизованных
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: { guestOnly: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: true }  // Требует авторизации
  },
  {
    path: '/services/:id',
    name: 'ServiceDetail',
    component: ServiceDetailView,
    meta: { title: 'Детали услуги' }
  },
  {
    path: '/orders/new',
    name: 'CreateOrder',
    component: CreateOrderView,
    meta: {
      title: 'Новая заявка',
      requiresAuth: true
    }
  },
  {
    path: '/admin/services',
    name: 'AdminServices',
    component: AdminServicesView,
    meta: {
      title: 'Управление услугами',
      requiresAuth: true,
      requiresAdmin: true  // Требует прав администратора
    }
  },
  {
    path: '/admin/services/new',
    name: 'AdminServiceCreate',
    component: AdminServiceEditView,
    meta: {
      title: 'Новая услуга',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/admin/services/:id',
    name: 'AdminServiceDetail',
    component: AdminServiceDetailView,
    meta: {
      title: 'Детали услуги',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/admin/services/:id/edit',
    name: 'AdminServiceEdit',
    component: AdminServiceEditView,
    meta: {
      title: 'Редактирование услуги',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/admin/orders',
    name: 'AdminOrders',
    component: AdminOrdersView,
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/admin/reviews',
    name: 'AdminReviews',
    component: AdminReviewsView,
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/orders',
    name: 'Orders',
    component: OrdersView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Навигационная охрана (Navigation Guards)
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.auth.token
  const user = store.state.auth.user
  const isAdmin = user?.role === 'admin' || user?.is_staff === true

  // Если маршрут только для гостей (неавторизованных)
  if (to.meta.guestOnly && isAuthenticated) {
    next('/')
    return
  }

  // Если маршрут требует авторизации
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }

  // Если маршрут требует админских прав
  if (to.meta.requiresAdmin && (!isAuthenticated || !isAdmin)) {
    next('/')
    return
  }

  next()
})

export default router
```

### Ключевые особенности маршрутизации:

| Фича | Описание |
|------|----------|
| **Мета-поля** | `guestOnly`, `requiresAuth`, `requiresAdmin` для контроля доступа |
| **Динамические параметры** | `:id` для передачи ID сущности (услуга, заявка) |
| **Навигационные гарды** | Проверка авторизации перед переходом на защищённые маршруты |
| **Ленивая загрузка** | Возможность подключения через `() => import(...)` для оптимизации |

---
## Подключен плагин vuetify

### Файл: `src\plugins\vuetify.js`
```javascript
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'


// Пастельные цвета
const lightTheme = {
    dark: false,
    colors: {
        primary: '#2f6aff',
        secondary: '#00cc66',
        accent: '#FFB6C1',
        success: '#77DD77',
        error: '#FF6961',
        warning: '#FFD700',
        info: '#84B6F4',
        background: '#F9F9F9',
        surface: '#FFFFFF',
    }
}


export default createVuetify({
    components,
    directives,
    theme: {
        defaultTheme: 'lightTheme',
        themes: {
            lightTheme,
        }
    },
    defaults: {
        VBtn: {
            color: 'primary',
            variant: 'flat',
            rounded: 'lg'
        },
        VCard: {
            rounded: 'lg',
            elevation: 2
        },
        VTextField: {
            variant: 'outlined',
            density: 'comfortable'
        }
    }
})

```

---

## Управление состоянием (Vuex/Store)

### Файл: `src/store/modules/auth.js`

```javascript
import axios from 'axios'

const API_URL = '/auth'  // Проксируется через Vite к бэкенду

export default {
  namespaced: true,
  state: {
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
    isLoading: false,
    error: null
  },
  getters: {
    isAuthenticated: state => !!state.token,
    isAdmin: state => state.user?.role === 'admin' || state.user?.is_staff === true,
    userName: state => state.user ? `${state.user.first_name} ${state.user.last_name}`.trim() : state.user?.username || 'Пользователь',
    userData: state => state.user,
    isLoading: state => state.isLoading,
    authError: state => state.error
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      localStorage.setItem('token', token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    },
    SET_USER(state, user) {
      state.user = user
      localStorage.setItem('user', JSON.stringify(user))
    },
    CLEAR_AUTH(state) {
      state.token = null
      state.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      delete axios.defaults.headers.common['Authorization']
    },
    SET_LOADING(state, status) {
      state.isLoading = status
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    CLEAR_ERROR(state) {
      state.error = null
    }
  },
  actions: {
    async login({ commit }, credentials) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        // Получение токена
        const response = await axios.post(`${API_URL}/jwt/create/`, {
          username: credentials.email,  // В проекте используется username вместо email
          password: credentials.password
        })
        
        const { access, refresh } = response.data
        commit('SET_TOKEN', access)
        
        // Получение данных пользователя
        const userResponse = await axios.get(`${API_URL}/users/me/`)
        commit('SET_USER', userResponse.data)
        
        return { success: true }
      } catch (error) {
        commit('SET_ERROR', error.response?.data || { detail: 'Ошибка авторизации' })
        return { success: false, error: error.response?.data }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async register({ commit }, userData) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        const response = await axios.post(`${API_URL}/users/`, userData)
        return { success: true, user: response.data }
      } catch (error) {
        commit('SET_ERROR', error.response?.data)
        return { success: false, error: error.response?.data }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async logout({ commit }) {
      commit('CLEAR_AUTH')
    },
    
    async updateProfile({ commit, state }, userData) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        const response = await axios.patch(`${API_URL}/users/${state.user.id}/`, userData)
        commit('SET_USER', response.data)
        return { success: true }
      } catch (error) {
        commit('SET_ERROR', error.response?.data)
        return { success: false, error: error.response?.data }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // Автоматическая установка токена при инициализации приложения
    initAuth({ commit }) {
      const token = localStorage.getItem('token')
      const user = localStorage.getItem('user')
      
      if (token) {
        commit('SET_TOKEN', token)
      }
      
      if (user) {
        commit('SET_USER', JSON.parse(user))
      }
    }
  }
}
```

### Файл: `src/store/index.js`

```javascript
import { createStore } from 'vuex'
import auth from './modules/auth'

export default createStore({
  modules: {
    auth
  }
})
```

### Использование в компонентах:

```vue
<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  computed: {
    ...mapGetters('auth', ['isAuthenticated', 'isAdmin', 'userName', 'userData', 'isLoading', 'authError'])
  },
  methods: {
    ...mapActions('auth', ['login', 'logout', 'register', 'updateProfile'])
  },
  mounted() {
    // Автоматическая инициализация аутентификации
    this.$store.dispatch('auth/initAuth')
  }
}
</script>
```

---

## Аутентификация и авторизация

### Процесс аутентификации:

1. **Регистрация пользователя**
   - Запрос: `POST /auth/users/`
   - Тело: `{ username, email, password, first_name, last_name, phone }`
   - Ответ: данные пользователя (без пароля)

2. **Получение JWT токена**
   - Запрос: `POST /auth/jwt/create/`
   - Тело: `{ username, password }`
   - Ответ: `{ access, refresh }`

3. **Хранение токена**
   - `access` токен сохраняется в `localStorage`
   - Токен автоматически добавляется в заголовок `Authorization: Bearer <token>` для всех запросов через `axios`

4. **Получение данных текущего пользователя**
   - Запрос: `GET /auth/users/me/`
   - Ответ: полные данные пользователя с ролью

5. **Обновление токена (опционально)**
   - Запрос: `POST /auth/jwt/refresh/`
   - Тело: `{ refresh }`
   - Ответ: новый `access` токен

### Защита маршрутов:

```javascript
// В компоненте страницы
export default {
  beforeRouteEnter(to, from, next) {
    // Проверка авторизации перед входом на страницу
    const token = localStorage.getItem('token')
    if (!token && to.meta.requiresAuth) {
      next('/login')
    } else {
      next()
    }
  }
}
```

---

## Ключевые компоненты фронтенда

### 1. Главная страница (`HomeView.vue`)

**Функционал:**
- Отображение приветственного сообщения
- Кнопки навигации в зависимости от роли пользователя:
  - Неавторизованные: регистрация, просмотр услуг
  - Авторизованные: личный кабинет, мои заявки
  - Администраторы: панели управления услугами, заявками, отзывами

**Особенности:**
- Использование `mapGetters` для получения состояния авторизации
- Динамическое отображение кнопок в зависимости от роли

```vue
<template>
  <v-container class="my-12">
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 text-center mb-4">Главная страница</h1>
        <div class="text-center mb-8">
          <!-- Кнопки навигации -->
          <v-btn to="/services" color="primary" class="mr-4">Услуги</v-btn>
          
          <!-- Только для неавторизованных -->
          <v-btn v-if="!isAuthenticated" to="/register" variant="outlined" color="primary">
            Регистрация
          </v-btn>
          
          <!-- Для авторизованных -->
          <v-btn v-if="isAuthenticated" to="/profile" color="secondary" class="mr-4">
            Личный кабинет
          </v-btn>
          
          <!-- Для администраторов -->
          <v-btn v-if="isAdmin" to="/admin/services" color="error">
            <v-icon start>mdi-shield-account</v-icon>
            Админ: Услуги
          </v-btn>
        </div>
        
        <!-- Информация о пользователе -->
        <div v-if="isAuthenticated" class="text-center">
          <p>Добро пожаловать, {{ userName }}</p>
          <p>Роль: {{ userData.role }}</p>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
```

### 2. Список услуг (`ServicesView.vue`)

**Функционал:**
- Отображение списка активных услуг
- Карточки услуг с изображением, названием, ценой, категорией
- Кнопка "Выбрать" для создания заявки
- Автоматическая переадресация на страницу входа для неавторизованных

**Особенности:**
- Загрузка данных через `axios.get('/api/services/')`
- Обработка изображений: извлечение имени файла из пути `primary_image`
- Обрезка длинного описания до 100 символов

```javascript
methods: {
  async loadServices() {
    this.loading = true
    try {
      const response = await axios.get('/api/services/')
      this.services = response.data
    } catch (error) {
      console.error('Ошибка загрузки услуг:', error)
      this.services = []
    } finally {
      this.loading = false
    }
  },
  
  getImagePath(service) {
    if (service.primary_image) {
      const parts = service.primary_image.split('/')
      const filename = parts[parts.length - 1]
      return `../../../../media/services/${service.id}/${filename}`
    }
    // Заглушка для отсутствующего изображения
    return 'data:image/svg+xml;utf8,<svg ...>Нет изображения</svg>'
  }
}
```

### 3. Создание заявки (`CreateOrderView.vue`)

**Функционал:**
- Отображение информации о выбранной услуге
- Поле для ввода комментария/пожеланий
- Отправка заявки через `POST /api/orders/`
- Автоматическое создание комментария к заявке с текстом пользователя

**Особенности:**
- Получение ID услуги из параметров маршрута: `this.$route.query.service_id`
- Валидация данных перед отправкой
- Обработка ошибок через `try/catch`

```javascript
async submitOrder() {
  this.loading = true
  this.error = null
  try {
    // Создание заявки
    const response = await axios.post('/api/orders/', this.form)
    const createdOrder = response.data
    
    // Автоматическое создание комментария с пожеланиями
    if (this.form.notes && this.form.notes.trim() !== '') {
      try {
        await axios.post('/api/admin/comments/', {
          order: createdOrder.id,
          content: this.form.notes,
          is_visible_to_user: true
        })
      } catch (commentError) {
        console.error('Ошибка создания комментария:', commentError)
      }
    }
    
    alert('Заявка успешно создана!')
    this.$router.push('/profile/orders')
  } catch (error) {
    console.error('Ошибка создания заявки:', error)
    this.error = error.response?.data?.detail || 'Ошибка при создании заявки'
  } finally {
    this.loading = false
  }
}
```

### 4. Личный кабинет (`ProfileView.vue`)

**Функционал:**
- Отображение информации о пользователе (имя, фамилия, email, телефон, роль)
- Форма редактирования профиля
- Обновление данных через `PATCH /auth/users/{id}/`

**Особенности:**
- Использование `watch` для синхронизации формы с данными пользователя
- Сохранение обновлённых данных в `localStorage`
- Отображение временных сообщений об успехе/ошибке

```javascript
watch: {
  user: {
    immediate: true,
    handler(newUser) {
      if (newUser) {
        this.editForm = {
          first_name: newUser.first_name || '',
          last_name: newUser.last_name || '',
          phone: newUser.phone || ''
        }
      }
    }
  }
}
```

### 5. Управление услугами (админ) (`AdminServicesView.vue`)

**Функционал:**
- Отображение всех услуг (включая неактивные)
- Визуальная индикация статуса (активна/неактивна)
- Кнопки действий: просмотр, редактирование, удаление
- Создание новой услуги через кнопку "Добавить услугу"

**Особенности:**
- Загрузка данных через админский эндпоинт: `GET /api/admin/services/`
- Обработка состояния удаления (`deletingId`) для отображения лоадера на кнопке
- Подтверждение удаления через `confirm()`

```javascript
async deleteService(service) {
  if (!confirm(`Удалить услугу "${service.name}"?`)) return
  this.deletingId = service.id
  try {
    await axios.delete(`/api/admin/services/${service.id}/`)
    this.services = this.services.filter(s => s.id !== service.id)
    alert('Услуга удалена')
  } catch (error) {
    console.error('Ошибка удаления:', error)
    alert('Ошибка при удалении услуги')
  } finally {
    this.deletingId = null
  }
}
```

### 6. Детали услуги (админ) (`AdminServiceDetailView.vue`)

**Функционал:**
- Отображение полной информации об услуге
- Управление статусом активности (активировать/деактивировать)
- Загрузка изображений через форму
- Редактирование и удаление услуги

**Особенности:**
- Отображение основного изображения через `getMainImage()`
- Модальное окно для загрузки изображений (`v-dialog`)
- Форматирование дат через `formatDate()`
- Подтверждение опасных действий (удаление, деактивация)

```javascript
methods: {
  async uploadImage() {
    if (!this.uploadFile) return
    const formData = new FormData()
    formData.append('service', this.service.id)
    formData.append('file', this.uploadFile)
    formData.append('alt_text', this.uploadAltText)
    formData.append('is_primary', this.uploadIsPrimary)
    formData.append('display_order', this.uploadDisplayOrder)
    
    try {
      await axios.post('/api/admin/files/upload/', formData)
      alert('Изображение загружено')
      this.showUploadDialog = false
      await this.loadService()
    } catch (error) {
      console.error('Ошибка загрузки:', error)
      alert('Ошибка при загрузке изображения')
    }
  }
}
```

### 7. Управление заявками (админ) (`AdminOrdersView.vue`)

**Функционал:**
- Отображение списка всех заявок
- Просмотр истории изменений статуса
- Изменение статуса заявки
- Добавление комментариев к заявке

**Особенности:**
- Загрузка истории через `GET /api/admin/orders/{id}/history/`
- Изменение статуса через `PATCH /api/admin/orders/{id}/status/`
- Модальные окна для истории, изменения статуса и комментариев

```javascript
async changeStatus() {
  try {
    await axios.patch(
      `/api/admin/orders/${this.selectedOrder.id}/status/`,
      { 
        status: this.newStatus, 
        comment: this.comment 
      }
    )
    // Обновление локального состояния или перезагрузка списка
  } finally {
    this.statusDialog = false
  }
}
```

---

## Интеграция с бэкендом (API)

### Базовые запросы через `axios`

```javascript
import axios from 'axios'

// Настройка базового URL (проксируется через Vite)
axios.defaults.baseURL = '/'

// Автоматическая установка токена из хранилища
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Обработка ошибок 401 (неавторизован)
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Очистка токена и перенаправление на страницу входа
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

### Карта эндпоинтов

| Функционал | Метод | Эндпоинт | Описание |
|------------|-------|----------|----------|
| **Аутентификация** | | | |
| Регистрация | POST | `/auth/users/` | Создание нового пользователя |
| Получение токена | POST | `/auth/jwt/create/` | Аутентификация и получение JWT |
| Обновление токена | POST | `/auth/jwt/refresh/` | Обновление access токена |
| Данные пользователя | GET | `/auth/users/me/` | Получение профиля текущего пользователя |
| Обновление профиля | PATCH | `/auth/users/me/` | Редактирование личных данных |
| **Услуги** | | | |
| Список услуг | GET | `/api/services/` | Публичный список активных услуг |
| Детали услуги | GET | `/api/services/{id}/` | Информация об услуге |
| Файлы услуги | GET | `/api/services/{id}/files/` | Изображения и файлы услуги |
| Отзывы услуги | GET | `/api/services/{id}/reviews/` | Опубликованные отзывы |
| Админ: список | GET | `/api/admin/services/` | Все услуги (включая неактивные) |
| Админ: создание | POST | `/api/admin/services/` | Создание новой услуги |
| Админ: редактирование | PATCH | `/api/admin/services/{id}/` | Обновление услуги |
| Админ: деактивация | POST | `/api/admin/services/{id}/deactivate/` | Скрытие услуги из публичного списка |
| Админ: удаление | DELETE | `/api/admin/services/{id}/` | Полное удаление услуги |
| **Заявки** | | | |
| Мои заявки | GET | `/api/orders/` | Список заявок текущего пользователя |
| Создание заявки | POST | `/api/orders/` | Оформление новой заявки |
| Детали заявки | GET | `/api/orders/{id}/` | Информация о заявке |
| Отмена заявки | POST | `/api/orders/{id}/cancel/` | Отмена пользователем |
| Комментарии заявки | GET | `/api/orders/{id}/comments/` | Комментарии, видимые пользователю |
| Админ: все заявки | GET | `/api/admin/orders/` | Список всех заявок |
| Админ: история | GET | `/api/admin/orders/{id}/history/` | История изменений статуса |
| Админ: изменение статуса | PATCH | `/api/admin/orders/{id}/status/` | Обновление статуса заявки |
| **Отзывы** | | | |
| Создание отзыва | POST | `/api/reviews/` | Оставление отзыва на завершенную заявку |
| Админ: все отзывы | GET | `/api/admin/reviews/` | Список всех отзывов |
| Админ: модерация | PATCH | `/api/admin/reviews/{id}/` | Публикация/скрытие отзыва |
| **Файлы** | | | |
| Админ: загрузка | POST | `/api/admin/files/upload/` | Загрузка изображения для услуги |
| Админ: управление | GET/PUT/PATCH/DELETE | `/api/admin/files/{id}/` | Работа с файлами |

---

## Чек-лист для развёртывания

### Бэкенд (Django)

```bash
# 1. Установка зависимостей
pip install -r requirements.txt

# 2. Применение миграций
python manage.py migrate

# 3. Создание суперпользователя (для админки)
python manage.py createsuperuser

# 4. Сборка статических файлов (для продакшена)
python manage.py collectstatic --noinput

# 5. Запуск сервера разработки
python manage.py runserver
```

### Фронтенд (Vue.js)

```bash
# 1. Установка зависимостей
cd frontend/brand_app
npm install

# 2. Запуск сервера разработки (с прокси к бэкенду)
npm run dev
# или
yarn dev

# 3. Сборка для продакшена
npm run build
# или
yarn build
```

### Интеграция фронтенда и бэкенда

1. Бэкенд: запуск через Gunicorn + Nginx на порту 8000
2. Фронтенд: сборка через `npm run build`, раздача статики через Nginx на порту 80
3. Настройка прокси в Nginx для `/api`, `/auth`, `/media`

### Проверка работоспособности

- [ ] Бэкенд доступен по `http://localhost:8000/admin/`
- [ ] API доступен по `http://localhost:8000/api/services/`
- [ ] Фронтенд доступен по `http://localhost:8080/`
- [ ] Регистрация нового пользователя работает
- [ ] Авторизация через JWT работает
- [ ] Создание заявки работает для авторизованного пользователя
- [ ] Админские функции работают для пользователя с ролью `admin`
- [ ] Изображения услуг загружаются и отображаются корректно
- [ ] Комментарии к заявкам создаются и отображаются

---

## Заключение

Документация предоставляет полное руководство по развёртыванию и использованию фронтенд-части проекта "Сайт для продвижения личного бренда". В результате выполнения лабораторной работы успешно реализована клиентская часть информационной системы администратора гостиницы на базе Vue 3 и Vuetify. :

- Современный фронтенд на Vue.js 3  
- Аутентификация через JWT (Djoser)  
- Разделение прав доступа (пользователь/админ)  
- Полноценные интерфейсы для всех ролей  
- Интеграция с бэкендом через REST API  
- Адаптивный дизайн через Vuetify  

