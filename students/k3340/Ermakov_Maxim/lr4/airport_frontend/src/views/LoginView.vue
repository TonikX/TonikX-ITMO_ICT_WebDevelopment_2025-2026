<template>
  <div class="page auth-page">
    <v-row justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card elevation="3">
          <v-card-title class="text-h5">Вход</v-card-title>

          <v-card-text>
            <v-form @submit.prevent="login">
              <v-text-field
                v-model="usernameInput"
                label="Логин"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-account"
                autocomplete="username"
                required
                class="mb-3"
              />

              <v-text-field
                v-model="password"
                label="Пароль"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-lock"
                type="password"
                autocomplete="current-password"
                required
                class="mb-3"
              />

              <div v-if="error" class="error mb-2">
                {{ error }}
              </div>

              <v-btn
                type="submit"
                color="primary"
                block
                :loading="loading"
              >
                Войти
              </v-btn>
            </v-form>

            <div class="mt-4 text-caption">
              Нет аккаунта?
              <RouterLink to="/register">Зарегистрироваться</RouterLink>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter, RouterLink } from "vue-router";
import api from "../api/api";
import { setAuth } from "../auth";

const router = useRouter();

const usernameInput = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");

const login = async () => {
  error.value = "";
  loading.value = true;
  try {
    const response = await api.post("/auth/token/login/", {
      username: usernameInput.value,
      password: password.value,
    });

    const token = response.data.auth_token;
    setAuth(token, usernameInput.value);

    router.push("/dashboard");
  } catch (e) {
    console.error(e);
    if (e.response && e.response.status === 400) {
      error.value = "Неверный логин или пароль.";
    } else {
      error.value = "Ошибка при входе. Попробуйте позже.";
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-page {
  max-width: 800px;
  margin: 0 auto;
}

.error {
  color: #d32f2f;
}
</style>