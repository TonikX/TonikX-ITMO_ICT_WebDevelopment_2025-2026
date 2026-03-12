<template>
  <v-container>
    <h2>Регистрация</h2>
    <v-text-field v-model="username" label="Имя пользователя" />
    <v-text-field v-model="password" label="Пароль" type="password" />
    <v-btn color="primary" @click="register">Зарегистрироваться</v-btn>
  </v-container>
</template>

<script>
import apiWrapper from "../api/index.js";

export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async register() {
      try {
        await apiWrapper.register(this.username, this.password);
        alert("Вы зарегистрированы");
        this.$router.push("/login");
      } catch (e) {
        alert("Ошибка регистрации");
      }
    },
  },
};
</script>
