<template>
  <div>
    <h1>Вход</h1>

    <v-form @submit.prevent="onSubmit" class="mt-4" style="max-width: 400px;">
      <v-text-field
        v-model="username"
        label="Логин"
        required
      />
      <v-text-field
        v-model="password"
        label="Пароль"
        type="password"
        required
      />
      <v-btn :loading="loading" type="submit" color="primary">Войти</v-btn>
    </v-form>

    <p v-if="error" class="mt-4" style="color: red;">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/api'
import { setAuthToken } from '../auth'

const router = useRouter()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const onSubmit = async () => {
  error.value = ''
  loading.value = true
  try {
    const { data } = await api.post('/auth/token/login/', {
      username: username.value,
      password: password.value,
    })
    setAuthToken(data.auth_token)
    router.push('/rooms')
  } catch (e) {
    error.value = 'Ошибка входа. Проверьте логин/пароль.'
  } finally {
    loading.value = false
  }
}
</script>
