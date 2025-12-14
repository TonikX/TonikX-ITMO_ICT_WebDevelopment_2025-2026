<template>
  <v-container class="fill-height justify-center">
    <v-card width="400" class="pa-4">
      <v-card-title>Регистрация</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="register">
          <v-text-field v-model="form.username" label="Логин" required></v-text-field>
          <v-text-field v-model="form.email" label="Email" required></v-text-field>
          <v-text-field v-model="form.password" label="Пароль" type="password" required></v-text-field>
          <v-text-field v-model="form.re_password" label="Повторите пароль" type="password" required></v-text-field>
          <v-btn type="submit" color="primary" block class="mt-4">Создать аккаунт</v-btn>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn to="/login" variant="text" block>Уже есть аккаунт? Войти</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import api from '../api';
import { useRouter } from 'vue-router';

const router = useRouter();
const form = ref({ username: '', email: '', password: '' });

const register = async () => {
  try {
    await api.post('/auth/users/', form.value);
    alert('Успешно! Теперь войдите.');
    router.push('/login');
  } catch (e) {
    alert('Ошибка: ' + JSON.stringify(e.response.data));
  }
};
</script>
