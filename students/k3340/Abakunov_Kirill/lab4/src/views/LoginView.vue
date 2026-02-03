<template>
  <v-row justify="center" class="mt-8">
    <v-col cols="12" sm="8" md="6" lg="4">
      <v-card class="pa-6" elevation="8">
        <v-card-title class="text-center text-h5 mb-4">
          <v-icon size="40" color="primary" class="mr-2">mdi-login</v-icon>
          Вход в систему
        </v-card-title>

        <v-form @submit.prevent="handleLogin" ref="formRef">
          <v-text-field
            v-model="form.username"
            label="Имя пользователя"
            prepend-inner-icon="mdi-account"
            :rules="[rules.required]"
            :error-messages="getFieldErrors('username')"
            class="mb-2"
          ></v-text-field>

          <v-text-field
            v-model="form.password"
            label="Пароль"
            prepend-inner-icon="mdi-lock"
            :type="showPassword ? 'text' : 'password'"
            :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="showPassword = !showPassword"
            :rules="[rules.required]"
            :error-messages="getFieldErrors('password')"
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
            Войти
          </v-btn>
        </v-form>

        <v-divider class="my-6"></v-divider>

        <div class="text-center">
          <span class="text-grey">Нет аккаунта?</span>
          <router-link to="/register" class="ml-2">Зарегистрироваться</router-link>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, reactive, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const formRef = ref(null)
const showPassword = ref(false)

const form = reactive({
  username: '',
  password: '',
})

const rules = {
  required: (v) => !!v || 'Обязательное поле',
}

const getFieldErrors = (field) => {
  if (authStore.error && typeof authStore.error === 'object' && authStore.error[field]) {
    return authStore.error[field]
  }
  return []
}

const handleLogin = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  const success = await authStore.login(form)
  if (success) {
    showSnackbar('Добро пожаловать!', 'success')
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  }
}
</script>
