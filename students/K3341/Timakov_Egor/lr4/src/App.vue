<template>
  <v-app>
    <v-app-bar color="primary" prominent>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Система управления типографией</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="!isAuthenticated" to="/login" text>Войти</v-btn>
      <v-btn v-if="!isAuthenticated" to="/register" text>Регистрация</v-btn>
      <v-menu v-if="isAuthenticated">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" text>
            {{ currentUser?.username }}
            <v-icon>mdi-chevron-down</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item to="/profile">Профиль</v-list-item>
          <v-list-item @click="logout">Выйти</v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" temporary>
      <v-list>
        <v-list-item to="/" prepend-icon="mdi-home">Главная</v-list-item>
        <v-list-item v-if="isAuthenticated" to="/employees" prepend-icon="mdi-account-group">Сотрудники</v-list-item>
        <v-list-item v-if="isAuthenticated" to="/authors" prepend-icon="mdi-account-edit">Авторы</v-list-item>
        <v-list-item v-if="isAuthenticated" to="/books" prepend-icon="mdi-book">Книги</v-list-item>
        <v-list-item v-if="isAuthenticated" to="/financial" prepend-icon="mdi-cash">Финансы</v-list-item>
        <v-list-item v-if="isAuthenticated" to="/reports" prepend-icon="mdi-chart-box">Отчёты</v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { computed, ref } from 'vue'
import { useAuthStore } from './stores/auth'

export default {
  name: 'App',
  setup() {
    const drawer = ref(false)
    const authStore = useAuthStore()

    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const currentUser = computed(() => authStore.user)

    const logout = async () => {
      await authStore.logout()
      window.location.href = '/login'
    }

    return {
      drawer,
      isAuthenticated,
      currentUser,
      logout
    }
  }
}
</script>
