<template>
  <v-app>
    <v-app-bar color="primary" v-if="isAuth">
      <v-app-bar-title>Bus Fleet</v-app-bar-title>
      <v-btn to="/">Drivers</v-btn>
      <v-btn to="/buses">Buses</v-btn>
      <v-btn to="/bus-types">Types</v-btn>
      <v-btn to="/routes">Routes</v-btn>
      <v-btn to="/schedules">Schedules</v-btn>
      <v-btn to="/absences">Absences</v-btn>
      <v-btn to="/report">Report</v-btn>
      <v-spacer />
      <v-btn to="/profile" icon="mdi-account" />
      <v-btn icon="mdi-logout" @click="logout" />
    </v-app-bar>
    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()
const isAuth = computed(() => !!localStorage.getItem('token') && !['/login', '/register'].includes(route.path))
const logout = () => { localStorage.removeItem('token'); router.push('/login') }
</script>
