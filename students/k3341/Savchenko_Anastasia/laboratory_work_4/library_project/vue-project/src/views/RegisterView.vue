<template>
  <div class="register-view">
    <h2>Регистрация</h2>

    <form @submit.prevent="handleRegister" class="register-form">
      <div class="form-group">
        <label for="reg-username">Имя пользователя:</label>
        <input
          id="reg-username"
          v-model="username"
          type="text"
          required
          placeholder="Придумайте логин"
          :disabled="auth.loading"
        />
      </div>

      <div class="form-group">
        <label for="reg-email">Email (необязательно):</label>
        <input
          id="reg-email"
          v-model="email"
          type="email"
          placeholder="example@mail.com"
          :disabled="auth.loading"
        />
      </div>

      <div class="form-group">
        <label for="reg-password">Пароль:</label>
        <input
          id="reg-password"
          v-model="password"
          type="password"
          required
          placeholder="Не менее 8 символов"
          :disabled="auth.loading"
        />
      </div>

      <div class="form-group">
        <label for="reg-password2">Повторите пароль:</label>
        <input
          id="reg-password2"
          v-model="password2"
          type="password"
          required
          placeholder="Повторите пароль"
          :disabled="auth.loading"
        />
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-if="success" class="success-message">
        Аккаунт успешно создан! <router-link to="/login">Войдите</router-link>
      </div>

      <button type="submit" :disabled="auth.loading" class="submit-btn">
        {{ auth.loading ? 'Регистрация...' : 'Зарегистрироваться' }}
      </button>
    </form>

    <p class="login-link">
      Уже есть аккаунт? <router-link to="/login">Войдите</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const error = ref('')
const success = ref(false)

const handleRegister = async () => {
  // Сброс ошибок
  error.value = ''
  success.value = false

  // Проверка паролей
  if (password.value !== password2.value) {
    error.value = 'Пароли не совпадают'
    return
  }

  // Проверка длины пароля
  if (password.value.length < 8) {
    error.value = 'Пароль должен содержать минимум 8 символов'
    return
  }

  // Подготовка данных
  const userData = {
    username: username.value,
    password: password.value,
    re_password: password2.value,
  }

  // Добавляем email если он есть
  if (email.value.trim()) {
    userData.email = email.value
  }

  try {
    await auth.register(userData)
    success.value = true

    // Очистка формы
    username.value = ''
    email.value = ''
    password.value = ''
    password2.value = ''
  } catch (err) {
    error.value = 'Ошибка регистрации. Попробуйте другой логин.'
  }
}
</script>

<style scoped>
.register-view {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.register-view h2 {
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

.error-message {
  background: #ffeaea;
  color: #e74c3c;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
  font-size: 14px;
}

.success-message {
  background: #e8f7ef;
  color: #27ae60;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
  font-size: 14px;
}

.success-message a {
  color: #27ae60;
  font-weight: 500;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;
}

.submit-btn:hover:not(:disabled) {
  background: #2980b9;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.login-link a {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>