<template>
  <v-app>
    <v-app-bar color="primary" v-if="showNavbar">
      <v-app-bar-title>Hotel Management System</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn variant="text" to="/" v-if="isAuthenticated">Главная</v-btn>
      <v-menu v-if="isAuthenticated">
        <template v-slot:activator="{ props }">
          <v-btn variant="text" v-bind="props">Управление</v-btn>
        </template>
        <v-list>
          <v-list-item to="/room-types" title="Типы номеров"></v-list-item>
          <v-list-item to="/floors" title="Этажи"></v-list-item>
          <v-list-item to="/rooms" title="Номера"></v-list-item>
          <v-list-item to="/guests" title="Гости"></v-list-item>
          <v-list-item to="/stays" title="Проживания"></v-list-item>
          <v-list-item to="/employees" title="Сотрудники"></v-list-item>
          <v-list-item to="/cleaning" title="График уборки"></v-list-item>
        </v-list>
      </v-menu>
      <v-btn variant="text" to="/profile" v-if="isAuthenticated">Профиль</v-btn>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('auth_token')
})

const showNavbar = computed(() => {
  return route.name !== 'Login' && route.name !== 'Register'
})
</script>

<style scoped></style>
