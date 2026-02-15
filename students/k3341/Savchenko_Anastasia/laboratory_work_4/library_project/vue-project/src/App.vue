<template>
  <v-app>
    <!-- ===== ШАПКА НАВИГАЦИИ ===== -->
    <v-app-bar color="primary" prominent>
      <v-container class="d-flex align-center pa-0">
        <v-toolbar-title class="text-h5 font-weight-bold mr-6">📚 Библиотека</v-toolbar-title>

        <!-- Главное меню (адаптируется под роль) -->
        <div class="nav-links">
          <!-- Книги: для админов - выпадающее меню, для читателей - простая ссылка -->
          <template v-if="auth.isAdmin">
            <v-menu offset-y>
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" variant="text" prepend-icon="mdi-book"
                  :class="{ 'active-tab': isBooksRoute }" class="nav-btn">
                  Книги <v-icon end>mdi-chevron-down</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item to="/admin/books" prepend-icon="mdi-book-open" title="Все книги" />
                <v-list-item to="/admin/books/add" prepend-icon="mdi-book-plus" title="➕ Добавить книгу" />
                <v-divider />
                <v-list-item to="/admin/books/decommission" prepend-icon="mdi-book-remove" title="Списать книгу" />
                <v-list-item to="/admin/copies/transfer" prepend-icon="mdi-swap-horizontal" title="Переместить экземпляр" />
              </v-list>
            </v-menu>
          </template>
          <v-btn v-else :to="{ name: 'books' }" :class="{ 'active-tab': $route.name === 'books' }"
            variant="text" prepend-icon="mdi-book" class="nav-btn">Книги</v-btn>

          <!-- Профиль только для обычных читателей -->
          <v-btn v-if="auth.isAuthenticated && !auth.isAdmin" :to="{ name: 'profile' }"
            :class="{ 'active-tab': $route.name === 'profile' }" variant="text" prepend-icon="mdi-account" class="nav-btn">
            Профиль
          </v-btn>

          <!-- Админ-меню (читатели, выдача, отчеты) -->
          <template v-if="auth.isAdmin">
            <v-menu offset-y>
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" variant="text" prepend-icon="mdi-account-group"
                  :class="{ 'active-tab': isReadersRoute }" class="nav-btn">
                  Читатели <v-icon end>mdi-chevron-down</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item to="/admin/readers" prepend-icon="mdi-account-search" title="Поиск читателей" />
                <v-list-item to="/admin/readers/register" prepend-icon="mdi-account-plus" title="Регистрация" />
              </v-list>
            </v-menu>

            <v-menu offset-y>
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" variant="text" prepend-icon="mdi-book-clock"
                  :class="{ 'active-tab': isLoansRoute }" class="nav-btn">
                  Выдача <v-icon end>mdi-chevron-down</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item to="/admin/issue-book" prepend-icon="mdi-book-plus" title="Выдать книгу" />
                <v-list-item to="/admin/on-loan" prepend-icon="mdi-book-clock" title="На руках" />
                <v-list-item to="/admin/manage-loans" prepend-icon="mdi-book-arrow-up" title="Управление" />
              </v-list>
            </v-menu>

            <v-btn :to="{ name: 'admin-reports' }" :class="{ 'active-tab': $route.name === 'admin-reports' }"
              variant="text" prepend-icon="mdi-chart-bar" class="nav-btn">Отчеты</v-btn>
          </template>
        </div>

        <v-spacer />

        <!-- Правая часть: выход/вход -->
        <div class="d-flex align-center">
          <v-btn v-if="auth.isAuthenticated" @click="logout" variant="text" prepend-icon="mdi-logout" class="logout-btn">
            Выйти
          </v-btn>
          <template v-else>
            <v-btn :to="{ name: 'login' }" variant="text" prepend-icon="mdi-login" class="mr-2">Войти</v-btn>
            <v-btn :to="{ name: 'register' }" variant="text" prepend-icon="mdi-account-plus">Регистрация</v-btn>
          </template>
        </div>
      </v-container>
    </v-app-bar>

    <!-- ===== ОТЛАДОЧНАЯ ПАНЕЛЬ (сворачиваемая) ===== -->
    <div v-if="auth.isAuthenticated && debugMode" class="debug-panel" :class="{ 'collapsed': debugCollapsed }">
      <div v-if="!debugCollapsed" class="debug-header">
        <strong>🔧 Отладка</strong>
        <div class="debug-controls">
          <button class="debug-toggle" @click="toggleDebug" title="Свернуть">◀</button>
          <button class="debug-close" @click="debugMode = false" title="Закрыть">✕</button>
        </div>
      </div>

      <div v-if="!debugCollapsed" class="debug-content">
        <div class="debug-item"><span>Пользователь:</span><span class="debug-value">{{ auth.user?.username }}</span></div>
        <div class="debug-item">
          <span>Роль:</span>
          <span :class="auth.isAdmin ? 'debug-admin' : 'debug-user'">
            {{ auth.isAdmin ? 'Администратор' : 'Читатель' }}
          </span>
        </div>
        <div class="debug-item">
          <span>Токен:</span>
          <span :class="auth.token ? 'debug-token' : 'debug-notoken'">
            {{ auth.token ? 'Активен' : 'Отсутствует' }}
          </span>
        </div>
        <div class="debug-actions">
          <button class="debug-test-btn" @click="testAPI">📡 Тест API</button>
        </div>
      </div>

      <!-- Свернутое состояние - только иконка -->
      <div v-if="debugCollapsed" class="debug-collapsed-icon" @click="toggleDebug" title="Развернуть">🔧</div>
    </div>

    <!-- Основной контент -->
    <v-main>
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
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from './stores/auth'
import apiClient from './api/client'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

// Состояние отладочной панели
const debugMode = ref(true)
const debugCollapsed = ref(false)

// Вычисляемые пути для подсветки активных пунктов меню
const isReadersRoute = computed(() => route.path.startsWith('/admin/readers'))
const isBooksRoute = computed(() =>
  route.path.startsWith('/admin/books') ||
  route.path.includes('/admin/books/add') ||
  route.path.includes('/admin/books/decommission') ||
  route.path.includes('/admin/copies/transfer')
)
const isLoansRoute = computed(() =>
  route.path.includes('/admin/issue-book') ||
  route.path.includes('/admin/on-loan') ||
  route.path.includes('/admin/manage-loans')
)

const logout = () => { auth.logout(); router.push('/login') }
const toggleDebug = () => { debugCollapsed.value = !debugCollapsed.value }

const testAPI = async () => {
  try {
    const res = await apiClient.get('books/')
    alert(`✅ API работает! Загружено ${res.data.length} книг`)
  } catch (e) { alert(`❌ Ошибка API: ${e.message}`) }
}
</script>

<style>
/* Глобальные стили */
#app, .v-application { width: 100% !important; max-width: none !important; }

/* Навигация */
.nav-links { display: flex; gap: 4px; }
.nav-btn { font-weight: 500; transition: all 0.2s; }
.nav-btn:hover { background-color: rgba(255,255,255,0.15) !important; }
.active-tab { background-color: rgba(255,255,255,0.25) !important; border-bottom: 3px solid white !important; }
.logout-btn { background-color: rgba(255,255,255,0.1) !important; }
.logout-btn:hover { background-color: rgba(255,255,255,0.2) !important; }

/* Отладочная панель */
.debug-panel {
  position: fixed; top: 80px; left: 20px; z-index: 1000;
  width: 240px; background: #ffeb3b; border: 2px solid #ff9800;
  border-radius: 8px; padding: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
}
.debug-panel.collapsed { width: 60px; padding: 12px 8px; }
.debug-panel.collapsed .debug-header strong,
.debug-panel.collapsed .debug-content { display: none; }

.debug-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 8px; border-bottom: 1px solid rgba(0,0,0,0.2); padding-bottom: 4px;
}
.debug-item { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 12px; }
.debug-value { font-weight: 600; color: #1a1a1a; }
.debug-admin { color: #c62828; font-weight: 600; }
.debug-user { color: #2e7d32; font-weight: 600; }
.debug-token { color: #2e7d32; font-weight: 600; }
.debug-notoken { color: #c62828; font-weight: 600; }

.debug-actions { margin-top: 12px; padding-top: 8px; border-top: 1px dashed rgba(0,0,0,0.2); }
.debug-test-btn {
  width: 100%; padding: 6px; background: #2196F3; color: white;
  border: none; border-radius: 4px; cursor: pointer;
}
.debug-test-btn:hover { background: #1976D2; }
.debug-collapsed-icon {
  width: 100%; height: 100%; display: flex; align-items: center;
  justify-content: center; font-size: 24px; cursor: pointer;
}

/* Основной контент - фиксированные отступы для ПК */
.v-main {
  padding: 84px 20px 20px 200px !important; /* top: 84px (шапка), left: 200px (отладка) */
  width: 100% !important;
  min-height: calc(100vh - 64px);
  transition: padding-left 0.3s;
}

.debug-toggle, .debug-close {
  width: 24px; height: 24px; border: none; background: rgba(0,0,0,0.1);
  border-radius: 4px; cursor: pointer; font-size: 14px;
}
.debug-toggle:hover, .debug-close:hover { background: rgba(0,0,0,0.2); }
</style>