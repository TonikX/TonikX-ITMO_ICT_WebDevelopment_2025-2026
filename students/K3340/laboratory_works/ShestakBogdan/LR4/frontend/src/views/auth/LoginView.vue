<template>
  <v-container class="mt-10" max-width="400">
    <h2 class="mb-4">Вход</h2>

    <v-form @submit.prevent="handleLogin">
      <v-text-field
        v-model="username"
        label="Логин"
        required
      />
      <v-text-field
        v-model="password"
        label="Пароль"
        type="password"
        required
      />

      <v-btn
        type="submit"
        color="primary"
        class="mt-4 mr-2"
        :disabled="loading"
      >
        Войти
      </v-btn>

      <v-btn
        variant="text"
        class="mt-4"
        @click="goRegister"
      >
        Регистрация
      </v-btn>
    </v-form>

    <p v-if="error" class="text-red mt-2">{{ error }}</p>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import http from "../../api/http";
import { login as setLoggedIn } from "../../store/auth"; // <- переименовали

const username = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");

const router = useRouter();

const handleLogin = async () => {
  loading.value = true;
  error.value = "";

  try {
    const res = await http.post("/auth/token/login/", {
      username: username.value,
      password: password.value,
    });

    // записываем токен и обновляем isLoggedIn
    setLoggedIn(res.data.auth_token);

    router.push("/drivers");
  } catch (e) {
    error.value = "Неверный логин или пароль";
    console.error(e);
  } finally {
    loading.value = false;
  }
};

const goRegister = () => {
  router.push("/register");
};
</script>