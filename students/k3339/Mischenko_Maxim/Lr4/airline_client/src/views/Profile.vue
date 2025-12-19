<template>
  <v-container>
    <v-card class="pa-4 mx-auto" max-width="600">
      <v-card-title>Профиль пользователя</v-card-title>
      <v-card-text v-if="user">
        <v-text-field v-model="user.username" label="Логин" readonly variant="filled"></v-text-field>
        <v-text-field v-model="user.email" label="Email"></v-text-field>
        <v-text-field v-model="user.name" label="Имя"></v-text-field> 
        <v-text-field v-model="user.surname" label="Фамилия"></v-text-field> 

        <v-btn color="success" @click="updateProfile" class="mr-2">Сохранить</v-btn>
        <v-btn color="error" @click="logout">Выйти</v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';
import { useRouter } from 'vue-router';

const router = useRouter();
const user = ref(null);

onMounted(async () => {
  try {
    const response = await api.get('/auth/users/me/');
    user.value = response.data;
  } catch (e) {
    router.push('/login');
  }
});

const updateProfile = async () => {
  try {
    await api.patch('/auth/users/me/', {
      email: user.value.email,
      name: user.value.name
    });
    alert('Данные обновлены!');
  } catch (e) {
    alert('Ошибка обновления');
  }
};

const logout = () => {
  api.post('/auth/token/logout/');
  localStorage.removeItem('auth_token');
  router.push('/login');
};
</script>
