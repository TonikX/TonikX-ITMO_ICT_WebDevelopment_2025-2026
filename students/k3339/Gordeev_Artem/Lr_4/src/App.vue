<template>
  <component :is="layout">
    <router-view />
  </component>

  <v-snackbar
    v-model="alertStore.visible"
    :color="alertStore.type"
    :timeout="alertStore.timeout"
    location="top right"
  >
    {{ alertStore.message }}
    <template v-slot:actions>
      <v-btn
        variant="text"
        @click="alertStore.close()"
      >
        Закрыть
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'
import { useAlertStore } from '@/stores/alert'

const route = useRoute()
const alertStore = useAlertStore()

const layout = computed(() => {
  return route.meta.layout === 'auth' ? AuthLayout : DefaultLayout
})
</script>
