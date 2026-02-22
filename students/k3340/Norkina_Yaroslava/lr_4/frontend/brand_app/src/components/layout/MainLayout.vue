<template>
  <v-app>
    <Header />
    <v-main>
      <v-container fluid class="pa-0">
        <router-view />
      </v-container>
    </v-main>
    <Footer />
  </v-app>
</template>

<script setup>
import Header from './Header.vue'
import Footer from './Footer.vue'
</script>

<style scoped>
.v-main {
  min-height: calc(100vh - 120px); /* Высота минус хедер и футер */
}
</style>