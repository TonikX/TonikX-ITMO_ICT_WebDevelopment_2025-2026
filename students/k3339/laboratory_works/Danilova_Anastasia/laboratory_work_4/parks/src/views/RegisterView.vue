<template>
  <v-container fluid class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="pa-4">
          <v-card-title class="text-center">Create Account</v-card-title>

          <v-form @submit.prevent="handleRegister">
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

            <v-text-field
              v-model="passwordConfirm"
              label="Confirm Password"
              type="password"
              class="mb-3"
              required
            ></v-text-field>

            <v-alert v-if="error" type="error" class="mb-3">{{
              error
            }}</v-alert>

            <v-alert v-if="success" type="success" class="mb-3">
              Registration successful! Redirecting...
            </v-alert>

            <v-btn
              type="submit"
              color="primary"
              block
              :loading="loading"
              class="mb-3"
            >
              Create Account
            </v-btn>

            <v-btn @click="router.push('/login')" variant="text" block>
              Back to Login
            </v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { register } from "@/services/authService";

const router = useRouter();

const username = ref("");
const password = ref("");
const passwordConfirm = ref("");
const error = ref("");
const success = ref(false);
const loading = ref(false);

const handleRegister = async () => {
  if (
    !username.value.trim() ||
    !password.value.trim() ||
    !passwordConfirm.value.trim()
  ) {
    error.value = "Please fill in all fields";
    return;
  }

  if (password.value !== passwordConfirm.value) {
    error.value = "Passwords do not match";
    return;
  }

  try {
    loading.value = true;
    error.value = "";

    await register(username.value, password.value);
    success.value = true;

    setTimeout(() => {
      router.push("/login");
    }, 1500);
  } catch (err) {
    if (err.response?.data) {
      const errorData = err.response.data;
      if (typeof errorData === "object") {
        const firstError = Object.values(errorData)[0];
        error.value = Array.isArray(firstError) ? firstError[0] : firstError;
      } else {
        error.value = errorData.toString();
      }
    } else {
      error.value = "Registration failed";
    }
  } finally {
    loading.value = false;
  }
};
</script>
