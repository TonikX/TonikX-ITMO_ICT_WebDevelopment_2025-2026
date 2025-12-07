<template>
  <v-row justify="center" align="center" class="fill-height">
    <v-col cols="12" sm="8" md="6" lg="4">
      <v-card class="pa-4">
        <v-card-title class="text-h4 text-center mb-4">Регистрация</v-card-title>

        <v-card-text>
          <v-form @submit.prevent="handleRegister">
            <v-text-field
              v-model="username"
              label="Имя пользователя"
              prepend-inner-icon="mdi-account"
              required
              variant="outlined"
              class="mb-2"
            ></v-text-field>

            <v-text-field
              v-model="email"
              label="Email (опционально)"
              type="email"
              prepend-inner-icon="mdi-email"
              variant="outlined"
              class="mb-2"
            ></v-text-field>

            <v-text-field
              v-model="password"
              label="Пароль"
              type="password"
              prepend-inner-icon="mdi-lock"
              required
              variant="outlined"
              class="mb-4"
            ></v-text-field>

            <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>

            <v-btn
              type="submit"
              color="primary"
              size="large"
              block
              :loading="authStore.isLoading"
            >
              Зарегистрироваться
            </v-btn>
          </v-form>
        </v-card-text>

        <v-card-actions class="justify-center">
          <span class="text-body-2">
            Уже есть аккаунт?
            <router-link to="/login" class="text-primary text-decoration-none">
              Войти
            </router-link>
          </span>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')

const handleRegister = async () => {
  error.value = ''
  if (!username.value || !password.value) {
    error.value = 'Введите имя пользователя и пароль'
    return
  }
  if (password.value.length < 8) {
    error.value = 'Пароль должен быть минимум 8 символов'
    return
  }
  const result = await authStore.register(username.value, email.value, password.value)
  if (result.success) {
    router.push('/')
  } else {
    error.value = result.error
  }
}
</script>

<style scoped>
.fill-height {
  min-height: calc(100vh - 64px);
}
</style>
