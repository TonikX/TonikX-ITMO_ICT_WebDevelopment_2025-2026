# Задание 1: Vue.js приложение

## Описание работы

В рамках данной лабораторной работы был создан проект на Vue.js с использованием компонентного подхода, Vue Router для маршрутизации и Axios для HTTP-запросов.

---

## Используемые технологии

| Технология | Версия | Назначение |
|------------|--------|------------|
| Vue.js | 3.x | Прогрессивный JavaScript фреймворк |
| Vue Router | 4.x | Официальный роутер для Vue.js |
| Axios | 1.x | HTTP-клиент для выполнения запросов |
| Vite | 7.x | Сборщик проекта |

---

## Выполненные задания

### 1. Создание первого компонента

Создан компонент `src/components/Hello.vue`:

```vue
<template>
  <div>
    <h1>Привет, это твой первый компонент</h1>
  </div>
</template>

<script>
export default {
  name: "Hello"
}
</script>
```

Компонент демонстрирует базовую структуру Vue-компонента с тремя секциями:

- `<template>` — HTML-разметка
- `<script>` — JavaScript логика
- `<style>` — стили компонента

### 2. Настройка Vue Router

Создан файл конфигурации роутера `src/router/index.js`:

```javascript
import Hello from "@/components/Hello.vue";
import Warriors from "@/views/Warriors.vue";
import {createRouter, createWebHistory} from "vue-router";

const routes = [
    {
        path: '/hi',
        component: Hello
    },
    {
        path: '/warriors',
        component: Warriors
    }
]

const router = createRouter({
    history: createWebHistory(), routes
})

export default router
```

Роутер подключен в `main.js`:

```javascript
import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'
import router from "./router";

createApp(App).use(router).mount('#app')
```

### 3. Разделение на Views и Components

Согласно best practices Vue.js, проект разделен на:

- **Views (представления)** — компоненты-страницы, доступные по URL
  - `Warriors.vue` — страница с информацией о воинах

- **Components (компоненты)** — переиспользуемые UI-элементы
  - `Hello.vue` — тестовый компонент
  - `WarriorForm.vue` — форма создания воина
  - `WarriorList.vue` — отображение списка воинов

### 4. Создание представления Warriors

Представление `src/views/Warriors.vue` демонстрирует:

- Использование дочерних компонентов (`WarriorForm`, `WarriorList`)
- Передача данных через `props` (директива `v-bind`)
- Асинхронные HTTP-запросы через Axios
- Lifecycle hook `mounted()` для загрузки данных при инициализации
- Методы компонента (`methods`)
- Реактивные данные (`data()`)

### 5. Компонент WarriorList

Компонент `src/components/WarriorList.vue` демонстрирует:

- Получение данных через `props`
- Директива `v-for` для отображения списка
- Интерполяция данных `{{ warrior.name }}`

### 6. Компонент WarriorForm

Компонент `src/components/WarriorForm.vue` демонстрирует:

- Двустороннее связывание данных (`v-model`)
- Обработка событий формы (`@submit.prevent`)
- Обработка клика (`v-on:click`)
- POST-запрос через Axios

---

## Маршруты приложения

| URL | Компонент | Описание |
|-----|-----------|----------|
| `/hi` | Hello.vue | Первый тестовый компонент |
| `/warriors` | Warriors.vue | Страница с воинами |

---

## Ключевые концепции Vue.js

### Компонентный подход

Приложение разбито на независимые компоненты, каждый из которых содержит свою разметку, логику и стили.

### Реактивность

Vue автоматически отслеживает изменения в данных и обновляет DOM.

### Директивы

- `v-for` — рендеринг списков
- `v-bind` — привязка атрибутов
- `v-model` — двустороннее связывание
- `v-on` — обработка событий

### Props

Механизм передачи данных от родительского компонента к дочернему.

---

## Запуск проекта

### Требования

- Node.js (LTS версия 16.18.0+)
- npm (версия 8.19.2+)

После запуска проект будет доступен по адресу: http://localhost:5173/

---

## Выводы

В ходе выполнения лабораторной работы были изучены основы Vue.js:

- Создание и структура компонентов
- Настройка маршрутизации с Vue Router
- Работа с HTTP-запросами через Axios
- Передача данных между компонентами
- Организация структуры проекта (views/components)

