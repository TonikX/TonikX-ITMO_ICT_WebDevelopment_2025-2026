<template>
  <v-container class="fill-height" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12">
        <v-card class="elevation-12">
          <v-toolbar color="primary" :dark="true" flat>
            <v-toolbar-title>Регистрация</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
              <v-text-field
                v-model="username"
                label="Имя пользователя"
                prepend-icon="mdi-account"
                type="text"
                required
              ></v-text-field>

              <v-text-field
                v-model="email"
                label="Email"
                prepend-icon="mdi-email"
                type="email"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Пароль"
                prepend-icon="mdi-lock"
                type="password"
                required
              ></v-text-field>

              <v-text-field
                v-model="rePassword"
                label="Подтверждение пароля"
                prepend-icon="mdi-lock-check"
                type="password"
                required
              ></v-text-field>

              <v-alert v-if="authStore.error" type="error" class="mt-3">
                {{ authStore.error }}
              </v-alert>

              <v-alert v-if="successMessage" type="success" class="mt-3">
                {{ successMessage }}
              </v-alert>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              @click="handleRegister"
              :loading="authStore.loading"
            >
              Зарегистрироваться
            </v-btn>
          </v-card-actions>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn variant="text" @click="router.push('/login')">
              Уже есть аккаунт? Войти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const rePassword = ref('')
const successMessage = ref('')

async function handleRegister() {
  if (password.value !== rePassword.value) {
    authStore.error = 'Пароли не совпадают'
    return
  }

  const success = await authStore.register({
    username: username.value,
    email: email.value,
    password: password.value,
    re_password: rePassword.value,
  })

  if (success) {
    successMessage.value = 'Регистрация успешна! Войдите в систему.'
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  }
}
</script>
