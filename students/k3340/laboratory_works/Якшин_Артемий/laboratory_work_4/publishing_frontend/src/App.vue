<template>
  <v-app>
    <v-navigation-drawer
      v-if="authStore.isAuthenticated"
      v-model="drawer"
      :rail="rail"
      permanent
      @click="rail = false"
      class="navigation-drawer"
    >
      <v-list-item
        :prepend-avatar="'https://api.dicebear.com/7.x/initials/svg?seed=' + (authStore.user?.username || 'U')"
        :title="authStore.user?.username || 'Пользователь'"
        :subtitle="authStore.user?.email || ''"
        nav
        class="user-item"
      >
        <template v-slot:append>
          <v-btn
            icon="mdi-chevron-left"
            variant="text"
            @click.stop="rail = !rail"
          ></v-btn>
        </template>
      </v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav class="nav-list">
        <v-list-item
          prepend-icon="mdi-view-dashboard"
          title="Главная"
          :to="{ name: 'home' }"
          rounded="lg"
        ></v-list-item>

        <v-list-subheader v-if="!rail">Управление</v-list-subheader>

        <v-list-item
          prepend-icon="mdi-account-group"
          title="Сотрудники"
          :to="{ name: 'employees' }"
          rounded="lg"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-feather"
          title="Авторы"
          :to="{ name: 'authors' }"
          rounded="lg"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-book-open-page-variant"
          title="Книги"
          :to="{ name: 'books' }"
          rounded="lg"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-file-document-edit"
          title="Контракты"
          :to="{ name: 'contracts' }"
          rounded="lg"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-account-tie"
          title="Заказчики"
          :to="{ name: 'customers' }"
          rounded="lg"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-cart"
          title="Заказы"
          :to="{ name: 'orders' }"
          rounded="lg"
        ></v-list-item>

        <v-divider class="my-2"></v-divider>

        <v-list-subheader v-if="!rail">Отчёты</v-list-subheader>

        <v-list-item
          prepend-icon="mdi-chart-bar"
          title="Отчёты"
          :to="{ name: 'reports' }"
          rounded="lg"
        ></v-list-item>
      </v-list>

      <template v-slot:append>
        <div class="pa-2">
          <v-btn
            v-if="!rail"
            block
            color="error"
            variant="tonal"
            prepend-icon="mdi-logout"
            @click="handleLogout"
          >
            Выйти
          </v-btn>
          <v-btn
            v-else
            icon="mdi-logout"
            color="error"
            variant="text"
            @click="handleLogout"
          ></v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <v-app-bar
      v-if="authStore.isAuthenticated"
      elevation="0"
      class="app-bar"
    >
      <v-app-bar-title class="app-title">
        <v-icon icon="mdi-book-open-variant" class="mr-2"></v-icon>
        Издательский дом
      </v-app-bar-title>

      <template v-slot:append>
        <v-btn
          icon
          @click="toggleTheme"
        >
          <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-weather-night' }}</v-icon>
        </v-btn>
        <v-btn
          icon="mdi-account-cog"
          :to="{ name: 'profile' }"
        ></v-btn>
      </template>
    </v-app-bar>

    <v-main :class="{ 'main-content': authStore.isAuthenticated }">
      <v-container fluid class="pa-6">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </v-container>
    </v-main>

    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
      location="top right"
    >
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn
          variant="text"
          @click="snackbar.show = false"
        >
          Закрыть
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script setup>
import { ref, reactive, provide, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from 'vuetify'

const router = useRouter()
const authStore = useAuthStore()
const vuetifyTheme = useTheme()

const drawer = ref(true)
const rail = ref(false)

const isDark = computed(() => vuetifyTheme.global.current.value.dark)

const snackbar = reactive({
  show: false,
  text: '',
  color: 'success'
})

const showSnackbar = (text, color = 'success') => {
  snackbar.text = text
  snackbar.color = color
  snackbar.show = true
}

provide('showSnackbar', showSnackbar)

const toggleTheme = () => {
  vuetifyTheme.global.name.value = isDark.value ? 'publishingTheme' : 'darkTheme'
}

const handleLogout = async () => {
  await authStore.logout()
  router.push({ name: 'login' })
  showSnackbar('Вы успешно вышли из системы', 'info')
}
</script>

<style>
:root {
  --font-serif: 'Cormorant Garamond', Georgia, serif;
  --font-sans: 'Source Sans 3', -apple-system, BlinkMacSystemFont, sans-serif;
}

body {
  font-family: var(--font-sans);
}

/* Light theme styles */
.v-theme--publishingTheme .navigation-drawer {
  background: linear-gradient(180deg, rgba(45, 62, 80, 0.02) 0%, rgba(201, 169, 89, 0.05) 100%) !important;
  border-right: 1px solid rgba(201, 169, 89, 0.2) !important;
}

.v-theme--publishingTheme .user-item {
  border-bottom: 1px solid rgba(201, 169, 89, 0.15);
}

.v-theme--publishingTheme .nav-list .v-list-item--active {
  background: linear-gradient(135deg, rgba(201, 169, 89, 0.15) 0%, rgba(201, 169, 89, 0.08) 100%);
  border-left: 3px solid #C9A959;
}

.v-theme--publishingTheme .app-bar {
  background: linear-gradient(90deg, #2D3E50 0%, #3D5166 100%) !important;
  border-bottom: 2px solid #C9A959 !important;
}

.v-theme--publishingTheme .main-content {
  background: linear-gradient(135deg, #F5F2EB 0%, #E8E6E3 50%, #F0EDE6 100%);
  min-height: 100vh;
}

/* Dark theme styles */
.v-theme--darkTheme .navigation-drawer {
  background: linear-gradient(180deg, rgba(37, 37, 64, 0.95) 0%, rgba(26, 26, 46, 0.98) 100%) !important;
  border-right: 1px solid rgba(201, 169, 89, 0.3) !important;
}

.v-theme--darkTheme .user-item {
  border-bottom: 1px solid rgba(201, 169, 89, 0.2);
}

.v-theme--darkTheme .nav-list .v-list-item--active {
  background: linear-gradient(135deg, rgba(201, 169, 89, 0.2) 0%, rgba(201, 169, 89, 0.1) 100%);
  border-left: 3px solid #C9A959;
}

.v-theme--darkTheme .app-bar {
  background: linear-gradient(90deg, #1A1A2E 0%, #252540 100%) !important;
  border-bottom: 2px solid #C9A959 !important;
}

.v-theme--darkTheme .main-content {
  background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #1A1A2E 100%);
  min-height: 100vh;
}

/* Common styles */
.app-title {
  font-family: var(--font-serif) !important;
  font-weight: 600 !important;
  font-size: 1.5rem !important;
  letter-spacing: 0.02em;
  color: #F5F2EB !important;
}

.v-card {
  border: 1px solid rgba(201, 169, 89, 0.15);
}

.v-card-title {
  font-family: var(--font-serif) !important;
  font-weight: 600 !important;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Scrollbar styling */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(45, 62, 80, 0.05);
}

::-webkit-scrollbar-thumb {
  background: rgba(201, 169, 89, 0.4);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(201, 169, 89, 0.6);
}
</style>

