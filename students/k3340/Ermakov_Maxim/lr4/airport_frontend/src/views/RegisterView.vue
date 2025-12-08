<template>
  <div class="page auth-page">
    <v-row justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card elevation="3">
          <v-card-title class="text-h5">Регистрация</v-card-title>

          <v-card-text>
            <v-form @submit.prevent="registerUser">
              <v-text-field
                v-model="username"
                label="Логин"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-account-plus"
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
                autocomplete="new-password"
                required
                class="mb-3"
              />

              <v-text-field
                v-model="rePassword"
                label="Повтор пароля"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-lock-check"
                type="password"
                autocomplete="new-password"
                required
                class="mb-3"
              />

              <div v-if="error" class="error mb-2">
                {{ error }}
              </div>

              <div v-if="success" class="success mb-2">
                Регистрация прошла успешно! Теперь вы можете
                <RouterLink to="/login">войти</RouterLink>.
              </div>

              <v-btn
                type="submit"
                color="primary"
                block
                :loading="loading"
              >
                Зарегистрироваться
              </v-btn>
            </v-form>

            <div class="mt-4 text-caption" v-if="!success">
              Уже есть аккаунт?
              <RouterLink to="/login">Войти</RouterLink>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";
import api from "../api/api";

const username = ref("");
const password = ref("");
const rePassword = ref("");

const loading = ref(false);
const error = ref("");
const success = ref(false);

const registerUser = async () => {
  error.value = "";
  success.value = false;

  if (password.value !== rePassword.value) {
    error.value = "Пароли не совпадают.";
    return;
  }

  loading.value = true;
  try {
    await api.post("/auth/users/", {
      username: username.value,
      password: password.value,
      re_password: rePassword.value,
    });

    success.value = true;
  } catch (e) {
    console.error(e);
    if (e.response && e.response.data) {
      error.value = JSON.stringify(e.response.data);
    } else {
      error.value = "Ошибка при регистрации.";
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

.success {
  color: #2e7d32;
}
</style>