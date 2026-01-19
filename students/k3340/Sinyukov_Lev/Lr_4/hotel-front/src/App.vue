<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>

    <AppSnackbar />
  </v-app>
</template>

<script setup>
import AppSnackbar from "@/components/AppSnackbar.vue";
</script>