<template>
  <v-app>
    <v-app-bar app color="primary" dark density="compact">
      <v-toolbar-title>Hotel Admin</v-toolbar-title>

      <template v-slot:append>
        <template v-if="isLoggedIn">
          <v-btn to="/dashboard" variant="text">Дашборд</v-btn>
          <v-btn to="/rooms" variant="text">Номера</v-btn>
          <v-btn to="/booking" variant="text">Бронь</v-btn>
          <v-btn to="/stays" variant="text">Заселения</v-btn>
          <v-btn to="/staff" variant="text">Персонал</v-btn>

          <v-menu>
            <template v-slot:activator="{ props }">
              <v-btn icon="mdi-account" v-bind="props"></v-btn>
            </template>
            <v-list>
              <v-list-item to="/profile" title="Профиль"></v-list-item>
              <v-list-item title="Выход" @click="logout" style="cursor: pointer; color: red;"></v-list-item>
            </v-list>
          </v-menu>
        </template>

        <template v-else>
          <v-btn to="/login" variant="text">Вход</v-btn>
          <v-btn to="/register" variant="outlined" class="ml-2">Регистрация</v-btn>
        </template>
      </template>
    </v-app-bar>

    <v-main class="bg-grey-lighten-4">
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { initAuthFromStorage, setAuthToken, isLoggedIn } from './auth'

const router = useRouter()

onMounted(() => {
  initAuthFromStorage()
})

const logout = () => {
  setAuthToken(null)
  router.push('/login')
}
</script>
