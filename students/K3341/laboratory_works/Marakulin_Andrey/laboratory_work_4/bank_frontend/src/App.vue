<template>
  <v-app>
    <v-main>
      <v-container>

        <v-toolbar dense>
          <v-toolbar-title>Bank API App</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn text to="/login">Login</v-btn>
          <v-btn text to="/register">Register</v-btn>
          <v-btn text to="/clients">Clients</v-btn>
          <v-btn text to="/profile">Profile</v-btn>
        </v-toolbar>

        <router-view></router-view>

      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
// Здесь не нужно ничего импортировать, кроме других компонентов, если они используются напрямую.
// Router-link, v-app, v-btn и т.д. доступны глобально.
</script>

<style scoped>
/* Ваши стили */
</style>