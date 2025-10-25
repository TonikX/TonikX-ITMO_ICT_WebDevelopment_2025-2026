<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Регистрация</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
              <v-text-field
                v-model="username"
                label="Имя пользователя"
                prepend-icon="mdi-account"
                type="text"
                required
              ></v-text-field>

              <v-text-field
                v-model="email"
                label="Email"
                prepend-icon="mdi-email"
                type="email"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Пароль"
                prepend-icon="mdi-lock"
                type="password"
                required
              ></v-text-field>

              <v-text-field
                v-model="rePassword"
                label="Подтверждение пароля"
                prepend-icon="mdi-lock-check"
                type="password"
                required
              ></v-text-field>

              <v-alert v-if="error" type="error" class="mt-3">
                {{ error }}
              </v-alert>

              <v-alert v-if="success" type="success" class="mt-3">
                Регистрация успешна! Перенаправление на страницу входа...
              </v-alert>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="handleRegister" :loading="loading">
              Зарегистрироваться
            </v-btn>
          </v-card-actions>
          <v-card-text class="text-center">
            <router-link to="/login">Уже есть аккаунт? Войти</router-link>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const rePassword = ref('')
const error = ref('')
const success = ref(false)
const loading = ref(false)

const handleRegister = async () => {
  error.value = ''
  success.value = false

  if (password.value !== rePassword.value) {
    error.value = 'Пароли не совпадают'
    return
  }

  loading.value = true

  const result = await authStore.register({
    username: username.value,
    email: email.value,
    password: password.value,
    re_password: rePassword.value
  })

  loading.value = false

  if (result.success) {
    success.value = true
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } else {
    error.value = typeof result.error === 'string' 
      ? result.error 
      : 'Ошибка регистрации. Проверьте введенные данные.'
  }
}
</script>