<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Вход в систему</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                label="Имя пользователя"
                prepend-icon="mdi-account"
                type="text"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Пароль"
                prepend-icon="mdi-lock"
                type="password"
                required
              ></v-text-field>

              <v-alert v-if="error" type="error" class="mt-3">
                {{ error }}
              </v-alert>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="handleLogin" :loading="loading">
              Войти
            </v-btn>
          </v-card-actions>
          <v-card-text class="text-center">
            <router-link to="/register">Нет аккаунта? Зарегистрироваться</router-link>
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
const password = ref('')
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  loading.value = true

  const result = await authStore.login({
    username: username.value,
    password: password.value
  })

  loading.value = false

  if (result.success) {
    router.push('/')
  } else {
    error.value = typeof result.error === 'string' 
      ? result.error 
      : 'Неверное имя пользователя или пароль'
  }
}
</script>