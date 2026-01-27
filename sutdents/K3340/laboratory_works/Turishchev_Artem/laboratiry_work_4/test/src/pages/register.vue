<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="6" md="4">
        <v-card class="pa-6">
          <v-card-title class="text-h5 text-center">Регистрация</v-card-title>
          <v-form @submit.prevent="register">
            <v-text-field
              v-model="username"
              label="Логин (username)"
              prepend-inner-icon="mdi-account"
              variant="outlined"
              required
            ></v-text-field>

            <v-text-field
              v-model="email"
              label="Email"
              type="email"
              prepend-inner-icon="mdi-email"
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
              color="success"
              block
              :loading="loading"
            >
              Зарегистрироваться
            </v-btn>

            <v-btn
              to="/login"
              variant="text"
              block
              class="mt-2"
            >
              Уже есть аккаунт? Войти
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
const email = ref('');
const password = ref('');
const loading = ref(false);
const router = useRouter();

const register = async () => {
  loading.value = true;
  try {
    await api.post('/auth/users/', {
      username: username.value,
      email: email.value,
      password: password.value,
    });
    alert('Регистрация успешна! Теперь войдите.');
    router.push('/login');
  } catch (err) {
    const errors = err.response?.data;
    let msg = 'Ошибка регистрации';
    if (errors) {
      msg = Object.entries(errors)
        .map(([field, msgs]) => `${field}: ${msgs.join(', ')}`)
        .join('\n');
    }
    alert(msg);
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>