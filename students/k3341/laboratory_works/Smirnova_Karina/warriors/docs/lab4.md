# Отчет по лабораторной работе №4

## Цель:

Реализация клиентской части приложения средствами vue.js.

### Реализовать CORS:

1. Устанавливаем django-cors-headers

```bash
pip install django-cors-headers
```

2. Добавляем 'corsheaders' в INSTALLED_APPS в settings.py

3. Добавляем corsheaders.middleware.CorsMiddleware в MIDDLEWARE в settings.py

4. Включаем CORS:

Для всех доменов:

```text
CORS_ORIGIN_ALLOW_ALL = True
```

Для указанных:

```text
CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'http//:localhost:8000',
)
```
### Реализовать frontend Vue.js:

**Описание эндпоинтов находится в файле frontendEndpoints.md**

#### Создание проекта:

Инициализируем проект с помощью команд:

```text
npm create vue@latest frontendAirCompany
cd frontend
npm install
```

#### Настройка:

Устанавливаем vuetify:

```text
vue add vuetify
npm install axios vuex vuex-persist
```

Настраиваем файлы для работы vuetify:

store/auth.js
```text
import axios from "axios";

const apiBaseURL = "http://127.0.0.1:8000/api/auth/";

export default {
  namespaced: true,
  state: {
    token: localStorage.getItem('token') || null,
    user: null,
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    setUser(state, user) {
      state.user = user;
    },
    clearAuthData(state) {
      state.token = null;
      state.user = null;
      localStorage.removeItem('token');
    },
  },
  actions: {
    async register(_, userData) {
      await axios.post(apiBaseURL + "users/", userData);
    },
    async login({ commit }, credentials) {
      const response = await axios.post(apiBaseURL + "token/login/", credentials);
      commit("setToken", response.data.auth_token);
    },
    async logout({ commit }) {
      await axios.post(apiBaseURL + "token/logout/", {
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      });
      commit("clearAuthData");
    },
    async getProfile({ commit, state }) {
      if (!state.token) return;
      const response = await axios.get(apiBaseURL + "users/me/", {
        headers: {
          Authorization: `Token ${state.token}`,
        },
      });
      console.log("Получен профиль:", response.data);
      commit("setUser", response.data);
    },
    async logout({ commit }) {
      commit('clearAuthData');
    },
    async updateProfile({ state, dispatch }, userData) {
      console.log("Отправка данных для обновления профиля:", userData);

      if (userData.email && userData.email !== state.user. email) {
        await axios. patch(
          apiBaseURL + "users/me/",
          { email: userData.email },
          {
            headers: {
              Authorization: `Token ${state.token}`,
            },
          }
        );
        console.log("Email обновлён");
      }

      if (userData.username && userData.username !== state.user.username) {
        await axios.post(
          apiBaseURL + "users/set_username/",
          {
            current_password: userData.current_password,
            new_username: userData.username
          },
          {
            headers: {
              Authorization: `Token ${state.token}`,
            },
          }
        );
        console.log("Username обновлён");
      }

      await dispatch("getProfile");
    },
    async changePassword({ state }, passwords) {
      console.log("Смена пароля")
      await axios.post(apiBaseURL + "users/set_password/", passwords, {
        headers: {
          Authorization: `Token ${state.token}`,
        },
      });
    },
  },
};
```

store/index.js
```text
import { createStore } from 'vuex';
import auth from './auth';

export default createStore({
  modules: {
    auth,
  },
});
```

vite.config.js
```text
import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

export default defineConfig({
  plugins: [
    vue({ template: { transformAssetUrls } }),
    vueDevTools(),
    vuetify({ autoImport: true }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
```

plugins/vuetify.js
```text
import { createVuetify } from 'vuetify';
import 'vuetify/styles';

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1976D2',
          secondary: '#424242',
          accent: '#82B1FF',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FB8C00',
        },
      },
    },
  },
});
```

Настраиваем общие файлы:

main.js
```text
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify'
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css';
import store from './store'

const app = createApp(App);

app.use(router);
app.use(vuetify);
app.use(store);
app.mount('#app');
```

App.vue
```text
<template>
  <div id="app">
    <Header />
    <router-view />
  </div>
</template>

<script>
import Header from './components/Header.vue';
export default {
  name: 'App',
  components: {
    Header,
  }
};
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  padding-bottom: 20px;
  min-height: 100vh;
}
</style>
```

Настраиваем маршруты:

router/index.js
```text
import { createRouter, createWebHistory } from 'vue-router';
import FlightList from '../components/FlightList.vue';
import CrewDetails from '../components/CrewDetails.vue';
import RouteDetails from '../components/RouteDetails.vue';
import RoutesList from '../components/RoutesList.vue';
import FlightDetails from '../components/FlightDetails.vue';
import AirlineCompanyList from '../components/AirLineCompanyList.vue';
import CreateCompany from '../components/CreateCompany.vue';
import CreateCrew from '../components/CreateCrew.vue';
import CreateCrewMember from '../components/CreateCrewMember.vue';
import CreateFlight from '../components/CreateFlight.vue';
import CreatePlane from '../components/CreatePlane.vue';
import CreateRoute from '../components/CreateRoute.vue';
import EditRoute from '@/components/EditRoute.vue';
import EditFlight from '../components/EditFlight.vue';
import EditCompany from '@/components/EditCompany.vue';
import PlaneList from '@/components/PlaneList.vue';
import EditPlane from '@/components/EditPlane.vue';
import CrewList from '../components/CrewList.vue';
import EditCrew from '../components/EditCrew.vue';
import EditCrewMember from '../components/EditCrewMember.vue';
import Register from '@/components/Register.vue';
import Login from '@/components/Login.vue';
import Profile from '@/components/Profile.vue';
import VariantTask from '@/components/VariantTask.vue';

const EmptyPage = { template: '<div style="padding: 20px;">Страница создания объекта</div>' };

const routes = [
  {
    path: '/flights',
    name: 'Flights',
    component: FlightList,
  },
  {
    path: '/crews/:id',
    name: 'CrewDetails',
    component: CrewDetails,
    props: true,
  },
  {
    path: '/routes',
    name: 'RoutesList',
    component: RoutesList,
  },
  {
    path: '/route/:id',
    name: 'RouteDetails',
    component: RouteDetails,
    props: true,
  },
  {
    path: '/flight/:id',
    name: 'FlightDetails',
    component: FlightDetails,
    props: true,
  },
  {
    path: '/airlines',
    name: 'AirlineCompanyList',
    component: AirlineCompanyList,
  },
  {
    path: '/edit-company/:id',
    component: EditCompany,
    name: 'EditCompany',
  },
  {
    path: '/create-plane',
    name: 'CreatePlane',
    component: CreatePlane,
  },
  {
    path: '/create-company',
    name: 'CreateCompany',
    component: CreateCompany,
  },
  {
    path: '/create-route',
    name: 'CreateRoute',
    component: CreateRoute,
  },
  {
    path: '/create-crew-member',
    name: 'CreateCrewMember',
    component: CreateCrewMember,
  },
  {
    path: '/create-crew',
    name: 'CreateCrew',
    component: CreateCrew,
  },
  {
    path: '/create-flight',
    name: 'CreateFlight',
    component: CreateFlight,
  },
  {
    path: '/routes',
    component: RoutesList,
    name: 'RoutesList',
  },
  {
    path: '/edit-route/:id',
    component: EditRoute,
    name: 'EditRoute',
  },
  {
    path: '/flights',
    component: FlightList,
    name: 'FlightList',
  },
  {
    path: '/edit-flight/:id',
    component: EditFlight,
    name: 'EditFlight',
  },
  {
    path: '/planes',
    name: 'PlaneList',
    component: PlaneList,
  },
  {
    path: '/edit-plane/:id',
    name: 'EditPlane',
    component: EditPlane,
    props: true,
  },
    {
    path: '/crews',
    name: 'CrewList',
    component: CrewList,
  },
  {
    path: '/edit-crew/:id',
    name: 'EditCrew',
    component: EditCrew,
    props: true,
  },
  {
    path: '/edit-crew-member/:id',
    name: 'EditCrewMember',
    component: EditCrewMember,
    props: true,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
  {
    path: '/variant-task',
    name: 'VariantTask',
    component: VariantTask,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
```

api/index.js
```text
import axios from 'axios';
import store from '@/store/index';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  timeout: 10000,
});

axiosInstance.interceptors.request. use(
  (config) => {
    const token = store.state.auth.token;
    if (token) {
      config.headers. Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const getFlights = () => {
  return axiosInstance.get('/api/flights/');
};

export const getFlight = (flightId) => {
  return axiosInstance.get(`/api/flights/${flightId}/`);
};

export const updateFlight = (flightId, flightData) => {
  return axiosInstance.put(`/api/flights/${flightId}/`, flightData);
};

export const getCrewDetail = (crewId) => {
  return axiosInstance.get(`/api/crews/${crewId}/`);
};

export const getRouteDetail = (routeId) => {
  return axiosInstance.get(`/api/routes/${routeId}/`);
}

export const getAirlineCompanies = () => {
  return axiosInstance.get('/api/airline-companies/');
};

export const getRoutes = () => {
  return axiosInstance.get('/api/routes/');
};

export const getPlanes = () => {
  return axiosInstance.get('/api/planes/');
};

export const getCrews = () => {
  return axiosInstance.get('/api/crews/');
};

export const getCrewDetails = (crewId) => {
  return axiosInstance.get(`/api/crews/${crewId}/`);
};

export const updateCrew = (crewId, crewData) => {
  return axiosInstance.put(`/api/crews/${crewId}/`, crewData);
};

export const getCrewMemberDetails = (memberId) => {
  return axiosInstance.get(`/api/crew-members/${memberId}/`);
};

export const updateCrewMember = (memberId, memberData) => {
  return axiosInstance.put(`/api/crew-members/${memberId}/`, memberData);
};

export const getCrewMembers = () => {
  return axiosInstance.get('/api/crew-members/');
};

export const getCompanyDetails = (companyId) => {
  return axiosInstance.get(`/api/airline-companies/${companyId}/`);
};

export const getPlaneDetails = (planeId) => {
  return axiosInstance.get(`/api/planes/${planeId}/`);
};

export const updateCompany = (companyId, companyData) => {
  return axiosInstance.put(`/api/airline-companies/${companyId}/`, companyData);
};

export const updatePlane = (planeId, planeData) => {
  return axiosInstance.put(`/api/planes/${planeId}/`, planeData);
};

export const createCompany = (companyData) => {
  return axiosInstance.post('/api/airline-companies/', companyData);
};

export const createPlane = (planeData) => {
  return axiosInstance.post('/api/planes/', planeData);
};

export const createRoute = (routeData) => {
  return axiosInstance.post('/api/routes/', routeData);
};

export const createFlight = (flightData) => {
  return axiosInstance.post('/api/flights/', flightData);
};

export const createCrewMember = (crewMemberData) => {
  return axiosInstance.post('/api/crew-members/', crewMemberData);
};

export const createCrew = (crewData) => {
  return axiosInstance.post('/api/crews/', crewData);
};

export const deleteCrewMember = (memberId) => {
  return axiosInstance.delete(`/api/crew-members/${memberId}/`);
};

export const deleteCrew = (crewId) => {
  return axiosInstance.delete(`/api/crews/${crewId}/`);
};

export const deletePlane = (planeId) => {
  return axiosInstance.delete(`/api/planes/${planeId}/`);
};

export const deleteFlight = (flightId) => {
  return axiosInstance.delete(`/api/flights/${flightId}/`);
};

export const deleteRoute = (routeId) => {
  return axiosInstance.delete(`/api/routes/${routeId}/`);
};

export const deleteCompany = (companyId) => {
  return axiosInstance.delete(`/api/airline-companies/${companyId}/`);
};

export default axiosInstance;
```

#### Создание компонентов:

Header:
```text
<template>
  <header class="main-header">
    <nav class="nav-bar">
      <router-link to="/routes" class="nav-link">Маршруты</router-link>
      <router-link to="/flights" class="nav-link">Рейсы</router-link>
      <router-link to="/airlines" class="nav-link">Компании</router-link>
      <router-link to="/planes" class="nav-link">Самолеты</router-link>
      <router-link to="/crews" class="nav-link">Команды</router-link>

      <template v-if="! isAuthenticated">
        <router-link to="/register" class="nav-link">Регистрация</router-link>
        <router-link to="/login" class="nav-link">Войти</router-link>
      </template>
      <template v-else>
        <router-link to="/profile" class="nav-link">Профиль</router-link>
        <button @click="logout" class="nav-link logout-button">Выход</button>
      </template>

      <div class="menu-container">
        <button class="menu-button" @click="toggleSidebar">
          <span class="menu-icon">☰</span>
        </button>
        <div class="sidebar" v-if="showSidebar">
          <ul class="sidebar-links">
            <li><router-link to="/create-plane" @click="toggleSidebar">Создать самолет</router-link></li>
            <li><router-link to="/create-company" @click="toggleSidebar">Создать компанию</router-link></li>
            <li><router-link to="/create-route" @click="toggleSidebar">Создать маршрут</router-link></li>
            <li><router-link to="/create-flight" @click="toggleSidebar">Создать рейс</router-link></li>
            <li><router-link to="/create-crew-member" @click="toggleSidebar">Создать работника</router-link></li>
            <li><router-link to="/create-crew" @click="toggleSidebar">Создать команду</router-link></li>
            <li class="divider"></li>
            <li><router-link to="/variant-task" @click="toggleSidebar">Задание варианта</router-link></li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      showSidebar: false,
    };
  },
  methods: {
    toggleSidebar() {
      this.showSidebar = !this. showSidebar;
    },
    async logout() {
      try {
        await this.$store.dispatch('auth/logout');

        this.$router.push('/login');
      } catch (error) {
        console.error('Ошибка при выходе:', error);
      }
    },
  },
  computed:  {
    isAuthenticated() {
      return !!this.$store.state.auth.token;
    },
  },
};
</script>

<style>
.main-header {
  background-color: #0f4c81;
  padding: 10px;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.nav-link {
  color:  white;
  text-decoration:  none;
  margin:  0 20px;
  font-size: 18px;
}

.nav-link:hover {
  text-decoration:  underline;
}

.logout-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.menu-container {
  position: relative;
  margin-left: 20px;
}

.menu-button {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
}

.menu-icon {
  display:  inline-block;
}

.sidebar {
  position: absolute;
  right: 0;
  top: 100%;
  margin-top: 10px;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
  padding: 10px;
  z-index: 10;
  min-width: 200px;
}

.sidebar-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-links li {
  padding: 5px 10px;
}

.sidebar-links a {
  text-decoration:  none;
  color: #0f4c81;
  font-size: 16px;
  display: block;
}

.sidebar-links a:hover {
  text-decoration: underline;
}

.divider {
  height: 1px;
  background-color:  #ddd;
  margin: 5px 0;
}
</style>
```

AirLineCompanyList.vue
```text
<template>
  <div class="company-list">
    <div class="content-wrapper">
      <h1>Список компаний</h1>

      <div class="search-company">
        <label for="search">Найти компанию по названию:</label>
        <input
          class="search-input"
          type="text"
          id="search"
          v-model="searchName"
          placeholder="Введите название компании"
        />
        <button @click="searchCompany" class="button button-primary">Найти компанию</button>
        <button @click="toggleFilters" class="button button-primary">Фильтры</button>
        <button @click="resetSearch" class="button button-danger">Очистить</button>
      </div>

      <div v-if="filteredCompanies.length > 0" class="companies-container">
        <div class="company-card" v-for="company in filteredCompanies" :key="company.id">
          <div class="company-header">
            <h2>{{ company.name }}</h2>
            <div class="button-group-header">
              <button @click="editCompany(company.id)" class="button button-primary button-small">Редактировать</button>
              <button @click="deleteCompanyItem(company.id)" class="button button-danger button-small">Удалить</button>
            </div>
          </div>

          <div class="section">
            <h3>Самолёты</h3>
            <div v-if="company.planes && company.planes.length > 0" class="items-grid">
              <div class="plane-card" v-for="plane in company.planes" :key="plane.id">
                <p><strong>Номер:</strong> {{ plane.number }}</p>
                <p><strong>Тип:</strong> {{ plane.type }}</p>
                <p><strong>Число мест:</strong> {{ plane. seats_capacity }}</p>
                <p><strong>Скорость:</strong> {{ plane. flight_speed }} км/ч</p>
                <p><strong>В ремонте:</strong> {{ plane. in_repair ? 'Да' : 'Нет' }}</p>
                <div class="button-group">
                  <button @click="editPlane(plane.id)" class="button button-primary button-small">Редактировать</button>
                  <button @click="deletePlane(plane.id)" class="button button-danger button-small">Удалить</button>
                </div>
              </div>
            </div>
            <p v-else class="no-data-small">Нет самолётов</p>
          </div>

          <div class="section">
            <h3>Работники</h3>
            <div v-if="company.crew_members && company.crew_members. length > 0" class="items-grid">
              <div class="employee-card" v-for="member in company.crew_members" :key="member.id">
                <p><strong>ФИО:</strong> {{ member.full_name }}</p>
                <p><strong>Возраст:</strong> {{ member.age }}</p>
                <p><strong>Образование:</strong> {{ member.education }}</p>
                <p><strong>Стаж:</strong> {{ member.work_experience }} лет</p>
                <p><strong>Допуск к рейсу:</strong> {{ member.flight_authorization ?  'Да' : 'Нет' }}</p>
                <p><strong>Должность:</strong> {{ member.position }}</p>
                <div class="button-group">
                  <button @click="editMember(member.id)" class="button button-primary button-small">Редактировать</button>
                  <button @click="deleteMember(member.id)" class="button button-danger button-small">Удалить</button>
                </div>
              </div>
            </div>
            <p v-else class="no-data-small">Нет работников</p>
          </div>
        </div>
      </div>
      <p v-else class="no-data">Нет подходящих компаний. </p>
    </div>

    <div v-if="showFilters" class="filters-panel">
      <h2>Фильтры</h2>
      <label>
        Номер самолета:
        <input type="text" v-model="filters.planeNumber" placeholder="Введите номер самолета" />
      </label><br/>
      <label>
        ФИО работника:
        <input type="text" v-model="filters. employeeName" placeholder="Введите ФИО работника" />
      </label><br/>
      <button @click="applyFilters" class="button button-primary button-full">Найти</button>
    </div>
  </div>
</template>

<script>
import { getAirlineCompanies, deleteCompany, deletePlane, deleteCrewMember } from '../api/index.js';

export default {
  name: 'AirlineCompanyList',
  data() {
    return {
      companies: [],
      searchName: "",
      filteredCompanies: [],
      showFilters: false,
      filters: {
        planeNumber: "",
        employeeName:  "",
      },
      error: null,
    };
  },
  async created() {
    await this.loadCompanies();
  },
  methods: {
    async loadCompanies() {
      try {
        const response = await getAirlineCompanies();
        this.companies = response.data;
        this. filteredCompanies = this. companies;
      } catch (err) {
        this.error = 'Ошибка загрузки информации о компаниях.';
        console.error(err);
      }
    },
    editCompany(id) {
      this.$router.push(`/edit-company/${id}`);
    },
    async deleteCompanyItem(id) {
      if (!confirm("Вы уверены, что хотите удалить компанию?")) {
        return;
      }
      try {
        await deleteCompany(id);
        alert("Компания успешно удалена.");
        this.companies = this.companies.filter(company => company.id !== id);
        this.filteredCompanies = this.filteredCompanies.filter(company => company.id !== id);
      } catch (err) {
        alert("Ошибка удаления компании.");
        console.error(err);
      }
    },
    editPlane(id) {
      this.$router.push(`/edit-plane/${id}`);
    },
    async deletePlane(id) {
      if (!confirm("Вы уверены, что хотите удалить самолет?")) {
        return;
      }
      try {
        await deletePlane(id);
        alert("Самолет успешно удален.");
        await this.loadCompanies();
      } catch (err) {
        alert("Ошибка удаления самолета.");
        console.error(err);
      }
    },
    editMember(memberId) {
      this.$router.push(`/edit-crew-member/${memberId}`);
    },
    async deleteMember(memberId) {
      if (!confirm("Вы уверены, что хотите удалить этого работника?")) {
        return;
      }
      try {
        await deleteCrewMember(memberId);
        alert("Работник успешно удален.");
        await this.loadCompanies();
      } catch (err) {
        alert("Ошибка удаления работника.");
        console.error(err);
      }
    },
    searchCompany() {
      if (this.searchName.trim()) {
        this.filteredCompanies = this.companies.filter(company =>
          company.name.toLowerCase().includes(this.searchName.toLowerCase())
        );
      }
    },
    resetSearch() {
      this.searchName = "";
      this.filters = {
        planeNumber: "",
        employeeName: "",
      };
      this.filteredCompanies = this.companies;
    },
    toggleFilters() {
      this.showFilters = !this. showFilters;
    },
    applyFilters() {
      this.filteredCompanies = this.companies.filter(company => {
        const matchesPlaneNumber =
          !this.filters.planeNumber ||
          (company.planes && company.planes. some(plane =>
            plane.number.toLowerCase().includes(this.filters.planeNumber.toLowerCase())
          ));

        const matchesEmployeeName =
          !this.filters.employeeName ||
          (company.crew_members && company. crew_members.some(member =>
            member.full_name. toLowerCase().includes(this.filters. employeeName.toLowerCase())
          ));

        return matchesPlaneNumber && matchesEmployeeName;
      });
      this.showFilters = false;
    },
  }
};
</script>

<style scoped>
.company-list {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 20px;
  font-size: 28px;
}

.companies-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.company-card {
  background-color: white;
  border:  1px solid #e0e0e0;
  padding: 25px;
  border-radius:  8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.company-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.company-header {
  display: flex;
  justify-content: space-between;
  align-items:  center;
  margin-bottom:  20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e0e0e0;
  flex-wrap: wrap;
  gap: 10px;
}

.company-header h2 {
  margin: 0;
  color:  #333;
  font-size: 24px;
}

.button-group-header {
  display:  flex;
  gap: 10px;
}

.section {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius:  8px;
  border: 1px solid #e9ecef;
}

.section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 20px;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
}

.plane-card,
.employee-card {
  padding: 15px;
  background-color: white;
  border-radius: 6px;
  border: 1px solid #dee2e6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.plane-card:hover,
.employee-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.12);
}

.plane-card p,
.employee-card p {
  margin: 6px 0;
  color:  #555;
  line-height: 1.5;
  font-size: 14px;
}

.search-company {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  background-color: white;
  padding: 20px;
  border-radius:  8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-company label {
  margin-right: 10px;
  font-weight: 500;
  color: #333;
}

.search-input {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius:  5px;
  min-width: 200px;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #007BFF;
}

.button {
  display: inline-block;
  padding: 10px 20px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  white-space: nowrap;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color:  #0056b3;
}

.button.button-danger {
  background-color: rgb(210, 37, 37);
}

.button.button-danger:hover {
  background-color: rgb(180, 20, 20);
}

.button-small {
  padding: 8px 15px;
  font-size:  13px;
}

.button-full {
  width:  100%;
  margin-top: 10px;
}

.button-group {
  display:  flex;
  gap: 10px;
  margin-top: 15px;
}

.button-group.button {
  flex: 1;
}

.filters-panel {
  position: fixed;
  top: 0;
  right: 0;
  height: 100%;
  width: 300px;
  background-color: white;
  border-left: 1px solid #ddd;
  padding: 20px;
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  z-index: 1000;
}

.filters-panel h2 {
  margin-top: 0;
  color:  #333;
}

.filters-panel label {
  display: block;
  margin-bottom: 15px;
  font-weight: 500;
  color: #333;
}

.filters-panel input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-size: 14px;
}

.filters-panel input:focus {
  outline: none;
  border-color: #007BFF;
}

.filters-panel.button {
  margin-top: 20px;
}

.no-data {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  color: #666;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.no-data-small {
  color: #666;
  font-style: italic;
  margin:  0;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .company-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .button-group-header {
    width: 100%;
  }

  .button-group-header.button {
    flex: 1;
  }

  .items-grid {
    grid-template-columns: 1fr;
  }

  .search-company {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    width: 100%;
  }

  .button {
    width: 100%;
  }
}
</style>
```

CreateCompany.vue
```text
<template>
  <div class="create-company">
    <div class="content-wrapper">
      <h1>Создать компанию</h1>

      <div v-if="!isAuthenticated" class="warning">
        <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать компанию.</p>
      </div>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="name">Название компании:</label>
            <input
              type="text"
              id="name"
              v-model="company.name"
              placeholder="Введите название компании"
              required
            />
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Создать</button>
            <button type="button" @click="$router.push('/airlines')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { createCompany } from '../api/index.js';

export default {
  name: 'CreateCompany',
  data() {
    return {
      company: {
        name: '',
      },
    };
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state. auth.token;
    },
  },
  methods: {
    async submitForm() {
      if (!this.company.name.trim()) {
        alert('Название компании не может быть пустым.');
        return;
      }
      try {
        const response = await createCompany(this.company);
        alert('Компания успешно создана.');
        console.log('Результат:', response. data);
        this.resetForm();
        this.$router.push('/airlines');
      } catch (err) {
        console.error('Ошибка создания компании:', err);

        if (err.response && err.response.status === 401) {
          alert('Ошибка:  требуется авторизация.');
        } else if (err. response && err.response.status === 403) {
          alert('Ошибка: доступ запрещён.');
        } else if (err.response && err.response.data) {
          alert(`Ошибка создания компании: ${JSON.stringify(err.response.data)}`);
        } else {
          alert('Ошибка создания компании.');
        }

        console.error(err);
      }
    },
    resetForm() {
      this.company = {
        name: '',
      };
    },
  },
};
</script>

<style scoped>
.create-company {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width:  800px;
  margin:  0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.warning {
  background-color: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 20px;
  color: #856404;
}

.warning p {
  margin: 0;
  font-size:  14px;
}

.warning a {
  color: #007BFF;
  text-decoration: none;
  font-weight: 500;
}

.warning a:hover {
  text-decoration: underline;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom:  20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 10px 15px;
  font-size:  14px;
  border:  1px solid #ddd;
  border-radius: 5px;
  box-sizing:  border-box;
  font-family: Arial, sans-serif;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.button {
  display: inline-block;
  padding: 12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display:  flex;
  gap: 10px;
  margin-top:  30px;
}

.button-group.button {
  flex: 1;
}

@media (max-width:  768px) {
  .content-wrapper {
    padding:  0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .button-group {
    flex-direction:  column;
  }

  .button-group.button {
    width: 100%;
  }
}
</style>
```

CreateCrew.vue
```text
<template>
  <div class="create-crew">
    <div class="content-wrapper">
      <h1>Создать команду</h1>

      <div v-if="!isAuthenticated" class="warning">
        <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать команду.</p>
      </div>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-section">
            <h3>Члены команды</h3>
            <p class="section-description">Выберите участников, которые входят в состав команды</p>

            <div class="members-list">
              <div class="member-checkbox" v-for="member in members" :key="member.id">
                <label :for="'member-' + member.id" class="checkbox-label">
                  <input
                    type="checkbox"
                    :id="'member-' + member.id"
                    :value="member.id"
                    v-model="crew.members"
                  />
                  <span class="member-info">
                    <span class="member-name">{{ member.full_name }}</span>
                    <span class="member-position">{{ member.position }}</span>
                  </span>
                </label>
              </div>
            </div>

            <p v-if="members.length === 0" class="no-data-small">Нет доступных участников</p>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Создать</button>
            <button type="button" @click="$router.push('/crews')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getCrewMembers, createCrew } from '../api/index.js';

export default {
  name: 'CreateCrew',
  data() {
    return {
      crew: {
        members: [],
      },
      members: [],
      error: null,
    };
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state.auth. token;
    },
  },
  async created() {
    try {
      const response = await getCrewMembers();
      this.members = response.data;
    } catch (err) {
      this.error = 'Ошибка загрузки участников экипажа. ';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      try {
        const response = await createCrew(this.crew);
        alert('Команда успешно создана.');
        console.log('Результат:', response.data);
        this.resetForm();
        this.$router.push('/crews');
      } catch (err) {
        console.error('Ошибка создания команды:', err);

        if (err.response && err.response. status === 401) {
          alert('Ошибка:   требуется авторизация.');
        } else if (err. response && err.response.status === 403) {
          alert('Ошибка: доступ запрещён.');
        } else if (err.response && err.response.data) {
          alert(`Ошибка создания команды: ${JSON.stringify(err.response.data)}`);
        } else {
          alert('Ошибка создания команды.');
        }

        console.error(err);
      }
    },
    resetForm() {
      this.crew = {
        members: [],
      };
    },
  },
};
</script>

<style scoped>
.create-crew {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width:  800px;
  margin:  0 auto;
  padding:  0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 30px;
  font-size:  28px;
}

.warning {
  background-color: #fff3cd;
  border:  1px solid #ffc107;
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 20px;
  color: #856404;
}

.warning p {
  margin: 0;
  font-size: 14px;
}

.warning a {
  color: #007BFF;
  text-decoration: none;
  font-weight: 500;
}

.warning a:hover {
  text-decoration:  underline;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 30px;
}

.form-section h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
  font-size: 20px;
}

.section-description {
  margin-bottom: 20px;
  color: #666;
  font-size: 14px;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 400px;
  overflow-y:  auto;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.member-checkbox {
  background-color: white;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  padding: 12px 15px;
  transition: all 0.2s ease;
}

.member-checkbox:hover {
  background-color: #f8f9fa;
  border-color: #007BFF;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  margin:  0;
  font-weight: normal;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  margin-right: 12px;
  cursor: pointer;
  accent-color: #007BFF;
  flex-shrink: 0;
}

.member-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.member-name {
  font-weight:  500;
  color: #333;
  font-size:  14px;
}

.member-position {
  color:  #666;
  font-size: 13px;
}

.button {
  display: inline-block;
  padding: 12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color:  #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top:  30px;
}

.button-group.button {
  flex: 1;
}

.no-data-small {
  color: #666;
  font-style: italic;
  margin:  0;
  padding: 20px;
  text-align: center;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .members-list {
    max-height: 300px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group.button {
    width: 100%;
  }
}
</style>
```

CreateCrewMember.vue
```text
<template>
  <div class="create-crew-member">
    <div class="content-wrapper">
      <h1>Создать члена экипажа</h1>

      <div v-if="!isAuthenticated" class="warning">
        <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать члена экипажа.</p>
      </div>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="full-name">ФИО:</label>
            <input type="text" id="full-name" v-model="crewMember.full_name" placeholder="Введите ФИО" required />
          </div>

          <div class="form-group">
            <label for="age">Возраст:</label>
            <input type="number" id="age" v-model="crewMember.age" placeholder="Введите возраст" required />
          </div>

          <div class="form-group">
            <label for="education">Образование:</label>
            <input type="text" id="education" v-model="crewMember.education" placeholder="Введите образование" required />
          </div>

          <div class="form-group">
            <label for="work-experience">Стаж работы (лет):</label>
            <input type="number" id="work-experience" v-model="crewMember.work_experience" placeholder="Введите стаж" required />
          </div>

          <div class="form-group">
            <label for="passport-info">Паспортные данные:</label>
            <input type="text" id="passport-info" v-model="crewMember.passport_info" placeholder="Введите паспортные данные" required />
          </div>

          <div class="form-group">
            <label for="position">Должность:</label>
            <select id="position" v-model="crewMember.position" required>
              <option value="" disabled selected>Выберите должность</option>
              <option value="командир">Командир</option>
              <option value="второй пилот">Второй пилот</option>
              <option value="штурман">Штурман</option>
              <option value="стюардесса">Стюардесса</option>
              <option value="стюард">Стюард</option>
            </select>
          </div>

          <div class="form-group">
            <label for="company">Компания:</label>
            <select id="company" v-model="crewMember.company_id" required>
              <option value="" disabled selected>Выберите компанию</option>
              <option v-for="company in companies" :value="company.id" :key="company.id">
                {{ company.name }}
              </option>
            </select>
          </div>

          <div class="form-group checkbox-group">
            <label for="flight_authorization">
              <input type="checkbox" id="flight_authorization" v-model="crewMember.flight_authorization" />
              <span>Допуск к рейсу</span>
            </label>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Создать</button>
            <button type="button" @click="$router.push('/crews')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { createCrewMember, getAirlineCompanies } from '../api/index.js';

export default {
  name: 'CreateCrewMember',
  data() {
    return {
      crewMember: {
        full_name: '',
        age: null,
        education: '',
        work_experience:  null,
        passport_info:  '',
        flight_authorization: false,
        company_id: '',
        position: '',
      },
      companies: [],
      error: null,
    };
  },
  async created() {
    try {
      const response = await getAirlineCompanies();
      this.companies = response.data;
    } catch (err) {
      this.error = 'Ошибка загрузки компаний. ';
      console.error(err);
    }
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state.auth. token;
    },
  },
  methods: {
    async submitForm() {
      console.log("Crew member for create:", this.crewMember)
      try {
        const response = await createCrewMember(this.crewMember);
        alert('Член экипажа успешно создан.')
        console.log('Результат:', response.data);
        this.resetForm();
        this.$router.push('/crews');
      } catch(err){
        console.error('Ошибка создания члена экипажа:', err);

        if (err.response && err.response.status === 401) {
          alert('Ошибка:  требуется авторизация.');
        } else if (err. response && err.response.status === 403) {
          alert('Ошибка: доступ запрещён.');
        } else if (err.response && err.response.data) {
          alert(`Ошибка создания члена экипажа: ${JSON.stringify(err.response.data)}`);
        } else {
          alert('Ошибка создания члена экипажа.');
        }

        console.error(err);
      }
    },
    resetForm() {
      this.crewMember = {
        full_name: '',
        age: null,
        education: '',
        work_experience: null,
        passport_info: '',
        flight_authorization: false,
        company_id: '',
        position: '',
      };
    }
  },
};
</script>

<style scoped>
.create-crew-member {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding:  0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.warning {
  background-color: #fff3cd;
  border:  1px solid #ffc107;
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 20px;
  color: #856404;
}

.warning p {
  margin: 0;
  font-size:  14px;
}

.warning a {
  color: #007BFF;
  text-decoration: none;
  font-weight: 500;
}

.warning a:hover {
  text-decoration: underline;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight:  500;
  color:  #333;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 15px;
  font-size:  14px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.checkbox-group label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.checkbox-group input[type="checkbox"] {
  width:  18px;
  height:  18px;
  margin-right: 10px;
  cursor: pointer;
  accent-color: #007BFF;
}

.checkbox-group span {
  font-weight: 500;
  color: #333;
}

.button {
  display: inline-block;
  padding: 12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display:  flex;
  gap: 10px;
  margin-top:  30px;
}

.button-group.button {
  flex: 1;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group.button {
    width: 100%;
  }
}
</style>
```

CreateFlight.vue
```text
<template>
  <div class="create-flight">
    <div class="content-wrapper">
      <h1>Создать рейс</h1>

      <div v-if="!isAuthenticated" class="warning">
        <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать рейс.</p>
      </div>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="flight-number">Номер рейса:</label>
            <input type="number" id="flight-number" v-model="flight.flight_number" placeholder="Введите номер рейса" required />
          </div>

          <div class="form-group">
            <label for="departure-point">Пункт вылета: </label>
            <input type="text" id="departure-point" v-model="flight.departure_point" placeholder="Введите пункт вылета" required />
          </div>

          <div class="form-group">
            <label for="arrival-point">Пункт прилета:</label>
            <input type="text" id="arrival-point" v-model="flight.arrival_point" placeholder="Введите пункт прилета" required />
          </div>

          <div class="form-group">
            <label for="departure-datetime">Дата и время вылета:</label>
            <input type="datetime-local" id="departure-datetime" v-model="flight.departure_datetime" required />
          </div>

          <div class="form-group">
            <label for="arrival-datetime">Дата и время прилета:</label>
            <input type="datetime-local" id="arrival-datetime" v-model="flight.arrival_datetime" required />
          </div>

          <div class="form-group">
            <label for="sold-tickets">Количество проданных билетов:</label>
            <input type="number" id="sold-tickets" v-model="flight.sold_tickets" placeholder="Введите количество проданных билетов" required />
          </div>

          <div class="form-group">
            <label for="route">Маршрут:</label>
            <select id="route" v-model="flight.route" required>
              <option value="" disabled selected>Выберите маршрут</option>
              <option v-for="route in routes" :value="route.id" :key="route.id">
                {{ route.departure_point }} → {{ route.destination_point }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="plane">Самолет:</label>
            <select id="plane" v-model="flight.plane" required>
              <option value="" disabled selected>Выберите самолет</option>
              <option v-for="plane in planes" :value="plane.id" :key="plane.id">
                {{ plane.number }} — {{ plane.type }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="crew">Экипаж (можно выбрать несколько):</label>
            <select id="crew" multiple v-model="flight.crew" required class="multi-select">
              <option v-for="crew in crews" :value="crew.id" :key="crew.id">
                Команда №{{ crew.id }}
              </option>
            </select>
            <small class="form-hint">Удерживайте Ctrl (Cmd на Mac) для выбора нескольких команд</small>
          </div>

          <div class="form-group checkbox-group">
            <label for="is_transit">
              <input type="checkbox" id="is_transit" v-model="flight.is_transit" />
              <span>Транзитный рейс</span>
            </label>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Создать</button>
            <button type="button" @click="$router.push('/flights')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getRoutes, getPlanes, getCrews, createFlight } from '@/api';

export default {
  name: 'CreateFlight',
  data() {
    return {
      flight: {
        flight_number: null,
        departure_point: '',
        arrival_point:  '',
        departure_datetime: '',
        arrival_datetime: '',
        sold_tickets: null,
        route: '',
        plane: '',
        crew: [],
        is_transit:  false,
      },
      routes: [],
      planes: [],
      crews: [],
      error:  null,
    };
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state.auth.token;
    },
  },
  async created() {
    try {
      const [routesResponse, planesResponse, crewsResponse] = await Promise. all([
        getRoutes(),
        getPlanes(),
        getCrews(),
      ]);
      this.routes = routesResponse.data;
      this.planes = planesResponse. data;
      this.crews = crewsResponse.data;
    } catch (err) {
      this.error = 'Ошибка загрузки данных.';
      console. error(err);
    }
  },
  methods: {
    async submitForm() {
      try {
        const flightData = {
          ...this.flight,
          departure_datetime: this.formatDate(this.flight. departure_datetime),
          arrival_datetime: this.formatDate(this.flight.arrival_datetime),
        };
        const response = await createFlight(flightData);
        alert('Рейс успешно создан.');
        this.resetForm();
        console.log(response.data);
        this.$router.push('/flights');
      } catch (err) {
        console.error('Ошибка создания рейса:', err);

        if (err.response && err.response. status === 401) {
          alert('Ошибка:  требуется авторизация.');
        } else if (err. response && err.response.status === 403) {
          alert('Ошибка: доступ запрещён.');
        } else if (err.response && err.response.data) {
          alert(`Ошибка создания рейса: ${JSON.stringify(err.response.data)}`);
        } else {
          alert('Ошибка создания рейса.');
        }

        console.error(err);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
    },
    resetForm() {
      this.flight = {
        flight_number: null,
        departure_point: '',
        arrival_point: '',
        departure_datetime:  '',
        arrival_datetime: '',
        sold_tickets: null,
        route: '',
        plane: '',
        crew: [],
        is_transit: false,
      };
    }
  },
};
</script>

<style scoped>
.create-flight {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width:  800px;
  margin:  0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 30px;
  font-size:  28px;
}

.warning {
  background-color: #fff3cd;
  border: 1px solid #ffc107;
  border-radius:  8px;
  padding: 15px 20px;
  margin-bottom: 20px;
  color: #856404;
}

.warning p {
  margin: 0;
  font-size: 14px;
}

.warning a {
  color: #007BFF;
  text-decoration: none;
  font-weight: 500;
}

.warning a:hover {
  text-decoration: underline;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color:  #333;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 15px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.multi-select {
  min-height: 120px;
}

.form-hint {
  display: block;
  margin-top: 5px;
  font-size: 12px;
  color: #666;
  font-style: italic;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.checkbox-group input[type="checkbox"] {
  width:  18px;
  height:  18px;
  margin-right: 10px;
  cursor: pointer;
  accent-color: #007BFF;
}

.checkbox-group span {
  font-weight: 500;
  color:  #333;
}

.button {
  display: inline-block;
  padding: 12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color:  #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display:  flex;
  gap: 10px;
  margin-top:  30px;
}

.button-group.button {
  flex: 1;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group . button {
    width: 100%;
  }
}
</style>
```

CreatePlane.vue
```text
<template>
  <div class="create-flight">
    <div class="content-wrapper">
      <h1>Создать рейс</h1>

      <div v-if="!isAuthenticated" class="warning">
        <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать рейс.</p>
      </div>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="flight-number">Номер рейса:</label>
            <input type="number" id="flight-number" v-model="flight.flight_number" placeholder="Введите номер рейса" required />
          </div>

          <div class="form-group">
            <label for="departure-point">Пункт вылета: </label>
            <input type="text" id="departure-point" v-model="flight.departure_point" placeholder="Введите пункт вылета" required />
          </div>

          <div class="form-group">
            <label for="arrival-point">Пункт прилета:</label>
            <input type="text" id="arrival-point" v-model="flight.arrival_point" placeholder="Введите пункт прилета" required />
          </div>

          <div class="form-group">
            <label for="departure-datetime">Дата и время вылета:</label>
            <input type="datetime-local" id="departure-datetime" v-model="flight.departure_datetime" required />
          </div>

          <div class="form-group">
            <label for="arrival-datetime">Дата и время прилета:</label>
            <input type="datetime-local" id="arrival-datetime" v-model="flight.arrival_datetime" required />
          </div>

          <div class="form-group">
            <label for="sold-tickets">Количество проданных билетов:</label>
            <input type="number" id="sold-tickets" v-model="flight.sold_tickets" placeholder="Введите количество проданных билетов" required />
          </div>

          <div class="form-group">
            <label for="route">Маршрут:</label>
            <select id="route" v-model="flight.route" required>
              <option value="" disabled selected>Выберите маршрут</option>
              <option v-for="route in routes" :value="route.id" :key="route.id">
                {{ route.departure_point }} → {{ route.destination_point }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="plane">Самолет:</label>
            <select id="plane" v-model="flight.plane" required>
              <option value="" disabled selected>Выберите самолет</option>
              <option v-for="plane in planes" :value="plane.id" :key="plane.id">
                {{ plane.number }} — {{ plane.type }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="crew">Экипаж (можно выбрать несколько):</label>
            <select id="crew" multiple v-model="flight.crew" required class="multi-select">
              <option v-for="crew in crews" :value="crew.id" :key="crew.id">
                Команда №{{ crew.id }}
              </option>
            </select>
            <small class="form-hint">Удерживайте Ctrl (Cmd на Mac) для выбора нескольких команд</small>
          </div>

          <div class="form-group checkbox-group">
            <label for="is_transit">
              <input type="checkbox" id="is_transit" v-model="flight.is_transit" />
              <span>Транзитный рейс</span>
            </label>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Создать</button>
            <button type="button" @click="$router.push('/flights')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getRoutes, getPlanes, getCrews, createFlight } from '@/api';

export default {
  name: 'CreateFlight',
  data() {
    return {
      flight: {
        flight_number: null,
        departure_point: '',
        arrival_point:  '',
        departure_datetime: '',
        arrival_datetime: '',
        sold_tickets: null,
        route: '',
        plane: '',
        crew: [],
        is_transit:  false,
      },
      routes: [],
      planes: [],
      crews: [],
      error:  null,
    };
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state.auth.token;
    },
  },
  async created() {
    try {
      const [routesResponse, planesResponse, crewsResponse] = await Promise. all([
        getRoutes(),
        getPlanes(),
        getCrews(),
      ]);
      this.routes = routesResponse.data;
      this.planes = planesResponse. data;
      this.crews = crewsResponse.data;
    } catch (err) {
      this.error = 'Ошибка загрузки данных.';
      console. error(err);
    }
  },
  methods: {
    async submitForm() {
      try {
        const flightData = {
          ...this.flight,
          departure_datetime: this.formatDate(this.flight. departure_datetime),
          arrival_datetime: this.formatDate(this.flight.arrival_datetime),
        };
        const response = await createFlight(flightData);
        alert('Рейс успешно создан.');
        this.resetForm();
        console.log(response.data);
        this.$router.push('/flights');
      } catch (err) {
        console.error('Ошибка создания рейса:', err);

        if (err.response && err.response. status === 401) {
          alert('Ошибка:  требуется авторизация.');
        } else if (err. response && err.response.status === 403) {
          alert('Ошибка: доступ запрещён.');
        } else if (err.response && err.response.data) {
          alert(`Ошибка создания рейса: ${JSON.stringify(err.response.data)}`);
        } else {
          alert('Ошибка создания рейса.');
        }

        console.error(err);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
    },
    resetForm() {
      this.flight = {
        flight_number: null,
        departure_point: '',
        arrival_point: '',
        departure_datetime:  '',
        arrival_datetime: '',
        sold_tickets: null,
        route: '',
        plane: '',
        crew: [],
        is_transit: false,
      };
    }
  },
};
</script>

<style scoped>
.create-flight {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width:  800px;
  margin:  0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 30px;
  font-size:  28px;
}

.warning {
  background-color: #fff3cd;
  border: 1px solid #ffc107;
  border-radius:  8px;
  padding: 15px 20px;
  margin-bottom: 20px;
  color: #856404;
}

.warning p {
  margin: 0;
  font-size: 14px;
}

.warning a {
  color: #007BFF;
  text-decoration: none;
  font-weight: 500;
}

.warning a:hover {
  text-decoration: underline;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color:  #333;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 15px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.multi-select {
  min-height: 120px;
}

.form-hint {
  display: block;
  margin-top: 5px;
  font-size: 12px;
  color: #666;
  font-style: italic;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.checkbox-group input[type="checkbox"] {
  width:  18px;
  height:  18px;
  margin-right: 10px;
  cursor: pointer;
  accent-color: #007BFF;
}

.checkbox-group span {
  font-weight: 500;
  color:  #333;
}

.button {
  display: inline-block;
  padding: 12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color:  #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display:  flex;
  gap: 10px;
  margin-top:  30px;
}

.button-group.button {
  flex: 1;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group . button {
    width: 100%;
  }
}
</style>
```

CreateRoute.vue
```text
<template>
  <div class="create-route">
    <div class="content-wrapper">
      <h1>Создать маршрут</h1>

      <div v-if="! isAuthenticated" class="warning">
        <p>Вы должны <router-link to="/login">войти</router-link>, чтобы создать маршрут.</p>
      </div>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="departure-point">Пункт вылета:</label>
            <input type="text" id="departure-point" v-model="route.departure_point" placeholder="Введите пункт вылета" required />
          </div>

          <div class="form-group">
            <label for="destination-point">Пункт назначения:</label>
            <input type="text" id="destination-point" v-model="route. destination_point" placeholder="Введите пункт назначения" required />
          </div>

          <div class="form-group">
            <label for="distance">Расстояние (км):</label>
            <input type="number" id="distance" v-model="route.distance" placeholder="Введите расстояние" required />
          </div>

          <div class="form-group">
            <label for="landing-points">Пункты посадки:</label>
            <textarea id="landing-points" v-model="route.landing_points" placeholder="Введите пункты посадки (через запятую)" rows="3"></textarea>
          </div>

          <div class="form-group">
            <label for="transit-landings">Транзитные посадки:</label>
            <textarea id="transit-landings" v-model="route.transit_landings" placeholder="Введите транзитные посадки (через запятую)" rows="3"></textarea>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Создать</button>
            <button type="button" @click="$router.push('/routes')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { createRoute } from '../api/index.js';

export default {
  name: 'CreateRoute',
  data() {
    return {
      route: {
        departure_point: '',
        destination_point: '',
        distance:  null,
        landing_points:  '',
        transit_landings:  '',
      },
    };
  },
  computed: {
    isAuthenticated() {
      return !!this.$store.state.auth.token;
    },
  },
  methods: {
    async submitForm() {
      try {
        const response = await createRoute(this.route);
        alert('Маршрут успешно создан.')
        console.log('Результат:', response.data);
        this.resetForm();
        this.$router.push('/routes');
      } catch(err){
        console.error('Ошибка создания маршрута:', err);

        if (err.response && err. response.status === 401) {
          alert('Ошибка:  требуется авторизация.');
        } else if (err.response && err.response.status === 403) {
          alert('Ошибка: доступ запрещён.');
        } else if (err.response && err.response.data) {
          alert(`Ошибка создания маршрута: ${JSON.stringify(err.response.data)}`);
        } else {
          alert('Ошибка создания маршрута.');
        }

        console.error(err);
      }
    },
    resetForm() {
      this.route = {
        departure_point:  '',
        destination_point: '',
        distance: null,
        landing_points: '',
        transit_landings: '',
      };
    }
  },
};
</script>

<style scoped>
.create-route {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width:  800px;
  margin:  0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.warning {
  background-color: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 20px;
  color: #856404;
}

.warning p {
  margin: 0;
  font-size:  14px;
}

.warning a {
  color: #007BFF;
  text-decoration: none;
  font-weight: 500;
}

.warning a:hover {
  text-decoration: underline;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom:  20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px 15px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.button {
  display: inline-block;
  padding: 12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.button-group.button {
  flex: 1;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group.button {
    width: 100%;
  }
}
</style>
```

CrewDetails.vue
```text
<template>
  <div class="crew-details">
    <h1>Детали команды №{{ crewId }}</h1>
    <ul>
      <li v-for="member in crewMembers" :key="member.id">
        ФИО: {{ member.full_name }}
        | Возраст: {{ member.age }}
        | Должность: {{ member.position }}
      </li>
    </ul>
    <p v-if="crewMembers.length === 0">Данные о команде недоступны</p>
  </div>
</template>

<script>
import { getCrewDetail } from '../api/index.js';
export default {
  name: 'CrewDetails',
  props: ['id'],
  data() {
    return {
      crewId: this.id,
      crewMembers: [],
      error: null,
    };
  },
  async created() {
    try {
      const response = await getCrewDetail(this.crewId);
      this.crewMembers = response.data.members;
    } catch (err) {
      this.error = 'Ошибка загрузки данных экипажа.';
      console.error(err);
    }
  },
};
</script>

<style>
.crew-details {
  margin: 20px;
}

h1 {
  font-size: 24px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}
</style>
```

CrewList.vue
```text
<template>
  <div class="crew-list">
    <div class="content-wrapper">
      <h1>Список команд</h1>

      <div class="search-crew">
        <label for="search">Найти команду по номеру:</label>
        <input
          class="search-input"
          type="text"
          id="search"
          v-model="searchId"
          placeholder="Введите номер команды"
        />
        <button @click="searchCrew" class="button button-primary">Найти команду</button>
        <button @click="toggleFilters" class="button button-primary">Фильтры</button>
        <button @click="resetSearch" class="button button-danger">Очистить</button>
      </div>

      <div v-if="filteredCrews.length > 0" class="crews-container">
        <div class="crew-card" v-for="crew in filteredCrews" :key="crew.id">
          <div class="crew-header">
            <h2>Команда №{{ crew.id }}</h2>
            <div class="button-group-header">
              <button @click="editCrew(crew.id)" class="button button-primary button-small">Редактировать команду</button>
              <button @click="deleteCrew(crew.id)" class="button button-danger button-small">Удалить команду</button>
            </div>
          </div>

          <div class="section">
            <h3>Участники команды</h3>
            <div v-if="crew.members && crew.members.length > 0" class="members-grid">
              <div class="member-card" v-for="member in crew.members" :key="member. id">
                <p><strong>ФИО:</strong> {{ member. full_name }}</p>
                <p><strong>Возраст:</strong> {{ member. age }}</p>
                <p><strong>Образование:</strong> {{ member.education }}</p>
                <p><strong>Стаж:</strong> {{ member. work_experience }} лет</p>
                <p><strong>Допуск к рейсу:</strong> {{ member.flight_authorization ?  'Да' : 'Нет' }}</p>
                <p><strong>Должность:</strong> {{ member.position }}</p>
                <div class="button-group">
                  <button @click="editMember(member.id)" class="button button-primary">Редактировать</button>
                  <button @click="deleteMember(member.id, crew.id)" class="button button-danger">Удалить</button>
                </div>
              </div>
            </div>
            <p v-else class="no-data-small">Нет участников в команде</p>
          </div>
        </div>
      </div>
      <p v-else class="no-data">Нет доступных команд</p>
    </div>

    <div v-if="showFilters" class="filters-panel">
      <h2>Фильтр</h2>
      <label>
        ФИО участника:
        <input type="text" v-model="filters. memberName" placeholder="Введите ФИО участника" />
      </label><br/>
      <button @click="applyFilters" class="button button-primary button-full">Найти</button>
    </div>
  </div>
</template>

<script>
import { getCrews, deleteCrew, deleteCrewMember } from '../api/index.js';

export default {
  name: 'CrewList',
  data() {
    return {
      crews: [],
      searchId:  "",
      filteredCrews: [],
      showFilters: false,
      filters: {
        memberName: "",
      },
      error: null,
    };
  },
  async created() {
    await this.loadCrews();
  },
  methods: {
    async loadCrews() {
      try {
        const response = await getCrews();
        this.crews = response.data;
        this.filteredCrews = this.crews;
      } catch (err) {
        this.error = 'Ошибка загрузки информации о командах.';
        console.error(err);
      }
    },
    editCrew(id) {
      this.$router.push(`/edit-crew/${id}`);
    },
    editMember(memberId) {
      this.$router.push(`/edit-crew-member/${memberId}`);
    },
    async deleteCrew(crewId) {
      if (!confirm("Вы уверены, что хотите удалить всю команду?")) {
        return;
      }
      try {
        await deleteCrew(crewId);
        alert("Команда успешно удалена.");
        this.crews = this.crews.filter(crew => crew.id !== crewId);
        this.filteredCrews = this.filteredCrews.filter(crew => crew.id !== crewId);
      } catch (err) {
        alert("Ошибка удаления команды.");
        console.error(err);
      }
    },
    async deleteMember(memberId, crewId) {
      if (!confirm("Вы уверены, что хотите удалить этого участника из команды?")) {
        return;
      }
      try {
        await deleteCrewMember(memberId);
        alert("Участник успешно удален.");
        await this.loadCrews();
      } catch (err) {
        alert("Ошибка удаления участника.");
        console.error(err);
      }
    },
    searchCrew() {
      const crewId = parseInt(this.searchId, 10);
      if (!isNaN(crewId)) {
        this.filteredCrews = this.crews.filter(crew => crew.id === crewId);
      }
    },
    resetSearch() {
      this.searchId = "";
      this.filters = {
        memberName: "",
      };
      this.filteredCrews = this. crews;
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;
    },
    applyFilters() {
      this.filteredCrews = this.crews.filter(crew => {
        const matchesMemberName =
          !this.filters. memberName ||
          (crew.members && crew.members. some(member =>
            member.full_name. toLowerCase().includes(this.filters. memberName.toLowerCase())
          ));

        return matchesMemberName;
      });
      this.showFilters = false;
    },
  },
};
</script>

<style scoped>
.crew-list {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.search-crew {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-crew label {
  margin-right: 10px;
  font-weight: 500;
  color: #333;
}

.search-input {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  min-width: 200px;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #007BFF;
}

.crews-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.crew-card {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 25px;
  border-radius:  8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.crew-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.crew-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e0e0e0;
  flex-wrap: wrap;
  gap: 10px;
}

.crew-header h2 {
  margin: 0;
  color:  #333;
  font-size: 24px;
}

.button-group-header {
  display:  flex;
  gap: 10px;
  flex-wrap: wrap;
}

.section {
  margin-top: 20px;
  padding:  15px;
  background-color:  #f8f9fa;
  border-radius: 8px;
  border:  1px solid #e9ecef;
}

.section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 20px;
}

.members-grid {
  display: grid;
  grid-template-columns:  repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
}

.member-card {
  padding: 15px;
  background-color: white;
  border-radius: 6px;
  border: 1px solid #dee2e6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.member-card:hover {
  transform:  translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.12);
}

.member-card p {
  margin: 6px 0;
  color:  #555;
  line-height: 1.5;
  font-size: 14px;
}

.button {
  display: inline-block;
  padding: 10px 20px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  white-space: nowrap;
  font-weight:  500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-danger {
  background-color:  rgb(210, 37, 37);
}

.button.button-danger:hover {
  background-color: rgb(180, 20, 20);
}

.button-small {
  padding: 8px 15px;
  font-size:  13px;
}

.button-full {
  width: 100%;
  margin-top: 10px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.button-group.button {
  flex: 1;
}

.filters-panel {
  position:  fixed;
  top: 0;
  right: 0;
  height: 100%;
  width: 300px;
  background-color: white;
  border-left: 1px solid #ddd;
  padding: 20px;
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  z-index:  1000;
}

.filters-panel h2 {
  margin-top: 0;
  color: #333;
}

.filters-panel label {
  display: block;
  margin-bottom: 15px;
  font-weight: 500;
  color: #333;
}

.filters-panel input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-size:  14px;
}

.filters-panel input:focus {
  outline: none;
  border-color: #007BFF;
}

.filters-panel . button {
  margin-top:  20px;
}

.no-data {
  background-color: white;
  padding:  20px;
  border-radius: 8px;
  text-align: center;
  color: #666;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.no-data-small {
  color: #666;
  font-style: italic;
  margin:  0;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .search-crew {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    width: 100%;
  }

  .button {
    width: 100%;
  }

  .crew-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .button-group-header {
    width: 100%;
  }

  .button-group-header.button {
    flex: 1;
  }

  .members-grid {
    grid-template-columns: 1fr;
  }
}
</style>
```

EditCompany.vue
```text
<template>
  <div class="edit-company">
    <div class="content-wrapper">
      <h1>Редактирование компании «{{ company.name }}»</h1>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="name">Название компании:</label>
            <input
              type="text"
              id="name"
              v-model="company.name"
              placeholder="Введите название компании"
              required
            />
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Сохранить</button>
            <button type="button" @click="$router. push('/airlines')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getCompanyDetails, updateCompany } from '../api/index.js';

export default {
  name:  'EditCompany',
  data() {
    return {
      company: {
        name:  '',
      },
      error:  null,
    };
  },
  async created() {
    const companyId = this.$route.params.id;
    try {
      const response = await getCompanyDetails(companyId);
      this.company = response. data;
    } catch (err) {
      this.error = 'Ошибка загрузки данных компании. ';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      const companyId = this.$route.params. id;
      try {
        await updateCompany(companyId, this.company);
        alert('Компания успешно обновлена.');
        this.$router.push('/airlines');
      } catch (err) {
        alert('Ошибка обновления компании.');
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
.edit-company {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height:  100vh;
  padding:  20px 0;
}

.content-wrapper {
  max-width:  800px;
  margin:  0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color:  #333;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 10px 15px;
  font-size:  14px;
  border:  1px solid #ddd;
  border-radius: 5px;
  box-sizing:  border-box;
  font-family: Arial, sans-serif;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow:  0 0 0 3px rgba(0, 123, 255, 0.1);
}

.button {
  display: inline-block;
  padding: 12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color:  #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.button-group.button {
  flex: 1;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding:  20px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group.button {
    width: 100%;
  }
}
</style>
```

EditCrew.vue
```text
<template>
  <div class="edit-crew">
    <div class="content-wrapper">
      <h1>Редактирование команды №{{ crew.id }}</h1>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-section">
            <h3>Участники команды</h3>
            <p class="section-description">Выберите участников, которые входят в состав команды</p>

            <div class="members-list">
              <div class="member-checkbox" v-for="member in allMembers" :key="member.id">
                <label :for="`member-${member.id}`" class="checkbox-label">
                  <input
                    type="checkbox"
                    :id="`member-${member.id}`"
                    :value="member.id"
                    v-model="selectedMemberIds"
                  />
                  <span class="member-info">
                    <span class="member-name">{{ member.full_name }}</span>
                    <span class="member-position">{{ member.position }}</span>
                  </span>
                </label>
              </div>
            </div>

            <p v-if="allMembers.length === 0" class="no-data-small">Нет доступных участников</p>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Сохранить изменения</button>
            <button type="button" @click="$router.push('/crews')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getCrewDetails, updateCrew, getCrewMembers } from '../api/index.js';

export default {
  name: 'EditCrew',
  data() {
    return {
      crew: {
        id: null,
      },
      allMembers: [],
      selectedMemberIds: [],
      error: null,
    };
  },
  async created() {
    const crewId = this.$route.params.id;
    try {
      const [crewResponse, membersResponse] = await Promise.all([
        getCrewDetails(crewId),
        getCrewMembers(),
      ]);

      this.crew = crewResponse.data;
      this.allMembers = membersResponse.data;

      this.selectedMemberIds = this. crew.members.map((member) => member.id);
    } catch (err) {
      this.error = 'Ошибка загрузки данных.';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      const crewId = this.$route.params.id;
      try {
        const updatedCrewData = {
          id: crewId,
          member_ids: this.selectedMemberIds,
        };
        await updateCrew(crewId, updatedCrewData);
        alert('Команда успешно обновлена.');
        this.$router.push('/crews');
      } catch (err) {
        alert('Ошибка сохранения изменений.');
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
.edit-crew {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color:  #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 30px;
}

.form-section h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
  font-size: 20px;
}

.section-description {
  margin-bottom: 20px;
  color: #666;
  font-size: 14px;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 400px;
  overflow-y:  auto;
  padding:  15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.member-checkbox {
  background-color: white;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  padding: 12px 15px;
  transition: all 0.2s ease;
}

.member-checkbox:hover {
  background-color: #f8f9fa;
  border-color: #007BFF;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  margin:  0;
  font-weight: normal;
}

.checkbox-label input[type="checkbox"] {
  width:  18px;
  height:  18px;
  margin-right: 12px;
  cursor: pointer;
  accent-color: #007BFF;
  flex-shrink: 0;
}

.member-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.member-name {
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.member-position {
  color: #666;
  font-size: 13px;
}

.button {
  display: inline-block;
  padding: 12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.button-group.button {
  flex: 1;
}

.no-data-small {
  color: #666;
  font-style: italic;
  margin:  0;
  padding: 20px;
  text-align: center;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .members-list {
    max-height: 300px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group.button {
    width: 100%;
  }
}
</style>
```

EditCrewMember.vue
```text
<template>
  <div class="edit-member">
    <div class="content-wrapper">
      <h1>Редактирование участника {{ member.full_name }}</h1>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="full_name">ФИО:</label>
            <input type="text" id="full_name" v-model="member.full_name" placeholder="Введите ФИО" required />
          </div>

          <div class="form-group">
            <label for="age">Возраст:</label>
            <input type="number" id="age" v-model="member.age" placeholder="Введите возраст" required />
          </div>

          <div class="form-group">
            <label for="education">Образование:</label>
            <input type="text" id="education" v-model="member.education" placeholder="Введите образование" required />
          </div>

          <div class="form-group">
            <label for="work_experience">Стаж работы (лет):</label>
            <input type="number" id="work_experience" v-model="member.work_experience" placeholder="Введите стаж работы" required />
          </div>

          <div class="form-group">
            <label for="passport_info">Паспортные данные:</label>
            <input type="text" id="passport_info" v-model="member.passport_info" placeholder="Введите паспортные данные" required />
          </div>

          <div class="form-group">
            <label for="flight_authorization">Допуск к рейсу:</label>
            <select id="flight_authorization" v-model="member. flight_authorization" required>
              <option :value="true">Да</option>
              <option :value="false">Нет</option>
            </select>
          </div>

          <div class="form-group">
            <label for="position">Должность:</label>
            <select id="position" v-model="member.position" required>
              <option value="" disabled selected>Выберите должность</option>
              <option value="командир">Командир</option>
              <option value="второй пилот">Второй пилот</option>
              <option value="штурман">Штурман</option>
              <option value="стюардесса">Стюардесса</option>
              <option value="стюард">Стюард</option>
            </select>
          </div>

          <div class="form-group">
            <label for="company">Компания:</label>
            <select id="company" v-model="member.company" required>
              <option v-for="company in companies" :value="company.id" :key="company.id">
                {{ company.name }}
              </option>
            </select>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Сохранить изменения</button>
            <button type="button" @click="$router.push('/crews')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getCrewMemberDetails, updateCrewMember, getAirlineCompanies } from '../api/index.js';

export default {
  name: 'EditCrewMember',
  data() {
    return {
      member: {
        full_name: '',
        age: null,
        education:  '',
        work_experience: null,
        passport_info: '',
        flight_authorization: false,
        position: '',
        company: null,
      },
      companies: [],
      error: null,
    };
  },
  async created() {
    const memberId = this.$route.params.id;
    try {
      const [memberResponse, companiesResponse] = await Promise.all([
        getCrewMemberDetails(memberId),
        getAirlineCompanies(),
      ]);
      this.member = memberResponse.data;
      this.companies = companiesResponse.data;
    } catch (err) {
      this.error = 'Ошибка загрузки данных.';
      console.error(err);
    }
  },
  methods:  {
    async submitForm() {
      const memberId = this.$route.params.id;
      const updatedData = {
        ...this.member,
        company_id: this.member.company,
      };
      console.log("Data:", updatedData)
      try {
        await updateCrewMember(memberId, updatedData);
        alert('Информация об участнике успешно обновлена.');
        this.$router.push('/crews');
      } catch (err) {
        alert('Ошибка сохранения изменений.');
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
.edit-member {
  font-family:  Arial, sans-serif;
  background-color: #f5f5f5;
  min-height:  100vh;
  padding:  20px 0;
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color:  #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom:  20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 15px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow:  0 0 0 3px rgba(0, 123, 255, 0.1);
}

.button {
  display: inline-block;
  padding:  12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.button-group.button {
  flex: 1;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding:  20px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group . button {
    width: 100%;
  }
}
</style>
```

EditFlight.vue
```text
<template>
  <div class="edit-flight">
    <div class="content-wrapper">
      <h1>Редактировать рейс №{{ flight.flight_number }}</h1>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="departure_point">Пункт вылета:</label>
            <input type="text" id="departure_point" v-model="flight.departure_point" required />
          </div>

          <div class="form-group">
            <label for="arrival_point">Пункт прилета:</label>
            <input type="text" id="arrival_point" v-model="flight.arrival_point" required />
          </div>

          <div class="form-group">
            <label for="departure_datetime">Дата вылета:</label>
            <input type="datetime-local" id="departure_datetime" v-model="flight.departure_datetime" required />
          </div>

          <div class="form-group">
            <label for="arrival_datetime">Дата прилета:</label>
            <input type="datetime-local" id="arrival_datetime" v-model="flight.arrival_datetime" required />
          </div>

          <div class="form-group">
            <label for="sold_tickets">Количество проданных билетов:</label>
            <input type="number" id="sold_tickets" v-model="flight.sold_tickets" required />
          </div>

          <div class="form-group checkbox-group">
            <label for="is_transit">
              <input type="checkbox" id="is_transit" v-model="flight.is_transit" />
              <span>Транзитный рейс</span>
            </label>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Сохранить</button>
            <button type="button" @click="$router.push('/flights')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getFlight, updateFlight } from '../api/index.js';

export default {
  name: 'EditFlight',
  data() {
    return {
      flight: {
        flight_number: '',
        departure_point:  '',
        arrival_point: '',
        departure_datetime: '',
        arrival_datetime: '',
        sold_tickets: '',
        is_transit: false,
      },
      error: null,
    };
  },
  async created() {
    const flightId = this.$route.params.id;
    try {
      const response = await getFlight(flightId);
      const flightData = response.data;

      this.flight.departure_datetime = this.formatDate(flightData. departure_datetime);
      this.flight.arrival_datetime = this. formatDate(flightData.arrival_datetime);

      this.flight = {
        ...flightData,
        departure_datetime: this.flight.departure_datetime,
        arrival_datetime: this.flight.arrival_datetime,
      };
    } catch (err) {
      this.error = 'Ошибка загрузки данных рейса.';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      const flightId = this.$route.params.id;

      const updateData = {
        flight_number: this.flight. flight_number,
        departure_point: this.flight.departure_point,
        arrival_point:  this.flight.arrival_point,
        departure_datetime: this. formatDate(this.flight.departure_datetime),
        arrival_datetime: this.formatDate(this. flight.arrival_datetime),
        sold_tickets: this.flight. sold_tickets,
        is_transit: this.flight.is_transit,
        plane: this. flight.plane.id,
        route: this.flight.route. id,
        crew: this. flight.crew.map((member) => member.id),
      };

      console.log('Отправляемые данные:', updateData);

      try {
        const response = await updateFlight(flightId, updateData);
        alert('Рейс успешно обновлен.');
        this.$router.push('/flights');
      } catch (err) {
        if (err.response && err.response.data) {
          console.error('Ответ ошибки от сервера:', err.response.data);
        }
        alert('Ошибка обновления.');
        console.error(err);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
    },
  },
};
</script>

<style scoped>
.edit-flight {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width:  800px;
  margin:  0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.form-container {
  background-color: white;
  border:  1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color:  #333;
  font-size: 14px;
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group input[type="datetime-local"] {
  width: 100%;
  padding: 10px 15px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow:  0 0 0 3px rgba(0, 123, 255, 0.1);
}

.checkbox-group label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.checkbox-group input[type="checkbox"] {
  width:  18px;
  height:  18px;
  margin-right: 10px;
  cursor: pointer;
  accent-color: #007BFF;
}

.checkbox-group span {
  font-weight: 500;
  color:  #333;
}

.button {
  display: inline-block;
  padding: 12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align:  center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.button-group.button {
  flex: 1;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group.button {
    width: 100%;
  }
}
</style>
```

EditPlane.vue
```text
<template>
  <div class="edit-plane">
    <div class="content-wrapper">
      <h1>Редактирование самолета №{{ plane.number }}</h1>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="number">Номер:</label>
            <input type="text" id="number" v-model="plane.number" placeholder="Введите номер самолета" required />
          </div>

          <div class="form-group">
            <label for="type">Тип:</label>
            <input type="text" id="type" v-model="plane.type" placeholder="Введите тип самолета" required />
          </div>

          <div class="form-group">
            <label for="seats_capacity">Число мест: </label>
            <input type="number" id="seats_capacity" v-model="plane.seats_capacity" placeholder="Введите число мест" required />
          </div>

          <div class="form-group">
            <label for="flight_speed">Скорость полета (км/ч):</label>
            <input type="number" id="flight_speed" v-model="plane.flight_speed" placeholder="Введите скорость полета" required />
          </div>

          <div class="form-group">
            <label for="in_repair">В ремонте:</label>
            <select id="in_repair" v-model="plane.in_repair" required>
              <option :value="true">Да</option>
              <option :value="false">Нет</option>
            </select>
          </div>

          <div class="form-group">
            <label for="airline_company">Компания:</label>
            <select id="airline_company" v-model="plane.airline_company" required>
              <option v-for="company in companies" :value="company.id" :key="company.id">
                {{ company.name }}
              </option>
            </select>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Сохранить</button>
            <button type="button" @click="$router.push('/planes')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getPlaneDetails, updatePlane, getAirlineCompanies } from '../api/index.js';

export default {
  name:  'EditPlane',
  data() {
    return {
      plane: {
        number:  '',
        type: '',
        seats_capacity: null,
        flight_speed: null,
        in_repair: false,
        airline_company: null,
      },
      companies: [],
      error: null,
    };
  },
  async created() {
    const planeId = this.$route.params.id;
    try {
      const [planeResponse, companiesResponse] = await Promise.all([
        getPlaneDetails(planeId),
        getAirlineCompanies(),
      ]);
      this.plane = planeResponse. data;
      this.companies = companiesResponse.data;
    } catch (err) {
      this.error = 'Ошибка загрузки данных.';
      console.error(err);
    }
  },
  methods: {
    async submitForm() {
      const planeId = this.$route. params.id;
      try {
        await updatePlane(planeId, this.plane);
        alert('Самолет успешно обновлен.');
        this.$router.push('/planes');
      } catch (err) {
        alert('Ошибка сохранения изменений.');
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
.edit-plane {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height:  100vh;
  padding:  20px 0;
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color:  #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.form-container {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom:  20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 15px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow:  0 0 0 3px rgba(0, 123, 255, 0.1);
}

.button {
  display: inline-block;
  padding:  12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.button-group.button {
  flex: 1;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group.button {
    width: 100%;
  }
}
</style>
```

EditProfile.vue
```text
<template>
  <v-container>
    <v-form @submit.prevent="updateProfile">
      <v-text-field v-model="form.username" label="Username" required></v-text-field>
      <v-btn type="submit" class="ma-2" color="primary">Сохранить</v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: this.$store.state.auth.user.username,
      },
    };
  },
  methods: {
    async updateProfile() {
      try {
        await this.$store.dispatch("auth/updateProfile", this.form);
        this.$router.push("/profile");
      } catch (error) {
        console.error("Ошибка обновления профиля:", error);
      }
    },
  },
};
</script>
```

EditRoute.vue
```text
<template>
  <div class="edit-route">
    <div class="content-wrapper">
      <h1>Редактировать маршрут</h1>

      <div class="form-container">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="departure_point">Пункт вылета:</label>
            <input type="text" id="departure_point" v-model="route.departure_point" required />
          </div>

          <div class="form-group">
            <label for="destination_point">Пункт назначения:</label>
            <input type="text" id="destination_point" v-model="route.destination_point" required />
          </div>

          <div class="form-group">
            <label for="distance">Расстояние (км):</label>
            <input type="number" id="distance" v-model="route.distance" required />
          </div>

          <div class="form-group">
            <label for="landing_points">Пункты посадки:</label>
            <textarea id="landing_points" v-model="route.landing_points" rows="3"></textarea>
          </div>

          <div class="form-group">
            <label for="transit_landings">Транзитные посадки:</label>
            <textarea id="transit_landings" v-model="route.transit_landings" rows="3"></textarea>
          </div>

          <div class="button-group">
            <button type="submit" class="button button-primary">Сохранить</button>
            <button type="button" @click="$router.push('/routes')" class="button button-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../api/index.js';

export default {
  name: 'EditRoute',
  data() {
    return {
      route:  {
        departure_point: '',
        destination_point: '',
        distance: null,
        landing_points: '',
        transit_landings: '',
      },
      error: null,
    };
  },
  async created() {
    const routeId = this.$route.params.id;
    try {
      const response = await axiosInstance.get(`/api/routes/${routeId}/`);
      this.route = response.data;
    } catch (err) {
      this.error = 'Ошибка загрузки данных маршрута.';
      console.error(err);
    }
  },
  methods:  {
    async submitForm() {
      const routeId = this.$route.params.id;
      try {
        await axiosInstance.put(`/api/routes/${routeId}/`, this.route);
        alert('Маршрут успешно обновлен.');
        this.$router.push('/routes');
      } catch (err) {
        alert('Ошибка сохранения маршрута.');
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
.edit-route {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width:  800px;
  margin: 0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.form-container {
  background-color: white;
  border:  1px solid #e0e0e0;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight:  500;
  color: #333;
  font-size: 14px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px 15px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007BFF;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.button {
  display: inline-block;
  padding: 12px 24px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align:  center;
  transition: background-color 0.3s ease;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-group {
  display:  flex;
  gap: 10px;
  margin-top:  30px;
}

.button-group.button {
  flex: 1;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .form-container {
    padding: 20px;
  }

  .button-group {
    flex-direction: column;
  }

  .button-group.button {
    width: 100%;
  }
}
</style>
```

FlightDetails.vue
```text
<template>
  <div class="flight-details">
    <div class="content-wrapper">
      <div class="header-section">
        <h1>Рейс №{{ flight.flight_number }}</h1>
        <div class="button-group-header">
          <button @click="editFlight" class="button button-primary button-small">Редактировать</button>
          <button @click="deleteFlight" class="button button-danger button-small">Удалить</button>
        </div>
      </div>

      <div class="details-container">
        <div class="section">
          <h2>Маршрут</h2>
          <div class="info-grid">
            <p><strong>Пункт вылета:</strong> {{ flight.departure_point }}</p>
            <p><strong>Пункт назначения:</strong> {{ flight. arrival_point }}</p>
            <p><strong>Транзитный:</strong> {{ flight.is_transit ? 'Да' : 'Нет' }}</p>
            <p><strong>Дата вылета:</strong> {{ flight.departure_datetime }}</p>
            <p><strong>Дата прилета:</strong> {{ flight. arrival_datetime }}</p>
            <p v-if="flight.plane"><strong>Количество проданных билетов:</strong> {{ flight.sold_tickets }} / {{ flight.plane.seats_capacity }}</p>
          </div>
        </div>

        <div class="section" v-if="flight.plane">
          <h2>Самолет</h2>
          <div class="info-grid">
            <p><strong>Номер:</strong> {{ flight.plane.number }}</p>
            <p><strong>Тип: </strong> {{ flight.plane.type }}</p>
            <p><strong>Число мест:</strong> {{ flight.plane.seats_capacity }}</p>
            <p><strong>Скорость полета:</strong> {{ flight.plane.flight_speed }} км/ч</p>
            <p v-if="flight.plane.in_repair"><strong>Состояние:</strong> <span class="status-repair">В ремонте</span></p>
          </div>
        </div>

        <div class="section" v-if="flight.crew && flight.crew.length > 0">
          <h2>Команда</h2>
          <div v-for="crew in flight.crew" :key="crew.id" class="crew-section">
            <h3>Экипаж №{{ crew.id }}</h3>
            <div class="members-grid">
              <div class="member-card" v-for="member in crew. members" :key="member.id">
                <p><strong>ФИО:</strong> {{ member.full_name }}</p>
                <p><strong>Возраст:</strong> {{ member. age }}</p>
                <p><strong>Образование:</strong> {{ member.education }}</p>
                <p><strong>Стаж работы:</strong> {{ member.work_experience }} лет</p>
                <p><strong>Должность: </strong> {{ member.position }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="back-button-container">
          <button @click="goBack" class="button button-secondary button-full">Вернуться к списку рейсов</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../api/index.js';
import { deleteFlight } from '../api/index.js';

export default {
  name: 'FlightDetails',
  props: ['id'],
  data() {
    return {
      flight: {},
      error: null,
    };
  },
  async created() {
    await this.loadFlight();
  },
  methods: {
    async loadFlight() {
      try {
        const response = await axiosInstance.get(`/api/flights/${this.id}/`);
        this.flight = response.data;
      } catch (err) {
        this.error = 'Ошибка загрузки информации о рейсе.';
        console.error(err);
        alert('Ошибка загрузки информации о рейсе.');
      }
    },
    editFlight() {
      this.$router.push(`/edit-flight/${this.id}`);
    },
    async deleteFlight() {
      if (!confirm("Вы уверены, что хотите удалить этот рейс?")) {
        return;
      }
      try {
        await deleteFlight(this.id);
        alert("Рейс успешно удален.");
        this.$router. push('/flights');
      } catch (err) {
        alert("Ошибка удаления рейса.");
        console.error(err);
      }
    },
    goBack() {
      this.$router.push('/flights');
    }
  },
};
</script>

<style scoped>
.flight-details {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 30px;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding:  20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex-wrap: wrap;
  gap: 15px;
}

.header-section h1 {
  margin: 0;
  color: #333;
  font-size: 28px;
}

.button-group-header {
  display:  flex;
  gap: 10px;
  flex-wrap: wrap;
}

.details-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section {
  background-color: white;
  padding:  25px;
  border-radius:  8px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
  font-size: 22px;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 10px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.info-grid p {
  margin: 0;
  color: #555;
  line-height: 1.6;
  font-size: 14px;
}

.info-grid strong {
  color: #333;
}

.status-repair {
  color:  #dc3545;
  font-weight: 500;
}

.crew-section {
  margin-top:  20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.crew-section:first-child {
  margin-top: 0;
}

.crew-section h3 {
  margin-top: 0;
  margin-bottom:  15px;
  color:  #333;
  font-size: 18px;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
}

.member-card {
  padding: 15px;
  background-color: white;
  border-radius: 6px;
  border: 1px solid #dee2e6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.member-card p {
  margin: 6px 0;
  color:  #555;
  line-height: 1.5;
  font-size: 14px;
}

.member-card strong {
  color: #333;
}

.button {
  display: inline-block;
  padding: 10px 20px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  white-space: nowrap;
  font-weight:  500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-danger {
  background-color: rgb(210, 37, 37);
}

.button.button-danger:hover {
  background-color: rgb(180, 20, 20);
}

.button.button-secondary {
  background-color: #6c757d;
}

.button.button-secondary:hover {
  background-color: #5a6268;
}

.button-small {
  padding: 8px 15px;
  font-size:  13px;
}

.button-full {
  width: 100%;
}

.back-button-container {
  margin-top: 20px;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .header-section {
    flex-direction: column;
    align-items: flex-start;
  }

  .button-group-header {
    width: 100%;
  }

  .button-group-header.button {
    flex: 1;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .members-grid {
    grid-template-columns: 1fr;
  }
}
</style>
```

FlightList.vue
```text
<template>
  <div class="flight-list">
    <div class="content-wrapper">
      <h1>Список рейсов</h1>

      <div class="search-flight">
        <label for="search">Найти рейс по номеру: </label>
        <input
          class="search-input"
          type="text"
          id="search"
          v-model="searchId"
          placeholder="Введите номер рейса"
        />
        <button @click="searchFlight" class="button button-primary">Найти рейс</button>
        <button @click="toggleFilters" class="button button-primary">Фильтры</button>
        <button @click="resetSearch" class="button button-danger">Очистить</button>
      </div>

      <div v-if="filteredFlights.length > 0" class="flights-container">
        <div class="flight-card" v-for="flight in filteredFlights" :key="flight.id">
          <h2>Рейс №{{ flight.flight_number }}</h2>
          <p v-if="flight.route"><strong>Номер маршрута:</strong> {{ flight.route.id }}</p>
          <p v-else><strong>Маршрута не существует</strong></p>
          <p><strong>Маршрут:</strong> {{ flight.departure_point }} → {{ flight.arrival_point }}</p>
          <p><strong>Транзитный:</strong> {{ flight.is_transit ? 'Да' :  'Нет' }}</p>
          <p><strong>Дата вылета:</strong> {{ flight.departure_datetime }}</p>
          <p><strong>Дата прилета: </strong> {{ flight.arrival_datetime }}</p>
          <p><strong>Количество проданных билетов:</strong> {{ flight.sold_tickets }}</p>
          <p v-if="flight.plane"><strong>Номер самолета:</strong> {{ flight.plane.number }}</p>
          <p v-else><strong>Самолета не существует</strong></p>
          <p v-if="flight.crew.length > 0"><strong>Номера команд:</strong>
            <span v-for="crew in flight.crew" :key="crew.id">
              Команда №{{ crew.id }}{{ flight.crew.indexOf(crew) < flight.crew.length - 1 ? ', ' : '' }}
            </span>
          </p>
          <div class="button-group">
            <button @click="editFlight(flight.id)" class="button button-primary">Редактировать</button>
            <button @click="deleteFlight(flight. id)" class="button button-danger">Удалить</button>
          </div>
          <router-link :to="`/flight/${flight.id}`" class="button button-primary button-full">
            Открыть информацию о рейсе
          </router-link>
        </div>
      </div>
      <p v-else class="no-data">Нет подходящих рейсов.</p>
    </div>

    <div v-if="showFilters" class="filters-panel">
      <h2>Фильтр</h2>
      <label>
        Номер маршрута:
        <input type="number" v-model="filters.routeId" placeholder="Введите номер маршрута" />
      </label><br/>
      <label>
        Пункт вылета:
        <input type="text" v-model="filters.departurePoint" placeholder="Введите пункт вылета" />
      </label><br/>
      <label>
        Пункт прилета:
        <input type="text" v-model="filters.arrivalPoint" placeholder="Введите пункт прилета" />
      </label><br/>
      <label>
        Дата вылета от:
        <input type="datetime-local" v-model="filters.minDepartureDatetime" />
      </label><br/>
      <label>
        Дата вылета до:
        <input type="datetime-local" v-model="filters.maxDepartureDatetime" />
      </label><br/>
      <label>
        Дата прилета от:
        <input type="datetime-local" v-model="filters.minArrivalDatetime" />
      </label><br/>
      <label>
        Дата прилета до:
        <input type="datetime-local" v-model="filters. maxArrivalDatetime" />
      </label><br/>
      <label>
        Количество билетов от:
        <input type="number" v-model="filters.minSoldTickets" placeholder="Минимум проданных билетов" />
      </label><br/>
      <label>
        Количество билетов до:
        <input type="number" v-model="filters.maxSoldTickets" placeholder="Максимум проданных билетов" />
      </label><br/>
      <button @click="applyFilters" class="button button-primary button-full">Найти</button>
    </div>
  </div>
</template>

<script>
import { getFlights, deleteFlight } from "../api/index.js";

export default {
  name: "FlightList",
  data() {
    return {
      flights:  [],
      searchId: "",
      filteredFlights: [],
      showFilters: false,
      filters: {
        routeId: null,
        departurePoint: "",
        arrivalPoint: "",
        minDepartureDatetime: "",
        maxDepartureDatetime: "",
        minArrivalDatetime: "",
        maxArrivalDatetime: "",
        minSoldTickets: null,
        maxSoldTickets: null,
      },
      error: null,
    };
  },
  async created() {
    try {
      const response = await getFlights();
      this.flights = response.data;
      this.filteredFlights = this.flights;
    } catch (err) {
      this.error = "Ошибка загрузки данных рейсов.";
      console.error(err);
    }
  },
  methods: {
    editFlight(id) {
      this.$router.push(`/edit-flight/${id}`);
    },
    async deleteFlight(id) {
      if (!confirm("Вы уверены, что хотите удалить рейс?")) {
        return;
      }
      try {
        await deleteFlight(id);
        alert("Рейс успешно удален.");
        this.flights = this.flights.filter(flight => flight.id !== id);
        this.filteredFlights = this.filteredFlights.filter(flight => flight.id !== id);
      } catch (err) {
        alert("Ошибка удаления рейса.");
        console.error(err);
      }
    },
    searchFlight() {
      const flight_number = parseInt(this.searchId, 10);
      if (!isNaN(flight_number)) {
        this.filteredFlights = this.flights.filter(flight => flight.flight_number === flight_number);
      }
    },
    resetSearch() {
      this.searchId = "";
      this.filters = {
        routeId: null,
        departurePoint: "",
        arrivalPoint: "",
        minDepartureDatetime: "",
        maxDepartureDatetime: "",
        minArrivalDatetime: "",
        maxArrivalDatetime: "",
        minSoldTickets: null,
        maxSoldTickets: null,
      };
      this.filteredFlights = this.flights;
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;
    },
    applyFilters() {
      this.filteredFlights = this.flights.filter(flight => {
        const matchesRouteId = !this. filters.routeId || (flight.route && flight.route.id === this.filters.routeId);
        const matchesDeparturePoint =
          !this. filters.departurePoint || flight. departure_point.includes(this. filters.departurePoint);
        const matchesArrivalPoint =
          !this.filters.arrivalPoint || flight.arrival_point.includes(this.filters.arrivalPoint);
        const matchesDepartureDatetime =
          (!this.filters.minDepartureDatetime ||
            new Date(flight.departure_datetime) >= new Date(this.filters.minDepartureDatetime)) &&
          (!this.filters.maxDepartureDatetime ||
            new Date(flight.departure_datetime) <= new Date(this.filters. maxDepartureDatetime));
        const matchesArrivalDatetime =
          (!this.filters.minArrivalDatetime ||
            new Date(flight.arrival_datetime) >= new Date(this.filters.minArrivalDatetime)) &&
          (!this. filters.maxArrivalDatetime ||
            new Date(flight. arrival_datetime) <= new Date(this.filters.maxArrivalDatetime));
        const matchesSoldTickets =
          (! this.filters.minSoldTickets || flight.sold_tickets >= this.filters.minSoldTickets) &&
          (!this. filters.maxSoldTickets || flight.sold_tickets <= this. filters.maxSoldTickets);

        return (
          matchesRouteId &&
          matchesDeparturePoint &&
          matchesArrivalPoint &&
          matchesDepartureDatetime &&
          matchesArrivalDatetime &&
          matchesSoldTickets
        );
      });
      this.showFilters = false;
    },
  },
};
</script>

<style scoped>
.flight-list {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 30px;
}

.flights-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.flight-card {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.3s ease;
}

.flight-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.flight-card h2 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 20px;
}

.flight-card p {
  margin: 8px 0;
  color:  #555;
  line-height: 1.5;
}

.search-flight {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  background-color: white;
  padding: 20px;
  border-radius:  8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-flight label {
  margin-right: 10px;
  font-weight: 500;
  color: #333;
}

.search-input {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  min-width: 200px;
  font-size: 14px;
}

.search-input:focus {
  outline:  none;
  border-color:  #007BFF;
}

.button {
  display: inline-block;
  padding:  10px 20px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  white-space: nowrap;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color:  #0056b3;
}

.button.button-danger {
  background-color: rgb(210, 37, 37);
}

.button.button-danger:hover {
  background-color: rgb(180, 20, 20);
}

.button-full {
  width: 100%;
  margin-top: 10px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.button-group.button {
  flex: 1;
}

.filters-panel {
  position: fixed;
  top: 0;
  right: 0;
  height: 100%;
  width: 300px;
  background-color: white;
  border-left: 1px solid #ddd;
  padding: 20px;
  box-shadow:  -5px 0 15px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  z-index: 1000;
}

.filters-panel h2 {
  margin-top: 0;
  color: #333;
}

.filters-panel label {
  display: block;
  margin-bottom: 15px;
  font-weight:  500;
  color: #333;
}

.filters-panel input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-size: 14px;
}

.filters-panel input:focus {
  outline: none;
  border-color: #007BFF;
}

.filters-panel.button {
  margin-top: 20px;
}

.no-data {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  color: #666;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .flights-container {
    grid-template-columns: 1fr;
  }

  .search-flight {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    width: 100%;
  }

  .button {
    width: 100%;
  }
}
</style>
```

Login.vue
```text
<template>
  <v-container>
    <v-form @submit.prevent="login">
      <v-text-field v-model="form.username" label="User name" required></v-text-field>
      <v-text-field v-model="form.password" label="Password" type="password" required></v-text-field>
      <v-btn type="submit" class="ma-2" color="primary">Войти</v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    async login() {
      try {
        await this.$store.dispatch("auth/login", this.form);
        this.$router.push("/profile");
      } catch (error) {
        console.error("Ошибка авторизации:", error);
      }
    },
  },
};
</script>
```

PlaneList.vue
```text
<template>
  <div class="plane-list">
    <div class="content-wrapper">
      <h1>Список самолетов</h1>

      <div class="search-plane">
        <label for="search">Найти самолет по номеру: </label>
        <input
          class="search-input"
          type="text"
          id="search"
          v-model="searchId"
          placeholder="Введите номер самолета"
        />
        <button @click="searchPlane" class="button button-primary">Найти самолет</button>
        <button @click="toggleFilters" class="button button-primary">Фильтры</button>
        <button @click="resetSearch" class="button button-danger">Очистить</button>
      </div>

      <div v-if="filteredPlanes.length > 0" class="planes-container">
        <div class="plane-card" v-for="plane in filteredPlanes" :key="plane.id">
          <h2>Самолет №{{ plane.number }}</h2>
          <p><strong>Тип самолета:</strong> {{ plane.type }}</p>
          <p><strong>Число мест:</strong> {{ plane. seats_capacity }}</p>
          <p><strong>Скорость полета:</strong> {{ plane.flight_speed }} км/ч</p>
          <p><strong>Компания:</strong> {{ plane.airline_company. name }}</p>
          <p><strong>В ремонте:</strong> {{ plane.in_repair ? 'Да' :  'Нет' }}</p>
          <div class="button-group">
            <button @click="editPlane(plane.id)" class="button button-primary">Редактировать</button>
            <button @click="deletePlane(plane. id)" class="button button-danger">Удалить</button>
          </div>
        </div>
      </div>
      <p v-else class="no-data">Нет подходящих самолетов.</p>
    </div>

    <div v-if="showFilters" class="filters-panel">
      <h2>Фильтры самолетов</h2>
      <label>
        Тип самолета:
        <input type="text" v-model="filters.type" placeholder="Введите тип самолета" />
      </label><br/>
      <label>
        Число мест от:
        <input type="number" v-model="filters.minSeatsCapacity" placeholder="Минимальное число мест" />
      </label><br/>
      <label>
        Число мест до:
        <input type="number" v-model="filters.maxSeatsCapacity" placeholder="Максимальное число мест" />
      </label><br/>
      <label>
        Скорость полета от (км/ч):
        <input type="number" v-model="filters.minFlightSpeed" placeholder="Минимальная скорость полета" />
      </label><br/>
      <label>
        Скорость полета до (км/ч):
        <input type="number" v-model="filters. maxFlightSpeed" placeholder="Максимальная скорость полета" />
      </label><br/>
      <label>
        Компания:
        <input type="text" v-model="filters.companyName" placeholder="Введите название компании" />
      </label><br/>
      <label>
        В ремонте:
        <select v-model="filters.inRepair">
          <option :value="null">Неважно</option>
          <option :value="true">Да</option>
          <option :value="false">Нет</option>
        </select>
      </label><br/>
      <button @click="applyFilters" class="button button-primary button-full">Найти</button>
    </div>
  </div>
</template>

<script>
import { getPlanes, deletePlane } from "../api/index.js";

export default {
  name: "PlaneList",
  data() {
    return {
      planes: [],
      searchId: "",
      filteredPlanes: [],
      showFilters: false,
      filters: {
        type: "",
        minSeatsCapacity: null,
        maxSeatsCapacity: null,
        minFlightSpeed: null,
        maxFlightSpeed: null,
        companyName: "",
        inRepair: null,
      },
      error: null,
    };
  },
  async created() {
    try {
      const response = await getPlanes();
      this.planes = response.data;
      this.filteredPlanes = this.planes;
    } catch (err) {
      this.error = "Ошибка загрузки данных самолетов.";
      console.error(err);
    }
  },
  methods:  {
    editPlane(id) {
      this.$router. push(`/edit-plane/${id}`);
    },
    async deletePlane(id) {
      if (!confirm("Вы уверены, что хотите удалить самолет?")) {
        return;
      }
      try {
        await deletePlane(id);
        alert("Самолет успешно удален.");
        this.planes = this.planes.filter(plane => plane.id !== id);
        this.filteredPlanes = this.filteredPlanes.filter(plane => plane.id !== id);
      } catch (err) {
        alert("Ошибка удаления самолета.");
        console.error(err);
      }
    },
    searchPlane() {
      const planeNumber = this.searchId.trim();
      console.log("planeNumber: ", planeNumber)
      if (planeNumber) {
        this.filteredPlanes = this.planes.filter(plane => plane.number === planeNumber);
      }
      console.log("filteredPlanes:", this.filteredPlanes)
    },
    resetSearch() {
      this.searchId = "";
      this.filters = {
        type: "",
        minSeatsCapacity: null,
        maxSeatsCapacity: null,
        minFlightSpeed:  null,
        maxFlightSpeed: null,
        companyName: "",
        inRepair:  null,
      };
      this.filteredPlanes = this. planes;
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;
    },
    applyFilters() {
      this.filteredPlanes = this.planes.filter(plane => {
        const matchesType = ! this.filters.type || plane. type.includes(this.filters. type);
        const matchesSeatsCapacity =
          (!this.filters.minSeatsCapacity || plane.seats_capacity >= this.filters.minSeatsCapacity) &&
          (!this.filters.maxSeatsCapacity || plane.seats_capacity <= this.filters.maxSeatsCapacity);
        const matchesFlightSpeed =
          (!this.filters.minFlightSpeed || plane.flight_speed >= this.filters.minFlightSpeed) &&
          (!this.filters.maxFlightSpeed || plane.flight_speed <= this. filters.maxFlightSpeed);
        const matchesCompany = ! this.filters.companyName || plane.airline_company.name. includes(this.filters.companyName);
        const matchesInRepair =
          this.filters.inRepair === null || plane.in_repair === this.filters.inRepair;

        return (
          matchesType &&
          matchesSeatsCapacity &&
          matchesFlightSpeed &&
          matchesCompany &&
          matchesInRepair
        );
      });
      this.showFilters = false;
    },
  },
};
</script>

<style scoped>
.plane-list {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 30px;
}

.planes-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.plane-card {
  background-color: white;
  border:  1px solid #e0e0e0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.3s ease;
}

.plane-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.plane-card h2 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 20px;
}

.plane-card p {
  margin:  8px 0;
  color:  #555;
  line-height: 1.5;
}

.search-plane {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  background-color: white;
  padding: 20px;
  border-radius:  8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-plane label {
  margin-right: 10px;
  font-weight: 500;
  color: #333;
}

.search-input {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  min-width: 200px;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #007BFF;
}

.button {
  display: inline-block;
  padding: 10px 20px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor:  pointer;
  font-size:  14px;
  text-align:  center;
  transition: background-color 0.3s ease;
  white-space: nowrap;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button.button-danger {
  background-color: rgb(210, 37, 37);
}

.button.button-danger:hover {
  background-color: rgb(180, 20, 20);
}

.button-full {
  width:  100%;
  margin-top: 10px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.button-group.button {
  flex: 1;
}

.filters-panel {
  position: fixed;
  top: 0;
  right: 0;
  height: 100%;
  width: 300px;
  background-color: white;
  border-left: 1px solid #ddd;
  padding: 20px;
  box-shadow:  -5px 0 15px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  z-index: 1000;
}

.filters-panel h2 {
  margin-top: 0;
  color: #333;
}

.filters-panel label {
  display: block;
  margin-bottom: 15px;
  font-weight:  500;
  color: #333;
}

.filters-panel input,
.filters-panel select {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-size: 14px;
}

.filters-panel input:focus,
.filters-panel select:focus {
  outline:  none;
  border-color:  #007BFF;
}

.filters-panel.button {
  margin-top: 20px;
}

.no-data {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  color: #666;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .planes-container {
    grid-template-columns: 1fr;
  }

  .search-plane {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    width: 100%;
  }

  .button {
    width: 100%;
  }
}
</style>
```

Profile.vue
```text
<template>
  <v-container>
    <h1>Профиль</h1>

    <v-card v-if="user && ! isEditing" class="pa-4">
      <v-card-text>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Username:</strong> {{ user.username }}</p>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="isEditing = true">Редактировать</v-btn>
      </v-card-actions>
    </v-card>

    <v-card v-if="isEditing" class="pa-4">
      <v-card-title>Редактировать профиль</v-card-title>
      <v-card-text>
        <v-alert v-if="errorMessage" type="error" closable @click:close="errorMessage = ''">
          {{ errorMessage }}
        </v-alert>

        <v-alert v-if="successMessage" type="success" closable @click:close="successMessage = ''">
          {{ successMessage }}
        </v-alert>

        <v-form @submit.prevent="saveProfile">
          <v-text-field
            v-model="form.email"
            label="Email"
            type="email"
            required
          ></v-text-field>
          <v-text-field
            v-model="form.username"
            label="Username"
            required
          ></v-text-field>

          <v-divider class="my-4"></v-divider>
          <h3>Текущий пароль (требуется для изменения username или пароля)</h3>

          <v-text-field
            v-model="passwordForm.current_password"
            label="Текущий пароль"
            type="password"
          ></v-text-field>

          <v-divider class="my-4"></v-divider>
          <h3>Сменить пароль (необязательно)</h3>

          <v-text-field
            v-model="passwordForm.new_password"
            label="Новый пароль"
            type="password"
          ></v-text-field>
          <v-text-field
            v-model="passwordForm. re_new_password"
            label="Подтвердите новый пароль"
            type="password"
          ></v-text-field>

          <v-card-actions>
            <v-btn type="submit" color="primary">Сохранить</v-btn>
            <v-btn @click="cancelEdit" color="grey">Отмена</v-btn>
          </v-card-actions>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      isEditing: false,
      form: {
        email: "",
        username: "",
      },
      passwordForm: {
        current_password: "",
        new_password: "",
        re_new_password: "",
      },
      errorMessage: "",
      successMessage: "",
    };
  },
  computed: {
    user() {
      return this.$store.state.auth.user;
    },
  },
  async created() {
    await this.$store.dispatch("auth/getProfile");
    if (this.user) {
      this.form.email = this.user.email;
      this.form.username = this.user.username;
    }
  },
  methods: {
    async saveProfile() {
      this.errorMessage = "";
      this.successMessage = "";

      try {
        if (this. form.username !== this.user.username && ! this.passwordForm.current_password) {
          this.errorMessage = "Для изменения username необходимо ввести текущий пароль";
          return;
        }

        console.log("Saving profile with data:", this.form, this.passwordForm);

        await this.$store.dispatch("auth/updateProfile", {
          email: this.form.email,
          username: this.form.username,
          current_password: this.passwordForm.current_password,
        });

        if (this.passwordForm.new_password) {
          if (! this.passwordForm.current_password) {
            this. errorMessage = "Для смены пароля необходимо ввести текущий пароль";
            return;
          }

          if (this.passwordForm.new_password !== this.passwordForm.re_new_password) {
            this.errorMessage = "Новые пароли не совпадают";
            return;
          }

          await this.$store.dispatch("auth/changePassword", {
            current_password: this.passwordForm.current_password,
            new_password: this.passwordForm.new_password,
            re_new_password: this.passwordForm.re_new_password,
          });
        }

        this.successMessage = "Профиль успешно обновлён";

        this.passwordForm = {
          current_password: "",
          new_password: "",
          re_new_password: "",
        };

        setTimeout(() => {
          this.isEditing = false;
        }, 1500);

      } catch (error) {
        console.error("Ошибка обновления профиля:", error);

        if (error.response && error.response.data) {
          const errors = error.response.data;
          if (errors.detail) {
            this.errorMessage = errors.detail;
          } else if (errors.current_password) {
            this.errorMessage = "Неверный текущий пароль";
          } else {
            this.errorMessage = JSON.stringify(errors);
          }
        } else {
          this.errorMessage = "Произошла ошибка при сохранении данных";
        }
      }
    },
    cancelEdit() {
      this.isEditing = false;
      this.errorMessage = "";
      this.successMessage = "";

      if (this.user) {
        this.form.email = this. user.email;
        this. form.username = this.user. username;
      }

      this.passwordForm = {
        current_password: "",
        new_password: "",
        re_new_password: "",
      };
    },
  },
};
</script>
```

Register.vue
```text
<template>
  <v-container>
    <v-form @submit.prevent="register">
      <v-alert v-if="errorMessage" type="error" closable @click:close="errorMessage = ''">
        {{ errorMessage }}
      </v-alert>

      <v-alert v-if="fieldErrors.length > 0" type="error" closable @click:close="fieldErrors = []">
        <ul>
          <li v-for="(error, index) in fieldErrors" :key="index">{{ error }}</li>
        </ul>
      </v-alert>

      <v-text-field v-model="form.email" label="Email" required></v-text-field>
      <v-text-field v-model="form.username" label="Username" required></v-text-field>
      <v-text-field v-model="form.password" label="Password" type="password" required></v-text-field>
      <v-btn type="submit" class="ma-2" color="primary">Зарегистрироваться</v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      form: {
        email: "",
        username: "",
        password: "",
      },
      errorMessage: "",
      fieldErrors:  [],
    };
  },
  methods: {
    async register() {
      this.errorMessage = "";
      this.fieldErrors = [];

      try {
        await this.$store.dispatch("auth/register", this.form);
        this.$router.push("/login");
      } catch (error) {
        console.error("Ошибка регистрации:", error);

        if (error.response && error.response.data) {
          const errors = error.response.data;

          if (errors.detail) {
            this.errorMessage = errors.detail;
          } else {
            for (const field in errors) {
              if (Array.isArray(errors[field])) {
                errors[field].forEach((msg) => {
                  this.fieldErrors.push(`${field}: ${msg}`);
                });
              } else {
                this.fieldErrors.push(`${field}: ${errors[field]}`);
              }
            }
          }
        } else {
          this.errorMessage = "Произошла неизвестная ошибка.  Попробуйте снова.";
        }
      }
    },
  },
};
</script>
```

RouteDetails.vue
```text
<template>
  <div class="route-details">
    <div class="content-wrapper">
      <h1>Маршрут №{{ routeId }}</h1>

      <div class="route-info-card">
        <h2>Информация о маршруте</h2>
        <p><strong>Пункт вылета:</strong> {{ route.departure_point }}</p>
        <p><strong>Пункт назначения:</strong> {{ route. destination_point }}</p>
        <p><strong>Расстояние:</strong> {{ route. distance }} км</p>
        <p v-if="route. landing_points"><strong>Пункты посадки:</strong> {{ route.landing_points }}</p>
        <p v-if="route.transit_landings"><strong>Транзитные посадки:</strong> {{ route. transit_landings }}</p>
      </div>

      <h2>Связанные рейсы</h2>
      <div v-if="route.flights && route.flights.length > 0" class="flights-container">
        <div class="flight-card" v-for="flight in route.flights" :key="flight.id">
          <h3>Рейс №{{ flight.flight_number }}</h3>
          <p><strong>Пункт вылета:</strong> {{ flight.departure_point }}</p>
          <p><strong>Пункт прилета:</strong> {{ flight. arrival_point }}</p>
          <p><strong>Дата вылета:</strong> {{ flight.departure_datetime }}</p>
          <p><strong>Дата прилета:</strong> {{ flight.arrival_datetime }}</p>
          <p><strong>Транзитный:</strong> {{ flight.is_transit ? 'Да' : 'Нет' }}</p>
          <p><strong>Количество проданных билетов:</strong> {{ flight.sold_tickets }}</p>
          <p><strong>Самолет:</strong> {{ flight.plane.number }}</p>
          <router-link :to="`/flight/${flight.id}`" class="button button-primary button-full">
            Открыть информацию о рейсе
          </router-link>
        </div>
      </div>
      <p v-else class="no-data">Рейсы не найдены. </p>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../api/index.js';

export default {
  name: 'RouteDetails',
  props: ['id'],
  data() {
    return {
      routeId: this.id,
      route: {},
      error: null,
    };
  },
  async created() {
    try {
      const response = await axiosInstance.get(`/api/routes/${this.routeId}/`);
      this.route = response.data;
    } catch (err) {
      this.error = 'Ошибка загрузки маршрута.';
      console.error(err);
    }
  },
};
</script>

<style scoped>
.route-details {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width:  1400px;
  margin: 0 auto;
  padding: 0 30px;
}

.content-wrapper h1 {
  color: #333;
  margin-bottom: 20px;
}

.content-wrapper h2 {
  color: #333;
  margin-top:  30px;
  margin-bottom: 20px;
}

.route-info-card {
  background-color: white;
  border:  1px solid #e0e0e0;
  padding:  20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.route-info-card h2 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 20px;
}

.route-info-card p {
  margin: 8px 0;
  color: #555;
  line-height: 1.5;
}

.flights-container {
  display: grid;
  grid-template-columns:  repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.flight-card {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.3s ease;
}

.flight-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.flight-card h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 18px;
}

.flight-card p {
  margin:  8px 0;
  color: #555;
  line-height: 1.5;
}

.button {
  display: inline-block;
  padding: 10px 20px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor:  pointer;
  font-size:  14px;
  text-align: center;
  transition:  background-color 0.3s ease;
  white-space:  nowrap;
  font-weight: 500;
}

.button.button-primary {
  background-color: #007BFF;
}

.button.button-primary:hover {
  background-color: #0056b3;
}

.button-full {
  width: 100%;
  margin-top: 15px;
}

.no-data {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  color: #666;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .flights-container {
    grid-template-columns: 1fr;
  }
}
</style>
```

RouteList.vue
```text
<template>
  <div class="routes-list">
    <div class="content-wrapper">
      <h1>Список маршрутов</h1>

      <div class="search-route">
        <label for="search">Найти маршрут по ID: </label>
        <input
          class="search-input"
          type="text"
          id="search"
          v-model="searchId"
          placeholder="Введите ID маршрута"
        />
        <button @click="searchRoute" class="button button-primary">Найти маршрут</button>
        <button @click="toggleFilters" class="button button-primary">Фильтры</button>
        <button @click="clearSearch" class="button button-danger">Очистить</button>
      </div>

      <div v-if="filteredRoutes.length > 0" class="routes-container">
        <div class="route-card" v-for="route in filteredRoutes" :key="route.id">
          <h2>Маршрут №{{ route. id }}</h2>
          <p><strong>Пункт вылета:</strong> {{ route.departure_point }}</p>
          <p><strong>Пункт назначения:</strong> {{ route.destination_point }}</p>
          <p><strong>Расстояние:</strong> {{ route.distance }} км</p>
          <p v-if="route.landing_points"><strong>Пункты посадки:</strong> {{ route.landing_points }}</p>
          <p v-if="route.transit_landings"><strong>Транзитные посадки:</strong> {{ route.transit_landings }}</p>
          <div class="button-group">
            <button @click="editRoute(route. id)" class="button button-primary">Редактировать</button>
            <button @click="deleteRouteItem(route.id)" class="button button-danger">Удалить</button>
          </div>
          <router-link :to="`/route/${route.id}`" class="button button-primary button-full">Открыть связанные рейсы</router-link>
        </div>
      </div>
      <p v-else>Маршруты с указанными параметрами не найдены.</p>
    </div>

    <div v-if="showFilters" class="filters-panel">
      <h2>Фильтры</h2>
      <label>
        Пункт вылета:
        <input type="text" v-model="filters.departurePoint" placeholder="Введите пункт вылета" />
      </label><br/>
      <label>
        Пункт назначения:
        <input type="text" v-model="filters.destinationPoint" placeholder="Введите пункт назначения" />
      </label><br/>
      <label>
        Расстояние от (км):
        <input type="number" v-model="filters. minDistance" placeholder="Минимальное расстояние" />
      </label><br/>
      <label>
        Расстояние до (км):
        <input type="number" v-model="filters.maxDistance" placeholder="Максимальное расстояние" />
      </label><br/>
      <button @click="applyFilters" class="button button-primary button-full">Найти</button>
    </div>
  </div>
</template>

<script>
import { getRoutes, deleteRoute } from "../api/index.js";

export default {
  name: "RoutesList",
  data() {
    return {
      routes: [],
      searchId: "",
      filteredRoutes: [],
      showFilters: false,
      filters: {
        departurePoint:  "",
        destinationPoint: "",
        minDistance: null,
        maxDistance: null,
      },
      error: null,
    };
  },
  async created() {
    try {
      const response = await getRoutes();
      this.routes = response.data;
      this. filteredRoutes = this.routes;
    } catch (err) {
      this.error = "Ошибка загрузки маршрутов. ";
      console.error(err);
    }
  },
  methods: {
    editRoute(id) {
      this.$router.push(`/edit-route/${id}`);
    },
    async deleteRouteItem(id) {
      if (!confirm("Вы уверены, что хотите удалить маршрут?")) {
        return;
      }
      console. log("Del route id:", id);
      try {
        await deleteRoute(id);
        alert("Маршрут успешно удален.");
        this.routes = this.routes.filter(route => route.id !== id);
        this.filteredRoutes = this.filteredRoutes.filter(route => route.id !== id);
      } catch (err) {
        alert("Ошибка удаления маршрута.");
        console.error(err);
      }
    },
    searchRoute() {
      const id = parseInt(this.searchId, 10);
      if (!isNaN(id)) {
        this.filteredRoutes = this.routes.filter(route => route.id === id);
      }
    },
    clearSearch() {
      this.searchId = "";
      this.filters = {
        departurePoint:  "",
        destinationPoint: "",
        minDistance: null,
        maxDistance: null,
      };
      this.filteredRoutes = this.routes;
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;
    },
    applyFilters() {
      this.filteredRoutes = this.routes.filter(route => {
        const matchesDeparturePoint =
          ! this.filters.departurePoint ||
          route.departure_point. toLowerCase().includes(this.filters. departurePoint.toLowerCase());

        const matchesDestinationPoint =
          !this.filters.destinationPoint ||
          route.destination_point.toLowerCase().includes(this.filters.destinationPoint.toLowerCase());

        const matchesMinDistance =
          !this.filters. minDistance || route.distance >= this.filters.minDistance;

        const matchesMaxDistance =
          !this.filters.maxDistance || route.distance <= this.filters. maxDistance;

        return (
          matchesDeparturePoint &&
          matchesDestinationPoint &&
          matchesMinDistance &&
          matchesMaxDistance
        );
      });
      this.showFilters = false;
    },
  },
};
</script>

<style>
.routes-list {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px 0;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 30px;
}

.routes-container {
  display: grid;
  grid-template-columns:  repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top:  20px;
}

.route-card {
  background-color: white;
  border:  1px solid #e0e0e0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.3s ease;
}

.route-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.route-card h2 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 20px;
}

.route-card p {
  margin:  8px 0;
  color:  #555;
  line-height: 1.5;
}

.search-route {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  background-color: white;
  padding: 20px;
  border-radius:  8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-route label {
  margin-right: 10px;
  font-weight: 500;
  color: #333;
}

.search-input {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  min-width: 200px;
  font-size: 14px;
}

.search-input: focus {
  outline: none;
  border-color: #007BFF;
}

.button {
  display: inline-block;
  padding: 10px 20px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  transition: background-color 0.3s ease;
  white-space: nowrap;
  font-weight: 500;
}

.button-primary {
  background-color: #007BFF;
}

.button-primary:hover {
  background-color: #0056b3;
}

.button.button-danger {
  background-color: rgb(210, 37, 37);
}

.button.button-danger:hover {
  background-color: rgb(180, 20, 20);
}

.button-full {
  width: 100%;
  margin-top: 10px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.button-group.button {
  flex: 1;
}

.filters-panel {
  position: fixed;
  top: 0;
  right: 0;
  height: 100%;
  width: 300px;
  background-color: white;
  border-left: 1px solid #ddd;
  padding: 20px;
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  z-index: 1000;
}

.filters-panel h2 {
  margin-top:  0;
  color: #333;
}

.filters-panel label {
  display: block;
  margin-bottom: 15px;
  font-weight:  500;
  color: #333;
}

.filters-panel input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  font-size: 14px;
}

.filters-panel input:focus {
  outline: none;
  border-color: #007BFF;
}

.filters-panel.button {
  margin-top: 20px;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 15px;
  }

  .routes-container {
    grid-template-columns: 1fr;
  }

  .search-route {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    width: 100%;
  }

  .button {
    width: 100%;
  }
}
</style>
```

VariantTask.vue
```text
<template>
  <div class="variant-task">
    <h1>Задания варианта</h1>

    <!-- Задание 1: Самая популярная марка самолета на маршруте -->
    <div class="task-section">
      <h2>1. Самая популярная марка самолета на маршруте</h2>

      <div class="input-group">
        <label for="route-select-1">Выберите маршрут:</label>
        <select id="route-select-1" v-model="task1.selectedRouteId" @change="fetchMostPopularPlane">
          <option value="" disabled>Выберите маршрут</option>
          <option v-for="route in routes" :value="route.id" :key="route.id">
            Маршрут №{{ route.id }}: {{ route.departure_point }} → {{ route.destination_point }}
          </option>
        </select>
      </div>

      <div v-if="task1.result" class="result-card success">
        <h3>Результат:</h3>
        <p><strong>Маршрут:</strong> {{ getSelectedRoute(task1.selectedRouteId)?.departure_point }} → {{ getSelectedRoute(task1.selectedRouteId)?.destination_point }}</p>
        <p><strong>Самая популярная марка самолета:</strong> {{ task1.result.plane_type }}</p>
        <p><strong>Количество рейсов:</strong> {{ task1.result.flight_count }}</p>
      </div>

      <div v-if="task1.noData" class="result-card warning">
        <p>Для выбранного маршрута нет данных о рейсах.</p>
      </div>

      <div v-if="task1.error" class="result-card error">
        <p>{{ task1.error }}</p>
      </div>
    </div>

    <!-- Задание 2: Маршруты с заполненностью менее XX% -->
    <div class="task-section">
        <h2>2. Маршрут/маршруты, по которым летают рейсы, заполненные менее чем на XX%</h2>

        <div class="input-group">
            <label for="percentage-input">Введите процент заполненности: </label>
            <input
            type="number"
            id="percentage-input"
            v-model.number="task2.percentage"
            placeholder="Например, 50"
            min="0"
            max="100"
            />
            <button @click="fetchRoutesBelowCapacity" class="search-button">Найти</button>
        </div>

        <div v-if="task2.result && task2.result.length > 0" class="result-card success">
            <h3>Найдено маршрутов:   {{ task2.result.length }}</h3>
            <div v-for="route in task2.result" :key="route.route_id" class="route-item">
                <p><strong>Маршрут №{{ route.route_id }}: </strong> {{ route.departure_point }} → {{ route.destination_point }}</p>
                <p><strong>Средняя заполненность:</strong>
                    {{ route.average_occupancy != null ? route.average_occupancy.toFixed(2) + '%' : 'Н/Д' }}
                </p>
            </div>
        </div>

        <div v-if="task2.result && task2.result.length === 0" class="result-card warning">
            <p>Маршруты с заполненностью менее {{ task2.percentage }}% не найдены.</p>
        </div>

        <div v-if="task2.error" class="result-card error">
            <p>{{ task2.error }}</p>
        </div>
    </div>

    <!-- Задание 3: Наличие свободных мест на рейс -->
    <div class="task-section">
      <h2>3. Наличие свободных мест на заданный рейс</h2>

      <div class="input-group">
        <label for="flight-select">Выберите рейс: </label>
        <select id="flight-select" v-model="task3.selectedFlightId" @change="fetchAvailableSeats">
          <option value="" disabled>Выберите рейс</option>
          <option v-for="flight in flights" :value="flight.id" :key="flight.id">
            Рейс №{{ flight.flight_number }}: {{ flight.departure_point }} → {{ flight.arrival_point }}
          </option>
        </select>
      </div>

      <div v-if="task3.result" class="result-card success">
        <h3>Результат: </h3>
        <p><strong>Свободных мест:</strong> {{ task3.result.available_seats }}</p>
      </div>

      <div v-if="task3.error" class="result-card error">
        <p>{{ task3.error }}</p>
      </div>
    </div>

    <!-- Задание 4: Количество самолетов в ремонте -->
    <div class="task-section">
      <h2>4. Количество самолетов, находящихся в ремонте</h2>

      <button @click="fetchPlanesUnderRepair" class="search-button">Получить данные</button>

      <div v-if="task4.result !== null" class="result-card success">
        <h3>Результат:</h3>
        <p><strong>Самолетов в ремонте:</strong> {{ task4.result.planes_under_repair }}</p>
      </div>

      <div v-if="task4.error" class="result-card error">
        <p>{{ task4.error }}</p>
      </div>
    </div>

    <!-- Задание 5: Количество работников компании -->
    <div class="task-section">
      <h2>5. Количество работников компании-авиаперевозчика</h2>

      <div class="input-group">
        <label for="company-select">Выберите компанию:</label>
        <select id="company-select" v-model="task5.selectedCompanyId" @change="fetchTotalEmployees">
          <option value="" disabled>Выберите компанию</option>
          <option v-for="company in companies" :value="company.id" :key="company.id">
            {{ company.name }}
          </option>
        </select>
      </div>

      <div v-if="task5.result" class="result-card success">
        <h3>Результат:</h3>
        <p><strong>Количество работников:</strong> {{ task5.result.total_employees }}</p>
      </div>

      <div v-if="task5.error" class="result-card error">
        <p>{{ task5.error }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { getRoutes, getFlights, getAirlineCompanies } from '@/api';
import axiosInstance from '@/api';

export default {
  name:  'VariantTask',
  data() {
    return {
      routes: [],
      flights: [],
      companies: [],

      task1: {
        selectedRouteId: '',
        result: null,
        noData: false,
        error: null,
      },

      task2: {
        percentage: null,
        result: null,
        error: null,
      },

      task3: {
        selectedFlightId: '',
        result: null,
        error:  null,
      },

      task4: {
        result: null,
        error: null,
      },

      task5: {
        selectedCompanyId: '',
        result:  null,
        error: null,
      },
    };
  },
  async created() {
    try {
      const [routesResponse, flightsResponse, companiesResponse] = await Promise.all([
        getRoutes(),
        getFlights(),
        getAirlineCompanies(),
      ]);
      this.routes = routesResponse.data;
      this.flights = flightsResponse.data;
      this. companies = companiesResponse.data;
    } catch (err) {
      console.error('Ошибка загрузки данных:', err);
    }
  },
  methods: {
    getSelectedRoute(routeId) {
      return this.routes.find(route => route.id === routeId);
    },
    getSelectedFlight(flightId) {
      return this.flights.find(flight => flight.id === flightId);
    },
    getSelectedCompany(companyId) {
      return this.companies.find(company => company.id === companyId);
    },

    async fetchMostPopularPlane() {
      this.task1.result = null;
      this.task1.noData = false;
      this.task1.error = null;

      if (!this.task1.selectedRouteId) return;

      try {
        const response = await axiosInstance.get(`/api/most_popular_plane_type/${this.task1.selectedRouteId}/`);
        this.task1.result = response.data;
      } catch (err) {
        console.error('Ошибка получения данных:', err);
        if (err.response && err.response.status === 404) {
          this.task1.noData = true;
        } else {
          this.task1.error = 'Произошла ошибка при получении данных. ';
        }
      }
    },

    async fetchRoutesBelowCapacity() {
      this.task2.result = null;
      this.task2.error = null;

      if (!this.task2.percentage && this.task2.percentage !== 0) {
        this.task2.error = 'Введите процент заполненности. ';
        return;
      }

      try {
        console.log('Запрос на получение маршрутов с заполненностью менее', this.task2.percentage, '%');
        const response = await axiosInstance.get(`/api/routes_below_capacity/${this.task2.percentage}/`);
        console.log('Ответ сервера:', response.data);
        if (response.data && response.data.under_capacity_routes) {
            this.task2.result = response.data.under_capacity_routes;
        } else {
            this.task2.result = [];
        }
      } catch (err) {
        console.error('Ошибка получения данных:', err);
        this.task2.error = 'Произошла ошибка при получении данных.';
      }
    },

    async fetchAvailableSeats() {
      this.task3.result = null;
      this.task3.error = null;

      if (!this.task3.selectedFlightId) return;

      try {
        const response = await axiosInstance.get(`/api/available_seats/${this.task3.selectedFlightId}/`);
        this.task3.result = response.data;
      } catch (err) {
        console.error('Ошибка получения данных:', err);
        this.task3.error = 'Произошла ошибка при получении данных. ';
      }
    },

    async fetchPlanesUnderRepair() {
      this.task4.result = null;
      this. task4.error = null;

      try {
        const response = await axiosInstance.get('/api/planes_under_repair/');
        this.task4.result = response.data;
      } catch (err) {
        console.error('Ошибка получения данных:', err);
        this.task4.error = 'Произошла ошибка при получении данных.';
      }
    },

    async fetchTotalEmployees() {
      this.task5.result = null;
      this.task5.error = null;

      if (!this.task5.selectedCompanyId) return;

      try {
        const response = await axiosInstance.get(`/api/total_employees/${this.task5.selectedCompanyId}/`);
        this.task5.result = response.data;
      } catch (err) {
        console.error('Ошибка получения данных:', err);
        this.task5.error = 'Произошла ошибка при получении данных. ';
      }
    },
  },
};
</script>

<style scoped>
.variant-task {
  margin:  20px;
  font-family: Arial, sans-serif;
  max-width: 1200px;
}

h1 {
  font-size:  32px;
  margin-bottom: 30px;
  color: #0f4c81;
  text-align: center;
}

.task-section {
  background-color: #f9f9f9;
  border:  1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin-bottom:  30px;
}

h2 {
  font-size: 22px;
  margin-bottom:  10px;
  color: #0f4c81;
}

.task-description {
  color: #666;
  margin-bottom: 15px;
  font-style: italic;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  font-weight:  bold;
  font-size: 16px;
}

.input-group select,
.input-group input {
  width: 100%;
  max-width: 500px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-bottom: 10px;
}

.search-button {
  padding: 10px 20px;
  font-size: 16px;
  color: white;
  background-color: #0f4c81;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.search-button:hover {
  background-color: #083a5e;
}

.result-card {
  padding: 20px;
  border-radius: 5px;
  margin-top: 15px;
}

.result-card h3 {
  margin-top: 0;
  margin-bottom: 15px;
}

.result-card p {
  margin:  8px 0;
  font-size: 16px;
}

.result-card.success {
  background-color: #e8f5e9;
  border-left: 4px solid #4caf50;
}

.result-card.warning {
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
  color: #856404;
}

.result-card.error {
  background-color: #f8d7da;
  border-left: 4px solid #dc3545;
  color: #721c24;
}

.route-item {
  background-color: white;
  padding: 10px;
  margin:  10px 0;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.route-item p {
  margin: 5px 0;
}
</style>
```