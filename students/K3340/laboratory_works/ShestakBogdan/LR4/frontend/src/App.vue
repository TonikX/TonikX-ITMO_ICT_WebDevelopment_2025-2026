<template>
  <v-app>
    <v-app-bar color="surface" dark>
      <v-app-bar-title>
        Диспетчерская автобусного парка
      </v-app-bar-title>

      <v-spacer />

      <!-- Навигация -->

      <v-btn
        variant="text"
        :to="{ name: 'Drivers' }"
      >
        Водители
      </v-btn>

      <v-btn
        variant="text"
        :to="{ name: 'Shifts' }"
      >
        Смены
      </v-btn>
      
      <v-divider vertical class="mx-2" />

      <v-btn
        v-if="isLoggedIn"
        variant="text"
        :to="{ name: 'Profile' }"
      >
        Профиль
      </v-btn>

      <!-- Вход/выход -->
      <v-btn
        v-if="!isLoggedIn"
        color="primary"
        variant="flat"
        @click="goLogin"
      >
        Войти
      </v-btn>

      <v-btn
        v-else
        color="primary"
        variant="flat"
        @click="logout"
      >
        Выйти
      </v-btn>
    </v-app-bar>

    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>

<script setup>
import { useRouter } from "vue-router";
import { isLoggedIn, logout as storeLogout } from "./store/auth";

const router = useRouter();

const goLogin = () => {
  router.push("/login");
};

const logout = () => {
  storeLogout();
  router.push("/login");
};
</script>

<style>
html,
body {
  background-color: #121212 !important;
  color: #ffffff;
}
</style>