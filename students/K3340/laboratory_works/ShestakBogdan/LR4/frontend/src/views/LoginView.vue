<template>
  <div>
    <h2>Вход</h2>
    <input v-model="username" placeholder="Логин" />
    <input v-model="password" placeholder="Пароль" type="password" />

    <button @click="login">Войти</button>
  </div>
</template>

<script setup>
import http from "../api/http.js";
import { ref } from "vue";
import { useRouter } from "vue-router";

const username = ref("");
const password = ref("");
const router = useRouter();

async function login() {
  try {
    const res = await http.post("/auth/token/login/", {
      username: username.value,
      password: password.value,
    });

    localStorage.setItem("auth_token", res.data.auth_token);
    router.push("/drivers"); // переход к списку водителей
  } catch (err) {
    alert("Ошибка авторизации");
    console.error(err);
  }
}
</script>