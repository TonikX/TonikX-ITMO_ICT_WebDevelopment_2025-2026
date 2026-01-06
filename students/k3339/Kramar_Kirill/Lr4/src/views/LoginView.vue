<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" type="text" required />
      <input v-model="password" placeholder="Password" type="password" required />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import API from "@/axios";
import TokenStore from "../stores/token.ts";

export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await API.post('/auth/token/login/', {
          username: this.username,
          password: this.password,
        });
        TokenStore.setToken(response.data.auth_token);
        console.log('Token saved:', TokenStore.getToken());
        //localStorage.setItem('token', response.data.auth_token);
        //console.log('Token:', localStorage.getItem('token'));
        this.$emit('login');
        this.$router.push('/profile');
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";
</style>
