<template>
  <v-container>
    <h2>Профиль</h2>
    <div v-if="user">
      <v-form @submit.prevent="updateProfile">
        <v-text-field v-model="form.username" label="Имя пользователя" />
        <v-text-field v-model="form.email" label="Email" />
        <v-btn type="submit" color="primary">Сохранить</v-btn>
      </v-form>

      <v-divider class="my-4"></v-divider>

      <h3>Изменить пароль</h3>
      <v-form @submit.prevent="changePassword">
        <v-text-field v-model="currentPassword" label="Текущий пароль" type="password" />
        <v-text-field v-model="newPassword" label="Новый пароль" type="password" />
        <v-btn type="submit" color="primary">Изменить</v-btn>
      </v-form>

      <v-divider class="my-4"></v-divider>

      <h3>Данные пользователя</h3>
      <p><strong>ID:</strong> {{ user.id }}</p>
      <p><strong>Имя пользователя:</strong> {{ user.username }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>

      <v-divider class="my-4"></v-divider>

      <h3>Токен авторизации</h3>
      <v-text-field :model-value="token" label="Token" readonly />

      <v-divider class="my-4"></v-divider>

      <h3>Все данные пользователя (JSON)</h3>
      <pre>{{ user }}</pre>

      <v-divider class="my-4"></v-divider>
      <v-btn color="error" @click="logout">Выход</v-btn>
    </div>
    <div v-else>
      <p>Вы не авторизованы</p>
      <v-btn color="primary" @click="$router.push('/login')">Войти</v-btn>
    </div>
  </v-container>
</template>

<script>
import apiWrapper from "../api/index.js";

export default {
  data() {
    return {
      user: null,
      form: {
        username: "",
        email: "",
      },
      currentPassword: "",
      newPassword: "",
      token: localStorage.getItem("token") || "",
    };
  },
  async mounted() {
    try {
      const res = await apiWrapper.getCurrentUser();
      this.user = res.data;
      this.form.username = this.user.username;
      this.form.email = this.user.email || "";
    } catch (e) {
      console.error("Failed to load user:", e);
      this.user = null;
    }
  },
  methods: {
    async updateProfile() {
      try {
        const res = await apiWrapper.updateUser(this.form);
        this.user = res.data;
        alert("Profile updated");
      } catch (e) {
        alert("Update failed");
      }
    },
    async changePassword() {
      try {
        await apiWrapper.setPassword(this.currentPassword, this.newPassword);
        alert("Password changed");
        this.currentPassword = "";
        this.newPassword = "";
      } catch (e) {
        alert("Password change failed");
      }
    },
    logout() {
      apiWrapper.logout();
      this.token = "";
      this.user = null;
      this.$router.push("/login");
    },
  },
};
</script>
