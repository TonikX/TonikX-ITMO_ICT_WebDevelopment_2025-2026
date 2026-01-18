<template>
  <v-app-bar app color="green lighten-2" dark>
    <v-toolbar-title>Hotel Management</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-tabs v-model="activeTab" grow>
      <v-tab @click="goTo('/login')" value="login">
        Login
      </v-tab>

      <v-tab @click="goTo('/profile')" value="profile">
        Profile
      </v-tab>

      <v-tab @click="goTo('/residents')" value="residents">
        Residents
      </v-tab>

      <v-tab @click="goTo('/reservations')" value="reservations">
        Reservations
      </v-tab>

      <v-tab @click="goTo('/rooms')" value="rooms">
        Rooms
      </v-tab>

      <v-tab @click="goTo('/workers')" value="workers">
        Workers
      </v-tab>

      <v-tab @click="goTo('/cleaning')" value="cleaning">
        Cleaning
      </v-tab>


      <v-menu>
        <template #activator="{ props }">
          <v-tab v-bind="props" value="queries">
            Запросы
          </v-tab>
        </template>

        <v-list>
          <v-list-item
            title="Поиск клиентов по комнате и датам"
            @click="goTo('/clients-by-room')"
          />
          <v-list-item
            title="О клиентах, прибывших из заданного города"
            @click="goTo('/clients-from-city')"
          />
          <v-list-item
            title="clients-with-city"
            @click="goTo('/clients-with-city')"
          />
          <v-list-item
            title="Отчёт по отелю"
            @click="goTo('/report')"
          />
          <v-list-item
            title="Уборка номера"
            @click="goTo('/cleaning-info-per-day')"
          />
          <v-list-item
            title="Свободные номера"
            @click="goTo('/available-rooms')"
          />

        </v-list>
      </v-menu>
    </v-tabs>
  </v-app-bar>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const activeTab = ref('residents')

watch(
  () => route.path,
  () => {
    if (route.path.startsWith('/residents')) {
      activeTab.value = 'residents'
    } else if (route.path.startsWith('/reservations')) {
      activeTab.value = 'reservations'
    } else if (route.path.startsWith('/rooms')) {
      activeTab.value = 'rooms'
    } else if (route.path.startsWith('/login')) {
      activeTab.value = 'login'
    }
  },
  { immediate: true }
)

const goTo = (path) => {
  router.push(path)
}
</script>
