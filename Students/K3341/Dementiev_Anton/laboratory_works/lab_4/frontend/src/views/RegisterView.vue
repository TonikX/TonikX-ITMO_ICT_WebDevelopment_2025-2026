<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark>
            <v-toolbar-title>Регистрация</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
              <v-text-field
                v-model="username"
                label="Имя пользователя"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                :error-messages="errors.username"
                required
                autofocus
              />
              <v-text-field
                v-model="password"
                label="Пароль"
                prepend-inner-icon="mdi-lock"
                type="password"
                variant="outlined"
                :error-messages="errors.password"
                required
              />
              <v-text-field
                v-model="passwordRetype"
                label="Подтвердите пароль"
                prepend-inner-icon="mdi-lock-check"
                type="password"
                variant="outlined"
                :error-messages="errors.passwordRetype"
                required
              />
              <v-alert
                v-if="authStore.error"
                type="error"
                variant="tonal"
                class="mb-4"
                closable
                @click:close="authStore.error = null"
              >
                {{ authStore.error }}
              </v-alert>
              <v-btn
                type="submit"
                color="primary"
                block
                size="large"
                :loading="authStore.loading"
                class="mt-4"
              >
                Зарегистрироваться
              </v-btn>
            </v-form>
          </v-card-text>
          <v-card-actions class="px-4 pb-4">
            <v-spacer />
            <v-btn variant="text" to="/login">
              Уже есть аккаунт? Войти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const passwordRetype = ref('')
const errors = reactive <{
  username: string[]
  password: string[]
  passwordRetype: string[]
}> ({
  username: [],
  password: [],
  passwordRetype: [],
})

async function handleRegister() {
  errors.username = []
  errors.password = []
  errors.passwordRetype = []

  if (!username.value) {
    errors.username.push('Имя пользователя обязательно')
  }
  if (!password.value) {
    errors.password.push('Пароль обязателен')
  }
  if (!passwordRetype.value) {
    errors.passwordRetype.push('Подтверждение пароля обязательно')
  }
  if (password.value && passwordRetype.value && password.value !== passwordRetype.value) {
    errors.passwordRetype.push('Пароли не совпадают')
  }

  if (errors.username.length || errors.password.length || errors.passwordRetype.length) {
    return
  }

  const result = await authStore.register(username.value, password.value, passwordRetype.value)

  if (result.success) {
    router.push('/')
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}
</style>

