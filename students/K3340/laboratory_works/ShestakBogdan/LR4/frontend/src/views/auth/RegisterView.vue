<template>
  <v-container class="mt-10" max-width="400">
    <h2 class="mb-4">Регистрация</h2>
    <v-form @submit.prevent="register">
      <v-text-field v-model="username" label="Логин" required />
      <v-text-field v-model="email" label="Email" type="email" required />
      <v-text-field v-model="password" label="Пароль" type="password" required />
      <v-text-field v-model="password2" label="Повтор пароля" type="password" required />

      <v-btn type="submit" color="primary" class="mt-4" :disabled="loading">
        Зарегистрироваться
      </v-btn>
      <v-btn variant="text" class="mt-4" @click="goLogin">
        Уже есть аккаунт
      </v-btn>
    </v-form>
    <p v-if="error" class="text-red">{{ error }}</p>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import http from '../../api/http'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const loading = ref(false)
const error = ref('')
const router = useRouter()

const register = async () => {
  error.value = ''
  if (password.value !== password2.value) {
    error.value = 'Пароли не совпадают'
    return
  }

  loading.value = true
  try {
    await http.post('/auth/users/', {
      username: username.value,
      email: email.value,
      password: password.value,
    })
    // после регистрации можно сразу отправить на логин
    router.push('/login')
  } catch (e) {
    error.value = 'Ошибка регистрации'
  } finally {
    loading.value = false
  }
}

const goLogin = () => {
  router.push('/login')
}
</script>