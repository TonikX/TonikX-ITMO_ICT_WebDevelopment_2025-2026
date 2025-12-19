<template>
  <v-container class="fill-height justify-center">
    <v-card width="400" class="pa-4">
      <v-card-title>Вход</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="login">
          <v-text-field v-model="form.username" label="Логин" required></v-text-field>
          <v-text-field v-model="form.password" label="Пароль" type="password" required></v-text-field>
          <v-btn type="submit" color="primary" block class="mt-4">Войти</v-btn>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn to="/register" variant="text" block>Нет аккаунта? Регистрация</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import api from '../api';
import { useRouter } from 'vue-router';

const router = useRouter();
const form = ref({ username: '', password: '' });

const login = async () => {
  try {
    const response = await api.post('/auth/token/login/', form.value);
    localStorage.setItem('auth_token', response.data.auth_token);
    router.push('/profile');
  } catch (e) {
    alert('Ошибка входа: ' + JSON.stringify(e.response.data));
  }
};
</script>
