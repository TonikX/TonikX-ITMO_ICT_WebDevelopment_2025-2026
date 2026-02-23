<template>
  <v-container>
    <h1>Вход</h1>
    <v-form @submit.prevent="login">
      <v-text-field v-model="form.username" label="Никнейм" type="text" required></v-text-field>

      <v-text-field v-model="form.password" label="Пароль" type="password" required></v-text-field>

      <v-btn color="primary" @click="login" :disabled="!form.username || !form.password" block> Войти </v-btn>
    </v-form>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import router from '@/router';
import axios from 'axios';
import { useTokenStore } from '@/stores/token';

const form = ref({
  username: '',
  password: '',
});

const store = useTokenStore();

async function login() {
  try {
    const res = await axios.post('api/auth/token/login/', form.value);
    store.setToken(res.data.auth_token);
    router.push('/rooms');
  } catch (e) {
    console.error(e);
  }
}
</script>

<style scoped></style>
