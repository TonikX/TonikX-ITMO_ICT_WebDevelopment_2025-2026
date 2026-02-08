<template>
  <div class="page">
    <h1>Профиль пользователя</h1>

    <div v-if="loading">Загружаем данные...</div>

    <div v-else-if="!isAuthenticated">
      <p>
        Вы не авторизованы. Пожалуйста,
        <RouterLink to="/login">войдите</RouterLink>.
      </p>
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else-if="user" class="card">
      <p><strong>ID аккаунта:</strong> {{ user.id }}</p>
      <p><strong>Имя пользователя:</strong> {{ user.username }}</p>
      <p v-if="user.email"><strong>Email:</strong> {{ user.email }}</p>
      <p v-if="user.date_joined">
        <strong>Дата регистрации:</strong> {{ formatDateTime(user.date_joined) }}
      </p>
      <p v-if="token">
        <strong>Токен авторизации:</strong>
        <code>{{ token }}</code>
      </p>

      <button class="logout-btn" @click="logout">
        Выйти
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, RouterLink } from "vue-router";
import api from "../api/api";
import { isAuthenticated, token, clearAuth } from "../auth";

const router = useRouter();
const user = ref(null);
const loading = ref(true);
const error = ref("");

const fetchUser = async () => {
  if (!isAuthenticated.value) {
    loading.value = false;
    return;
  }

  try {
    const response = await api.get("/auth/users/me/");
    user.value = response.data;
  } catch (e) {
    console.error(e);

    // Если токен мёртвый / невалидный — разлогиниваем и кидаем на /login
    if (e.response && e.response.status === 401) {
      clearAuth();
      router.push("/login");
      return;
    }

    error.value = "Не удалось загрузить данные пользователя.";
  } finally {
    loading.value = false;
  }
};

const formatDateTime = (isoString) => {
  if (!isoString) return "";
  return new Date(isoString).toLocaleString();
};

const logout = async () => {
  try {
    await api.post("/auth/token/logout/");
  } catch (e) {
    console.error(e);
  } finally {
    clearAuth();
    router.push("/login");
  }
};

onMounted(fetchUser);
</script>

<style scoped>
.card {
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #ddd;
  max-width: 500px;
  margin-top: 16px;
}

code {
  display: inline-block;
  padding: 2px 4px;
  background-color: #f5f5f5;
  border-radius: 4px;
  font-size: 12px;
  word-break: break-all;
}

.logout-btn {
  margin-top: 16px;
  padding: 8px 12px;
  cursor: pointer;
}

.error {
  color: #d32f2f;
  margin-top: 8px;
}
</style>