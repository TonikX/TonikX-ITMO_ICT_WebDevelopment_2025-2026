<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-card-title class="bg-primary text-white">
            Вход в систему
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
                v-model="password"
                label="Пароль"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                :rules="passwordRules"
                required
                variant="outlined"
              />
            </v-form>
            <div v-if="error" class="mt-3">
              <v-alert type="error" dense>{{ error }}</v-alert>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" :disabled="!valid || loading" @click="handleLogin">
              Войти
            </v-btn>
          </v-card-actions>
          <v-card-actions>
            <v-spacer />
            <v-btn variant="text" color="primary" to="/register">
              Нет аккаунта? Зарегистрироваться
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
const username = ref('')
const password = ref('')

const usernameRules = [
  (v) => !!v || 'Имя пользователя обязательно',
]

const passwordRules = [
  (v) => !!v || 'Пароль обязателен',
]

const handleLogin = async () => {
  error.value = ''
  loading.value = true

  try {
    const response = await authAPI.login(username.value, password.value)
    localStorage.setItem('auth_token', response.data.auth_token)
    router.push('/')
  } catch (err) {
    if (err.response?.data?.non_field_errors) {
      error.value = err.response.data.non_field_errors[0]
    } else {
      error.value = 'Ошибка при входе. Проверьте правильность данных.'
    }
  } finally {
    loading.value = false
  }
}
</script>

