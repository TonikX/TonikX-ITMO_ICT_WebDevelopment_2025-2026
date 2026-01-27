<template>
  <v-app>
    <TopBar />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import TopBar from '@/components/TopBar.vue';
</script>