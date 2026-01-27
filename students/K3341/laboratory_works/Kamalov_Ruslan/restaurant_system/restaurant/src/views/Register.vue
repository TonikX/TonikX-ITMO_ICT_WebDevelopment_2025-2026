<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Регистрация</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
              <v-text-field
                v-model="form.username"
                label="Имя пользователя"
                prepend-icon="mdi-account"
                type="text"
                :error-messages="errors.username"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.email"
                label="Email"
                prepend-icon="mdi-email"
                type="email"
                :error-messages="errors.email"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.password"
                label="Пароль"
                prepend-icon="mdi-lock"
                type="password"
                :error-messages="errors.password"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.re_password"
                label="Подтвердите пароль"
                prepend-icon="mdi-lock-check"
                type="password"
                :error-messages="errors.re_password"
                required
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              @click="handleRegister"
              :loading="loading"
              :disabled="!isFormValid"
            >
              Зарегистрироваться
            </v-btn>
          </v-card-actions>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="$router.push('/login')"> Уже есть аккаунт? Войти </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const { register } = useAuthStore();

const form = ref({
  username: "",
  email: "",
  password: "",
  re_password: "",
});

const errors = ref({});
const loading = ref(false);

const isFormValid = computed(() => {
  return (
    form.value.username &&
    form.value.email &&
    form.value.password &&
    form.value.re_password &&
    form.value.password === form.value.re_password
  );
});

const handleRegister = async () => {
  loading.value = true;
  errors.value = {};

  if (form.value.password !== form.value.re_password) {
    errors.value.re_password = ["Пароли не совпадают"];
    loading.value = false;
    return;
  }

  const result = await register(form.value);

  if (result.success) {
    router.push("/login");
  } else {
    if (result.error) {
      errors.value = result.error;
    }
  }

  loading.value = false;
};
</script>
