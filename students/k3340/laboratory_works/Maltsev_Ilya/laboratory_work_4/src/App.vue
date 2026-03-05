<script setup>

import {tokenStore} from "@/stores/token.js";
import router from "@/utils/router.js";
import axios from "axios";

const token = tokenStore()

if (token.token) {
  axios.defaults.headers.common['Authorization'] = `Token ${token.token}`
}

function logout() {
  token.deleteToken()
  router.push("/login")
}

</script>

<template>
  <v-layout class="rounded rounded-md">
    <v-app-bar permanent>
      <div class="d-flex align-center">
        <v-list-item title="Страховое агентство"></v-list-item>
        <template v-if="token.token">
          <router-link to="/agents" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Агенты"></v-list-item>
          </router-link>
          <router-link to="/organizations" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Организации"></v-list-item>
          </router-link>
          <router-link to="/clients" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Клиенты"></v-list-item>
          </router-link>
          <router-link to="/reports" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Отчёт"></v-list-item>
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

    <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
      <router-view/>
    </v-main>
  </v-layout>
</template>


<style scoped>

</style>