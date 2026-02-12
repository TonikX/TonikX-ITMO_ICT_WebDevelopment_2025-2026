<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-card-title class="bg-primary text-white">
            Регистрация
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-text-field
                v-model="username"
                label="Имя пользователя"
                name="username"
                prepend-icon="mdi-account"
                type="text"
                :rules="usernameRules"
                required
                variant="outlined"
              />
              <v-text-field
                v-model="email"
                label="Email"
                name="email"
                prepend-icon="mdi-email"
                type="email"
                :rules="emailRules"
                required
                variant="outlined"
              />
              <v-text-field
                v-model="password"
                label="Пароль"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                :rules="passwordRules"
                required
                variant="outlined"
              />
              <v-text-field
                v-model="confirmPassword"
                label="Подтвердите пароль"
                name="confirmPassword"
                prepend-icon="mdi-lock-check"
                type="password"
                :rules="confirmPasswordRules"
                required
                variant="outlined"
              />
            </v-form>
            <div v-if="error" class="mt-3">
              <v-alert type="error" dense>{{ error }}</v-alert>
            </div>
            <div v-if="success" class="mt-3">
              <v-alert type="success" dense>
                Регистрация успешна! Перенаправление на страницу входа...
              </v-alert>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" :disabled="!valid || loading" @click="handleRegister">
              Зарегистрироваться
            </v-btn>
          </v-card-actions>
          <v-card-actions>
            <v-spacer />
            <v-btn variant="text" color="primary" to="/login">
              Уже есть аккаунт? Войти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../services/api'

const router = useRouter()

const valid = ref(false)
const loading = ref(false)
const error = ref('')
const success = ref(false)
const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const usernameRules = [
  (v) => !!v || 'Имя пользователя обязательно',
  (v) => (v && v.length >= 3) || 'Имя пользователя должно содержать минимум 3 символа',
]

const emailRules = [
  (v) => !!v || 'Email обязателен',
  (v) => /.+@.+\..+/.test(v) || 'Email должен быть валидным',
]

const passwordRules = [
  (v) => !!v || 'Пароль обязателен',
  (v) => (v && v.length >= 8) || 'Пароль должен содержать минимум 8 символов',
]

const confirmPasswordRules = [
  (v) => !!v || 'Подтверждение пароля обязательно',
  (v) => v === password.value || 'Пароли не совпадают',
]

const handleRegister = async () => {
  error.value = ''
  success.value = false

  if (!valid.value) {
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Пароли не совпадают'
    return
  }

  loading.value = true

  try {
    await authAPI.register(username.value, password.value, email.value)
    success.value = true
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err) {
    if (err.response?.data) {
      const data = err.response.data
      if (data.username) {
        error.value = `Имя пользователя: ${data.username[0]}`
      } else if (data.email) {
        error.value = `Email: ${data.email[0]}`
      } else if (data.password) {
        error.value = `Пароль: ${data.password[0]}`
      } else {
        error.value = 'Ошибка при регистрации. Проверьте правильность данных.'
      }
    } else {
      error.value = 'Ошибка при регистрации. Попробуйте еще раз.'
    }
  } finally {
    loading.value = false
  }
}
</script>

