<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark>
            <v-toolbar-title>Вход в систему</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
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
                Войти
              </v-btn>
            </v-form>
          </v-card-text>
          <v-card-actions class="px-4 pb-4">
            <v-spacer />
            <v-btn variant="text" to="/register">
              Нет аккаунта? Зарегистрироваться
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
const errors = reactive({
  username: [] as string[],
  password: [] as string[],
})

async function handleLogin() {
  errors.username = []
  errors.password = []

  // Валидация
  if (!username.value) {
    errors.username.push('Имя пользователя обязательно')
  }
  if (!password.value) {
    errors.password.push('Пароль обязателен')
  }

  if (errors.username.length || errors.password.length) {
    return
  }

  const result = await authStore.login(username.value, password.value)

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

