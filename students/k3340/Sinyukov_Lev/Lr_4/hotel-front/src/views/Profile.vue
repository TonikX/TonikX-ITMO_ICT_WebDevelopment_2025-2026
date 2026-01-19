<template>
  <v-card>
    <v-card-title>Профиль</v-card-title>
    <v-card-text>
      <div v-if="auth.user">
        <div><b>ID:</b> {{ auth.user.id }}</div>
        <div><b>Username:</b> {{ auth.user.username }}</div>
        <div v-if="auth.user.email"><b>Email:</b> {{ auth.user.email }}</div>
      </div>

      <v-divider class="my-4" />

      <h3 class="mb-2">Смена пароля</h3>
      <v-alert v-if="msg" type="success" class="mb-3">{{ msg }}</v-alert>
      <v-alert v-if="err" type="error" class="mb-3">{{ err }}</v-alert>

      <v-form @submit.prevent="change">
        <v-text-field v-model="current" label="Current password" type="password" />
        <v-text-field v-model="n1" label="New password" type="password" />
        <v-text-field v-model="n2" label="Repeat new password" type="password" />
        <v-btn type="submit">Change</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();

const current = ref("");
const n1 = ref("");
const n2 = ref("");

const msg = ref("");
const err = ref("");

async function change() {
  msg.value = "";
  err.value = "";
  try {
    await auth.changePassword(current.value, n1.value, n2.value);
    msg.value = "Пароль успешно изменён";
    current.value = n1.value = n2.value = "";
  } catch (e) {
    err.value = JSON.stringify(e.response?.data || e.message);
  }
}
</script>