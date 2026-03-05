<script setup>
import { ref } from "vue"
import { setToken } from "../api"

const username = ref("")
const email = ref("")
const password = ref("")
const error = ref("")
const loading = ref(false)
const success = ref(false)

async function register() {
  loading.value = true
  error.value = ""
  success.value = false

  try {
    const res = await fetch("http://127.0.0.1:8000/api/auth/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value,
      }),
    })

    // ВАЖНО: читаем как текст, потому что бэк может вернуть не-JSON (IntegrityError и т.п.)
    const text = await res.text()
    let data
    try {
      data = JSON.parse(text)
    } catch {
      data = { detail: text }
    }

    if (!res.ok) {
      throw new Error(data?.detail || JSON.stringify(data))
    }

    if (!data?.token) {
      throw new Error("No token returned from server")
    }

    setToken(data.token)
    success.value = true
  } catch (e) {
    error.value = e?.message ?? String(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-card max-width="560" class="mx-auto">
    <v-card-title>Register</v-card-title>

    <v-card-text>
      <v-alert v-if="success" type="success" variant="tonal" class="mb-3">
        Account created. Token saved. You can open Account page and change password.
      </v-alert>

      <v-alert v-if="error" type="error" variant="tonal" class="mb-3">
        {{ error }}
      </v-alert>

      <v-text-field v-model="username" label="Username" />
      <v-text-field v-model="email" label="Email (optional)" />
      <v-text-field v-model="password" label="Password" type="password" />

      <v-btn block :loading="loading" @click="register">
        Create account
      </v-btn>
    </v-card-text>
  </v-card>
</template>