<template>
  <v-app-bar color="primary" flat>
    <v-app-bar-title class="text-white">
      Управление отелем
    </v-app-bar-title>

    <v-spacer></v-spacer>

    <v-menu v-if="isAuthenticated">
      <template v-slot:activator="{ props }">
        <v-btn
          v-bind="props"
          variant="text"
          class="text-white"
        >
          Навигация
          <v-icon end>mdi-menu-down</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item to="/">
          <v-list-item-title>Главная</v-list-item-title>
        </v-list-item>
        <v-list-item to="/rooms">
          <v-list-item-title>Номера</v-list-item-title>
        </v-list-item>
        <v-list-item to="/guests">
          <v-list-item-title>Гости</v-list-item-title>
        </v-list-item>
        <v-list-item to="/staff">
          <v-list-item-title>Персонал</v-list-item-title>
        </v-list-item>
        <v-list-item to="/floors">
          <v-list-item-title>Этажи</v-list-item-title>
        </v-list-item>
        <v-list-item to="/livingRecords">
          <v-list-item-title>Записи проживания</v-list-item-title>
        </v-list-item>
        <v-list-item to="/cleaningSchedules">
          <v-list-item-title>Графики уборки</v-list-item-title>
        </v-list-item>
        <v-list-item to="/cleaningRecords">
          <v-list-item-title>Записи уборки</v-list-item-title>
        </v-list-item>
        <v-list-item to="/requests">
          <v-list-item-title>Запросы</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <v-btn
      v-if="!isAuthenticated"
      to="/login"
      variant="text"
      class="text-white"
    >
      Вход
    </v-btn>

    <v-btn
      v-if="!isAuthenticated"
      to="/register"
      variant="text"
      class="text-white"
    >
      Регистрация
    </v-btn>

    <v-menu v-if="isAuthenticated">
      <template v-slot:activator="{ props }">
        <v-btn icon v-bind="props">
          <v-icon color="white">mdi-account</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item @click="logout">
          <v-list-item-title>Выйти</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';

const router = useRouter();

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('auth_token');
});

const logout = () => {
  api.post('/auth/token/logout/')
    .finally(() => {
      localStorage.removeItem('auth_token');
      router.push('/login');
    });
};
</script>