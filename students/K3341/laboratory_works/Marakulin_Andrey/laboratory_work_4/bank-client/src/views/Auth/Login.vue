<template>
  <v-card class="mx-auto mt-10 pa-4" max-width="400">
    <v-card-title>Вход</v-card-title>
    <v-form @submit.prevent="submit">
      <v-text-field v-model="form.username" label="Логин" prepend-icon="mdi-account"></v-text-field>
      <v-text-field v-model="form.password" label="Пароль" type="password" prepend-icon="mdi-lock"></v-text-field>
      <v-btn type="submit" block color="primary" :loading="loading" class="mt-2">Войти</v-btn>
      <v-alert v-if="error" type="error" class="mt-3" density="compact">{{ error }}</v-alert>
    </v-form>
  </v-card>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useAuthStore } from '../../stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const form = reactive({ username: '', password: '' });
const loading = ref(false);
const error = ref('');

const submit = async () => {
  loading.value = true;
  error.value = '';
  try {
    await authStore.login(form);
    router.push('/clients');
  } catch (e) {
    error.value = 'Ошибка входа. Проверьте данные.';
  } finally {
    loading.value = false;
  }
};
</script>