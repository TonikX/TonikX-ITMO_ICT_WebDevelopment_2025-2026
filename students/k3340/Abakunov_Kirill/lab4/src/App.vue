<template>
  <v-app>
    <v-app-bar color="primary" prominent>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      
      <v-toolbar-title>
        <router-link to="/" class="text-white text-decoration-none">
          Система управления гостиницей
        </router-link>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <template v-if="authStore.isAuthenticated">
        <v-btn icon @click="toggleTheme">
          <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-moon-waning-crescent' }}</v-icon>
        </v-btn>
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn icon v-bind="props">
              <v-icon>mdi-account-circle</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item :title="authStore.user?.username" subtitle="Профиль" to="/profile">
              <template v-slot:prepend>
                <v-icon>mdi-account</v-icon>
              </template>
            </v-list-item>
            <v-divider></v-divider>
            <v-list-item @click="handleLogout">
              <template v-slot:prepend>
                <v-icon>mdi-logout</v-icon>
              </template>
              <v-list-item-title>Выйти</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
      <template v-else>
        <v-btn icon @click="toggleTheme">
          <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-moon-waning-crescent' }}</v-icon>
        </v-btn>
        <v-btn to="/login" variant="text">Войти</v-btn>
        <v-btn to="/register" variant="outlined" class="ml-2">Регистрация</v-btn>
      </template>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" temporary>
      <v-list nav>
        <v-list-item to="/" prepend-icon="mdi-home" title="Главная"></v-list-item>
        <v-divider class="my-2"></v-divider>
        <v-list-item to="/rooms" prepend-icon="mdi-door" title="Номера"></v-list-item>
        <v-list-item to="/guests" prepend-icon="mdi-account-group" title="Гости"></v-list-item>
        <v-list-item to="/staff" prepend-icon="mdi-account-hard-hat" title="Служащие"></v-list-item>
        <v-list-item to="/schedules" prepend-icon="mdi-calendar-clock" title="Расписания уборки"></v-list-item>
        <v-divider class="my-2"></v-divider>
        <v-list-item 
          v-if="authStore.isAuthenticated" 
          to="/reports" 
          prepend-icon="mdi-chart-bar" 
          title="Отчёты"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer app class="bg-grey-lighten-3">
      <v-row justify="center" no-gutters>
        <v-col class="text-center" cols="12">
          <span class="text-grey">Лабораторная работа №4 — Vue.js + Vuetify</span>
        </v-col>
      </v-row>
    </v-footer>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="3000">
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar.show = false">Закрыть</v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script setup>
import { ref, provide, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from 'vuetify'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const theme = useTheme()
const authStore = useAuthStore()

const drawer = ref(false)
const isDark = ref(theme.global.current.value.dark)

const snackbar = reactive({
  show: false,
  text: '',
  color: 'success'
})

const showSnackbar = (text, color = 'success') => {
  snackbar.text = text
  snackbar.color = color
  snackbar.show = true
}

provide('showSnackbar', showSnackbar)

const toggleTheme = () => {
  isDark.value = !isDark.value
  theme.global.name.value = isDark.value ? 'dark' : 'light'
}

const handleLogout = async () => {
  await authStore.logout()
  showSnackbar('Вы успешно вышли из системы', 'info')
  router.push('/')
}
</script>
