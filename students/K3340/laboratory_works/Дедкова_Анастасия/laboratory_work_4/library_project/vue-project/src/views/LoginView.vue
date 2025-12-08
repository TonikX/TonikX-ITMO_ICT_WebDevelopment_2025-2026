<template>
  <div class="login-page">
    <h1>Вход</h1>

    <form @submit.prevent="handleLogin" class="login-form">
      <input v-model="username" placeholder="Имя пользователя" required />
      <input v-model="password" type="password" placeholder="Пароль" required />

      <button :disabled="loading">
        <span v-if="loading">⏳</span>
        <span v-else>Войти</span>
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </form>

    <p class="reg-hint">
      Нет аккаунта?
      <RouterLink to="/register">Зарегистрируйтесь</RouterLink>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter, RouterLink } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const loading  = ref(false)
const error    = ref(null)

const handleLogin = async () => {
  loading.value = true
  error.value = null
  try {
    await auth.login(username.value, password.value)
    router.replace('/')
  } catch {
    error.value = 'Неверный логин или пароль'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page { max-width: 380px; margin: 80px auto; text-align: center; }
h1 { margin-bottom: 24px; }
.login-form { display: flex; flex-direction: column; gap: 14px; }
input {
  padding: 10px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
}
button {
  background: #4f46e5;
  color: #fff;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  padding: 10px 14px;
  cursor: pointer;
}
button:disabled { opacity: .6; cursor: default; }
.error { color: #b91c1c; margin-top: 6px; }
.reg-hint {
  margin-top: 28px;
  font-size: 14px;
  color: #475569;
}
.reg-hint a {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 600;
}
.reg-hint a:hover { text-decoration: underline; }
</style>
