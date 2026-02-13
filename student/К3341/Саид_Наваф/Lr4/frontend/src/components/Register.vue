<template>
  <div>
    <h2>Регистрация</h2>
    <form @submit.prevent="register">
      <div><input v-model="username" placeholder="username" required /></div>
      <div><input v-model="email" placeholder="email" required /></div>
      <div><input v-model="password" type="password" placeholder="password" required /></div>
      <button type="submit">Зарегистрироваться</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'Register',
  data() {
    return { username: '', email: '', password: '', message: null };
  },
  methods: {
    async register() {
      this.message = null;
      try {
        // Djoser: POST /auth/users/ для регистрации
        await api.post('/auth/users/', {
          username: this.username,
          email: this.email,
          password: this.password,
        });
        this.message = 'Пользователь зарегистрирован. Проверьте e-mail при необходимости.';
        this.username = this.email = this.password = '';
      } catch (e) {
        this.message = 'Ошибка регистрации';
      }
    },
  },
};
</script>