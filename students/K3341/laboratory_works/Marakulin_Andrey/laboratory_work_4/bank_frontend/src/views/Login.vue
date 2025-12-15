<template>
  <v-container>
    <v-card class="mx-auto" max-width="450">
      <v-card-title class="text-h5 primary white--text pa-4">
        Вход в систему
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="login">
          <v-text-field
              v-model="username"
              label="Имя пользователя"
              prepend-icon="mdi-account"
              required
            ></v-text-field>

            <v-text-field
              v-model="password"
              label="Пароль"
              prepend-icon="mdi-lock"
              type="password"
              required
            ></v-text-field>

            <v-btn
              color="primary"
              class="mr-4"
              type="submit"
              :loading="loading"
            >
              Войти
            </v-btn>
          <v-btn
            text
            @click="$router.push('/register')"
          >
            Регистрация
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';
// Для валидации, если вы делали Практическую работу 4.1,
// мы можем использовать библиотеку Vuelidate (или используем простую встроенную валидацию)

const router = useRouter();
const username = ref('');
const password = ref('');
const error = ref(null);
const loading = ref(false);

// Здесь используем простую заглушку для валидации
const v$ = {
    username: { $invalid: computed(() => username.value.length === 0) },
    password: { $invalid: computed(() => password.value.length === 0) },
    $invalid: computed(() => v$.username.$invalid.value || v$.password.$invalid.value)
};
const usernameErrors = computed(() => v$.username.$invalid.value && username.value.length === 0 ? ['Введите имя пользователя'] : []);
const passwordErrors = computed(() => v$.password.$invalid.value && password.value.length === 0 ? ['Введите пароль'] : []);


const login = async () => {
  error.value = null;
  loading.value = true;

  try {
    const response = await api.post('/auth/token/login/', {
      username: username.value,
      password: password.value,
    });

    const token = response.data.auth_token;

    // 1. Сохранение токена
    localStorage.setItem('authToken', token);

    // 2. Перенаправление на защищенную страницу
    router.push('/clients');

  } catch (err) {
    if (err.response && err.response.status === 400) {
      error.value = 'Неверные учетные данные. Проверьте логин и пароль.';
    } else {
      error.value = 'Произошла ошибка при подключении к серверу.';
      console.error(err);
    }
    localStorage.removeItem('authToken'); // Убедимся, что токен удален в случае ошибки
  } finally {
    loading.value = false;
  }
};
</script>