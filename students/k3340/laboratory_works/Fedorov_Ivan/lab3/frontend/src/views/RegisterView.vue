<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="5">
        <v-card>
          <v-card-title>Регистрация</v-card-title>
          <v-card-text>
            <v-text-field v-model="username" label="Username" />
            <v-text-field v-model="email" label="Email (необязательно)" />
            <v-text-field v-model="password" label="Password" type="password" />
            <v-text-field v-model="rePassword" label="Repeat password" type="password" />

            <v-alert v-if="msg" type="success" class="mb-3">{{ msg }}</v-alert>
            <v-alert v-if="error" type="error" class="mb-3">{{ error }}</v-alert>

            <v-btn color="primary" block :loading="loading" @click="doRegister">
              Создать аккаунт
            </v-btn>
            <v-btn class="mt-2" variant="text" block to="/login">Назад ко входу</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { register } from "../services/auth";

const router = useRouter();
const username = ref("");
const email = ref("");
const password = ref("");
const rePassword = ref("");
const loading = ref(false);
const error = ref("");
const msg = ref("");

async function doRegister() {
  error.value = "";
  msg.value = "";
  loading.value = true;
  try {
    await register(username.value, password.value, rePassword.value, email.value);
    msg.value = "Успешно! Теперь войдите.";
    setTimeout(() => router.push("/login"), 800);
  } catch (e) {
    const data = e?.response?.data;
    error.value = typeof data === "string" ? data : JSON.stringify(data);
  } finally {
    loading.value = false;
  }
}
</script>
