<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      :temporary="false"
      permanent
      app
    >
      <v-list-item
        prepend-icon="mdi-book-open-variant"
        title="Читальный зал"
        subtitle="Система управления"
      ></v-list-item>
      <v-divider></v-divider>
      <v-list density="compact" nav>
        <v-list-item
          prepend-icon="mdi-view-dashboard"
          title="Панель управления"
          value="dashboard"
          :to="{ name: 'Dashboard' }"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-book-open-page-variant"
          title="Читальные залы"
          value="reading-rooms"
          :to="{ name: 'ReadingRooms' }"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-account"
          title="Читатели"
          value="readers"
          :to="{ name: 'Readers' }"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-calendar-clock"
          title="Бронирования"
          value="reservations"
          :to="{ name: 'Reservations' }"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-account-tie"
          title="Библиотекари"
          value="librarians"
          :to="{ name: 'Librarians' }"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-chart-box"
          title="Отчеты"
          value="reports"
          :to="{ name: 'Reports' }"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Система управления читальным залом</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props">
            <v-avatar size="32">
              <v-icon>mdi-account</v-icon>
            </v-avatar>
          </v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-title>Добро пожаловать, {{ authStore.user?.username || 'Администратор' }}!</v-list-item-title>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="handleLogout">
            <v-list-item-title>Выйти</v-list-item-title>
            <template v-slot:prepend>
              <v-icon>mdi-logout</v-icon>
            </template>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const drawer = ref(true)
const router = useRouter()
const authStore = useAuthStore()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

