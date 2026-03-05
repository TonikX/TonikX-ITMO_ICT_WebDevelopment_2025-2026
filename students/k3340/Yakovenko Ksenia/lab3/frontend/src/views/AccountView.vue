<script setup>
import { computed, ref } from "vue"
import { apiFetchJson, clearToken, getToken } from "../api"

const token = computed(() => getToken())
const oldPassword = ref("")
const newPassword = ref("")
const loading = ref(false)
const error = ref("")
const success = ref("")

async function changePassword() {
  loading.value = true
  error.value = ""
  success.value = ""
  try {
    if (!token.value) throw new Error("Not logged in (no token). Please login/register first.")

    const res = await apiFetch("/auth/change-password/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        old_password: oldPassword.value,
        new_password: newPassword.value,
      }),
    })

    const data = await res.json().catch(() => ({}))
    if (!res.ok) throw new Error(data?.detail || JSON.stringify(data) || `HTTP ${res.status}`)

    success.value = "Password changed successfully."
    oldPassword.value = ""
    newPassword.value = ""
  } catch (e) {
    error.value = e?.message ?? String(e)
  } finally {
    loading.value = false
  }
}

function logout() {
  clearToken()
  success.value = "Logged out (token removed)."
  error.value = ""
}
</script>

<template>
  <v-card max-width="640" class="mx-auto">
    <v-card-title>Account</v-card-title>
    <v-card-text>
      <v-alert v-if="!token" type="warning" variant="tonal" class="mb-3">
        You are not logged in. Please use Login or Register.
      </v-alert>

      <v-alert v-if="success" type="success" variant="tonal" class="mb-3">{{ success }}</v-alert>
      <v-alert v-if="error" type="error" variant="tonal" class="mb-3">{{ error }}</v-alert>

      <div class="d-flex align-center justify-space-between mb-4">
        <div style="max-width: 420px; overflow: hidden; text-overflow: ellipsis;">
          <strong>Token:</strong> {{ token || "—" }}
        </div>
        <v-btn variant="tonal" @click="logout">Logout</v-btn>
      </div>

      <v-divider class="mb-4" />

      <h3 class="mb-2">Change password</h3>
      <v-text-field v-model="oldPassword" label="Old password" type="password" />
      <v-text-field v-model="newPassword" label="New password" type="password" />

      <v-btn :loading="loading" @click="changePassword">Change</v-btn>
    </v-card-text>
  </v-card>
</template>