<template>
  <div class="register-container">
    <v-card class="register-card" width="400" elevation="2">
      <v-card-title class="text-center">
        <div class="register-title">
          <v-icon color="primary" class="mr-2">mdi-account-plus</v-icon>
          Регистрация
        </div>
      </v-card-title>

      <v-card-text>
        <v-form @submit.prevent="register">
          <v-text-field
              v-model="form.username"
              label="Логин *"
              outlined
              dense
              prepend-icon="mdi-account"
              class="mb-3"
              required
              :rules="[v => !!v || 'Обязательное поле']"
          />

          <v-text-field
              v-model="form.email"
              label="Email"
              outlined
              dense
              prepend-icon="mdi-email"
              class="mb-3"
              type="email"
          />

          <v-text-field
              v-model="form.password"
              label="Пароль *"
              outlined
              dense
              prepend-icon="mdi-lock"
              :type="showPassword ? 'text' : 'password'"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showPassword = !showPassword"
              class="mb-1"
              required
              :rules="[v => !!v || 'Обязательное поле', v => v.length >= 8 || 'Минимум 8 символов']"
          />

          <v-alert
              v-if="error"
              type="error"
              dense
              class="mb-4"
          >
            {{ error }}
          </v-alert>

          <v-alert
              v-if="success"
              type="success"
              dense
              class="mb-4"
          >
            {{ success }}
          </v-alert>

          <v-btn
              color="primary"
              block
              large
              @click="register"
              :loading="loading"
              class="register-btn"
          >
            Зарегистрироваться
          </v-btn>

          <div class="login-link mt-4 text-center">
            <router-link to="/login" class="link">
              <v-icon small class="mr-1">mdi-login</v-icon>
              Уже есть аккаунт? Войти
            </router-link>
          </div>
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
      form: {
        username: "",
        email: "",
        password: "",
      },
      showPassword: false,
      error: null,
      success: null,
      loading: false,
    };
  },
  methods: {
    async register() {
      if (!this.form.username.trim() || !this.form.password.trim()) {
        this.error = "Заполните обязательные поля";
        return;
      }

      if (this.form.password.length < 8) {
        this.error = "Пароль должен содержать минимум 8 символов";
        return;
      }

      this.loading = true;
      this.error = null;
      this.success = null;

      try {
        await api.post("auth/users/", {
          username: this.form.username,
          password: this.form.password,
          email: this.form.email || undefined,
        });

        this.success = "Регистрация успешна! Теперь вы можете войти в систему.";
        this.form = {
          username: "",
          email: "",
          password: "",
        };

        // Автоматический переход на страницу входа через 2 секунды
        setTimeout(() => {
          this.$router.push("/login");
        }, 2000);

      } catch (error) {
        console.error("Ошибка регистрации:", error);

        if (error.response?.data?.username) {
          this.error = "Пользователь с таким логином уже существует";
        } else if (error.response?.data?.email) {
          this.error = "Пользователь с таким email уже существует";
        } else {
          this.error = "Ошибка регистрации. Попробуйте позже.";
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 20px;
  padding-top: 100px;
}

.register-card {
  border-radius: 8px;
}

.register-title {
  font-size: 20px;
  font-weight: 500;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 20px 0 10px;
}

.register-btn {
  border-radius: 4px;
  text-transform: none;
  font-weight: 500;
  margin-top: 10px;
}

.login-link {
  font-size: 14px;
}

.link {
  color: #1976d2;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}

.link:hover {
  text-decoration: underline;
}

/* Адаптивность */
@media (max-width: 450px) {
  .register-card {
    width: 100% !important;
    max-width: 400px;
  }

  .register-title {
    font-size: 18px;
  }
}
</style>