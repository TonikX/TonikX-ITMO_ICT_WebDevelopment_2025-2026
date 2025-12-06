<template>
  <v-row justify="center" align="center" class="fill-height">
    <v-col cols="12" sm="8" md="6" lg="4">
      <v-card class="pa-4">
        <v-card-title class="text-h4 text-center mb-4">
          Регистрация
        </v-card-title>

        <v-card-text>
          <v-form ref="formRef" v-model="valid">
            <v-text-field
              v-model="email"
              label="Email"
              type="email"
              prepend-inner-icon="mdi-email"
              :rules="emailRules"
              required
              variant="outlined"
              class="mb-2"
            ></v-text-field>

            <v-text-field
              v-model="username"
              label="Имя пользователя (опционально)"
              prepend-inner-icon="mdi-account"
              hint="Если не указано, будет сгенерировано из email"
              persistent-hint
              variant="outlined"
              class="mb-2"
            ></v-text-field>

            <v-text-field
              v-model="password"
              label="Пароль"
              type="password"
              prepend-inner-icon="mdi-lock"
              :rules="passwordRules"
              required
              variant="outlined"
              class="mb-2"
            ></v-text-field>

            <v-text-field
              v-model="rePassword"
              label="Подтверждение пароля"
              type="password"
              prepend-inner-icon="mdi-lock-check"
              :rules="rePasswordRules"
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
              @click="handleRegister"
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
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const formRef = ref(null)
const valid = ref(false)
const email = ref('')
const username = ref('')
const password = ref('')
const rePassword = ref('')

const emailRules = [
  (v) => !!v || 'Email обязателен',
  (v) => /.+@.+\..+/.test(v) || 'Email должен быть валидным',
]

const passwordRules = [
  (v) => !!v || 'Пароль обязателен',
  (v) => (v && v.length >= 8) || 'Пароль должен содержать минимум 8 символов',
]

const rePasswordRules = [
  (v) => !!v || 'Подтверждение пароля обязательно',
  (v) => v === password.value || 'Пароли не совпадают',
]

const handleRegister = async () => {
  const { valid: isValid } = await formRef.value.validate()
  if (!isValid) return

  const result = await authStore.register(
    email.value,
    username.value || undefined,
    password.value,
    rePassword.value
  )

  if (result.success) {
    showSnackbar('Регистрация успешна! Добро пожаловать!', 'success')
    router.push('/profile')
  } else {
    showSnackbar(result.error || 'Ошибка регистрации', 'error')
  }
}
</script>

<style scoped>
.fill-height {
  min-height: calc(100vh - 64px);
}
</style>
