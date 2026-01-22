<template>
  <v-container fluid class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="pa-4">
          <v-card-title class="text-center">Sign In</v-card-title>

          <v-form @submit.prevent="handleLogin">
            <v-text-field
              v-model="username"
              label="Username"
              class="mb-3"
              required
            ></v-text-field>

            <v-text-field
              v-model="password"
              label="Password"
              type="password"
              class="mb-3"
              required
            ></v-text-field>

            <v-alert v-if="error" type="error" class="mb-3">{{
              error
            }}</v-alert>

            <v-btn
              type="submit"
              color="primary"
              block
              :loading="loading"
              class="mb-3"
            >
              Sign In
            </v-btn>

            <v-btn @click="router.push('/')" variant="text" block class="mb-3">
              Back to Home
            </v-btn>

            <v-divider class="my-3"></v-divider>

            <p class="text-center text-caption">Demo: user / user123</p>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login, getCurrentUser } from "@/services/authService";
import { useAuthStore } from "@/store/auth";

const username = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  if (!username.value.trim() || !password.value.trim()) {
    error.value = "Please fill in all fields";
    return;
  }

  try {
    loading.value = true;
    error.value = "";

    const data = await login(username.value, password.value);
    authStore.setToken(data.auth_token);

    const userData = await getCurrentUser(data.auth_token);
    authStore.setUser(userData);

    router.push("/dashboard");
  } catch (e) {
    error.value = "Invalid username or password";
  } finally {
    loading.value = false;
  }
};
</script>
