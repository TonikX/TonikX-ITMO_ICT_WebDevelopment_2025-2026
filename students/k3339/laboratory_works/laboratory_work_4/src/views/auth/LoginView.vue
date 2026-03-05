<script setup>
import {ref} from "vue";
import router from "@/utils/router.js";
import {tokenStore} from "@/stores/token.js"
import axios from "axios";

const token = tokenStore()
const form = ref({
  username: '',
  password: ''
})

function login() {
  axios.post('/auth/token/login', form.value).then(response => {
        if (response.status === 200) {
          token.setToken(response.data.auth_token)
          router.push('employees/')
        }
      }
  ).catch(error => console.log(error))
}

function register() {
  router.push("/register")
}

</script>

<template>
  <v-app>
    <v-container class="d-flex align-center justify-center fill-height">
      <div class="w-50 text-center">
        <h2>Вход</h2>
        <v-text-field label="Логин" v-model="form.username"></v-text-field>
        <v-text-field label="Пароль" v-model="form.password" type="password"></v-text-field>
        <div class="d-flex justify-center mt-4">
          <v-btn class="mx-2" color="primary" @click="login">Войти</v-btn>
          <v-btn class="mx-2" color="secondary" @click="register">Зарегистрироваться</v-btn>
        </div>
      </div>
    </v-container>
  </v-app>
</template>

<style scoped>

</style>
