<template>
  <div class="register-view">
    <h2>Регистрация</h2>

    <form @submit.prevent="handleRegister">
      <!-- Имя пользователя -->
      <div class="form-group">
        <label for="username">Имя пользователя:</label>
        <input id="username" v-model="username" type="text" required placeholder="Логин" :disabled="auth.loading" />
      </div>

      <!-- Email (опционально) -->
      <div class="form-group">
        <label for="email">Email (необязательно):</label>
        <input id="email" v-model="email" type="email" placeholder="example@mail.com" :disabled="auth.loading" />
      </div>

      <!-- Пароль -->
      <div class="form-group">
        <label for="password">Пароль:</label>
        <input id="password" v-model="password" type="password" required placeholder="Не менее 8 символов" :disabled="auth.loading" />
      </div>

      <!-- Подтверждение пароля -->
      <div class="form-group">
        <label for="password2">Повторите пароль:</label>
        <input id="password2" v-model="password2" type="password" required placeholder="Повторите пароль" :disabled="auth.loading" />
      </div>

      <!-- Сообщения об ошибке/успехе -->
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">
        ✅ Аккаунт создан!<br>
        <small>Перенаправление на привязку билета...</small><br>
        <router-link to="/link-reader">Перейти сейчас</router-link>
      </div>

      <!-- Кнопка регистрации -->
      <button type="submit" :disabled="auth.loading" class="submit-btn">
        {{ auth.loading ? 'Регистрация...' : 'Зарегистрироваться' }}
      </button>
    </form>

    <!-- Ссылка на вход -->
    <p class="login-link">
      Уже есть аккаунт? <router-link to="/login">Войдите</router-link>
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
const email = ref('')
const password = ref('')
const password2 = ref('')
const error = ref('')
const success = ref(false)

// Обработка регистрации
const handleRegister = async () => {
  error.value = ''; success.value = false

  // Валидация
  if (password.value !== password2.value) {
    error.value = 'Пароли не совпадают'
    return
  }
  if (password.value.length < 8) {
    error.value = 'Пароль должен быть минимум 8 символов'
    return
  }

  // Подготовка данных для API
  const userData = {
    username: username.value,
    password: password.value,
    re_password: password2.value,
  }
  if (email.value.trim()) userData.email = email.value

  try {
    await auth.register(userData)
    success.value = true
    // Очистка формы
    username.value = email.value = password.value = password2.value = ''

    // Редирект на привязку билета через 2 сек
    setTimeout(() => router.push('/link-reader'), 2000)
  } catch (err) {
    error.value = err.response?.data?.username
      ? 'Пользователь уже существует'
      : 'Ошибка регистрации'
  }
}
</script>

<style scoped>
.register-view {
  max-width: 450px;
  margin: 40px auto;
  padding: 35px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
.register-view h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
}

.form-group { margin-bottom: 20px; }
.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #495057;
}
.form-group input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 15px;
  box-sizing: border-box;
  transition: 0.3s;
}
.form-group input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52,152,219,0.1);
}
.form-group input:disabled {
  background: #f8f9fa;
  border-color: #dee2e6;
}

.error {
  background: #fee;
  color: #e74c3c;
  padding: 12px 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #e74c3c;
}
.success {
  background: #e8f8f0;
  color: #27ae60;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: center;
  border-left: 4px solid #27ae60;
}
.success a {
  color: #27ae60;
  font-weight: 600;
}

.submit-btn {
  width: 100%;
  padding: 14px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
  margin-top: 10px;
}
.submit-btn:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(52,152,219,0.3);
}
.submit-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  animation: pulse 1.5s infinite;
}

.login-link {
  text-align: center;
  margin-top: 25px;
  color: #7f8c8d;
}
.login-link a {
  color: #3498db;
  font-weight: 600;
  text-decoration: none;
}
.login-link a:hover { text-decoration: underline; }

@keyframes pulse {
  0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; }
}

@media (max-width: 480px) {
  .register-view { margin: 20px; padding: 25px; }
  .register-view h2 { font-size: 24px; }
}
</style>