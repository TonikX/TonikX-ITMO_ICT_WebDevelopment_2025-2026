<template>
  <v-app>
    <v-app-bar app color="primary" dark v-if="$route.name !== 'Login' && $route.name !== 'Register'">
      <v-toolbar-title>Лизинг Авто</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text to="/" v-if="isAuthenticated">Главная</v-btn>
      <v-btn text to="/profile" v-if="isAuthenticated">Профиль</v-btn>

      <!-- Кнопка в админку (только для админов) -->
      <v-btn text to="/admin" v-if="isAdmin">
        <v-icon left>mdi-shield-account</v-icon>
        Админка
      </v-btn>

      <v-btn text @click="logout" v-if="isAuthenticated">Выйти</v-btn>
      <v-btn text to="/login" v-else>Войти</v-btn>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>

    <v-footer app color="grey lighten-3" v-if="$route.name !== 'Login' && $route.name !== 'Register'">
      <v-col class="text-center" cols="12">
        {{ new Date().getFullYear() }} — Лизинг Авто
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'App',
  computed: {
    ...mapGetters('auth', ['isAuthenticated', 'user'])
  },
  methods: {
    ...mapActions('auth', ['logout']),
    handleLogout() {
      this.logout()
      this.$router.push('/login')
    }
  },
  created() {
    // При загрузке приложения проверяем авторизацию
    if (this.isAuthenticated && !this.user) {
      this.$store.dispatch('auth/fetchUser')
    }
  }
}
</script>