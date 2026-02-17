<template>
  <div class="register-page">
    <div class="register-container">
      <h1>Регистрация</h1>
      <form @submit.prevent="handleRegister" class="register-form">
        <div v-if="error" class="error-message">{{ error }}</div>
        <input
          v-model="formData.username"
          type="text"
          placeholder="Имя пользователя"
          class="input"
          required
        />
        <input
          v-model="formData.email"
          type="email"
          placeholder="Email"
          class="input"
          required
        />
        <input
          v-model="formData.first_name"
          type="text"
          placeholder="Имя"
          class="input"
        />
        <input
          v-model="formData.last_name"
          type="text"
          placeholder="Фамилия"
          class="input"
        />
        <select v-model="formData.role" class="input" required>
          <option value="captain">Капитан</option>
          <option value="curator">Куратор</option>
          <option value="jury">Жюри</option>
        </select>
        <input
          v-model="formData.password"
          type="password"
          placeholder="Пароль"
          class="input"
          required
        />
        <input
          v-model="formData.password_retype"
          type="password"
          placeholder="Повторите пароль"
          class="input"
          required
        />
        <button type="submit" class="btn" :disabled="loading">
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>
        <p class="login-link">
          Уже есть аккаунт? <router-link to="/login">Войти</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import { authAPI, apiErrorMessage } from '@/api'

export default {
  name: 'Register',
  data() {
    return {
      formData: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        role: 'captain',
        password: '',
        password_retype: ''
      },
      error: '',
      loading: false
    }
  },
  methods: {
    async handleRegister() {
      this.error = ''
      
      if (this.formData.password !== this.formData.password_retype) {
        this.error = 'Пароли не совпадают'
        return
      }
      
      this.loading = true
      try {
        await authAPI.register(this.formData)
        this.$router.push('/login')
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
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.register-container {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.register-container h1 {
  margin: 0 0 1.5rem 0;
  text-align: center;
  color: #2d7ef7;
}

.register-form {
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

.login-link {
  text-align: center;
  margin-top: 1rem;
  color: #666;
}

.login-link a {
  color: #2d7ef7;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
