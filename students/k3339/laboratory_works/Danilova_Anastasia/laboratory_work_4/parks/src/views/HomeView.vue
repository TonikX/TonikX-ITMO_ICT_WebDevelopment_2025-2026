<template>
  <div class="home">
    <h2>Welcome to parks app!</h2>
    <p>Authorization is required to access this app:</p>
    <div class="">
      <router-link to="/login"><button>Login</button></router-link>
      <router-link to="/register"><button>Register</button></router-link>
    </div>
  </div>
</template>
<script setup>
import router from "@/router";
</script>
<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}
button {
  margin: 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
