<template>
  <div class="login-container">
    <v-card class="login-card" width="400" elevation="2">
      <v-card-title class="text-center">
        <div class="login-title">
          <v-icon color="primary" class="mr-2">mdi-hospital</v-icon>
          Вход в систему
        </div>
      </v-card-title>

      <v-card-text>
        <v-form @submit.prevent="login">
          <v-text-field
              v-model="username"
              label="Логин"
              outlined
              dense
              prepend-icon="mdi-account"
              class="mb-3"
              required
          />

          <v-text-field
              v-model="password"
              label="Пароль"
              outlined
              dense
              prepend-icon="mdi-lock"
              :type="showPassword ? 'text' : 'password'"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showPassword = !showPassword"
              class="mb-1"
              required
              @keyup.enter="login"
          />

          <v-alert
              v-if="error"
              type="error"
              dense
              class="mb-4"
          >
            {{ error }}
          </v-alert>

          <v-btn
              color="primary"
              block
              large
              @click="login"
              :loading="loading"
              class="login-btn"
          >
            Войти
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import api from "../api/axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      showPassword: false,
      error: null,
      loading: false,
    };
  },
  methods: {
    async login() {
      if (!this.username.trim() || !this.password.trim()) {
        this.error = "Заполните все поля";
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        const response = await api.post("/auth/jwt/create/", {
          username: this.username,
          password: this.password,
        });

        localStorage.setItem("token", response.data.access);

        window.location.href = "/patients";

      } catch (error) {
        console.error("Ошибка входа:", error);
        this.error = "Неверный логин или пароль";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 20px;
  padding-top: 100px;
}

.login-card {
  border-radius: 8px;
}

.login-title {
  font-size: 20px;
  font-weight: 500;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 20px 0 10px;
}

.login-btn {
  border-radius: 4px;
  text-transform: none;
  font-weight: 500;
  margin-top: 10px;
}

/* Адаптивность */
@media (max-width: 450px) {
  .login-card {
    width: 100% !important;
    max-width: 400px;
  }

  .login-title {
    font-size: 18px;
  }
}
</style>