<template>
  <v-app>
    <Navigation />

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <v-footer app>
      <v-spacer></v-spacer>
      <div>Guard Market &copy; {{ new Date().getFullYear() }}</div>
    </v-footer>
  </v-app>
</template>

<script setup>
import Navigation from '@/components/Navigation.vue'
</script>