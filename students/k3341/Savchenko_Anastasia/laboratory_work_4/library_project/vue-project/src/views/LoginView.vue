<template>
  <div class="login-view">
    <h2>Вход в систему</h2>

    <form @submit.prevent="handleLogin">
      <!-- Поле логина -->
      <div class="form-group">
        <label for="username">Имя пользователя:</label>
        <input id="username" v-model="username" type="text" required placeholder="Логин" :disabled="auth.loading" />
      </div>

      <!-- Поле пароля -->
      <div class="form-group">
        <label for="password">Пароль:</label>
        <input id="password" v-model="password" type="password" required placeholder="Пароль" :disabled="auth.loading" />
      </div>

      <!-- Ошибка авторизации -->
      <div v-if="auth.error" class="error">{{ auth.error }}</div>

      <!-- Кнопка входа -->
      <button type="submit" :disabled="auth.loading" class="submit-btn">
        {{ auth.loading ? 'Вход...' : 'Войти' }}
      </button>
    </form>

    <!-- Ссылка на регистрацию -->
    <p class="register-link">
      Нет аккаунта? <router-link to="/register">Зарегистрируйтесь</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

// Данные формы
const username = ref('')
const password = ref('')

// Обработка входа
const handleLogin = async () => {
  try {
    await auth.login(username.value, password.value)
    router.push('/books') // редирект после успешного входа
  } catch (error) {
    // Ошибка уже обработана в store
  }
}
</script>

<style scoped>
.login-view {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.login-view h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #555;
}
.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
}
.form-group input:focus {
  outline: none;
  border-color: #42b983;
}

.error {
  background: #ffeaea;
  color: #e74c3c;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
  font-size: 14px;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;
}
.submit-btn:hover:not(:disabled) { background: #3aa876; }
.submit-btn:disabled { background: #ccc; cursor: not-allowed; }

.register-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
}
.register-link a {
  color: #42b983;
  text-decoration: none;
  font-weight: 500;
}
.register-link a:hover { text-decoration: underline; }
</style>