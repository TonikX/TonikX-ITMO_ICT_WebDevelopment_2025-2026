<template>
  <v-layout>
    <v-navigation-drawer v-model="drawer" permanent>
      <v-list density="compact" nav>
        <v-list-item title="Airline Admin" subtitle="Vue + DRF" />
        <v-divider class="my-2" />
        <v-list-item :to="{name:'companies'}" prepend-icon="mdi-domain" title="Компании" />
        <v-list-item :to="{name:'aircrafts'}" prepend-icon="mdi-airplane" title="Самолёты" />
        <v-list-item :to="{name:'airports'}" prepend-icon="mdi-airport" title="Аэропорты" />
        <v-list-item :to="{name:'employees'}" prepend-icon="mdi-account-group" title="Сотрудники" />
        <v-list-item :to="{name:'crews'}" prepend-icon="mdi-account-multiple" title="Экипажи" />
        <v-list-item :to="{name:'crewMembers'}" prepend-icon="mdi-account-plus" title="Состав экипажа" />
        <v-list-item :to="{name:'flights'}" prepend-icon="mdi-map-marker-path" title="Рейсы" />
        <v-list-item :to="{name:'transitStops'}" prepend-icon="mdi-map-marker" title="Транзитные остановки" />
        <v-list-item :to="{name:'reports'}" prepend-icon="mdi-chart-box" title="Запросы/Отчёты" />
        <v-divider class="my-2" />
        <v-list-item :to="{name:'profile'}" prepend-icon="mdi-account" title="Профиль" />
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-app-bar flat>
        <v-app-bar-nav-icon @click="drawer = !drawer" />
        <v-toolbar-title>{{ title }}</v-toolbar-title>
        <v-spacer />
        <v-btn variant="text" prepend-icon="mdi-logout" @click="logout">Выйти</v-btn>
      </v-app-bar>

      <v-container class="py-6" fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-layout>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const drawer = ref(true)
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
auth.hydrate()

const title = computed(() => route.meta?.title || (route.name ? String(route.name) : 'Dashboard'))

async function logout() {
  await auth.logout()
  router.push({ name: 'login' })
}
</script>
