# Отчет по лабораторной работе №4
### Тема: Реализация клиентской части приложения средствами Vue.js

### Структура проекта

Проект представляет собой Single Page Application (SPA), разработанное на фреймворке Vue 3 с использованием сборщика Vite.

1.  **Конфигурация и зависимости**
    * `vite.config.js` — настройки сборщика Vite.
    * `package.json` — список зависимостей (Vue, Vuetify, Pinia, Axios, Vue Router).
    * `src/main.js` — точка входа: подключение плагинов (Router, Pinia, Vuetify) и монтирование приложения.

2.  **Исходный код (`src/`)**
    * `api/axios.js` — настроенный экземпляр HTTP-клиента с перехватчиками (interceptors) для автоматического добавления токена авторизации.
    * `stores/` — хранилища состояний (State Management) на базе Pinia.
        * `auth.js` — хранит токен и статус авторизации, содержит методы `login`, `register`, `logout`.
    * `router/index.js` — конфигурация маршрутизации. Определяет пути к страницам и защищает их навигационными хуками (`beforeEach`).
    * `views/` — компоненты-страницы:
        * `Auth/` — страницы входа (`Login.vue`) и регистрации (`Register.vue`).
        * `Clients/` — CRUD интерфейсы для клиентов (`ClientList`, `ClientForm`, `ClientDetail`).
        * `Products/` — интерфейсы для вкладов и кредитов.
        * `Passports/` — интерфейсы для управления паспортами.
    * `App.vue` — корневой компонент, содержащий навигационную панель (`v-app-bar`) и область для отображения страниц (`router-view`).



## 1. Настройка взаимодействия с API (Axios & CORS)

Для общения с серверной частью (Django REST Framework из ЛР №3) используется библиотека **Axios**. Настроен глобальный перехватчик запросов, который проверяет наличие токена в `localStorage` и добавляет его в заголовок `Authorization`.

**Код:**

*src/api/axios.js:*
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default api;
```



## 2. Управление состоянием и Аутентификация (Pinia)

Для хранения состояния авторизации используется библиотека **Pinia**. Хранилище `useAuthStore` отвечает за:
1.  Отправку запроса на получение токена (`/auth/token/login/`).
2.  Сохранение токена в `localStorage`.
3.  Реактивное обновление интерфейса (скрытие/показ кнопок в меню).

**Код:**

*src/stores/auth.js:*
```javascript
import { defineStore } from 'pinia';
import api from '../api/axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
  }),
  actions: {
    async login(credentials) {
      const response = await api.post('/auth/token/login/', credentials);
      this.token = response.data.auth_token;
      this.isAuthenticated = true;
      localStorage.setItem('token', this.token);
    },
    logout() {
      this.token = null;
      this.isAuthenticated = false;
      localStorage.removeItem('token');
    }
  }
});
```



## 3. Реализация интерфейсов (Vue Router & Views)

Настроена маршрутизация с помощью **Vue Router**. Реализована защита маршрутов: неавторизованные пользователи перенаправляются на страницу входа.

### 3.1. Список и CRUD операции
Реализованы страницы для просмотра списков сущностей (Клиенты, Паспорта, Вклады, Кредиты) с использованием компонента `v-data-table` из библиотеки Vuetify. Добавлены кнопки для перехода к редактированию, просмотру деталей и удалению.

**Код:**

*src/views/Clients/ClientList.vue (фрагмент):*
```html
<template>
  <v-card>
    <v-data-table :headers="headers" :items="clients" :loading="loading">
      <template v-slot:item.actions="{ item }">
        <v-btn icon="mdi-eye" :to="`/clients/${item.id}`"></v-btn>
        <v-btn icon="mdi-pencil" :to="`/clients/${item.id}/edit`"></v-btn>
        <v-btn icon="mdi-delete" @click="deleteClient(item.id)"></v-btn>
      </template>
    </v-data-table>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../../api/axios';
// ... логика загрузки данных ...
</script>
```

### 3.2. Работа со связанными данными (Forms)
При создании зависимых сущностей (например, Вклада или Паспорта) реализована подгрузка списков для выбора родительского объекта (`v-select`). Например, при создании Вклада мы выбираем Клиента (Паспорт) и Валюту из выпадающего списка.

**Код:**

*src/views/Products/DepositForm.vue (фрагмент):*
```html
<v-select
  v-model="form.passport"
  :items="passports"
  item-title="selectTitle"
  item-value="id"
  label="Выберите паспорт клиента"
></v-select>

<script setup>
onMounted(async () => {
  const [passReq, typeReq] = await Promise.all([
    api.get('/api/v1/passports/'),
    api.get('/api/v1/deposit-types/')
  ]);
  passports.value = passReq.data.map(p => ({
    ...p,
    selectTitle: `${p.series} ${p.number} (${p.fio})`
  }));
});
</script>
```

### 3.3. Отображение вложенных данных (Details)
На страницах детального просмотра (`ClientDetail`, `LoanDetail`) реализовано отображение вложенных структур, полученных от API (сериализаторы из ЛР №3).
* У Клиента отображается список его Паспортов.
* У Кредита отображается График платежей (`payouts`).



## 4. Пользовательский интерфейс (Vuetify)

Для стилизации приложения использована библиотека компонентов **Vuetify** (Material Design).
Использованные компоненты:
* `v-app-bar` — навигационная панель.
* `v-data-table` — таблицы с пагинацией и сортировкой.
* `v-card` — контейнеры для контента.
* `v-text-field`, `v-select`, `v-textarea` — элементы форм.
* `v-btn`, `v-icon` — кнопки и иконки (@mdi/font).
* `v-chip` — для выделения статусов или сумм.

**Пример интерфейса (Главное меню в App.vue):**
```html
<template v-if="authStore.isAuthenticated">
  <v-btn to="/clients">Клиенты</v-btn>
  <v-btn to="/deposits">Вклады</v-btn>
  <v-btn to="/credits">Кредиты</v-btn>
  <v-spacer></v-spacer>
  <v-btn icon="mdi-logout" @click="handleLogout"></v-btn>
</template>
```

### Выводы

В ходе выполнения лабораторной работы была разработана клиентская часть (Frontend) веб-приложения для банковской системы.

* Изучены основы **Vue 3** и **Composition API** (`setup`, `ref`, `onMounted`).

* Настроено глобальное состояние приложения с помощью **Pinia** (авторизация).

* Организовано взаимодействие с REST API через **Axios** (JWT-токены, CRUD-запросы).

* Реализован динамический интерфейс с использованием библиотеки **Vuetify**.

* Настроена клиентская маршрутизация (**Vue Router**) и защита страниц.

* Реализованы сложные формы с выпадающими списками и отображение вложенных данных (Master-Detail).