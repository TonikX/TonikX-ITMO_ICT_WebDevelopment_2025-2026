<template>
  <div class="login-page">
    <v-card class="login-card" rounded="xl" elevation="8">

      <v-card-title class="py-3">
        <div class="text-h5 font-weight-medium">
          {{ isRegister ? 'Регистрация' : 'Вход' }}
        </div>
        <div class="admin-subtitle">Панель администратора</div>
      </v-card-title>

      <v-card-text class="pt-2">
        <v-alert v-if="error" type="error" variant="tonal" class="mb-4" :text="error" />
        <v-alert v-if="successMsg" type="success" variant="tonal" class="mb-4" :text="successMsg" />

        <v-form @submit.prevent="isRegister ? submitRegister() : submitLogin()">

          <v-text-field
            v-model.trim="form.username"
            label="Имя пользователя"
            variant="outlined"
            density="comfortable"
            :disabled="loading"
            class="mb-3"
          />

          <!-- Только при регистрации -->
          <v-text-field
            v-if="isRegister"
            v-model.trim="form.email"
            label="Email"
            type="email"
            variant="outlined"
            density="comfortable"
            :disabled="loading"
            class="mb-3"
          />

          <v-text-field
            v-model="form.password"
            label="Пароль"
            :type="showPassword ? 'text' : 'password'"
            variant="outlined"
            density="comfortable"
            :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="showPassword = !showPassword"
            :disabled="loading"
            class="mb-3"
          />

          <!-- Только при регистрации -->
          <v-text-field
            v-if="isRegister"
            v-model="form.re_password"
            label="Повторите пароль"
            :type="showPassword ? 'text' : 'password'"
            variant="outlined"
            density="comfortable"
            :disabled="loading"
            class="mb-3"
          />

          <v-btn
            type="submit"
            block
            color="black"
            class="text-none mt-1"
            size="large"
            :loading="loading"
            :disabled="!canSubmit"
          >
            {{ isRegister ? 'Зарегистрироваться' : 'Войти' }}
          </v-btn>
        </v-form>

        <!-- Переключатель -->
        <div class="text-center mt-4 text-body-2 text-grey-darken-1">
          <template v-if="isRegister">
            Уже есть аккаунт?
            <a href="#" class="switch-link" @click.prevent="switchMode">Войти</a>
          </template>
          <template v-else>
            Нет аккаунта?
            <a href="#" class="switch-link" @click.prevent="switchMode">Зарегистрироваться</a>
          </template>
        </div>
      </v-card-text>

    </v-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const router = useRouter()
const auth = useAuthStore()

const isRegister = ref(false)
const loading = ref(false)
const error = ref('')
const successMsg = ref('')
const showPassword = ref(false)

const form = ref({
  username: '',
  email: '',
  password: '',
  re_password: '',
})

const canSubmit = computed(() => {
  if (!form.value.username || !form.value.password) return false
  if (isRegister.value && form.value.password !== form.value.re_password) return false
  return true
})

function switchMode() {
  isRegister.value = !isRegister.value
  error.value = ''
  successMsg.value = ''
  form.value = { username: '', email: '', password: '', re_password: '' }
}

function formatErr(e) {
  const d = e?.response?.data
  if (!d) return 'Ошибка запроса'
  if (typeof d === 'string') return d
  if (typeof d === 'object') {
    return Object.entries(d)
      .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : String(v)}`)
      .join(' | ')
  }
  return 'Ошибка'
}

async function submitLogin() {
  error.value = ''
  loading.value = true
  try {
    const ok = await auth.login(form.value.username, form.value.password)
    if (ok) {
      router.push({ name: 'dashboard' })
    } else {
      error.value = 'Неверный логин или пароль'
    }
  } catch (e) {
    error.value = formatErr(e)
  } finally {
    loading.value = false
  }
}

async function submitRegister() {
  error.value = ''
  successMsg.value = ''
  loading.value = true
  try {
    await api.post('auth/users/', {
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      re_password: form.value.re_password,
    })
    successMsg.value = 'Аккаунт создан! Теперь войдите.'
    // Автоматически переключаем на форму входа через 1.5 сек
    setTimeout(() => {
      isRegister.value = false
      successMsg.value = ''
      form.value.password = ''
      form.value.re_password = ''
    }, 1500)
  } catch (e) {
    error.value = formatErr(e)
  } finally {
    loading.value = false
  }
}
</script>