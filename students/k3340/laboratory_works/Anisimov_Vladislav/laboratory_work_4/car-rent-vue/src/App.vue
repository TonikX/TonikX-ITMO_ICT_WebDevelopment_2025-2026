<template>
  <v-app>
    <AppBar v-if="showNavigation" />
    
    <v-main>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-main>

    <!-- Уведомления -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
      location="bottom right"
    >
      {{ snackbar.message }}
    </v-snackbar>
  </v-app>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import AppBar from '@/components/AppBar.vue'

const route = useRoute()

// Показывать навигацию только на страницах, где это нужно
const showNavigation = computed(() => {
  return route.meta.requiresAuth !== false
})

// Глобальные уведомления
const snackbar = ref({
  show: false,
  message: '',
  color: 'success'
})
</script>

<style>
/* Глобальные стили */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Кастомные стили для скроллбара */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #bdbdbd;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #9e9e9e;
}

/* Улучшение отображения в Vuetify */
.v-card {
  border-radius: 12px !important;
}

.v-btn {
  text-transform: none !important;
  letter-spacing: normal !important;
}
</style>