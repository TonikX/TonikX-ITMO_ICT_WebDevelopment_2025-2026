<script setup>
import {ref} from "vue";
import router from "@/utils/router.js";
import {tokenStore} from "@/stores/token.js"
import axios from "axios";

const tokenStorage = tokenStore()
const form = ref({
  email: '',
  username: '',
  password: ''
})

function register() {
  axios.post('/auth/users/', form.value).then(async response => {
        if (response.status === 201) {
          const token = await getToken(form.value.username, form.value.password);
          tokenStorage.setToken(token)
          await router.push('employees/')
        }
      }
  ).catch(error => console.log(error))
}

function login() {
  router.push("/login");
}

async function getToken(username, password) {
  return axios.post('/auth/token/login/', {username: username, password: password}).then(response => {
    if (response.status === 200) {
      return response.data.auth_token;
    }
  }).catch(error => console.log(error))
}

</script>

<template>
  <v-app>
    <v-container class="d-flex align-center justify-center fill-height">
      <div class="w-50 text-center">
        <h2>Регистрация</h2>
        <v-text-field label="Почта" v-model="form.email"></v-text-field>
        <v-text-field label="Логин" v-model="form.username"></v-text-field>
        <v-text-field label="Пароль" v-model="form.password" type="password"></v-text-field>
        <div class="d-flex justify-center mt-4">
          <v-btn class="mx-2" @click="register">Зарегистрироваться</v-btn>
          <v-btn class="mx-2" @click="login">Войти</v-btn>
        </div>
      </div>
    </v-container>
  </v-app>
</template>

<style scoped>

</style>