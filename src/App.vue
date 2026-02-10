<script setup>

import {tokenStore} from "@/stores/token.js";
import router from "@/router/index.js";

const token = tokenStore()

function logout() {
  token.deleteToken()
  router.push("/login")
}
</script>

<template>
  <v-layout class="rounded rounded-md">
    <v-app-bar permanent>
      <div class="d-flex align-center">
        <v-list-item title="Отель"></v-list-item>
        <template v-if="token.token">
          <router-link to="/clients" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Клиенты"></v-list-item>
          </router-link>
          <router-link to="/schedule" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Расписание"></v-list-item>
          </router-link>
          <router-link to="/employees" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Сотрудники"></v-list-item>
          </router-link>
          <router-link to="/rooms" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Комнаты"></v-list-item>
          </router-link>
          <router-link to="/stay_records" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Бронирования"></v-list-item>
          </router-link>
          <router-link to="/profile" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Профиль"></v-list-item>
             </router-link>
        </template>
      </div>

      <v-spacer/>

      <div class="d-flex align-center">
        <template v-if="!token.token">
          <router-link to="/login" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Войти"></v-list-item>
          </router-link>
          <router-link to="/register" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Зарегистрироваться"></v-list-item>
          </router-link>
        </template>
        <template v-else>
          <v-list-item class="text-red" @click="logout">Выйти</v-list-item>
        </template>
      </div>
    </v-app-bar>

    <v-main class="d-flex align-center justify-center">
      <router-view />
    </v-main>
  </v-layout>
</template>


<style scoped>

</style>