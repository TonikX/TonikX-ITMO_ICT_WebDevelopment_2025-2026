<template>
  <div class="reg-page">
    <h1>Регистрация аккаунта</h1>
    <p class="subtitle">
      Аккаунт нужен только для входа на сайт. Сам читательский билет
      и карточку читателя создаёт библиотекарь.
    </p>

    <form class="reg-form" @submit.prevent="submit">
      <label class="field">
        <span class="label">Логин</span>
        <input
          v-model="form.username"
          type="text"
          required
          autocomplete="username"
          placeholder="Придумайте логин"
        />
      </label>

      <label class="field">
        <span class="label">E-mail (необязательно)</span>
        <input
          v-model="form.email"
          type="email"
          autocomplete="email"
          placeholder="name@example.com"
        />
      </label>

      <label class="field">
        <span class="label">Пароль</span>
        <input
          v-model="form.password"
          type="password"
          required
          autocomplete="new-password"
          placeholder="Минимум 8 символов"
        />
      </label>

      <label class="field">
        <span class="label">Повторите пароль</span>
        <input
          v-model="form.password2"
          type="password"
          required
          autocomplete="new-password"
          placeholder="Ещё раз пароль"
        />
      </label>

      <button class="primary-btn" type="submit" :disabled="loading">
        <span v-if="loading">Создаём аккаунт…</span>
        <span v-else>Зарегистрироваться</span>
      </button>

      <p v-if="error" class="status status-error">
        {{ error }}
      </p>

      <p v-if="success" class="status status-success">
        Аккаунт создан. Теперь можете <RouterLink to="/login">войти</RouterLink>.
      </p>
    </form>

    <p class="login-hint">
      Уже есть аккаунт?
      <RouterLink to="/login">Войти</RouterLink>
    </p>

    <div class="info-block">
      <h2>Как это работает?</h2>
      <ul>
        <li>1. Библиотекарь оформляет вам читательский билет в системе.</li>
        <li>2. Вы регистрируете веб-аккаунт с логином и паролем.</li>
        <li>
          3. После входа на сайт на странице
          «Профиль читателя» вы вводите номер билета и паспорт, чтобы посмотреть
          свои книги.
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({
  username: '',
  email: '',
  password: '',
  password2: '',
})

const loading = ref(false)
const error = ref(null)
const success = ref(false)

const submit = async () => {
  error.value = null
  success.value = false

  if (form.value.password !== form.value.password2) {
    error.value = 'Пароли не совпадают'
    return
  }

  loading.value = true

  try {
    await axios.post('http://127.0.0.1:8000/auth/users/', {
      username: form.value.username,
      password: form.value.password,
      re_password: form.value.password2,
      email: form.value.email || undefined,
    })

    success.value = true

  } catch (e) {
    console.error(e)
    error.value = 'Некорректные данные. Проверьте логин и пароль.'
  } finally {
    loading.value = false
  }
}
</script>



<style scoped>
.reg-page {
  max-width: 480px;
  margin: 48px auto 64px;
  padding: 0 16px;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI',
    sans-serif;
  color: #0f172a;
}

h1 {
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 24px;
}

.reg-form {
  background: #ffffff;
  border-radius: 18px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
  border: 1px solid #e2e8f0;
  padding: 20px 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.label {
  font-size: 13px;
  color: #475569;
}

input {
  padding: 9px 12px;
  border-radius: 10px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  font-size: 14px;
  outline: none;
  transition:
    border-color 0.12s ease,
    box-shadow 0.12s ease,
    background 0.12s ease;
}

input:focus {
  border-color: #6366f1;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.primary-btn {
  margin-top: 4px;
  border: none;
  background: linear-gradient(135deg, #4f46e5, #6366f1);
  color: white;
  padding: 10px 16px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 20px rgba(79, 70, 229, 0.35);
  transition:
    transform 0.12s ease,
    box-shadow 0.12s ease,
    opacity 0.12s ease;
}

.primary-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 14px 28px rgba(79, 70, 229, 0.4);
}

.primary-btn:disabled {
  opacity: 0.65;
  cursor: default;
  transform: none;
  box-shadow: 0 6px 14px rgba(148, 163, 184, 0.4);
}

.status {
  margin-top: 6px;
  font-size: 13px;
  padding: 8px 10px;
  border-radius: 12px;
}

.status-error {
  background: #fef2f2;
  color: #b91c1c;
}

.status-success {
  background: #ecfdf3;
  color: #166534;
}

.login-hint {
  margin-top: 18px;
  font-size: 14px;
  color: #475569;
  text-align: center;
}

.login-hint a {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 600;
}

.login-hint a:hover {
  text-decoration: underline;
}

.info-block {
  margin-top: 28px;
  font-size: 14px;
  color: #475569;
}

.info-block h2 {
  font-size: 16px;
  margin-bottom: 6px;
}

.info-block ul {
  padding-left: 18px;
  margin: 0;
}

.info-block li + li {
  margin-top: 4px;
}
</style>
