<template>
  <v-row justify="center" class="mt-10">
    <v-col cols="12" sm="8" md="6" lg="4">
      <v-card class="pa-6">
        <v-card-title class="text-h5 text-center mb-4">
          Регистрация
        </v-card-title>

        <v-alert
            v-if="error"
            type="error"
            class="mb-4"
            @close="error = null"
            closable
        >
          {{ formatError(error) }}
        </v-alert>

        <v-form @submit.prevent="handleSubmit">
          <v-text-field
              v-model="form.email"
              label="Email"
              type="email"
              required
              :rules="[rules.required, rules.email]"
              :disabled="isLoading"
              class="mb-3"
          ></v-text-field>

          <v-text-field
              v-model="form.name"
              label="Имя"
              required
              :rules="[rules.required]"
              :disabled="isLoading"
              class="mb-3"
          ></v-text-field>

          <v-text-field
              v-model="form.surname"
              label="Фамилия"
              required
              :rules="[rules.required]"
              :disabled="isLoading"
              class="mb-3"
          ></v-text-field>

          <v-text-field
              v-model="form.patronymic"
              label="Отчество"
              :disabled="isLoading"
              class="mb-3"
          ></v-text-field>

          <v-text-field
              v-model="form.password"
              label="Пароль"
              type="password"
              required
              :rules="[rules.required, rules.minLength]"
              :disabled="isLoading"
              class="mb-3"
          ></v-text-field>

          <v-text-field
              v-model="form.re_password"
              label="Подтверждение пароля"
              type="password"
              required
              :rules="[rules.required, passwordMatch]"
              :disabled="isLoading"
              class="mb-4"
          ></v-text-field>

          <v-btn
              type="submit"
              color="primary"
              block
              :loading="isLoading"
              :disabled="!formValid"
          >
            Зарегистрироваться
          </v-btn>
        </v-form>

        <v-divider class="my-6"></v-divider>

        <div class="text-center">
          <p class="mb-2">Уже есть аккаунт?</p>
          <v-btn to="/login" variant="text" color="primary">
            Войти
          </v-btn>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const isLoading = ref(false)
const error = ref(null)

const form = reactive({
  email: '',
  name: '',
  surname: '',
  patronymic: '',
  password: '',
  re_password: ''
})

const rules = {
  required: value => !!value || 'Обязательное поле',
  email: value => {
    const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return pattern.test(value) || 'Некорректный email'
  },
  minLength: value => value.length >= 8 || 'Минимум 8 символов'
}

const passwordMatch = () => {
  return form.password === form.re_password || 'Пароли не совпадают'
}

const formValid = computed(() => {
  return form.email &&
      form.name &&
      form.surname &&
      form.password &&
      form.re_password &&
      form.password === form.re_password
})

const formatError = (errorData) => {
  if (typeof errorData === 'string') return errorData
  if (errorData.detail) return errorData.detail

  // Обработка ошибок валидации Django
  let errorMessages = []
  for (const [field, messages] of Object.entries(errorData)) {
    if (Array.isArray(messages)) {
      errorMessages.push(...messages.map(msg => `${field}: ${msg}`))
    } else {
      errorMessages.push(`${field}: ${messages}`)
    }
  }
  return errorMessages.join(', ')
}

const handleSubmit = async () => {
  isLoading.value = true
  error.value = null

  try {
    await authStore.register(form)
  } catch (err) {
    error.value = err.response?.data || 'Ошибка регистрации'
    console.error('Registration failed:', err)
  } finally {
    isLoading.value = false
  }
}
</script>