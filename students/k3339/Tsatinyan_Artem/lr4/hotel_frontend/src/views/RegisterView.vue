<template>
  <div>
    <h1>Регистрация</h1>

    <v-form @submit.prevent="onSubmit" style="max-width: 400px;">
      <v-text-field v-model="username" label="Логин" required />
      <v-text-field v-model="email" label="Email" />
      <v-text-field v-model="password" label="Пароль" type="password" required />
      <v-btn :loading="loading" type="submit" color="primary">Зарегистрироваться</v-btn>
    </v-form>

    <p v-if="message" class="mt-4" style="color: green;">{{ message }}</p>
    <p v-if="error" class="mt-2" style="color: red;">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api/api'

const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const message = ref('')
const error = ref('')

const onSubmit = async () => {
  loading.value = true
  message.value = ''
  error.value = ''
  try {
    await api.post('/auth/users/', {
      username: username.value,
      email: email.value || undefined,
      password: password.value,
    })
    message.value = 'Пользователь создан. Теперь можете войти на странице /login.'
  } catch (e) {
    error.value = 'Ошибка регистрации'
  } finally {
    loading.value = false
  }
}
</script>
