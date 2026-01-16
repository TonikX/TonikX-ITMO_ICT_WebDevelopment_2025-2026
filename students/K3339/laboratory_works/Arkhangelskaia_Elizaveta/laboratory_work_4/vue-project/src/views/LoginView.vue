<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card elevation="6">
          <v-card-title class="text-h5 text-center">
            Вход
          </v-card-title>

          <v-card-text>
            <v-text-field
              v-model="username"
              label="Логин"
              prepend-inner-icon="mdi-account"
              outlined
              dense
            />

            <v-text-field
              v-model="password"
              label="Пароль"
              type="password"
              prepend-inner-icon="mdi-lock"
              outlined
              dense
            />

            <v-btn
              color="green lighten-2"
              class="mt-4"
              block
              @click="login"
            >
              Войти
            </v-btn>

            <v-alert
              v-if="error"
              type="error"
              class="mt-3"
              dense
            >
              {{ error }}
            </v-alert>
          </v-card-text>

          <v-card-actions class="justify-center">
            <span>Нет аккаунта?</span>
            <router-link to="/register" class="ml-1">
              Зарегистрироваться
            </router-link>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')

const login = async () => {
  error.value = ''

  try {
    const response = await api.post('auth/token/login/', {
      username: username.value,
      password: password.value
    })

    localStorage.setItem('token', response.data.auth_token)
    router.push('/')
  } catch {
    error.value = 'Неверный логин или пароль'
  }
}
</script>
