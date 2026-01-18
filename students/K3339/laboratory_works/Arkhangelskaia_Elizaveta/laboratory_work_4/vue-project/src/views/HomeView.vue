<template>
  <v-container class="fill-height d-flex justify-center align-center">
    <v-card width="100%" max-width="400">
      <v-card-title class="justify-center">Вход</v-card-title>
        <v-btn color="secondary" class="mt-3" @click="$router.push('/profile')">Профиль</v-btn>


        <div v-if="error" class="error-message mt-2" style="color:red; text-align:center;">
          {{ error }}
        </div>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')

const login = async () => {
  try {
    const response = await api.post('auth/token/login/', {
      username: username.value,
      password: password.value
    })
    localStorage.setItem('token', response.data.auth_token)
    router.push('/')
  } catch {
    error.value = 'Неверный логин или пароль'
  }
}
</script>
