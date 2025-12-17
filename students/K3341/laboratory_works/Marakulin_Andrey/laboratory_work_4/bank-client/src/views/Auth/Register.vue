<template>
  <v-card class="mx-auto mt-10 pa-4" max-width="400">
    <v-card-title>Регистрация сотрудника</v-card-title>
    <v-form @submit.prevent="submit">
      <v-text-field v-model="form.username" label="Логин" required></v-text-field>
      <v-text-field v-model="form.email" label="Email" required></v-text-field>
      <v-text-field v-model="form.password" label="Пароль" type="password" required></v-text-field>
      <v-btn type="submit" block color="secondary" :loading="loading" class="mt-2">Зарегистрироваться</v-btn>
    </v-form>
  </v-card>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useAuthStore } from '../../stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const form = reactive({ username: '', email: '', password: '' });
const loading = ref(false);

const submit = async () => {
  loading.value = true;
  try {
    await authStore.register(form);
    alert('Регистрация успешна! Теперь войдите.');
    router.push('/login');
  } catch (e) {
    alert('Ошибка регистрации');
  } finally {
    loading.value = false;
  }
};
</script>