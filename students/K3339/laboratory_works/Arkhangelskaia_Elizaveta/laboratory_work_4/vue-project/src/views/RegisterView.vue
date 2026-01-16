<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card elevation="6">
          <v-card-title class="text-h5 text-center">
            Регистрация
          </v-card-title>

          <v-card-text>
            <v-text-field
              v-model="username"
              label="Логин"
              prepend-inner-icon="mdi-account"
              outlined
              dense
            />

            <v-text-field
              v-model="password"
              label="Пароль"
              type="password"
              prepend-inner-icon="mdi-lock"
              outlined
              dense
            />

            <v-text-field
              v-model="re_password"
              label="Повторите пароль"
              type="password"
              prepend-inner-icon="mdi-lock-check"
              outlined
              dense
            />

            <v-btn
              color="green lighten-2"
              block
              class="mt-4"
              @click="register"
            >
              Зарегистрироваться
            </v-btn>

            <v-alert
              v-if="error"
              type="error"
              class="mt-3"
              dense
            >
              {{ error }}
            </v-alert>
            <v-alert
              v-if="success"
              type="success"
              color="#1B5E20"
              class="mt-3"
              dense
            >
              {{ success }}
            </v-alert>

          </v-card-text>

        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()

const username = ref('')
const password = ref('')
const re_password = ref('')
const error = ref('')
const success = ref('')

const register = async () => {
  error.value = ''
  success.value = ''

  if (password.value !== re_password.value) {
    error.value = 'Пароли не совпадают'
    return
  }

  try {
    await api.post('auth/users/', {
      username: username.value,
      password: password.value,
      re_password: re_password.value
    })

    success.value = 'Пользователь успешно зарегистрирован!'

    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch {
    error.value = 'Ошибка регистрации. Возможно, пользователь уже существует'
  }
}
</script>
