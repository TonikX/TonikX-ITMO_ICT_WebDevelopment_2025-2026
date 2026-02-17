<script setup>
/**
 * LoginView.vue - Страница авторизации.
 * Работает с Djoser Token Authentication. Получает токен и сохраняет его для API-сервиса.
 */
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

// Состояние полей ввода
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

// Правила валидации (базовые)
const rules = {
  required: v => !!v || 'Обязательное поле'
}

/**
 * Функция авторизации.
 * Отправляет логин/пароль на бэкенд и получает уникальный ключ (Token).
 */
async function login() {
  // Если поля пустые, встроенная валидация Vuetify покажет ошибку, 
  // но мы дополнительно проверяем здесь для надежности.
  if (!username.value || !password.value) return

  loading.value = true
  error.value = ''

  try {
    const response = await api.post('/auth/token/login/', {
      username: username.value,
      password: password.value,
    })

    // Извлекаем токен из ответа Django
    const token = response.data.auth_token
    localStorage.setItem('auth_token', token)

    // Переходим на главную. 
    // Перезагрузка нужна, чтобы компонент Navbar обновил состояние isAuthenticated.
    router.push('/')
    setTimeout(() => window.location.reload(), 50)

  } catch (e) {
    console.error('Ошибка входа:', e)
    if (e.response && e.response.status === 400) {
      error.value = 'Неверное имя пользователя или пароль'
    } else {
      error.value = 'Сервер недоступен. Проверьте соединение.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <!-- Центрируем карточку по вертикали и горизонтали -->
  <v-container class="fill-height justify-center bg-grey-lighten-4">
    <v-card width="450" elevation="8" class="rounded-lg pa-6">

      <!-- Заголовок и лого -->
      <div class="text-center mb-6">
        <v-icon icon="mdi-office-building" size="x-large" color="primary" class="mb-2"></v-icon>
        <h2 class="text-h4 font-weight-bold color-primary">Hotel Admin</h2>
        <p class="text-subtitle-1 text-grey">Вход в панель управления</p>
      </div>

      <v-form @submit.prevent="login">
        <!-- Поле логина -->
        <v-text-field v-model="username" label="Имя пользователя" prepend-inner-icon="mdi-account" variant="outlined"
          density="comfortable" :rules="[rules.required]" class="mb-2"></v-text-field>

        <!-- Поле пароля -->
        <v-text-field v-model="password" label="Пароль" type="password" prepend-inner-icon="mdi-lock" variant="outlined"
          density="comfortable" :rules="[rules.required]" class="mb-4"></v-text-field>

        <!-- Вывод ошибок -->
        <v-alert v-if="error" type="error" variant="tonal" density="compact" class="mb-4">
          {{ error }}
        </v-alert>

        <!-- Кнопка входа -->
        <v-btn type="submit" color="primary" block size="large" :loading="loading" elevation="2">
          Войти в систему
        </v-btn>
      </v-form>

      <v-divider class="my-6"></v-divider>

      <!-- Ссылка на регистрацию -->
      <div class="text-center">
        <span class="text-grey-darken-1">Еще не зарегистрированы? </span>
        <v-btn to="/register" variant="text" color="primary" class="font-weight-bold" :ripple="false">
          Создать аккаунт
        </v-btn>
      </div>
    </v-card>
  </v-container>
</template>

<style scoped>
/* Дополнительные стили для красоты */
.color-primary {
  color: #1867C0;
}
</style>