<template>
  <div class="container">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <input v-model="email" placeholder="Email" type="email" required />
      <input v-model="username" placeholder="Username" type="text" required />
      <input v-model="password" placeholder="Password" type="password" required />
      <input v-model="re_password" placeholder="Confirm Password" type="password" required />
      <button type="submit">Register</button>
    </form>
    <footer>
      <p>Already have an account? <RouterLink to="/login">Login</RouterLink></p>
    </footer>
  </div>
</template>

<script>
import API from "@/axios";

export default {
  data() {
    return {
      email: "",
      username: "",
      password: "",
      re_password: "",
    };
  },
  methods: {
    async register() {
      try {
        await API.post('/auth/users/', {
          email: this.email,
          username: this.username,
          password: this.password,
          re_password: this.re_password,
        });
        this.$router.push('/login');
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
