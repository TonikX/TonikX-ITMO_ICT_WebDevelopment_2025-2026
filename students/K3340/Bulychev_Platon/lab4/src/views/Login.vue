<template>
  <v-row justify="center" class="mt-16">
    <v-col cols="12" md="4">
      <v-card title="Login">
        <v-card-text>
          <v-text-field v-model="username" label="Username" />
          <v-text-field v-model="password" label="Password" type="password" />
          <v-alert v-if="error" type="error" density="compact" class="mb-3">{{ error }}</v-alert>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="login" block>Login</v-btn>
        </v-card-actions>
        <v-card-text class="text-center">
          <router-link to="/register">Register</router-link>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const login = async () => {
  try {
    const { data } = await api.post('/auth/token/login/', { username: username.value, password: password.value })
    localStorage.setItem('token', data.auth_token)
    router.push('/')
  } catch { error.value = 'Invalid credentials' }
}
</script>
