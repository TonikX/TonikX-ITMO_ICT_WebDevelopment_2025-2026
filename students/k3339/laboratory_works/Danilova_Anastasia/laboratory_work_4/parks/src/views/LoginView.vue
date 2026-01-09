<script setup></script>

<template>
  <div class="login-page">
    <h2>Login</h2>
    <form>
      <div>
        <label for="email">Email:</label>
        <input
          type="text"
          id="email"
          name="email"
          placeholder="Email required"
        />
      </div>
      <div>
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          placeholder="Password required"
        />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="error" style="color: red">{{ error }}</p>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { login, getCurrentUser } from "@/services/authService";
import { useAuthStore } from "@/store/auth";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const error = ref("");

const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  try {
    error.value = "";
    const data = await login(email.value, password.value);
    authStore.setToken(data.auth_token);

    const userData = await getCurrentUser(data.auth_token);
    authStore.setUser(userData);

    router.push("/");
  } catch (err) {
    error.value = "Login failed. Please check your credentials.";
  }
};
</script>

<style scoped>
.login-page {
  margin: 100px auto;
  font-family: Arial, Helvetica, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  justify-content: center;
  text-align: center;
}
form {
  display: flex;
  flex-direction: column;
  padding: 20px 40px;
  gap: 30px;
  width: 50%;
  background-color: antiquewhite;
}
</style>
