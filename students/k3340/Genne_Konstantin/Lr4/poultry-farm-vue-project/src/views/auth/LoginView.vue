<template>
  <v-container fluid fill-height>
    <v-row justify="center">
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-title class="text-center">Вход</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="login">
              <v-text-field v-model="form.username" label="Имя пользователя" required />
              <v-text-field v-model="form.password" type="password" label="Пароль" required />
              <v-btn type="submit" color="primary" block :loading="authStore.loading">Войти</v-btn>
              <div class="text-center mt-2">
                <router-link to="/register">Регистрация</router-link>
              </div>
              <v-alert v-if="authStore.error" type="error" class="mt-3">{{ authStore.error }}</v-alert>
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
const form = reactive({ username: '', password: '' })

const login = async () => {
  await authStore.login(form.username, form.password)
  if (authStore.isAuthenticated) router.push('/')
}
</script>