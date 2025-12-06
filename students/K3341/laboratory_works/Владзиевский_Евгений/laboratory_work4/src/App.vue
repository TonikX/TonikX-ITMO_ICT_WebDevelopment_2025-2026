<template>
  <v-app>
    <v-app-bar flat density="comfortable" color="white" class="app-bar">
      <v-btn to="/" variant="text" color="primary" prepend-icon="mdi-fire" class="font-weight-bold">Лента</v-btn>
      <v-btn to="/recommended" variant="text">Рекомендации</v-btn>
      <v-btn to="/create" variant="text">Новый пост</v-btn>
      <v-btn to="/my" variant="text">Мои посты</v-btn>
      <v-spacer></v-spacer>
      <v-btn v-if="user" to="/profile" variant="text" prepend-icon="mdi-account-circle-outline">{{ user.name }}</v-btn>
      <v-btn v-if="user" variant="tonal" color="secondary" class="ml-2" @click="handleLogout">Выйти</v-btn>
      <template v-else>
        <v-btn to="/login" variant="text">Войти</v-btn>
        <v-btn to="/register" variant="flat" color="primary" class="ml-2">Регистрация</v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <v-container class="py-8" max-width="1100">
        <v-alert v-if="!ready" type="info" variant="tonal" class="mb-4">Загружаем сессию...</v-alert>
        <router-view v-if="ready"></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { initAuth, logout, useAuthState } from './stores/auth'

const router = useRouter()
const state = useAuthState()
const user = computed(() => state.user)
const ready = computed(() => state.ready)

onMounted(() => {
  initAuth()
})

const handleLogout = () => {
  logout()
  router.push({ name: 'login' })
}
</script>

<style scoped>
.app-bar {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(6px);
}
</style>
