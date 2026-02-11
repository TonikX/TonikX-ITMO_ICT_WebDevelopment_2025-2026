<template>
  <div id="app">
    <!-- Vuetify приложение -->
    <v-app>
      <!-- Навигация -->
      <v-app-bar v-if="auth.isAuthenticated" color="primary" prominent>
        <v-toolbar-title>📚 Библиотека</v-toolbar-title>
        <v-spacer></v-spacer>

        <v-btn :to="{ name: 'books' }" variant="text" prepend-icon="mdi-book">Книги</v-btn>
        <v-btn :to="{ name: 'profile' }" variant="text" prepend-icon="mdi-account">Профиль</v-btn>
        <v-btn v-if="auth.isAdmin" :to="{ name: 'on-loan' }" variant="text" prepend-icon="mdi-book-clock">На руках</v-btn>
        <v-btn v-if="auth.isAdmin" :to="{ name: 'manage-loans' }" variant="text" prepend-icon="mdi-book-arrow-up">Выдача</v-btn>
        <v-btn v-if="auth.isAdmin" :to="{ name: 'reports' }" variant="text" prepend-icon="mdi-chart-bar">Отчёты</v-btn>
        <v-btn @click="logout" variant="text" prepend-icon="mdi-logout">Выйти</v-btn>
      </v-app-bar>

      <v-app-bar v-else color="primary" prominent>
        <v-toolbar-title>📚 Библиотека</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn :to="{ name: 'login' }" variant="text" prepend-icon="mdi-login">Войти</v-btn>
        <v-btn :to="{ name: 'register' }" variant="text" prepend-icon="mdi-account-plus">Регистрация</v-btn>
      </v-app-bar>

      <!-- Отладочный блок слева -->
      <div v-if="auth.isAuthenticated" class="debug-panel">
        <strong>Отладка</strong>
        <div>Пользователь: {{ auth.user?.username }}</div>
        <div>Статус: {{ auth.user?.is_staff ? 'Админ' : 'Читатель' }}</div>
        <div>Токен: {{ auth.token ? 'Есть' : 'Нет' }}</div>
      </div>

      <!-- Основной контент -->
      <v-main>
        <router-view />
      </v-main>

      <!-- Подвал -->
      <v-footer app color="primary" class="text-white">
        <v-spacer></v-spacer>
      </v-footer>
    </v-app>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
const router = useRouter()

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>

<style>
#app {
  width: 100vw;
  min-height: 100vh;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Отладочный блок слева вертикальный */
.debug-panel {
  background: #ffeb3b;
  padding: 8px 12px;
  font-size: 11px;
  color: #000000;
  border-right: 1px solid #ff9800;
  border-bottom: 1px solid #ff9800;
  z-index: 1000;
  position: fixed;
  top: 64px;
  left: 0;
  width: 160px; /* Фиксированная ширина */
  min-height: calc(100vh - 64px);
  box-shadow: 2px 0 4px rgba(0,0,0,0.1);
}

.debug-panel div {
  margin-top: 6px;
  line-height: 1.2;
}

.debug-panel strong {
  color: #000000;
  display: block;
  margin-bottom: 8px;
  font-size: 12px;
  border-bottom: 1px solid rgba(0,0,0,0.2);
  padding-bottom: 4px;
}

/* Смещаем основной контент вправо на ширину отладочного блока */
.v-main {
  padding-left: 160px !important; /* Ширина отладочного блока */
  padding: 0 !important;
  width: 100% !important;
  min-height: calc(100vh - 64px);
}

.v-application {
  width: 100% !important;
  max-width: none !important;
  padding-left: 0 !important;
}
</style>