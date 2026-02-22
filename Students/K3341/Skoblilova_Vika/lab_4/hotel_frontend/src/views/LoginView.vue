<template>
  <v-container class="fill-height" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="4">
        <v-card elevation="3" class="pa-6">
          <v-card-title class="text-center mb-6">
            <h2>Вход в систему</h2>
          </v-card-title>

          <v-form @submit.prevent="handleLogin" ref="form">
            <v-text-field
              v-model="credentials.username"
              label="Имя пользователя"
              :rules="[v => !!v || 'Обязательное поле']"
              required
              class="mb-4"
            />

            <v-text-field
              v-model="credentials.password"
              label="Пароль"
              type="password"
              :rules="[v => !!v || 'Обязательное поле']"
              required
              class="mb-6"
            />

            <v-btn
              type="submit"
              color="primary"
              block
              size="large"
              :loading="loading"
            >
              Войти
            </v-btn>

            <div class="text-center mt-4">
              <router-link to="/register" class="text-decoration-none">
                Нет аккаунта? Зарегистрируйтесь
              </router-link>
            </div>
          </v-form>

          <v-alert v-if="error" type="error" class="mt-4">
            {{ error }}
          </v-alert>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const form = ref(null)

const credentials = reactive({
  username: '',
  password: ''
})

const handleLogin = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  loading.value = true
  error.value = ''

  try {
    // Используем Djoser endpoint для входа
    const response = await axios.post('auth/token/login/', credentials)
    const token = response.data.auth_token

    // Сохраняем токен
    localStorage.setItem('auth_token', token)

    // Получаем данные пользователя
    const userResponse = await axios.get('auth/users/me/')
    localStorage.setItem('user', JSON.stringify(userResponse.data))

    // Перенаправляем на главную
    router.push('/dashboard')
  } catch (err) {
    error.value = err.response?.data?.message || 'Ошибка авторизации'
  } finally {
    loading.value = false
  }
}
</script>