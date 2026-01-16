# Vue.js приложение для управления колледжем

## Обзор

Современное одностраничное приложение (SPA) построенное на Vue.js 3 с использованием TypeScript и Vuetify для создания интерфейса системы управления колледжем.

## Архитектура приложения

### main.ts - Точка входа
```typescript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(vuetify)
app.mount('#app')
```

### App.vue - Корневой компонент
```vue
<template>
  <v-app>
    <v-navigation-drawer app>
      <!-- Навигационное меню -->
    </v-navigation-drawer>
    
    <v-app-bar app>
      <!-- Верхняя панель -->
    </v-app-bar>
    
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
```

## Основные возможности

### 1. Управление студентами
- Просмотр списка студентов
- Добавление новых студентов
- Редактирование информации о студентах
- Поиск и фильтрация

### 2. Управление дисциплинами
- Каталог дисциплин
- Информация о преподавателях
- Расписание занятий

### 3. Система оценок
- Ввод оценок
- Просмотр успеваемости
- Статистика по предметам

## Vue Composition API

### Пример компонента
```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

const students = ref([])
const searchQuery = ref('')

const filteredStudents = computed(() => {
  return students.value.filter(student => 
    student.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const loadStudents = async () => {
  // Загрузка данных из API
}
</script>

<template>
  <v-container>
    <v-text-field 
      v-model="searchQuery" 
      label="Поиск студентов"
      prepend-inner-icon="mdi-magnify"
    />
    
    <v-data-table 
      :items="filteredStudents"
      :headers="headers"
    />
  </v-container>
</template>
```

## Pinia Store

### Store для управления состоянием
```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useStudentStore = defineStore('students', () => {
  const students = ref([])
  const loading = ref(false)
  
  const studentCount = computed(() => students.value.length)
  
  const fetchStudents = async () => {
    loading.value = true
    try {
      const response = await axios.get('/api/students/')
      students.value = response.data
    } finally {
      loading.value = false
    }
  }
  
  return {
    students,
    loading,
    studentCount,
    fetchStudents
  }
})
```

## Vue Router

### Конфигурация маршрутов
```typescript
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/students',
    name: 'Students',
    component: () => import('../views/StudentsView.vue')
  },
  {
    path: '/subjects',
    name: 'Subjects',
    component: () => import('../views/SubjectsView.vue')
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
```

## Vuetify компоненты

Приложение использует Vuetify 3 для создания Material Design интерфейса:

- **v-app** - Корневой контейнер приложения
- **v-navigation-drawer** - Боковое меню навигации
- **v-app-bar** - Верхняя панель приложения
- **v-data-table** - Таблицы данных
- **v-card** - Карточки для отображения информации
- **v-dialog** - Модальные окна
- **v-form** - Формы с валидацией

## API интеграция

Используется Axios для HTTP запросов к Django REST API:

```typescript
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8000/api/'

export default axios
```