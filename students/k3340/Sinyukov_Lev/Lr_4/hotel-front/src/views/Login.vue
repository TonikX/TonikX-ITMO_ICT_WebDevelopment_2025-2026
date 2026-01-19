<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card>
          <v-card-title>Вход</v-card-title>

          <v-card-text>
            <v-alert v-if="errorText" type="error" class="mb-3">
              {{ errorText }}
            </v-alert>

            <v-form @submit.prevent="submit">
              <v-text-field
                v-model="username"
                label="Username"
                autocomplete="username"
              />
              <v-text-field
                v-model="password"
                label="Password"
                type="password"
                autocomplete="current-password"
              />

              <v-btn :loading="auth.loading" type="submit" block class="mt-2">
                Login
              </v-btn>
            </v-form>

            <div class="mt-3">
              Нет аккаунта?
              <router-link to="/register">Регистрация</router-link>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

const username = ref("");
const password = ref("");

const errorText = computed(() => {
  if (!auth.error) return "";
  if (typeof auth.error === "string") return auth.error;
  return JSON.stringify(auth.error);
});

async function submit() {
  await auth.login(username.value, password.value);
  await router.replace("/");
}
</script>
