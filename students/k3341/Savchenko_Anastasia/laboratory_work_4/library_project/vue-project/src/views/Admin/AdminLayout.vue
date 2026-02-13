<template>
  <v-app>
    <v-app-bar color="primary">
      <v-toolbar-title>📚 Админ-панель</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn @click="logout">Выйти</v-btn>
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const logout = () => { auth.logout(); router.push('/login') }
</script>