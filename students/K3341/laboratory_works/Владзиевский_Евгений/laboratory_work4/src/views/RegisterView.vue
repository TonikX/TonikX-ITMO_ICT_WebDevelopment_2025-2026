<template>
  <v-row justify="center">
    <v-col cols="12" md="6">
      <v-card elevation="2" class="pa-6">
        <v-card-title class="text-h5 font-weight-bold pb-2">Регистрация</v-card-title>
        <v-card-subtitle class="pb-4">Создайте аккаунт, чтобы публиковать посты и общаться.</v-card-subtitle>

        <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>

        <v-form @submit.prevent="submit">
          <v-text-field v-model="form.name" label="Имя" required prepend-inner-icon="mdi-account"></v-text-field>
          <v-text-field v-model="form.login" label="Логин" required prepend-inner-icon="mdi-at"></v-text-field>
          <v-text-field
            v-model="form.password"
            label="Пароль"
            type="password"
            required
            prepend-inner-icon="mdi-lock"
          ></v-text-field>
          <v-btn :loading="loading" color="primary" type="submit" block class="mt-4">Зарегистрироваться</v-btn>
          <v-btn to="/login" variant="text" block class="mt-2">У меня уже есть аккаунт</v-btn>
        </v-form>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { signUp } from '../stores/auth'

const form = reactive({ name: '', login: '', password: '' })
const loading = ref(false)
const error = ref('')
const router = useRouter()

const submit = async () => {
  loading.value = true
  error.value = ''
  try {
    await signUp(form)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось зарегистрироваться'
  } finally {
    loading.value = false
  }
}
</script>
