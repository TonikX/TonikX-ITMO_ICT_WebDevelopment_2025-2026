<!-- src/App.vue -->
<template>
  <v-app>
    <!-- Хедер -->
    <v-app-bar color="primary" density="compact" flat>
      <!-- Логотип / Название с переходом на дашборд -->
      <v-app-bar-title class="text-white" style="cursor: pointer;" @click="goToDashboard">
        Птицефабрика
      </v-app-bar-title>

      <v-spacer />

      <!-- Профиль и выход (только для авторизованных) -->
      <v-menu v-if="authStore.isAuthenticated" offset-y>
        <template #activator="{ props }">
          <v-btn icon v-bind="props">
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>
        <v-list density="compact">
          <v-list-item to="/profile">
            <v-list-item-title>Мой профиль</v-list-item-title>
          </v-list-item>
          <v-divider />
          <v-list-item @click="logout">
            <v-list-item-title>Выйти</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <!-- Основной контент -->
    <v-main>
      <router-view />
    </v-main>

    <!-- Футер (опционально) -->
    <v-footer v-if="authStore.isAuthenticated" app color="grey-lighten-3">
      <span class="text-caption">Птицефабрика • {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script setup>
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

// Переход на дашборд
const goToDashboard = () => {
  if (authStore.isAuthenticated) {
    router.push('/')
  }
}

// Выход
const logout = () => {
  authStore.logout()
  router.push('/login')
}

// Человекочитаемые названия ролей
const roleLabels = {
  director: 'Директор',
  hr_manager: 'HR-менеджер',
  coordinator: 'Координатор',
  employee: 'Сотрудник'
}
</script>

<style scoped>
.v-app-bar-title {
  font-weight: 500;
}
</style>