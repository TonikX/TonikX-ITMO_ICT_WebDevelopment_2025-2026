
<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="6" md="4">
        <v-card class="pa-6">
          <v-card-title class="text-h5 text-center">Вход</v-card-title>
          <v-form @submit.prevent="login">
            <v-text-field
              v-model="username"
              label="Логин (username)"
              prepend-inner-icon="mdi-account"
              variant="outlined"
              required
            ></v-text-field>

            <v-text-field
              v-model="password"
              label="Пароль"
              type="password"
              prepend-inner-icon="mdi-lock"
              variant="outlined"
              required
            ></v-text-field>

            <v-btn
              type="submit"
              color="primary"
              block
              :loading="loading"
            >
              Войти
            </v-btn>

            <v-btn
              to="/register"
              variant="text"
              block
              class="mt-2"
            >
              Нет аккаунта? Зарегистрироваться
            </v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';

const username = ref('');
const password = ref('');
const loading = ref(false);
const router = useRouter();

const login = async () => {
  loading.value = true;
  try {
    const res = await api.post('/auth/token/login/', {
      username: username.value,
      password: password.value,
    });
    localStorage.setItem('auth_token', res.data.auth_token);
    router.push('/');
  } catch (err) {
    alert('Неверный логин или пароль');
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>