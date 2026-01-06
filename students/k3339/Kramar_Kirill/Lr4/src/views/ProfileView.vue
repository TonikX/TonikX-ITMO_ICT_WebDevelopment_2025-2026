<template>
  <div>
    <h2>Profile</h2>
    <p>Welcome, {{ user?.username }}</p>
    <button @click="logout">Logout</button>
  </div>
</template>

<script>
import API from "@/axios";

export default {
  data() {
    return {
      user: null,
    };
  },
  async mounted() {
    try {
      const response = await API.get('/auth/users/me/');
      this.user = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$emit('logout')
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
@import "@/assets/styles.css";
</style>