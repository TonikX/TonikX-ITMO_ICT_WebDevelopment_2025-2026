<template>
  <v-app>
    <!-- Навигационная панель для десктопов -->
    <v-app-bar
      v-if="isAuthenticated && !isMobile"
      color="primary"
      app
      elevation="3"
    >
      <!-- Левый блок: Информация о станции -->
      <div class="d-flex flex-column ml-4 mr-6">
        <div class="d-flex align-center mb-1">
          <span class="text-caption text-white text-medium-emphasis mr-2">Станция:</span>
          <span class="text-subtitle-2 font-weight-medium white--text">
            {{ companyTitle }}
          </span>
        </div>
        <div class="d-flex align-center">
          <span class="text-caption text-white text-medium-emphasis mr-2">Адрес:</span>
          <span class="text-caption text-grey-lighten-2 text-truncate" style="max-width: 250px">
            {{ stationAddress }}
          </span>
        </div>
      </div>

      <v-spacer></v-spacer>

      <!-- Центральный блок: Навигация -->
      <div class="d-flex align-center ga-2">
        <v-btn
          v-for="item in menuItems"
          :key="item.route"
          :to="item.route"
          variant="text"
          color="white"
          size="small"
          class="text-none px-3"
          :class="{ 'active-link': $route.path === item.route }"
        >
          <v-icon v-if="item.icon" :icon="item.icon" size="small" class="mr-1"></v-icon>
          {{ item.title }}
        </v-btn>
      </div>

      <v-spacer></v-spacer>

      <!-- Правый блок: Пользователь и выход -->
      <div class="d-flex align-center mr-4">
        <v-chip size="small" variant="flat" color="white" class="text-primary mr-2">
          <v-icon size="small" icon="mdi-account" class="mr-1"></v-icon>
          {{ userData?.username }}
        </v-chip>
        <v-btn
          @click="handleLogout"
          variant="flat"
          color="error"
          icon="mdi-logout"
          size="small"
          title="Выйти"
        ></v-btn>
      </div>
    </v-app-bar>

    <!-- Навигационная панель для мобильных -->
    <v-app-bar
      v-if="isAuthenticated && isMobile"
      color="primary"
      app
      elevation="3"
    >
      <v-app-bar-nav-icon
        @click="drawer = !drawer"
        variant="text"
        color="white"
      ></v-app-bar-nav-icon>

      <v-app-bar-title class="text-subtitle-2 font-weight-medium white--text">
        {{ companyTitle }}
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <v-btn
        @click="handleLogout"
        variant="text"
        color="white"
        icon="mdi-logout"
        size="small"
      ></v-btn>
    </v-app-bar>

    <!-- Боковое меню для мобильных -->
    <v-navigation-drawer
      v-if="isAuthenticated"
      v-model="drawer"
      location="left"
      temporary
      :width="300"
    >
      <v-list density="compact" nav>
        <v-list-item class="px-4 py-3 bg-primary">
          <template v-slot:prepend>
            <v-icon color="white" icon="mdi-gas-station"></v-icon>
          </template>
          <v-list-item-title class="text-white font-weight-bold">
            Топливная система
          </v-list-item-title>
        </v-list-item>

        <!-- Информация о станции -->
        <v-list-item class="px-4 py-3">
          <v-list-item-subtitle class="text-caption text-medium-emphasis">
            Станция:
          </v-list-item-subtitle>
          <v-list-item-title class="text-subtitle-2 font-weight-medium">
            {{ companyTitle }}
          </v-list-item-title>
          
          <v-list-item-subtitle class="text-caption text-medium-emphasis mt-1">
            Адрес:
          </v-list-item-subtitle>
          <v-list-item-title class="text-subtitle-2">
            {{ stationAddress }}
          </v-list-item-title>
          
          <v-list-item-subtitle class="text-caption text-medium-emphasis mt-1">
            Пользователь:
          </v-list-item-subtitle>
          <v-list-item-title class="text-subtitle-2">
            {{ userData?.username }}
          </v-list-item-title>
        </v-list-item>

        <v-divider class="my-2"></v-divider>

        <!-- Навигация -->
        <v-list-item
          v-for="item in menuItems"
          :key="item.route"
          :to="item.route"
          @click="drawer = false"
          :active="isRouteActive(item.route)"
        >
          <template v-slot:prepend>
            <v-icon :icon="item.icon"></v-icon>
          </template>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>

        <v-divider class="my-2"></v-divider>

        <!-- Выход -->
        <v-list-item @click="handleLogout" class="text-error">
          <template v-slot:prepend>
            <v-icon color="error" icon="mdi-logout"></v-icon>
          </template>
          <v-list-item-title class="text-error">Выйти</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Основной контент -->
    <v-main>
      <v-container fluid class="pa-3 pa-sm-4">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useAuthStore } from './stores/auth'
import { useRoute } from 'vue-router'

const authStore = useAuthStore()
const route = useRoute()

const drawer = ref(false)
const isMobile = ref(false)

const isAuthenticated = computed(() => authStore.isAuthenticated)
const stationAddress = computed(() => authStore.stationAddress)
const companyTitle = computed(() => authStore.companyTitle)
const userData = computed(() => authStore.userData)

// Меню навигации с иконками
const menuItems = [
  { title: 'Главная', route: '/', icon: 'mdi-home' },
  { title: 'Продажа топлива', route: '/fuel-sale', icon: 'mdi-gas-station' },
  { title: 'Анализ продаж', route: '/sales-summary', icon: 'mdi-chart-bar' },
  { title: 'Выдача карт', route: '/issue-card', icon: 'mdi-card-account-details' },
]

// Проверка активного маршрута
const isRouteActive = (routePath) => {
  return route.path === routePath
}

// Определение мобильного устройства
const checkMobile = () => {
  isMobile.value = window.innerWidth < 960
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkMobile)
})

const handleLogout = () => {
  authStore.logout()
}
</script>

<style scoped>
/* Стили для активной ссылки на десктопе */
.active-link {
  background-color: rgba(255, 255, 255, 0.15) !important;
  border-radius: 4px;
}

/* Стили для ссылок на десктопе */
.v-btn--variant-text.v-btn--active.active-link {
  background-color: rgba(255, 255, 255, 0.15) !important;
}

/* Адаптивность для мобильных устройств */
@media (max-width: 960px) {
  .v-app-bar {
    padding-left: 8px;
    padding-right: 8px;
  }
  
  .v-container {
    padding-left: 8px;
    padding-right: 8px;
  }
}

/* Обрезка длинного текста */
.text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Для очень маленьких экранов */
@media (max-width: 400px) {
  .text-truncate {
    max-width: 150px;
  }
}
</style>