<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title>Библиотека</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text to="/books">Книги</v-btn>
      <v-btn text to="/halls">Залы</v-btn>
      <v-btn text to="/readers">Читатели</v-btn>
      <v-btn text to="/issues">Выдачи</v-btn>
      <v-btn text to="/reports">Запросы</v-btn>
      <v-btn text to="/profile">Профиль</v-btn>
      <v-btn v-if="!isAuthenticated" text to="/login">Вход</v-btn>
      <v-btn v-if="!isAuthenticated" text to="/register">Регистрация</v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const isAuthenticated = ref(!!localStorage.getItem("token"));

watch(
  () => route.fullPath,
  () => {
    isAuthenticated.value = !!localStorage.getItem("token");
  },
  { immediate: true },
);
</script>

<style scoped></style>
