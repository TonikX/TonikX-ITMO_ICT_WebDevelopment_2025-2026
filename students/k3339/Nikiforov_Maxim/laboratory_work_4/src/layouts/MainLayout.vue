<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const drawer = ref(false)
const auth = useAuthStore()
const router = useRouter()

const navItems = [
  { title: 'Главная', to: { name: 'home' }, icon: 'mdi-home' },
  { title: 'Читальные залы', to: { name: 'reading-rooms' }, icon: 'mdi-book-open-variant' },
  { title: 'Читатели', to: { name: 'readers' }, icon: 'mdi-account-group' },
  { title: 'Книги', to: { name: 'books' }, icon: 'mdi-book' },
  { title: 'Закрепления', to: { name: 'assignments' }, icon: 'mdi-bookmark' },
  { title: 'Операции библиотекаря', to: { name: 'librarian' }, icon: 'mdi-library' },
  { title: 'Запросы', to: { name: 'queries' }, icon: 'mdi-magnify' },
]

async function onLogout() {
  await auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <v-app>
    <v-app-bar color="primary" density="compact">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-toolbar-title>Библиотека</v-toolbar-title>
      <v-spacer />
      <v-btn :to="{ name: 'profile' }" variant="text" icon="mdi-account" />
      <v-btn variant="text" icon="mdi-logout" @click="onLogout" />
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" temporary>
      <v-list nav density="compact">
        <v-list-item
          v-for="item in navItems"
          :key="item.title"
          :to="item.to"
          :prepend-icon="item.icon"
          :title="item.title"
        />
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>
