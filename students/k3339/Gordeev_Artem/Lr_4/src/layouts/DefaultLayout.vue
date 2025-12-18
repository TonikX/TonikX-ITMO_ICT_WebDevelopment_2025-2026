<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item title="Типография" subtitle="Панель управления"></v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list density="compact" nav>
        <v-list-item prepend-icon="mdi-view-dashboard" title="Обзор" to="/dashboard"></v-list-item>
        <v-list-item prepend-icon="mdi-book" title="Книги" to="/books"></v-list-item>
        <v-list-item prepend-icon="mdi-account-group" title="Авторы" to="/authors"></v-list-item>
        <v-list-item prepend-icon="mdi-file-document" title="Контракты" to="/contracts"></v-list-item>
        <v-list-item prepend-icon="mdi-chart-bar" title="Отчеты" to="/reports"></v-list-item>
        <v-list-item prepend-icon="mdi-account-cog" title="Профиль" to="/profile"></v-list-item>
      </v-list>
      <template v-slot:append>
        <div class="pa-2">
          <v-btn block color="error" @click="logout">Выйти</v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <v-app-bar app color="primary" density="compact">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-app-bar-title>Панель управления</v-app-bar-title>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const drawer = ref(true)
const router = useRouter()

const logout = () => {
  router.push('/login')
}
</script>
