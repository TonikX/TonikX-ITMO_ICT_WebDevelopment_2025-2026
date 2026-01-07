<template>
  <div class="login-container">
    <div class="login-form">
      <h2>Вход в систему</h2>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Логин:</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            :disabled="isLoading"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Пароль:</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            :disabled="isLoading"
          />
        </div>
        
        <div v-if="error" class="error-message">
          {{ getErrorMessage() }}
        </div>
        
        <button 
          type="submit" 
          :disabled="isLoading"
          class="submit-btn"
        >
          <span v-if="isLoading">Вход...</span>
          <span v-else>Войти</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: ''
})

const error = ref(null)

const getErrorMessage = () => {
  if (!error.value) return ''
  
  if (typeof error.value === 'object') {
    if (error.value.non_field_errors) {
      return error.value.non_field_errors[0]
    }
    return 'Неверные данные для входа'
  }
  
  return error.value
}

const handleLogin = async () => {
  error.value = null
  
  const result = await authStore.login({
    username: form.username,
    password: form.password
  })
  
  if (!result.success) {
    error.value = result.error
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.login-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.submit-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: #f8d7da;
  border-radius: 4px;
}
</style>