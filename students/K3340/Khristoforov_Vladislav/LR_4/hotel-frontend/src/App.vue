<script setup>
/**
 * App.vue - Корневой компонент приложения.
 * Задает глобальную разметку (Layout) с навигацией и областью контента.
 */
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
</script>

<template>
  <!-- v-app: Точка входа для стилей и функционала Vuetify -->
  <v-app>
    <Navbar />

    <!-- v-main: Контейнер для контента. Автоматически добавляет отступы (padding), 
         чтобы контент не перекрывался Navbar'ом -->
    <v-main>
      <!-- Сюда подставляются компоненты страниц в зависимости от URL -->
      <RouterView />
    </v-main>
  </v-app>
</template>