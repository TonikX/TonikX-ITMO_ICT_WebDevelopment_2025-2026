<!-- src/App.vue -->
<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Hotel SPA</v-toolbar-title>
      <v-spacer />
      <RouterLink to="/login" class="mx-2">Вход</RouterLink>
      <RouterLink to="/register" class="mx-2">Регистрация</RouterLink>
      <RouterLink to="/profile" class="mx-2">Профиль</RouterLink>
      <RouterLink to="/rooms" class="mx-2">Номера</RouterLink>
      <RouterLink to="/check-in" class="mx-2">Заселение</RouterLink>
      <RouterLink to="/reports/free-rooms" class="mx-2">Свободные номера</RouterLink>
    </v-app-bar>

    <v-main>
      <v-container class="mt-8">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { onMounted } from 'vue'
import { initAuthFromStorage } from './auth'

onMounted(() => {
  initAuthFromStorage()
})
</script>

<style>
a {
  color: white;
  text-decoration: none;
}
a.router-link-active {
  text-decoration: underline;
}
</style>
