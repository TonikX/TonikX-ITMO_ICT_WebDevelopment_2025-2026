<template>
  <v-container class="fill-height" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="4">
        <v-card elevation="3" class="pa-6">
          <v-card-title class="text-center mb-6">
            <h2>Регистрация</h2>
          </v-card-title>

          <v-form @submit.prevent="handleRegister" ref="form">
            <v-text-field
              v-model="formData.username"
              label="Имя пользователя"
              :rules="[v => !!v || 'Обязательное поле']"
              required
              class="mb-4"
            />

            <v-text-field
              v-model="formData.email"
              label="Email"
              type="email"
              :rules="[
                v => !!v || 'Обязательное поле',
                v => /.+@.+\..+/.test(v) || 'Неверный формат email'
              ]"
              required
              class="mb-4"
            />

            <v-text-field
              v-model="formData.password"
              label="Пароль"
              type="password"
              :rules="[
                v => !!v || 'Обязательное поле',
                v => v.length >= 8 || 'Минимум 8 символов'
              ]"
              required
              class="mb-4"
            />

            <v-text-field
              v-model="formData.re_password"
              label="Подтверждение пароля"
              type="password"
              :rules="[
                v => !!v || 'Обязательное поле',
                v => v === formData.password || 'Пароли не совпадают'
              ]"
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
              Зарегистрироваться
            </v-btn>

            <div class="text-center mt-4">
              <router-link to="/login" class="text-decoration-none">
                Уже есть аккаунт? Войдите
              </router-link>
            </div>
          </v-form>

          <v-alert v-if="error" type="error" class="mt-4">
            {{ error }}
          </v-alert>

          <v-alert v-if="success" type="success" class="mt-4">
            {{ success }}
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
const success = ref('')
const form = ref(null)

const formData = reactive({
  username: '',
  email: '',
  password: '',
  re_password: ''
})

const handleRegister = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  loading.value = true
  error.value = ''
  success.value = ''

  try {
    // Используем Djoser endpoint для регистрации
    await axios.post('auth/users/', formData)

    success.value = 'Регистрация успешна! Вы будете перенаправлены на страницу входа.'

    // Через 2 секунды перенаправляем на страницу входа
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err) {
    if (err.response?.data) {
      // Обработка ошибок валидации от Django
      const errors = err.response.data
      error.value = Object.values(errors).flat().join(', ')
    } else {
      error.value = 'Ошибка регистрации'
    }
  } finally {
    loading.value = false
  }
}
</script>