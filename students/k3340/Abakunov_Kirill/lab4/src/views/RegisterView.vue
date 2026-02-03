<template>
  <v-row justify="center" class="mt-8">
    <v-col cols="12" sm="8" md="6" lg="4">
      <v-card class="pa-6" elevation="8">
        <v-card-title class="text-center text-h5 mb-4">
          <v-icon size="40" color="primary" class="mr-2">mdi-account-plus</v-icon>
          Регистрация
        </v-card-title>

        <v-form @submit.prevent="handleRegister" ref="formRef">
          <v-text-field
            v-model="form.username"
            label="Имя пользователя"
            prepend-inner-icon="mdi-account"
            :rules="[rules.required, rules.minLength(3)]"
            :error-messages="getFieldErrors('username')"
            class="mb-2"
          ></v-text-field>

          <v-text-field
            v-model="form.email"
            label="Email"
            type="email"
            prepend-inner-icon="mdi-email"
            :rules="[rules.required, rules.email]"
            :error-messages="getFieldErrors('email')"
            class="mb-2"
          ></v-text-field>

          <v-text-field
            v-model="form.password"
            label="Пароль"
            prepend-inner-icon="mdi-lock"
            :type="showPassword ? 'text' : 'password'"
            :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="showPassword = !showPassword"
            :rules="[rules.required, rules.minLength(8)]"
            :error-messages="getFieldErrors('password')"
            class="mb-2"
          ></v-text-field>

          <v-text-field
            v-model="form.re_password"
            label="Подтверждение пароля"
            prepend-inner-icon="mdi-lock-check"
            :type="showPassword ? 'text' : 'password'"
            :rules="[rules.required, rules.passwordMatch]"
            :error-messages="getFieldErrors('re_password')"
            class="mb-4"
          ></v-text-field>

          <v-alert
            v-if="authStore.error && typeof authStore.error === 'object' && authStore.error.non_field_errors"
            type="error"
            class="mb-4"
            closable
          >
            {{ authStore.error.non_field_errors.join(', ') }}
          </v-alert>

          <v-btn
            type="submit"
            color="primary"
            size="large"
            block
            :loading="authStore.loading"
          >
            Зарегистрироваться
          </v-btn>
        </v-form>

        <v-divider class="my-6"></v-divider>

        <div class="text-center">
          <span class="text-grey">Уже есть аккаунт?</span>
          <router-link to="/login" class="ml-2">Войти</router-link>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, reactive, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const formRef = ref(null)
const showPassword = ref(false)

const form = reactive({
  username: '',
  email: '',
  password: '',
  re_password: '',
})

const rules = {
  required: (v) => !!v || 'Обязательное поле',
  minLength: (min) => (v) => (v && v.length >= min) || `Минимум ${min} символов`,
  email: (v) => /.+@.+\..+/.test(v) || 'Некорректный email',
  passwordMatch: (v) => v === form.password || 'Пароли не совпадают',
}

const getFieldErrors = (field) => {
  if (authStore.error && typeof authStore.error === 'object' && authStore.error[field]) {
    return authStore.error[field]
  }
  return []
}

const handleRegister = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  const success = await authStore.register(form)
  if (success) {
    showSnackbar('Регистрация успешна!', 'success')
    router.push('/')
  }
}
</script>
