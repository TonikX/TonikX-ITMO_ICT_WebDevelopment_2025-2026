<template>
  <v-row justify="center" class="mt-10">
    <v-col cols="12" sm="8" md="6" lg="4">
      <v-card class="pa-6">
        <v-card-title class="text-h5 text-center mb-4">
          Вход в систему
        </v-card-title>

        <v-alert
            v-if="authStore.error"
            type="error"
            class="mb-4"
            @close="authStore.error = null"
            closable
        >
          {{ authStore.error }}
        </v-alert>

        <v-form @submit.prevent="handleSubmit" ref="loginForm">
          <v-text-field
              v-model="form.email"
              label="Email"
              type="email"
              required
              :rules="[rules.required, rules.email]"
              :disabled="authStore.isLoading"
              class="mb-4"
              @keyup.enter="handleSubmit"
          ></v-text-field>

          <v-text-field
              v-model="form.password"
              label="Пароль"
              type="password"
              required
              :rules="[rules.required]"
              :disabled="authStore.isLoading"
              class="mb-4"
              @keyup.enter="handleSubmit"
          ></v-text-field>

          <v-btn
              type="submit"
              color="primary"
              block
              :loading="authStore.isLoading"
              :disabled="!formValid"
          >
            Войти
          </v-btn>
        </v-form>

        <v-divider class="my-6"></v-divider>

        <div class="text-center">
          <p class="mb-2">Нет аккаунта?</p>
          <v-btn to="/register" variant="text" color="primary">
            Зарегистрироваться
          </v-btn>
        </div>

        <div class="text-center mt-4">
          <v-btn to="/" variant="text" color="grey">
            <v-icon start>mdi-arrow-left</v-icon>
            Назад на главную
          </v-btn>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const loginForm = ref(null)

const form = reactive({
  email: '',
  password: ''
})

const rules = {
  required: value => !!value || 'Обязательное поле',
  email: value => {
    const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return pattern.test(value) || 'Некорректный email'
  }
}

const formValid = computed(() => {
  return form.email && form.password && rules.email(form.email)
})

const handleSubmit = async () => {
  // Проверяем валидность формы
  if (loginForm.value) {
    const { valid } = await loginForm.value.validate()
    if (!valid) return
  }

  try {
    await authStore.login(form)
  } catch (error) {
    // Ошибка уже обрабатывается в authStore
    console.error('Login failed:', error)
  }
}
</script>