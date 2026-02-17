<template>
  <div class="login-page">
    <div class="login-container">
      <h1>Вход</h1>
      <form @submit.prevent="handleLogin" class="login-form">
        <div v-if="error" class="error-message">{{ error }}</div>
        <input
          v-model="email"
          type="email"
          placeholder="Email"
          class="input"
          required
        />
        <input
          v-model="password"
          type="password"
          placeholder="Пароль"
          class="input"
          required
        />
        <button type="submit" class="btn" :disabled="loading">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
        <p class="register-link">
          Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import { authAPI, apiErrorMessage } from '@/api'

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      error: '',
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      this.error = ''
      this.loading = true
      try {
        const response = await authAPI.login(this.email, this.password)
        localStorage.setItem('authToken', response.auth_token)
        
        // Получаем информацию о пользователе
        const user = await authAPI.getMe()
        localStorage.setItem('user', JSON.stringify(user))
        window.dispatchEvent(new Event('auth-changed'))
        
        this.$router.push('/')
      } catch (e) {
        this.error = apiErrorMessage(e)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.login-container {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-container h1 {
  margin: 0 0 1.5rem 0;
  text-align: center;
  color: #2d7ef7;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.register-link {
  text-align: center;
  margin-top: 1rem;
  color: #666;
}

.register-link a {
  color: #2d7ef7;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
