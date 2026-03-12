<template>
  <v-container>
    <v-text-field v-model="username" label="Имя пользователя" />
    <v-text-field v-model="password" label="Пароль" type="password" />
    <v-btn color="primary" @click="login">Войти</v-btn>
  </v-container>
</template>

<script>
import apiWrapper from "../api/index.js";

export default {
  data() {
    return { username: "", password: "" };
  },
  methods: {
    async login() {
      try {
        console.log("Attempting login with:", this.username);
        const res = await apiWrapper.login(this.username, this.password);
        console.log("Login response:", res);
        const token = localStorage.getItem("token");
        console.log("Token in localStorage:", token ? "Set" : "Not set");
        if (token) {
          this.$router.push({ name: "books" });
        } else {
          alert("Token not saved");
        }
      } catch (e) {
        console.error("Login error:", e);
        alert(`Login failed: ${e.message || "Unknown error"}`);
      }
    },
  },
};
</script>
