<template>
  <div>
    <h2>Вход</h2>
    <form @submit.prevent="login">
      <div>
        <label>Username</label>
        <input v-model="username" required />
      </div>
      <div>
        <label>Password</label>
        <input v-model="password" type="password" required />
      </div>
      <button type="submit">Войти</button>
    </form>
    <p v-if="error" style="color:red">{{ error }}</p>
  </div>
</template>

<script>
import api, { setAuthToken } from '@/services/api';

export default {
  name: 'Login',
  data() {
    return { username: '', password: '', error: null };
  },
  methods: {
    async login() {
      this.error = null;
      try {
        const res = await api.post('/api/token/', {
          username: this.username,
          password: this.password,
        });
        const token = res.data.access;
        setAuthToken(token);
        // Перенаправить на список владельцев
        this.$router.push('/owners');
      } catch (e) {
        this.error = 'Ошибка входа: проверьте логин/пароль';
      }
    },
  },
};
</script>