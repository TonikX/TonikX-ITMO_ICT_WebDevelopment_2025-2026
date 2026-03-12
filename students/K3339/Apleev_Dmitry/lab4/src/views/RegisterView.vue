<template>
  <v-row justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card>
        <v-card-title class="text-h6">регистрация</v-card-title>
        <v-card-text>
          <v-alert v-if="error" type="error" density="compact" class="mb-2">
            {{ error }}
          </v-alert>

          <v-form @submit.prevent="onSubmit">
            <v-text-field
              v-model="username"
              label="логин"
              variant="outlined"
              density="comfortable"
              required
            />
            <v-text-field
              v-model="email"
              label="email"
              variant="outlined"
              density="comfortable"
            />
            <v-text-field
              v-model="password"
              label="пароль"
              type="password"
              variant="outlined"
              density="comfortable"
              required
            />
            <v-text-field
              v-model="password2"
              label="повтор пароля"
              type="password"
              variant="outlined"
              density="comfortable"
              required
            />

            <v-btn :loading="loading" type="submit" color="primary" class="mt-2" block>
              зарегистрироваться
            </v-btn>

            <v-btn class="mt-2" variant="text" block @click="$router.push('/login')">
              уже есть аккаунт? вход
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiRegister } from '../api'

// форма регистрации пользователя
const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')

const loading = ref(false)
const error = ref('')

const router = useRouter()

const onSubmit = async () => {
  error.value = ''

  if (!username.value || !password.value || !password2.value) {
    error.value = 'заполните обязательные поля'
    return
  }
  if (password.value !== password2.value) {
    error.value = 'пароли не совпадают'
    return
  }

  loading.value = true
  try {
    await apiRegister({
      username: username.value,
      email: email.value || undefined,
      password: password.value,
      re_password: password2.value
    })
    router.push('/login')
  } catch (e) {
    error.value = 'ошибка регистрации, проверьте данные'
  } finally {
    loading.value = false
  }
}
</script>

