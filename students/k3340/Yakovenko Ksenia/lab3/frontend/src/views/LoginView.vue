<script setup>
import { ref } from "vue"
import { setToken } from "../api"

const username = ref("")
const password = ref("")
const error = ref("")
const loading = ref(false)

async function login() {
  loading.value = true
  error.value = ""
  try {
    const res = await fetch("http://127.0.0.1:8000/api/auth/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ username: username.value, password: password.value }),
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data?.detail || `HTTP ${res.status}`)
    setToken(data.token)
  } catch (e) {
    error.value = e?.message ?? String(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-card max-width="520" class="mx-auto">
    <v-card-title>Login</v-card-title>
    <v-card-text>
      <v-alert v-if="error" type="error" variant="tonal" class="mb-3">{{ error }}</v-alert>

      <v-text-field v-model="username" label="Username" />
      <v-text-field v-model="password" label="Password" type="password" />

      <v-btn block :loading="loading" @click="login">Sign in</v-btn>
    </v-card-text>
  </v-card>
</template>