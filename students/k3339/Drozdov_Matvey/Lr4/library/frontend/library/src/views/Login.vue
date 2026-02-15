<template>
  <div class="page">
    <div class="card">
      <div class="head">
        <div>
          <h2 class="title">Вход</h2>
          <div class="subtitle">Войдите в систему библиотеки</div>
        </div>
      </div>

      <form @submit.prevent="onSubmit" class="form">
        <label class="label">Логин</label>
        <input
          class="input"
          placeholder="Введите логин"
          v-model="username"
          autocomplete="username"
        />

        <label class="label">Пароль</label>
        <input
          class="input"
          type="password"
          placeholder="Введите пароль"
          v-model="password"
          autocomplete="current-password"
        />

        <button class="btn primary" type="submit" :disabled="loading || !canSubmit">
          {{ loading ? "Вхожу..." : "Войти" }}
        </button>

        <div v-if="error" class="error">
          {{ error }}
        </div>

        <div class="footer">
          <router-link class="link" to="/register">
            Нет аккаунта? Регистрация
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const auth = useAuthStore();

const username = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");

const canSubmit = computed(() => username.value.trim() && password.value);

async function onSubmit() {
  error.value = "";
  loading.value = true;

  try {
    await auth.login(username.value, password.value);
    router.push("/");
  } catch (e) {
    error.value = "Не удалось войти.\nПроверь логин/пароль";
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
  max-width: 420px;
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

.error {
  margin-top: 10px;
  border: 1px solid #f2b8b8;
  background: #fff5f5;
  color: #a00;
  padding: 10px;
  white-space: pre-line;
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

@media (max-width: 420px) {
  .card {
    padding: 14px;
  }
}
</style>