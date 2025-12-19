<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card>
          <v-card-title class="text-h5 text-center pa-4">
            Регистрация
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
              <v-text-field
                v-model="username"
                label="Имя пользователя"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                required
              ></v-text-field>
              <v-text-field
                v-model="email"
                label="Email (необязательно)"
                prepend-inner-icon="mdi-email"
                variant="outlined"
                type="email"
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="Пароль"
                type="password"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                required
              ></v-text-field>
              <v-select
                v-model="role"
                label="Роль"
                :items="roles"
                prepend-inner-icon="mdi-account-key"
                variant="outlined"
                required
              ></v-select>
              <v-alert v-if="error" type="error" class="mt-2">{{ error }}</v-alert>
              <v-alert v-if="success" type="success" class="mt-2">
                Регистрация успешна! {{ authStore.isAuthenticated ? 'Перенаправление в систему...' : 'Перенаправление на страницу входа...' }}
              </v-alert>
              <v-btn
                type="submit"
                color="primary"
                block
                class="mt-4"
                :loading="loading"
              >
                Зарегистрироваться
              </v-btn>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn variant="text" :to="{ name: 'login' }">
              Уже есть аккаунт? Войти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const role = ref('teacher')
const roles = [
  { title: 'Администратор', value: 'admin' },
  { title: 'Завуч', value: 'head_teacher' },
  { title: 'Учитель', value: 'teacher' }
]
const error = ref('')
const success = ref(false)
const loading = ref(false)

const handleRegister = async () => {
  error.value = ''
  success.value = false
  loading.value = true
  try {
    // Отправляем email только если он заполнен
    const emailValue = email.value.trim() || null
    const response = await authStore.register(username.value, emailValue, password.value, role.value)
    
    // Если регистрация успешна и пользователь автоматически залогинен
    if (response.access_token) {
      success.value = true
      setTimeout(() => {
        router.push({ name: 'home' })
      }, 1500)
    } else {
      // Если токены не вернулись, перенаправляем на страницу входа
      success.value = true
      setTimeout(() => {
        router.push({ name: 'login' })
      }, 2000)
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Ошибка регистрации'
  } finally {
    loading.value = false
  }
}
</script>

