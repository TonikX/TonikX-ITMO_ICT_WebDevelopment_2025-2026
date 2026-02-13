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
        ✅ Аккаунт успешно создан!
        <p class="success-text">Сейчас вы будете перенаправлены на страницу привязки читательского билета...</p>
        <router-link to="/link-reader" class="success-link">Перейти сейчас</router-link>
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

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

    // Перенаправление на страницу привязки билета через 2 секунды
    setTimeout(() => {
      router.push('/link-reader')
    }, 2000)

  } catch (err) {
    if (err.response?.data?.username) {
      error.value = 'Пользователь с таким именем уже существует'
    } else {
      error.value = 'Ошибка регистрации. Попробуйте другой логин.'
    }
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
  font-size: 28px;
  font-weight: 600;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #495057;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 15px;
  box-sizing: border-box;
  transition: all 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52,152,219,0.1);
}

.form-group input:disabled {
  background-color: #f8f9fa;
  border-color: #dee2e6;
}

.error-message {
  background: #fee;
  color: #e74c3c;
  padding: 12px 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 14px;
  border-left: 4px solid #e74c3c;
}

.success-message {
  background: #e8f8f0;
  color: #27ae60;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 16px;
  text-align: center;
  border-left: 4px solid #27ae60;
}

.success-message p {
  margin: 10px 0 5px;
  font-size: 14px;
}

.success-link {
  display: inline-block;
  margin-top: 10px;
  color: #27ae60;
  font-weight: 600;
  text-decoration: none;
  padding: 8px 20px;
  background: rgba(39,174,96,0.1);
  border-radius: 20px;
  transition: all 0.3s;
}

.success-link:hover {
  background: #27ae60;
  color: white;
  text-decoration: none;
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
  transition: all 0.3s;
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
}

.login-link {
  text-align: center;
  margin-top: 25px;
  color: #7f8c8d;
  font-size: 15px;
}

.login-link a {
  color: #3498db;
  text-decoration: none;
  font-weight: 600;
  margin-left: 5px;
}

.login-link a:hover {
  text-decoration: underline;
  color: #2980b9;
}

/* Анимация загрузки */
@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.submit-btn:disabled {
  animation: pulse 1.5s infinite;
}

/* Адаптивность */
@media (max-width: 480px) {
  .register-view {
    margin: 20px;
    padding: 25px;
  }

  .register-view h2 {
    font-size: 24px;
  }
}
</style>