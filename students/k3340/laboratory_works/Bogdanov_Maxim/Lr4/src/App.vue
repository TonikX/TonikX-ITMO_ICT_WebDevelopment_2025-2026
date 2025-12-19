<template>
  <v-app>
    <v-app-bar color="primary" dark>
      <v-app-bar-title>Система управления школой</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="authStore.isAuthenticated" icon @click="toggleTheme">
        <v-icon>{{ theme.global.name.value === 'light' ? 'mdi-weather-night' : 'mdi-weather-sunny' }}</v-icon>
      </v-btn>
      <v-menu v-if="authStore.isAuthenticated" location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props">
            <v-icon>mdi-account-circle</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-title>{{ authStore.user?.username }}</v-list-item-title>
            <v-list-item-subtitle>{{ authStore.user?.role }}</v-list-item-subtitle>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="logout">
            <v-list-item-title>Выйти</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer v-if="authStore.isAuthenticated" permanent>
      <v-list>
        <v-list-item prepend-icon="mdi-view-dashboard" title="Главная" value="home" :to="{ name: 'home' }"></v-list-item>
        <v-list-item v-if="isAdmin" prepend-icon="mdi-account-tie" title="Учителя" value="teachers" :to="{ name: 'teachers' }"></v-list-item>
        <v-list-item v-if="isAdmin" prepend-icon="mdi-school" title="Ученики" value="students" :to="{ name: 'students' }"></v-list-item>
        <v-list-item v-if="isAdmin" prepend-icon="mdi-google-classroom" title="Классы" value="classes" :to="{ name: 'classes' }"></v-list-item>
        <v-list-item v-if="isAdmin" prepend-icon="mdi-calendar-clock" title="Расписание" value="schedules" :to="{ name: 'schedules' }"></v-list-item>
        <v-list-item prepend-icon="mdi-star" title="Оценки" value="grades" :to="{ name: 'grades' }"></v-list-item>
        <v-list-item prepend-icon="mdi-chart-line" title="Статистика" value="info" :to="{ name: 'info' }"></v-list-item>
        <v-list-item prepend-icon="mdi-file-document" title="Отчеты" value="reports" :to="{ name: 'reports' }"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from 'vuetify'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const theme = useTheme()
const authStore = useAuthStore()

const isAdmin = computed(() => authStore.user?.role === 'admin')

const toggleTheme = () => {
  theme.global.name.value = theme.global.name.value === 'light' ? 'dark' : 'light'
}

const logout = () => {
  authStore.logout()
  router.push({ name: 'login' })
}
</script>

