<template>
  <v-container fluid fill-height>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-title class="text-center">Регистрация</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="register">
              <v-text-field
                v-model="form.username"
                label="Имя пользователя"
                required
              />
              <v-text-field
                v-model="form.email"
                label="Email"
                type="email"
              />
              <v-text-field
                v-model="form.password"
                label="Пароль"
                type="password"
                required
              />
              <v-text-field
                v-model="form.re_password"
                label="Повторите пароль"
                type="password"
                required
              />
              <v-btn type="submit" color="primary" block :loading="authStore.loading">Зарегистрироваться</v-btn>
              <div class="text-center mt-2">
                <router-link to="/login">Уже есть аккаунт?</router-link>
              </div>
              <v-alert v-if="authStore.error" type="error" class="mt-3">
                {{ formatError(authStore.error) }}
              </v-alert>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { reactive } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const form = reactive({
  username: '',
  email: '',
  password: '',
  re_password: ''
})

const formatError = (error) => {
  if (typeof error === 'string') return error
  if (error.password) return error.password[0]
  if (error.username) return error.username[0]
  if (error.email) return error.email[0]
  return 'Ошибка регистрации'
}

const register = async () => {
  if (form.password !== form.re_password) {
    authStore.error = 'Пароли не совпадают'
    return
  }
  await authStore.register(form)
  if (authStore.isAuthenticated) {
    router.push('/')
  }
}
</script>