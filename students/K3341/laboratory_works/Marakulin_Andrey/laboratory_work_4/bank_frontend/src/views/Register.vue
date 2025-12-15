<template>
  <v-container>
    <v-card class="mx-auto" max-width="450">
      <v-card-title class="text-h5 success white--text pa-4">
        Регистрация нового пользователя
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="register">

          <v-text-field
            v-model="username"
            label="Имя пользователя"
            prepend-icon="mdi-account-plus"
            required
          ></v-text-field>

          <v-text-field
            v-model="email"
            label="Email"
            prepend-icon="mdi-email"
            type="email"
            required
          ></v-text-field>

          <v-text-field
            v-model="password"
            label="Пароль"
            prepend-icon="mdi-lock"
            type="password"
            required
          ></v-text-field>

          <v-alert
            v-if="error"
            type="error"
            dense
            text
            class="mb-3"
          >
            {{ error }}
          </v-alert>

          <v-btn
            color="success"
            class="mr-4"
            type="submit"
            :loading="loading"
          >
            Зарегистрироваться
          </v-btn>
          <v-btn
            text
            @click="$router.push('/login')"
          >
            Уже есть аккаунт?
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../authApi';

const router = useRouter();
const username = ref('');
const email = ref('');
const password = ref('');
const error = ref(null);
const loading = ref(false);

const register = async () => {
  error.value = null;
  loading.value = true;

  try {
    await api.post('/auth/users/', {
      username: username.value,
      email: email.value,
      password: password.value,
    });

    // Регистрация успешна, перенаправляем на страницу входа
    alert('Регистрация прошла успешно! Теперь войдите в систему.');
    router.push('/login');

  } catch (err) {
    if (err.response && err.response.data) {
        // DRF часто возвращает ошибки валидации в объекте
        const errors = err.response.data;
        if (errors.username) error.value = `Имя пользователя: ${errors.username.join(', ')}`;
        else if (errors.email) error.value = `Email: ${errors.email.join(', ')}`;
        else if (errors.password) error.value = `Пароль: ${errors.password.join(', ')}`;
        else error.value = 'Ошибка при регистрации.';
    } else {
        error.value = 'Произошла ошибка при подключении к серверу.';
    }
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>