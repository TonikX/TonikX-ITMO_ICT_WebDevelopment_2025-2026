<template>
  <div class="page">
    <div class="card">
      <div class="head">
        <div>
          <h2 class="title">Регистрация</h2>
          <div class="subtitle">Создайте аккаунт, чтобы пользоваться системой</div>
        </div>
      </div>

      <form @submit.prevent="onSubmit" class="form">
        <label class="label">Email</label>
        <input
          class="input"
          type="email"
          placeholder="name@example.com"
          v-model="email"
          autocomplete="email"
        />

        <label class="label">Логин</label>
        <input
          class="input"
          type="text"
          placeholder="Придумайте логин"
          v-model="username"
          autocomplete="username"
        />

        <label class="label">Пароль</label>
        <input
          class="input"
          type="password"
          placeholder="Придумайте пароль"
          v-model="password"
          autocomplete="new-password"
        />

        <button class="btn primary" type="submit" :disabled="loading || !canSubmit">
          {{ loading ? "Создаю..." : "Создать аккаунт" }}
        </button>

        <div class="footer">
          <router-link class="link" to="/login">Уже есть аккаунт? Войти</router-link>
        </div>

        <div v-if="success" class="success">
          Аккаунт создан. Сейчас перенаправлю на вход…
        </div>

        <div v-if="error" class="error">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();

const email = ref("");
const username = ref("");
const password = ref("");

const loading = ref(false);
const error = ref("");
const success = ref(false);

const API_URL = "http://127.0.0.1:8000";

const canSubmit = computed(() => {
  return email.value.trim() && username.value.trim() && password.value;
});

async function onSubmit() {
  error.value = "";
  success.value = false;
  loading.value = true;

  try {
    await axios.post(`${API_URL}/auth/users/`, {
      email: email.value.trim(),
      username: username.value.trim(),
      password: password.value,
    });

    success.value = true;
    setTimeout(() => router.push("/login"), 700);
  } catch (e) {
    const data = e.response?.data;

    if (data && typeof data === "object") {
      const lines = [];
      for (const key in data) {
        const v = data[key];
        lines.push(`${key}: ${Array.isArray(v) ? v.join(", ") : String(v)}`);
      }
      error.value = lines.join("\n");
    } else {
      error.value = "Ошибка регистрации. Проверь, что бэкенд запущен и путь /auth/users/ существует.";
    }
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.page {
  min-height: calc(100vh - 40px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px 14px;
}

.card {
  width: 100%;
  max-width: 460px;
  border: 1px solid #ddd;
  background: #fff;
  padding: 16px;
}

.head {
  display: flex;
  gap: 12px;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 1px solid #eee;
  margin-bottom: 12px;
}

.logo {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border: 1px solid #ddd;
  font-size: 22px;
}

.title {
  margin: 0;
  font-size: 22px;
}

.subtitle {
  margin-top: 4px;
  font-size: 14px;
  opacity: 0.75;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.label {
  margin-top: 8px;
  font-weight: 700;
  font-size: 14px;
}

.input {
  width: 95%;
  padding: 10px;
  border: 1px solid teal;
  outline: none;
}

.input:focus {
  border-color: #0a8;
}

.btn {
  padding: 10px 12px;
  border: 1px solid teal;
  background: #fff;
  cursor: pointer;
  margin-top: 10px;
}

.primary {
  width: 100%;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.footer {
  margin-top: 10px;
  display: flex;
  justify-content: center;
}

.link {
  text-decoration: none;
  color: teal;
  font-weight: 600;
}

.link:hover {
  text-decoration: underline;
}

.success {
  margin-top: 10px;
  border: 1px solid #b9e5c2;
  background: #f4fff7;
  color: #166534;
  padding: 10px;
}

.error {
  margin-top: 10px;
  border: 1px solid #f2b8b8;
  background: #fff5f5;
  color: #a00;
  padding: 10px;
  white-space: pre-line;
}

@media (max-width: 420px) {
  .card {
    padding: 14px;
  }
}
</style>