<template>
  <v-row justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card>
        <v-card-title class="text-h6">вход</v-card-title>
        <v-card-text>
          <v-alert v-if="auth.error.value" type="error" density="compact" class="mb-2">
            {{ auth.error.value }}
          </v-alert>

          <v-form @submit.prevent="onSubmit">
            <v-text-field
              v-model="username"
              label="логин"
              variant="outlined"
              density="comfortable"
              required
            />
            <v-text-field
              v-model="password"
              label="пароль"
              type="password"
              variant="outlined"
              density="comfortable"
              required
            />

            <v-btn
              :loading="auth.loading.value"
              type="submit"
              color="primary"
              class="mt-2"
              block
            >
              войти
            </v-btn>

            <v-btn class="mt-2" variant="text" block @click="$router.push('/register')">
              нет аккаунта? регистрация
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

// форма авторизации
const username = ref('')
const password = ref('')

const auth = useAuthStore()
const router = useRouter()

const onSubmit = async () => {
  if (!username.value || !password.value) {
    auth.error.value = 'заполните логин и пароль'
    return
  }

  try {
    await auth.login({
      username: username.value,
      password: password.value
    })
    router.push('/rooms')
  } catch (e) {
    // ошибка уже показана через auth.error
  }
}
</script>

