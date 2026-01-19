<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="5">
        <v-card>
          <v-card-title>Регистрация</v-card-title>

          <v-card-text>
            <v-alert v-if="errorText" type="error" class="mb-3">
              {{ errorText }}
            </v-alert>

            <v-alert v-if="ok" type="success" class="mb-3">
              Успешно! Теперь войдите.
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
                autocomplete="new-password"
              />
              <v-text-field
                v-model="rePassword"
                label="Repeat password"
                type="password"
                autocomplete="new-password"
              />

              <v-btn :loading="auth.loading" type="submit" block class="mt-2">
                Register
              </v-btn>
            </v-form>

            <div class="mt-3">
              Уже есть аккаунт?
              <router-link to="/login">Вход</router-link>
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
const rePassword = ref("");
const ok = ref(false);

const errorText = computed(() => {
  if (!auth.error) return "";
  if (typeof auth.error === "string") return auth.error;
  return JSON.stringify(auth.error);
});

async function submit() {
  ok.value = false;
  await auth.register({
    username: username.value,
    password: password.value,
    re_password: rePassword.value,
  });
  ok.value = true;
  setTimeout(() => router.push("/login"), 700);
}
</script>