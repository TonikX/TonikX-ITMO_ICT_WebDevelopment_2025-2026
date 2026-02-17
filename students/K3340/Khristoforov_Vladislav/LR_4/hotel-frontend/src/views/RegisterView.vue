<script setup>
/**
 * RegisterView.vue - Страница регистрации новых пользователей (администраторов).
 * Использует стандартный эндпоинт Djoser /auth/users/ для создания записи в БД Django.
 */
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

// Состояние формы
const form = ref({
  username: '',
  email: '',
  password: '',
})

const error = ref('')
const loading = ref(false)
const valid = ref(false) // Статус валидации формы
const formRef = ref(null) // Ссылка на DOM-элемент формы

// Правила валидации полей
const rules = {
  required: v => !!v || 'Обязательное поле',
  email: v => /.+@.+\..+/.test(v) || 'Введите корректный Email',
  passwordMin: v => (v && v.length >= 8) || 'Пароль должен быть не менее 8 символов'
}

/**
 * Функция регистрации.
 * Сначала проверяет валидность формы, затем отправляет данные на бэкенд.
 */
async function register() {
  const { valid: isFormValid } = await formRef.value.validate()
  if (!isFormValid) return

  loading.value = true
  error.value = ''

  try {
    // Отправка данных на Djoser (создание пользователя)
    await api.post('/auth/users/', form.value)

    // Вместо alert лучше использовать переход с параметром или просто перенаправить
    router.push({ path: '/login', query: { registered: 'true' } })

  } catch (e) {
    console.error('Ошибка регистрации:', e)

    // Получаем ошибки валидации от Django (например, "user with this username already exists")
    const serverErrors = e.response?.data
    if (serverErrors) {
      // Превращаем объект ошибок в одну строку для вывода в v-alert
      error.value = Object.values(serverErrors).flat().join(', ')
    } else {
      error.value = 'Не удалось связаться с сервером'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <!-- fill-height центрирует контент по вертикали -->
  <v-container class="fill-height justify-center bg-grey-lighten-4">
    <v-card width="450" elevation="8" class="pa-6 rounded-lg">

      <div class="text-center mb-6">
        <v-icon icon="mdi-account-plus" size="x-large" color="success" class="mb-2"></v-icon>
        <h2 class="text-h4 font-weight-bold">Регистрация</h2>
        <p class="text-subtitle-1 text-grey">Создание аккаунта администратора</p>
      </div>

      <v-form ref="formRef" v-model="valid" @submit.prevent="register">
        <!-- Логин -->
        <v-text-field v-model="form.username" label="Имя пользователя (логин)" variant="outlined"
          prepend-inner-icon="mdi-account-outline" density="comfortable" :rules="[rules.required]"
          class="mb-2"></v-text-field>

        <!-- Email -->
        <v-text-field v-model="form.email" label="Email" type="email" variant="outlined"
          prepend-inner-icon="mdi-email-outline" density="comfortable" :rules="[rules.required, rules.email]"
          class="mb-2"></v-text-field>

        <!-- Пароль -->
        <v-text-field v-model="form.password" label="Пароль" type="password" variant="outlined"
          prepend-inner-icon="mdi-lock-outline" density="comfortable" :rules="[rules.required, rules.passwordMin]"
          class="mb-4" hint="Минимум 8 символов" persistent-hint></v-text-field>

        <!-- Ошибки от сервера -->
        <v-alert v-if="error" type="error" variant="tonal" density="compact" class="mb-4">
          {{ error }}
        </v-alert>

        <!-- Кнопка отправки -->
        <v-btn type="submit" color="success" block size="large" :loading="loading" elevation="2">
          Создать аккаунт
        </v-btn>
      </v-form>

      <v-divider class="my-6"></v-divider>

      <div class="text-center">
        <span class="text-grey-darken-1">Уже есть аккаунт? </span>
        <v-btn to="/login" variant="text" color="primary" class="font-weight-bold">
          Войти
        </v-btn>
      </div>
    </v-card>
  </v-container>
</template>

<style scoped>
/* Локальные стили для страницы регистрации */
</style>