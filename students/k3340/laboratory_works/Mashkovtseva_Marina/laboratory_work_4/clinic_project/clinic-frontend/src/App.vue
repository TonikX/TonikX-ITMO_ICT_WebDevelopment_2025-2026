<template>
  <v-app>
    <!-- Всегда показываем навбар кроме страниц логина/регистрации -->
    <v-app-bar app color="primary" dark v-if="showNavbar">
      <v-toolbar-title>Clinic System</v-toolbar-title>
      <v-spacer />

      <!-- Динамически проверяем токен каждый раз -->
      <template v-if="hasToken()">
        <v-btn text to="/profile">Профиль</v-btn>
        <v-btn text to="/patients">Пациенты</v-btn>
        <v-btn text to="/visits">Визиты</v-btn>
        <v-btn text to="/payments">Платежи</v-btn>
        <v-btn text to="/room">Кабинеты</v-btn>
        <v-btn text to="/doctor">Врачи</v-btn>
        <v-btn text @click="logout">Выйти</v-btn>
      </template>

      <template v-else>
        <v-btn text to="/login">Войти</v-btn>
        <v-btn text to="/register">Регистрация</v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
export default {
  computed: {
    showNavbar() {
      return this.$route.name !== 'Login' && this.$route.name !== 'Register';
    }
  },
  methods: {
    // Проверяем токен напрямую каждый раз
    hasToken() {
      return !!localStorage.getItem('token');
    },
    logout() {
      localStorage.removeItem("token");
      window.location.href = "/login";
    },
  },
};
</script>