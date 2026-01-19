<template>
  <v-layout>
    <AppNav />

    <v-main>
      <v-container fluid class="py-4">
        <router-view />
      </v-container>
    </v-main>
  </v-layout>
</template>

<script setup>
import AppNav from "@/components/AppNav.vue";
</script>