<template>
  <v-row justify="center" align="center" class="fill-height">
    <v-col cols="12" sm="8" md="6" lg="4">
      <v-card class="pa-4">
        <v-card-title class="text-h4 text-center mb-4">
          Вход
        </v-card-title>

        <v-card-text>
          <v-form ref="formRef" v-model="valid">
            <v-text-field
              v-model="usernameOrEmail"
              label="Email или имя пользователя"
              prepend-inner-icon="mdi-account"
              :rules="usernameOrEmailRules"
              required
              variant="outlined"
              class="mb-2"
              hint="Введите email или имя пользователя"
              persistent-hint
            ></v-text-field>

            <v-text-field
              v-model="password"
              label="Пароль"
              type="password"
              prepend-inner-icon="mdi-lock"
              :rules="passwordRules"
              required
              variant="outlined"
              class="mb-4"
            ></v-text-field>

            <v-btn
              color="primary"
              size="large"
              block
              :loading="authStore.isLoading"
              :disabled="!valid || authStore.isLoading"
              @click="handleLogin"
            >
              Войти
            </v-btn>
          </v-form>
        </v-card-text>

        <v-card-actions class="justify-center">
          <span class="text-body-2">
            Нет аккаунта?
            <router-link to="/register" class="text-primary text-decoration-none">
              Зарегистрироваться
            </router-link>
          </span>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const formRef = ref(null)
const valid = ref(false)
const usernameOrEmail = ref('')
const password = ref('')

const usernameOrEmailRules = [
  (v) => !!v || 'Email или имя пользователя обязательно',
]

const passwordRules = [
  (v) => !!v || 'Пароль обязателен',
]

const handleLogin = async () => {
  const { valid: isValid } = await formRef.value.validate()
  if (!isValid) return

  const result = await authStore.login(usernameOrEmail.value, password.value)

  if (result.success) {
    showSnackbar('Успешный вход!', 'success')
    const redirect = route.query.redirect || '/profile'
    router.push(redirect)
  } else {
    showSnackbar(result.error || 'Ошибка входа', 'error')
  }
}
</script>

<style scoped>
.fill-height {
  min-height: calc(100vh - 64px);
}
</style>
