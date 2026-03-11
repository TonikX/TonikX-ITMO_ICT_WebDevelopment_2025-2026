<template>
  <v-container>
    <h1>Регистрация</h1>
    <v-form @submit.prevent="register">
      <v-text-field v-model="form.username" label="Никнейм" type="text" required></v-text-field>

      <v-text-field v-model="form.email" label="Email" type="text" required></v-text-field>

      <v-text-field v-model="form.password_1" label="Пароль" type="password" required></v-text-field>

      <v-text-field v-model="form.password_2" label="Подтверждение пароля" type="password" required></v-text-field>

      <v-btn
        color="primary"
        @click="register"
        :disabled="!form.username || !form.password_1 || !form.email || form.password_1 !== form.password_2"
        block
      >
        Зарегистрироваться
      </v-btn>
    </v-form>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import router from '@/router';
import axios from 'axios';

const form = ref({
  username: '',
  email: '',
  password_1: '',
  password_2: '',
});

async function register() {
  if (form.value.password_1 !== form.value.password_2) {
    alert('Пароли не совпадают');
  }
  try {
    await axios.post('/api/auth/users/', {
      email: form.value.email,
      username: form.value.username,
      password: form.value.password_1,
    });
    alert('Вы зарегистрировались');
    router.push('/login');
  } catch (error) {
    console.error('Ошибка регистрации:', error);
    alert('Ошибка, попробуйте снова');
  }
}
</script>

<style scoped></style>
