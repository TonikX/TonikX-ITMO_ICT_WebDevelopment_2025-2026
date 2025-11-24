<template>
  <v-card max-width="400" class="mx-auto mt-10">
    <v-card-title>Вход</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="submit">
        <v-text-field v-model="form.username" label="Логин" required />
        <v-text-field v-model="form.password" label="Пароль" type="password" required />
        <v-alert v-if="error" type="error" class="mb-3">{{ error }}</v-alert>
        <v-btn type="submit" color="primary" block :loading="loading">Войти</v-btn>
      </v-form>
      <v-btn to="/register" variant="text" block class="mt-2">Регистрация</v-btn>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const form = reactive({ username: '', password: '' })
const loading = ref(false)
const error = ref('')

const submit = async () => {
  loading.value = true
  error.value = ''
  try {
    await auth.login(form.username, form.password)
    router.push('/')
  } catch (e) {
    error.value = 'Неверный логин или пароль'
  }
  loading.value = false
}
</script>
