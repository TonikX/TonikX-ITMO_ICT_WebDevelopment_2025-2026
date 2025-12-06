<template>
  <v-app>
    <v-app-bar
      color="primary"
      prominent
      dark
    >
      <v-app-bar-nav-icon
        v-if="$vuetify.display.mobile"
        @click="drawer = !drawer"
      ></v-app-bar-nav-icon>

      <v-toolbar-title>
        <router-link to="/" class="text-white text-decoration-none">
          Drones App
        </router-link>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn
        v-if="authStore.isAuthenticated"
        to="/drones"
        variant="text"
        class="mr-2"
      >
        Дроны
      </v-btn>

      <v-btn
        v-if="!authStore.isAuthenticated"
        to="/login"
        variant="text"
        class="mr-2"
      >
        Вход
      </v-btn>

      <v-btn
        v-if="!authStore.isAuthenticated"
        to="/register"
        variant="outlined"
        class="mr-2"
      >
        Регистрация
      </v-btn>

      <v-menu
        v-if="authStore.isAuthenticated"
        location="bottom"
      >
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            icon
            variant="text"
          >
            <v-avatar size="32">
              <v-icon>mdi-account</v-icon>
            </v-avatar>
          </v-btn>
        </template>

        <v-list>
          <v-list-item
            prepend-icon="mdi-account"
            :title="authStore.displayName"
            :subtitle="authStore.user?.email"
            disabled
          ></v-list-item>
          <v-divider></v-divider>
          <v-list-item
            prepend-icon="mdi-account-circle"
            title="Профиль"
            to="/profile"
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-airplane"
            title="Дроны"
            to="/drones"
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-cog"
            title="Настройки"
            to="/settings"
          ></v-list-item>
          <v-divider></v-divider>
          <v-list-item
            prepend-icon="mdi-logout"
            title="Выход"
            @click="handleLogout"
          ></v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      temporary
      v-if="$vuetify.display.mobile"
    >
      <v-list>
        <v-list-item
          v-if="!authStore.isAuthenticated"
          prepend-icon="mdi-login"
          title="Вход"
          to="/login"
        ></v-list-item>
        <v-list-item
          v-if="!authStore.isAuthenticated"
          prepend-icon="mdi-account-plus"
          title="Регистрация"
          to="/register"
        ></v-list-item>
        <v-list-item
          v-if="authStore.isAuthenticated"
          prepend-icon="mdi-account-circle"
          title="Профиль"
          to="/profile"
        ></v-list-item>
        <v-list-item
          v-if="authStore.isAuthenticated"
          prepend-icon="mdi-airplane"
          title="Дроны"
          to="/drones"
        ></v-list-item>
        <v-list-item
          v-if="authStore.isAuthenticated"
          prepend-icon="mdi-cog"
          title="Настройки"
          to="/settings"
        ></v-list-item>
        <v-list-item
          v-if="authStore.isAuthenticated"
          prepend-icon="mdi-logout"
          title="Выход"
          @click="handleLogout"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <!-- Snackbar для уведомлений -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
      location="top"
    >
      {{ snackbar.message }}
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
import { ref, provide } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const drawer = ref(false)

// Snackbar для глобальных уведомлений
const snackbar = ref({
  show: false,
  message: '',
  color: 'success',
  timeout: 5000,
})

// Функция для показа уведомлений (можно использовать в дочерних компонентах)
const showSnackbar = (message, color = 'success', timeout = 5000) => {
  snackbar.value = {
    show: true,
    message,
    color,
    timeout,
  }
}

// Предоставляем функцию дочерним компонентам
provide('showSnackbar', showSnackbar)

const handleLogout = () => {
  authStore.logout()
  showSnackbar('Вы успешно вышли из системы', 'info')
}
</script>

<style scoped>
.text-white {
  color: white !important;
}
</style>
