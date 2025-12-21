<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

const form = ref({
  username: '',
  email: '',
  password: '',
  re_password: '',
})
const showPassword = ref(false)
const showPassword2 = ref(false)

const submit = async () => {
  try {
    await auth.register(form.value)
    router.push('/dashboard')
  } catch (e) {
    // ошибка в сторе
  }
}
</script>

<template>
  <v-row justify="center">
    <v-col cols="12" md="6">
      <v-card elevation="3">
        <v-card-title class="text-h6">Регистрация</v-card-title>
        <v-card-subtitle>Создание учётки через Djoser</v-card-subtitle>
        <v-card-text>
          <v-alert v-if="auth.error" type="error" density="compact" class="mb-4">
            <div v-if="typeof auth.error === 'string'">{{ auth.error }}</div>
            <div v-else>
              <div v-for="(messages, key) in auth.error" :key="key">
                <strong>{{ key }}:</strong> {{ messages }}
              </div>
            </div>
          </v-alert>
          <v-form @submit.prevent="submit">
            <v-text-field
              v-model="form.username"
              label="Имя пользователя"
              prepend-inner-icon="mdi-account"
              autocomplete="username"
              required
            />
            <v-text-field
              v-model="form.email"
              label="Email (опционально)"
              prepend-inner-icon="mdi-email"
              autocomplete="email"
            />
            <v-text-field
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              label="Пароль"
              prepend-inner-icon="mdi-lock"
              :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showPassword = !showPassword"
              autocomplete="new-password"
              required
            />
            <v-text-field
              v-model="form.re_password"
              :type="showPassword2 ? 'text' : 'password'"
              label="Повторите пароль"
              prepend-inner-icon="mdi-lock-check"
              :append-inner-icon="showPassword2 ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showPassword2 = !showPassword2"
              autocomplete="new-password"
              required
            />
            <v-btn
              type="submit"
              color="primary"
              block
              :loading="auth.loading"
              :disabled="!form.username || !form.password || form.password !== form.re_password"
              class="mt-2"
            >
              Зарегистрироваться
            </v-btn>
          </v-form>
          <div class="mt-4 text-body-2">
            Уже есть учётка?
            <RouterLink to="/login">Войти</RouterLink>
          </div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>


