<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card>
          <v-card-title>Вход</v-card-title>
          <v-card-text>
            <v-text-field v-model="username" label="Username" />
            <v-text-field v-model="password" label="Password" type="password" />
            <v-alert v-if="error" type="error" class="mb-3">{{ error }}</v-alert>
            <v-btn color="primary" block :loading="loading" @click="doLogin">Войти</v-btn>

            <v-btn class="mt-2" variant="text" block to="/register">
              Регистрация
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "../services/auth";

const router = useRouter();
const username = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");

async function doLogin() {
  error.value = "";
  loading.value = true;
  try {
    await login(username.value, password.value);
    router.push("/rooms");
  } catch (e) {
    error.value = e?.response?.data?.detail || "Ошибка входа";
  } finally {
    loading.value = false;
  }
}
</script>
