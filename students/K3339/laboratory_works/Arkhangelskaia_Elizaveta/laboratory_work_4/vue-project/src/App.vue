<template>
  <v-app>
    <AppHeader />

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import AppHeader from './components/AppHeader.vue'
</script>
