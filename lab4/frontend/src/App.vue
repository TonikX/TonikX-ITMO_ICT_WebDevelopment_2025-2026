<template>
  <v-app>
    <v-app-bar color="primary" dark>
      <v-app-bar-nav-icon
        v-if="authStore.isAuthenticated"
        @click="drawer = !drawer"
      />
      <v-app-bar-title>Система управления типографией</v-app-bar-title>
      <v-spacer />
      <v-btn v-if="authStore.isAuthenticated" icon="mdi-account" to="/profile" />
      <v-btn v-if="authStore.isAuthenticated" icon="mdi-logout" @click="handleLogout" />
      <v-btn v-else icon="mdi-login" to="/login" />
    </v-app-bar>

    <v-navigation-drawer
      v-if="authStore.isAuthenticated"
      v-model="drawer"
      temporary
    >
      <v-list>
        <v-list-item prepend-icon="mdi-home" title="Главная" to="/" />
        <v-list-item prepend-icon="mdi-newspaper-variant" title="Газеты" to="/newspapers" />
        <v-list-item prepend-icon="mdi-printer" title="Типографии" to="/printing-houses" />
        <v-list-item prepend-icon="mdi-email" title="Почтовые отделения" to="/post-offices" />
        <v-list-item prepend-icon="mdi-truck-delivery" title="Распределения" to="/distributions" />
        <v-divider class="my-2" />
        <v-list-item prepend-icon="mdi-account" title="Профиль" to="/profile" />
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const drawer = ref(false)

onMounted(async () => {
  // Инициализация при загрузке приложения
  if (authStore.token) {
    await authStore.init()
  }
})

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style>
#app {
  font-family: 'Roboto', sans-serif;
}
</style>
