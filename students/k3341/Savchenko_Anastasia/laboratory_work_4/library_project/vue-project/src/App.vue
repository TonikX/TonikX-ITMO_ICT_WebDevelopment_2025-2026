<template>
  <v-app>
    <!-- Навигация: авторизованные -->
    <v-app-bar v-if="auth.isAuthenticated" color="primary" prominent>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-toolbar-title>📚 Библиотека</v-toolbar-title>
      <v-spacer />

      <v-btn :to="{ name: 'books' }" variant="text" prepend-icon="mdi-book">Книги</v-btn>
      <v-btn :to="{ name: 'profile' }" variant="text" prepend-icon="mdi-account">Профиль</v-btn>

      <!-- Админ-меню -->
      <template v-if="auth.isAdmin">
        <v-btn :to="{ name: 'on-loan' }" variant="text" prepend-icon="mdi-book-clock">На руках</v-btn>
        <v-btn :to="{ name: 'manage-loans' }" variant="text" prepend-icon="mdi-book-arrow-up">Выдача</v-btn>
        <v-btn :to="{ name: 'admin-issue-book' }" variant="text" prepend-icon="mdi-book-plus" color="success">Выдать книгу</v-btn>
        <v-btn :to="{ name: 'reports' }" variant="text" prepend-icon="mdi-chart-bar">Отчёты</v-btn>
        <v-btn :to="{ name: 'admin-dashboard' }" variant="text" prepend-icon="mdi-cog" color="yellow-lighten-3">Админ-панель</v-btn>
      </template>

      <v-btn @click="logout" variant="text" prepend-icon="mdi-logout">Выйти</v-btn>
    </v-app-bar>

    <!-- Навигация: гости -->
    <v-app-bar v-else color="primary" prominent>
      <v-toolbar-title>📚 Библиотека</v-toolbar-title>
      <v-spacer />
      <v-btn :to="{ name: 'login' }" variant="text" prepend-icon="mdi-login">Войти</v-btn>
      <v-btn :to="{ name: 'register' }" variant="text" prepend-icon="mdi-account-plus">Регистрация</v-btn>
    </v-app-bar>

    <!-- Боковое меню (админ) -->
    <v-navigation-drawer v-if="auth.isAdmin" v-model="drawer" temporary>
      <v-list>
        <v-list-item :title="'Админ: ' + (auth.user?.username || '')">
          <template v-slot:prepend><v-icon color="primary">mdi-shield-account</v-icon></template>
        </v-list-item>
        <v-divider />
        <v-list-item to="/admin" prepend-icon="mdi-view-dashboard" title="Дашборд" />
        <v-list-item to="/admin/readers" prepend-icon="mdi-account-group" title="Читатели" />
        <v-list-item to="/admin/readers/register" prepend-icon="mdi-account-plus" title="Регистрация читателя" />
        <v-divider />
        <v-list-item to="/admin/books" prepend-icon="mdi-book" title="Книги" />
        <v-list-item to="/admin/issue-book" prepend-icon="mdi-book-plus" title="Выдать книгу" />
        <v-list-item to="/admin/books/add" prepend-icon="mdi-book-plus" title="Добавить книгу" />
        <v-list-item to="/admin/books/decommission" prepend-icon="mdi-book-remove" title="Списать книгу" />
        <v-list-item to="/admin/copies/transfer" prepend-icon="mdi-swap-horizontal" title="Переместить экземпляр" />
      </v-list>
    </v-navigation-drawer>

    <!-- Отладочная панель -->
    <div v-if="auth.isAuthenticated" class="debug-panel">
      <strong>🔧 Отладка</strong>
      <div class="debug-item"><span>Пользователь:</span><span class="debug-value">{{ auth.user?.username }}</span></div>
      <div class="debug-item">
        <span>Статус:</span>
        <span :class="auth.user?.is_staff ? 'debug-admin' : 'debug-user'">
          {{ auth.user?.is_staff ? 'Админ' : 'Читатель' }}
        </span>
      </div>
      <div class="debug-item">
        <span>Токен:</span>
        <span :class="auth.token ? 'debug-token' : 'debug-notoken'">{{ auth.token ? 'Есть' : 'Нет' }}</span>
      </div>
      <div class="debug-actions">
        <v-btn size="x-small" color="info" @click="testAPI" block>Тест API</v-btn>
      </div>
    </div>

    <!-- Основной контент -->
    <v-main :class="{ 'admin-view': auth.isAdmin }">
      <router-view />
    </v-main>

    <!-- Подвал -->
    <v-footer app color="primary" class="text-white">
      <v-spacer />
      <div>📚 Библиотечная система &copy; {{ new Date().getFullYear() }}</div>
    </v-footer>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import apiClient from './api/client'

const auth = useAuthStore()
const router = useRouter()
const drawer = ref(false)

const logout = () => { auth.logout(); router.push('/login') }
const testAPI = async () => {
  try {
    const res = await apiClient.get('books/')
    alert(`✅ API работает! Загружено ${res.data.length} книг`)
  } catch (e) { alert(`❌ Ошибка API: ${e.message}`) }
}
</script>

<style>
/* ----- Глобальные стили ----- */
#app, .v-application { width: 100% !important; max-width: none !important; }

/* ----- Отладочная панель ----- */
.debug-panel {
  position: fixed; top: 64px; left: 0; z-index: 1000;
  width: 180px; height: calc(100vh - 64px);
  background: #ffeb3b; color: #000;
  border-right: 2px solid #ff9800;
  padding: 12px; font-size: 11px;
  overflow-y: auto; box-shadow: 2px 0 8px rgba(0,0,0,0.15);
}
.debug-panel strong { display: block; margin-bottom: 12px; border-bottom: 1px solid rgba(0,0,0,0.3); padding-bottom: 6px; }
.debug-item { display: flex; justify-content: space-between; margin-bottom: 8px; }
.debug-value { font-weight: 600; color: #1a1a1a; }
.debug-admin { background: rgba(198,40,40,0.1); color: #c62828; padding: 2px 6px; border-radius: 4px; font-weight: 600; }
.debug-user { background: rgba(46,125,50,0.1); color: #2e7d32; padding: 2px 6px; border-radius: 4px; font-weight: 600; }
.debug-token { color: #2e7d32; font-weight: 600; }
.debug-notoken { color: #c62828; font-weight: 600; }
.debug-actions { margin-top: 16px; padding-top: 12px; border-top: 1px dashed rgba(0,0,0,0.2); }

/* ----- Основной контент ----- */
.v-main {
  padding: 84px 20px 20px 200px !important;
  width: 100% !important;
  min-height: calc(100vh - 64px);
  transition: padding-left 0.3s;
}
.v-main.admin-view { padding-left: 240px !important; }

/* ----- Vuetify ----- */
.v-container { max-width: 100% !important; }
.v-btn { margin: 0 2px; }

/* ----- Адаптивность ----- */
@media (max-width: 768px) {
  .debug-panel { width: 140px; }
  .v-main { padding: 74px 10px 20px 160px !important; }
  .v-main.admin-view { padding-left: 180px !important; }
}
@media (max-width: 480px) {
  .debug-panel { width: 120px; }
  .v-main { padding-left: 140px !important; }
  .v-main.admin-view { padding-left: 160px !important; }
}
</style>