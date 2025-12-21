<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const form = ref({ username: '', password: '' })
const showPassword = ref(false)

const submit = async () => {
  try {
    await auth.login(form.value)
    const next = route.query.next || '/dashboard'
    router.push(next)
  } catch (e) {
    // ошибка уже сохранена в store
  }
}
</script>

<template>
  <v-row justify="center">
    <v-col cols="12" md="5">
      <v-card elevation="3">
        <v-card-title class="text-h6">Вход</v-card-title>
        <v-card-subtitle>Авторизация через Djoser token</v-card-subtitle>
        <v-card-text>
          <v-alert
            v-if="auth.error"
            type="error"
            density="compact"
            class="mb-4"
            :text="auth.error?.detail || 'Ошибка входа'"
          />
          <v-form @submit.prevent="submit">
            <v-text-field
              v-model="form.username"
              label="Имя пользователя"
              prepend-inner-icon="mdi-account"
              autocomplete="username"
              required
            />
            <v-text-field
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              label="Пароль"
              prepend-inner-icon="mdi-lock"
              :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showPassword = !showPassword"
              autocomplete="current-password"
              required
            />
            <v-btn
              type="submit"
              color="primary"
              block
              :loading="auth.loading"
              :disabled="!form.username || !form.password"
              class="mt-2"
            >
              Войти
            </v-btn>
          </v-form>
          <div class="mt-4 text-body-2">
            Нет аккаунта?
            <RouterLink to="/register">Зарегистрироваться</RouterLink>
          </div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>


