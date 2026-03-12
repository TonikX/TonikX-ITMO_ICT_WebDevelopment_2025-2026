# Лабораторная работа №4: Реализация клиентской части средствами Vue.js

## Название работы

Реализация клиентской части средствами Vue.js.

## Цель работы

Создание клиентской часть веб-приложения для системы управления библиотекой с использованием Vue.js и Vuetify.

## Задание

1. Настроить для серверной части, реализованной в лабораторной работе №3 CORS (Cross-origin resource sharing)
2. Реализовать интерфейсы авторизации, регистрации и изменения учетных данных и настроить взаимодействие с серверной частью
3. Реализовать список интерфейсов для взаимодействия с серверной частью в соответствии с предметной областью выбранной в 3 лабораторной работе
4. Подключить vuetify или аналогичную библиотеку

## Предметная область

Создание клиентского интерфейса для системы управления библиотекой, обеспечивающего удобную работу с:

- Книгами в библиотеке
- Читателями библиотеки
- Читальными залами
- Выдачей книг
- Статистическими отчетами

## Выполнение работы

### 1. Настройка проекта

Был создан Vue.js проект в папке `lab4/library-frontend/` со следующей структурой:

```
library-frontend/
├── src/
│   ├── api/           # API модуль для взаимодействия с сервером
│   ├── views/         # Vue компоненты страниц
│   ├── router/        # Маршрутизация приложения
│   ├── App.vue        # Главный компонент приложения
│   └── main.js        # Точка входа
├── package.json       # Зависимости проекта
└── vite.config.js     # Конфигурация Vite
```

### 2. Настройка зависимостей

В файле `package.json` были добавлены необходимые зависимости:

```json
{
  "dependencies": {
    "@mdi/font": "^7.4.47",
    "axios": "^1.13.6",
    "vue": "^3.5.29",
    "vue-router": "^5.0.3",
    "vuetify": "^4.0.1"
  }
}
```

### 3. Настройка Vuetify

В файле `src/main.js` была выполнена настройка Vuetify:

```javascript
import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

const vuetify = createVuetify({
  components,
  directives,
});

const app = createApp(App);
app.use(vuetify);
app.use(router);
app.mount("#app");
```

### 4. Настройка CORS на сервере

В файле `settings.py` (лабораторная работа №3) был добавлен `corsheaders`:

```python
INSTALLED_APPS = [
    # ... другие приложения
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ... другие middleware
]

CORS_ALLOW_ALL_ORIGINS = True
```

Это позволяет фронтенду на `localhost:5173` обращаться к бэкенду на `localhost:8000`.

### 5. Реализация API модуля

#### Создание HTTP клиента (`src/api/axios.js`)

```javascript
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const publicAuthEndpoints = [
    "/auth/token/login/",
    "/auth/users/",
    "/auth/token/logout/",
  ];

  const isPublicEndpoint = publicAuthEndpoints.some(
    (endpoint) => config.url === endpoint,
  );

  if (!isPublicEndpoint) {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error(
      "API Error:",
      error.response?.status,
      error.response?.data || error.message,
    );
    return Promise.reject(error);
  },
);

export default api;
```

**Особенности реализации:**

- Автоматическое добавление токена авторизации в заголовки
- Обработка ошибок с логированием
- Базовый URL для всех запросов

#### API функции (`src/api/index.js`)

```javascript
// Функции аутентификации
async function login(username, password) {
  const res = await api.post("/auth/token/login/", { username, password });
  const token = res.data.auth_token || res.data.token;
  if (token) localStorage.setItem("token", token);
  return res.data;
}

async function logout() {
  try {
    await api.post("/auth/token/logout/");
  } catch (e) {}
  localStorage.removeItem("token");
}

async function register(username, password, email = "") {
  return api.post("/auth/users/", { username, password, email });
}

async function getCurrentUser() {
  return api.get("/auth/users/me/");
}

async function updateUser(data) {
  return api.put("/auth/users/me/", data);
}

async function setPassword(current_password, new_password) {
  return api.post("/auth/users/set_password/", {
    current_password,
    new_password,
  });
}

// Функции для работы с книгами
async function getBooks() {
  return api.get("/api/books/");
}

async function getBooksInHalls() {
  return api.get("/api/books-in-halls/");
}

async function createBook(data) {
  return api.post("/api/books/", data);
}

async function updateBook(id, data) {
  return api.put(`/api/books/${id}/`, data);
}

// Функции для работы с залами
async function getHalls() {
  return api.get("/api/halls/");
}

async function createHall(data) {
  return api.post("/api/halls/", data);
}

// Функции для работы с читателями
async function getReaders() {
  return api.get("/api/readers/");
}

async function createReader(data) {
  return api.post("/api/readers/", data);
}

// Функции для работы с выдачами
async function getIssues() {
  return api.get("/api/issues/");
}

async function createIssue(data) {
  return api.post("/api/issues/", data);
}

// Статистические функции
async function getReaderBooks(readerId) {
  return api.get(`/api/readers/${readerId}/books/`);
}

async function getIssuesOverdue() {
  return api.get("/api/issues/overdue/");
}

async function getReadersUnder20() {
  return api.get("/api/readers/under_20/");
}

async function getEducationStats() {
  return api.get("/api/readers/education_stats/");
}

async function getRareBooksReaders() {
  return api.get("/api/readers/rare_books/");
}
```

### 6. Реализация интерфейсов аутентификации

#### Страница входа (`src/views/Login.vue`)

```vue
<template>
  <v-container>
    <v-text-field v-model="username" label="Имя пользователя" />
    <v-text-field v-model="password" label="Пароль" type="password" />
    <v-btn color="primary" @click="login">Войти</v-btn>
  </v-container>
</template>

<script>
import apiWrapper from "../api/index.js";

export default {
  data() {
    return { username: "", password: "" };
  },
  methods: {
    async login() {
      try {
        console.log("Attempting login with:", this.username);
        const res = await apiWrapper.login(this.username, this.password);
        console.log("Login response:", res);
        const token = localStorage.getItem("token");
        console.log("Token in localStorage:", token ? "✓ Set" : "✗ Not set");
        if (token) {
          this.$router.push({ name: "books" });
        } else {
          alert("Token not saved");
        }
      } catch (e) {
        console.error("Login error:", e);
        alert(`Login failed: ${e.message || "Unknown error"}`);
      }
    },
  },
};
</script>
```

#### Страница регистрации (`src/views/Register.vue`)

```vue
<template>
  <v-container>
    <h2>Регистрация</h2>
    <v-text-field v-model="username" label="Имя пользователя" />
    <v-text-field v-model="password" label="Пароль" type="password" />
    <v-btn color="primary" @click="register">Зарегистрироваться</v-btn>
  </v-container>
</template>

<script>
import apiWrapper from "../api/index.js";

export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async register() {
      try {
        await apiWrapper.register(this.username, this.password);
        alert("Вы зарегистрированы");
        this.$router.push("/login");
      } catch (e) {
        alert("Ошибка регистрации");
      }
    },
  },
};
</script>
```

#### Страница профиля (`src/views/Profile.vue`)

```vue
<template>
  <v-container>
    <h2>Профиль</h2>
    <div v-if="user">
      <v-form @submit.prevent="updateProfile">
        <v-text-field v-model="form.username" label="Имя пользователя" />
        <v-text-field v-model="form.email" label="Email" />
        <v-btn type="submit" color="primary">Сохранить</v-btn>
      </v-form>

      <v-divider class="my-4"></v-divider>

      <h3>Изменить пароль</h3>
      <v-form @submit.prevent="changePassword">
        <v-text-field
          v-model="currentPassword"
          label="Текущий пароль"
          type="password"
        />
        <v-text-field
          v-model="newPassword"
          label="Новый пароль"
          type="password"
        />
        <v-btn type="submit" color="primary">Изменить</v-btn>
      </v-form>

      <v-divider class="my-4"></v-divider>

      <h3>Данные пользователя</h3>
      <p><strong>ID:</strong> {{ user.id }}</p>
      <p><strong>Имя пользователя:</strong> {{ user.username }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>

      <v-divider class="my-4"></v-divider>

      <h3>Токен авторизации</h3>
      <v-text-field :model-value="token" label="Token" readonly />

      <v-divider class="my-4"></v-divider>
      <v-btn color="error" @click="logout">Выход</v-btn>
    </div>
    <div v-else>
      <p>Вы не авторизованы</p>
      <v-btn color="primary" @click="$router.push('/login')">Войти</v-btn>
    </div>
  </v-container>
</template>

<script>
import apiWrapper from "../api/index.js";

export default {
  data() {
    return {
      user: null,
      form: {
        username: "",
        email: "",
      },
      currentPassword: "",
      newPassword: "",
      token: localStorage.getItem("token") || "",
    };
  },
  async mounted() {
    try {
      const res = await apiWrapper.getCurrentUser();
      this.user = res.data;
      this.form.username = this.user.username;
      this.form.email = this.user.email || "";
    } catch (e) {
      console.error("Failed to load user:", e);
      this.user = null;
    }
  },
  methods: {
    async updateProfile() {
      try {
        const res = await apiWrapper.updateUser(this.form);
        this.user = res.data;
        alert("Profile updated");
      } catch (e) {
        alert("Update failed");
      }
    },
    async changePassword() {
      try {
        await apiWrapper.setPassword(this.currentPassword, this.newPassword);
        alert("Password changed");
        this.currentPassword = "";
        this.newPassword = "";
      } catch (e) {
        alert("Password change failed");
      }
    },
    logout() {
      apiWrapper.logout();
      this.token = "";
      this.user = null;
      this.$router.push("/login");
    },
  },
};
</script>
```

### 7. Реализация навигации и маршрутизации

#### Главный компонент (`src/App.vue`)

```vue
<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title>Библиотека</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text to="/books">Книги</v-btn>
      <v-btn text to="/halls">Залы</v-btn>
      <v-btn text to="/readers">Читатели</v-btn>
      <v-btn text to="/issues">Выдачи</v-btn>
      <v-btn text to="/reports">Запросы</v-btn>
      <v-btn text to="/profile">Профиль</v-btn>
      <v-btn v-if="!isAuthenticated" text to="/login">Вход</v-btn>
      <v-btn v-if="!isAuthenticated" text to="/register">Регистрация</v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const isAuthenticated = ref(!!localStorage.getItem("token"));

watch(
  () => route.fullPath,
  () => {
    isAuthenticated.value = !!localStorage.getItem("token");
  },
  { immediate: true },
);
</script>
```

#### Маршрутизация (`src/router/index.js`)

```javascript
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/", redirect: "/books" },
  { path: "/books", name: "books", component: Books },
  {
    path: "/books/create",
    name: "book-create",
    component: BookForm,
    meta: { requiresAuth: true },
  },
  {
    path: "/books/:id/edit",
    name: "book-edit",
    component: BookForm,
    meta: { requiresAuth: true },
  },
  { path: "/halls", name: "halls", component: Halls },
  {
    path: "/halls/create",
    name: "hall-create",
    component: HallForm,
    meta: { requiresAuth: true },
  },
  {
    path: "/halls/:id",
    name: "hall-detail",
    component: HallDetail,
    meta: { requiresAuth: true },
  },
  { path: "/readers", name: "readers", component: Readers },
  {
    path: "/readers/create",
    name: "reader-create",
    component: ReaderForm,
    meta: { requiresAuth: true },
  },
  { path: "/issues", name: "issues", component: Issues },
  {
    path: "/issues/create",
    name: "issue-create",
    component: IssueForm,
    meta: { requiresAuth: true },
  },
  { path: "/login", name: "login", component: Login },
  { path: "/register", name: "register", component: Register },
  { path: "/profile", name: "profile", component: Profile },
  {
    path: "/reports",
    name: "reports",
    component: Reports,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to) => {
  const token = localStorage.getItem("token");
  if (to.meta && to.meta.requiresAuth && !token) {
    return { name: "login" };
  }
  return true;
});

export default router;
```

**Особенности маршрутизации:**

- Защита маршрутов, требующих аутентификации
- Автоматическое перенаправление на страницу входа
- Иерархическая структура URL

### 8. Реализация интерфейсов для работы с данными

#### Список книг (`src/views/Books.vue`)

```vue
<template>
  <v-container>
    <v-row class="mb-4">
      <v-col>
        <h2>Книги</h2>
      </v-col>
      <v-col class="d-flex justify-end">
        <v-btn color="primary" @click="$router.push({ name: 'book-create' })"
          >Добавить книгу</v-btn
        >
      </v-col>
    </v-row>

    <v-simple-table>
      <thead>
        <tr>
          <th>Название</th>
          <th>Авторы</th>
          <th>Зал</th>
          <th>Копий</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in booksInHalls" :key="item.id">
          <td>{{ item.book_title }}</td>
          <td>{{ item.authors || "-" }}</td>
          <td>{{ item.hall_name }}</td>
          <td>{{ item.copies }}</td>
          <td>
            <v-btn
              small
              @click="
                $router.push({ name: 'book-edit', params: { id: item.book } })
              "
              >Редактировать книгу</v-btn
            >
            <v-btn
              small
              @click="
                $router.push({
                  name: 'book-in-hall-edit',
                  params: { id: item.id },
                })
              "
              >Зал / копии</v-btn
            >
            <v-btn small color="error" @click="remove(item.id)">Удалить</v-btn>
          </td>
        </tr>
      </tbody>
    </v-simple-table>
  </v-container>
</template>

<script>
import api from "../api/index.js";

export default {
  data() {
    return { booksInHalls: [] };
  },
  methods: {
    async load() {
      try {
        const res = await api.getBooksInHalls();
        this.booksInHalls = res.data;
      } catch (e) {
        console.error(e);
      }
    },
    async remove(id) {
      if (!confirm("Удалить запись о книге в зале?")) return;
      try {
        await api.deleteBookInHall(id);
        this.load();
      } catch (e) {
        console.error(e);
      }
    },
  },
  mounted() {
    this.load();
  },
};
</script>
```

#### Список залов (`src/views/Halls.vue`)

```vue
<template>
  <v-container>
    <v-row class="mb-4">
      <v-col><h2>Залы</h2></v-col>
      <v-col class="d-flex justify-end">
        <v-btn color="primary" @click="$router.push({ name: 'hall-create' })"
          >Добавить зал</v-btn
        >
      </v-col>
    </v-row>

    <v-simple-table>
      <thead>
        <tr>
          <th>Номер</th>
          <th>Название</th>
          <th>Вместимость (разных книг)</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="h in halls" :key="h.id">
          <td>{{ h.number }}</td>
          <td>
            <v-btn
              text
              @click="
                $router.push({ name: 'hall-detail', params: { id: h.id } })
              "
            >
              {{ h.name }}
            </v-btn>
          </td>
          <td>{{ h.capacity }}</td>
          <td>
            <v-btn
              small
              @click="
                $router.push({ name: 'hall-detail', params: { id: h.id } })
              "
            >
              Открыть
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-simple-table>
  </v-container>
</template>

<script>
import api from "../api/index.js";

export default {
  data() {
    return { halls: [] };
  },
  methods: {
    async load() {
      try {
        const res = await api.getHalls();
        this.halls = res.data;
      } catch (e) {
        console.error(e);
      }
    },
  },
  mounted() {
    this.load();
  },
};
</script>
```

#### Форма создания/редактирования книги (`src/views/BookForm.vue`)

```vue
<template>
  <v-container>
    <h2>{{ isEdit ? "Edit Book" : "Create Book" }}</h2>

    <v-form ref="form" @submit.prevent="submit">
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field v-model="book.title" label="Название" required />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field v-model="book.authors" label="Авторы" />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field v-model="book.publisher" label="Издатель" />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field v-model.number="book.year" label="Год" type="number" />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field v-model="book.code" label="Код" />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field v-model="book.section" label="Раздел" />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            v-model.number="book.copies"
            label="Копий"
            type="number"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            :items="halls"
            item-title="name"
            item-value="id"
            v-model="book.hall"
            label="Зал"
          />
        </v-col>
      </v-row>

      <v-row class="mt-4">
        <v-col>
          <v-btn color="primary" @click="submit">Сохранить</v-btn>
          <v-btn text @click="$router.back()">Отмена</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import api from "../api/index.js";

export default {
  data() {
    return {
      book: {
        title: "",
        authors: "",
        publisher: "",
        year: null,
        section: "",
        code: "",
        copies: 1,
        hall: null,
      },
      halls: [],
      isEdit: false,
    };
  },
  async mounted() {
    const id = this.$route.params.id;
    await this.loadHalls();
    if (id) {
      this.isEdit = true;
      try {
        const res = await api.getBook(id);
        this.book = {
          title: res.data.title,
          authors: res.data.authors,
          publisher: res.data.publisher,
          year: res.data.year,
          section: res.data.section,
          code: res.data.code,
          copies: res.data.copies,
          hall: res.data.hall,
        };
      } catch (e) {
        console.error(e);
      }
    }
  },
  methods: {
    async loadHalls() {
      try {
        const res = await api.getHalls();
        this.halls = res.data;
      } catch (e) {
        console.error(e);
      }
    },
    async submit() {
      try {
        if (this.isEdit) {
          await api.updateBook(this.$route.params.id, this.book);
        } else {
          await api.createBook(this.book);
        }
        this.$router.push({ name: "books" });
      } catch (e) {
        console.error(e);
        alert("Ошибка сохранения книги");
      }
    },
  },
};
</script>
```

### 9. Реализация статистических отчетов

#### Страница отчетов (`src/views/Reports.vue`)

```vue
<template>
  <v-container>
    <h2>Запросы для библиотекаря</h2>

    <v-divider class="my-4" />

    <section class="mb-6">
      <h3>Книги, закрепленные за читателем</h3>
      <v-row>
        <v-col cols="12" md="6">
          <v-select
            v-model="selectedReaderId"
            :items="readers"
            item-title="full_name"
            item-value="id"
            label="Выберите читателя"
          />
        </v-col>
        <v-col cols="12" md="6" class="d-flex align-end">
          <v-btn
            color="primary"
            @click="loadReaderBooks"
            :disabled="!selectedReaderId"
          >
            Показать книги
          </v-btn>
        </v-col>
      </v-row>
      <v-list v-if="readerBooks.length">
        <v-list-item v-for="(b, idx) in readerBooks" :key="idx">
          <v-list-item-title>{{ b }}</v-list-item-title>
        </v-list-item>
      </v-list>
      <p v-else class="text-muted">Нет данных для выбранного читателя.</p>
    </section>

    <v-divider class="my-4" />

    <section class="mb-6">
      <h3>Читатели с просроченными книгами (&gt; 1 месяца)</h3>
      <v-btn color="primary" @click="loadOverdueReaders"
        >Загрузить список</v-btn
      >
      <v-list v-if="overdueReaders.length" class="mt-3">
        <v-list-item v-for="(r, idx) in overdueReaders" :key="idx">
          <v-list-item-title>{{ r }}</v-list-item-title>
        </v-list-item>
      </v-list>
      <p v-else class="text-muted mt-3">Нет данных.</p>
    </section>

    <v-divider class="my-4" />

    <section class="mb-6">
      <h3>Читатели с редкими книгами (копий ≤ 2)</h3>
      <v-btn color="primary" @click="loadRareBooksReaders">Загрузить</v-btn>
      <v-simple-table class="mt-3" v-if="rareBooksReaders.length">
        <thead>
          <tr>
            <th>Читатель</th>
            <th>Книга</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, idx) in rareBooksReaders" :key="idx">
            <td>{{ row.reader }}</td>
            <td>{{ row.book }}</td>
          </tr>
        </tbody>
      </v-simple-table>
      <p v-else class="text-muted mt-3">Нет данных.</p>
    </section>

    <v-divider class="my-4" />

    <section class="mb-6">
      <h3>Количество читателей младше 20 лет</h3>
      <v-btn color="primary" @click="loadUnder20">Посчитать</v-btn>
      <p class="mt-3" v-if="under20Count !== null">
        Всего читателей младше 20 лет: <strong>{{ under20Count }}</strong>
      </p>
    </section>

    <v-divider class="my-4" />

    <section class="mb-6">
      <h3>Статистика по образованию (в %)</h3>
      <v-btn color="primary" @click="loadEducationStats">Показать</v-btn>
      <v-simple-table class="mt-3" v-if="educationStats">
        <thead>
          <tr>
            <th>Категория</th>
            <th>Процент</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Начальное</td>
            <td>{{ educationStats.primary }}%</td>
          </tr>
          <tr>
            <td>Среднее</td>
            <td>{{ educationStats.secondary }}%</td>
          </tr>
          <tr>
            <td>Высшее</td>
            <td>{{ educationStats.higher }}%</td>
          </tr>
          <tr>
            <td>Ученая степень</td>
            <td>{{ educationStats.degree }}%</td>
          </tr>
        </tbody>
      </v-simple-table>
      <p v-else class="text-muted mt-3">Нет данных.</p>
    </section>
  </v-container>
</template>

<script>
import api from "../api/index.js";

export default {
  data() {
    return {
      readers: [],
      selectedReaderId: null,
      readerBooks: [],
      overdueReaders: [],
      rareBooksReaders: [],
      under20Count: null,
      educationStats: null,
    };
  },
  async mounted() {
    try {
      const res = await api.getReaders();
      this.readers = res.data;
    } catch (e) {
      console.error(e);
    }
  },
  methods: {
    async loadReaderBooks() {
      if (!this.selectedReaderId) return;
      try {
        const res = await api.getReaderBooks(this.selectedReaderId);
        this.readerBooks = res.data;
      } catch (e) {
        console.error(e);
        this.readerBooks = [];
      }
    },
    async loadOverdueReaders() {
      try {
        const res = await api.getIssuesOverdue();
        this.overdueReaders = res.data;
      } catch (e) {
        console.error(e);
        this.overdueReaders = [];
      }
    },
    async loadRareBooksReaders() {
      try {
        const res = await api.getRareBooksReaders();
        this.rareBooksReaders = res.data;
      } catch (e) {
        console.error(e);
        this.rareBooksReaders = [];
      }
    },
    async loadUnder20() {
      try {
        const res = await api.getReadersUnder20();
        this.under20Count = res.data.readers_under_20 ?? null;
      } catch (e) {
        console.error(e);
        this.under20Count = null;
      }
    },
    async loadEducationStats() {
      try {
        const res = await api.getEducationStats();
        this.educationStats = {
          primary: res.data["primary_%"],
          secondary: res.data["secondary_%"],
          higher: res.data["higher_%"],
          degree: res.data["degree_%"],
        };
      } catch (e) {
        console.error(e);
        this.educationStats = null;
      }
    },
  },
};
</script>
```

### 10. Особенности реализации с Vuetify

#### Используемые компоненты Vuetify:

- **v-app** - основной контейнер приложения
- **v-app-bar** - панель навигации
- **v-container** - контейнер для контента
- **v-row/v-col** - система сеток для адаптивной верстки
- **v-btn** - кнопки с различными стилями
- **v-text-field** - текстовые поля ввода
- **v-select** - выпадающие списки
- **v-simple-table** - таблицы для отображения данных
- **v-form** - формы с валидацией
- **v-list** - списки для отображения данных
- **v-divider** - разделители
- **v-spacer** - распорка для выравнивания

#### Преимущества Vuetify:

1. **Material Design** - современный и консистентный дизайн
2. **Адаптивность** - автоматическая адаптация под разные размеры экранов
3. **Темы** - легкая кастомизация цветовой схемы
4. **Доступность** - встроенная поддержка доступности (a11y)
5. **Иконки** - интеграция с Material Design Icons

## Запуск проекта

1. Установка зависимостей:

```bash
npm install
```

2. Запуск сервера разработки:

```bash
npm run dev
```

3. Сборка для продакшена:

```bash
npm run build
```

4. Предпросмотр сборки:

```bash
npm run preview
```

## Архитектурные решения

### 1. Разделение ответственности

- **API модуль** - централизованное взаимодействие с сервером
- **Views** - компоненты страниц
- **Router** - управление навигацией
- **App.vue** - глобальная структура приложения

### 2. Управление состоянием

- **LocalStorage** для хранения токена авторизации
- **Реактивные данные** Vue 3 для управления состоянием компонентов
- **Глобальная навигация** с динамической проверкой аутентификации

### 3. Обработка ошибок

- Централизованная обработка HTTP ошибок в axios interceptor
- Пользовательские сообщения об ошибках
- Graceful degradation при отсутствии данных

### 4. Безопасность

- Автоматическое добавление токена в заголовки
- Защита маршрутов требующих аутентификации
- Корректная обработка выхода из системы

## Интеграция с серверной частью

### 1. CORS настройка

Серверная часть (лабораторная работа №3) была настроена для приема запросов с фронтенда:

```python
# settings.py
INSTALLED_APPS = ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware']
CORS_ALLOW_ALL_ORIGINS = True
```

### 2. Аутентификация

- Токенная аутентификация через Django REST Framework
- Автоматическое сохранение и использование токена
- Обработка истечения срока токена

### 3. API эндпоинты

Полная интеграция со всеми эндпоинтами серверной части:

- CRUD операции для всех сущностей
- Статистические запросы
- Управление пользователями

## Подключение к API

### 1. Создание HTTP клиента с Axios

Для взаимодействия с серверной частью был создан специальный HTTP клиент в файле `src/api/axios.js`:

```javascript
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});
```

**Ключевые параметры:**

- `baseURL: "http://127.0.0.1:8000"` - базовый адрес сервера Django
- `headers: {'Content-Type': 'application/json'}` - формат данных JSON

### 2. Автоматическая аутентификация через Interceptors

Для автоматического добавления токена авторизации был настроен request interceptor:

```javascript
api.interceptors.request.use((config) => {
  const publicAuthEndpoints = [
    "/auth/token/login/",
    "/auth/users/",
    "/auth/token/logout/",
  ];

  const isPublicEndpoint = publicAuthEndpoints.some(
    (endpoint) => config.url === endpoint,
  );

  if (!isPublicEndpoint) {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
  }

  return config;
});
```

**Механизм работы:**

1. Проверяется, является ли эндпоинт публичным (не требующим авторизации)
2. Для защищенных эндпоинтов извлекается токен из localStorage
3. Токен добавляется в заголовок `Authorization: Token ${token}`

### 3. Централизованная обработка ошибок

Response interceptor для обработки ошибок:

```javascript
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error(
      "API Error:",
      error.response?.status,
      error.response?.data || error.message,
    );
    return Promise.reject(error);
  },
);
```

### 4. Создание API функций

В файле `src/api/index.js` были созданы функции для каждого эндпоинта:

#### Аутентификация:

```javascript
async function login(username, password) {
  const res = await api.post("/auth/token/login/", { username, password });
  const token = res.data.auth_token || res.data.token;
  if (token) localStorage.setItem("token", token);
  return res.data;
}

async function getCurrentUser() {
  return api.get("/auth/users/me/");
}
```

#### Работа с книгами:

```javascript
async function getBooks() {
  return api.get("/api/books/");
}

async function createBook(data) {
  return api.post("/api/books/", data);
}

async function updateBook(id, data) {
  return api.put(`/api/books/${id}/`, data);
}
```

#### Статистические запросы:

```javascript
async function getReaderBooks(readerId) {
  return api.get(`/api/readers/${readerId}/books/`);
}

async function getIssuesOverdue() {
  return api.get("/api/issues/overdue/");
}
```

### 5. Использование в Vue компонентах

Пример использования API в компоненте:

```javascript
import api from "../api/index.js";

export default {
  methods: {
    async loadBooks() {
      try {
        const res = await api.getBooks();
        this.books = res.data;
      } catch (e) {
        console.error("Ошибка загрузки книг:", e);
      }
    },

    async createBook() {
      try {
        await api.createBook(this.bookData);
        this.$router.push({ name: "books" });
      } catch (e) {
        alert("Ошибка создания книги");
      }
    },
  },
};
```

### 6. Процесс аутентификации

1. **Вход пользователя:**
   - Отправка POST запроса на `/auth/token/login/`
   - Сохранение полученного токена в localStorage
   - Автоматическое добавление токена в последующие запросы

2. **Проверка токена:**
   - Каждый защищенный запрос включает токен в заголовках
   - Сервер проверяет валидность токена
   - При неверном токене возвращается ошибка 401

3. **Выход из системы:**
   - Отправка POST запроса на `/auth/token/logout/`
   - Удаление токена из localStorage
   - Перенаправление на страницу входа

### 7. Соответствие эндпоинтам сервера

Все API функции соответствуют эндпоинтам, определенным в Django REST Framework:

| Функция            | HTTP метод | Эндпоинт             | Назначение            |
| ------------------ | ---------- | -------------------- | --------------------- |
| `getBooks()`       | GET        | `/api/books/`        | Получение списка книг |
| `createBook()`     | POST       | `/api/books/`        | Создание новой книги  |
| `updateBook()`     | PUT        | `/api/books/{id}/`   | Обновление книги      |
| `deleteBook()`     | DELETE     | `/api/books/{id}/`   | Удаление книги        |
| `login()`          | POST       | `/auth/token/login/` | Аутентификация        |
| `register()`       | POST       | `/auth/users/`       | Регистрация           |
| `getCurrentUser()` | GET        | `/auth/users/me/`    | Текущий пользователь  |

### 8. Обработка CORS

Для разрешения кросс-доменных запросов в Django был настроен CORS:

```python
# settings.py
INSTALLED_APPS = ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware']
CORS_ALLOW_ALL_ORIGINS = True
```

Это позволяет фронтенду на `localhost:5173` обращаться к бэкенду на `localhost:8000`.

## Выводы

В ходе выполнения лабораторной работы были успешно решены все поставленные задачи:

1. **Настроен CORS** для взаимодействия фронтенда и бэкенда
2. **Реализованы интерфейсы аутентификации** (вход, регистрация, профиль)
3. **Созданы интерфейсы для работы** с книгами, залами, читателями, выдачами
4. **Подключена библиотека Vuetify** для создания современного UI
5. **Реализованы статистические отчеты** в соответствии с требованиями
6. **Настроена маршрутизация** с защитой авторизованных страниц
7. **Создана адаптивная верстка** с использованием Material Design

Система готова к использованию и предоставляет полноценный клиентский интерфейс для управления библиотекой с современной архитектурой Vue 3 + Vuetify и надежной интеграцией с Django REST API.
