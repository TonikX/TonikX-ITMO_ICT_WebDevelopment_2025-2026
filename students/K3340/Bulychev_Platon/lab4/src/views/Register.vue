<template>
  <v-row justify="center" class="mt-16">
    <v-col cols="12" md="4">
      <v-card title="Register">
        <v-card-text>
          <v-text-field v-model="username" label="Username" />
          <v-text-field v-model="email" label="Email" />
          <v-text-field v-model="password" label="Password" type="password" />
          <v-alert v-if="error" type="error" density="compact" class="mb-3">{{ error }}</v-alert>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="register" block>Register</v-btn>
        </v-card-actions>
        <v-card-text class="text-center">
          <router-link to="/login">Login</router-link>
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
const email = ref('')
const password = ref('')
const error = ref('')
const register = async () => {
  try {
    await api.post('/auth/users/', { username: username.value, email: email.value, password: password.value })
    router.push('/login')
  } catch { error.value = 'Registration failed' }
}
</script>
