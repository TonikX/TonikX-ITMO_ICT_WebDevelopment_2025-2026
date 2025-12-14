<template>
  <v-app>
    <v-app-bar color="primary" dark>
      <v-app-bar-title>Система управления гостиницей</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="!isAuthenticated" to="/login" text>Вход</v-btn>
      <v-btn v-if="!isAuthenticated" to="/register" text>Регистрация</v-btn>
      <v-btn v-if="isAuthenticated" @click="logout" text>Выход</v-btn>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import { useAuth } from './composables/useAuth'

export default {
  name: 'App',
  setup() {
    const { isAuthenticated, logout } = useAuth()
    return { isAuthenticated, logout }
  }
}
</script>

