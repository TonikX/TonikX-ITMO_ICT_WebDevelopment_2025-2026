<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card elevation="12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Вход в систему</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field label="Логин" v-model="username" prepend-icon="mdi-account" type="text" />
              <v-text-field label="Пароль" v-model="password" prepend-icon="mdi-lock" type="password" />
              <v-btn type="submit" color="primary" block class="mt-4">Войти</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  const success = await auth.login(username.value, password.value)
  if (success) {
    router.push('/')
  } else {
    alert('Неверный логин или пароль!')
  }
}
</script>
