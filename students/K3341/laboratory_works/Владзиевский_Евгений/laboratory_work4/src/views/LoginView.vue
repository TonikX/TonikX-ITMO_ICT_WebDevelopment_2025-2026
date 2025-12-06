<template>
  <v-row justify="center">
    <v-col cols="12" md="6">
      <v-card elevation="2" class="pa-6">
        <v-card-title class="text-h5 font-weight-bold pb-2">Вход</v-card-title>
        <v-card-subtitle class="pb-4">Используйте логин и пароль, полученные при регистрации.</v-card-subtitle>

        <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>

        <v-form @submit.prevent="submit">
          <v-text-field v-model="form.login" label="Логин" required prepend-inner-icon="mdi-account"></v-text-field>
          <v-text-field
            v-model="form.password"
            label="Пароль"
            type="password"
            required
            prepend-inner-icon="mdi-lock"
          ></v-text-field>
          <v-btn :loading="loading" color="primary" type="submit" block class="mt-4">Войти</v-btn>
          <v-btn to="/register" variant="text" block class="mt-2">Нет аккаунта? Зарегистрируйтесь</v-btn>
        </v-form>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { signIn } from '../stores/auth'

const form = reactive({ login: '', password: '' })
const loading = ref(false)
const error = ref('')
const route = useRoute()
const router = useRouter()

const submit = async () => {
  loading.value = true
  error.value = ''
  try {
    await signIn(form)
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось войти'
  } finally {
    loading.value = false
  }
}
</script>
