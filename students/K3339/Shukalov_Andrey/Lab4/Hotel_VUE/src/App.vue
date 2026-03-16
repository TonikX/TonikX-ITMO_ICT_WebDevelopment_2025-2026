<template>
  <v-app>
    <v-app-bar app color="primary" black>
      <v-container>
        <v-row>
          <v-col>
            <v-btn text to="/">Отель</v-btn>
          </v-col>
          <v-col v-if="token.token" class="d-flex justify-end">
            <v-btn text to="/rooms">Номера</v-btn>
            <v-btn text to="/clients">Клиенты</v-btn>
            <v-btn text to="/employees">Работники</v-btn>
            <v-btn text to="/schedule">Расписание</v-btn>
            <v-btn text to="/profile">Профиль</v-btn>
            <v-btn text @click="logout">Выйти</v-btn>
          </v-col>

          <v-col v-else class="d-flex justify-end">
            <v-btn text to="/login">Войти</v-btn>
            <v-btn text to="/register">Зарегистрироваться</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { useTokenStore } from '@/stores/token';
import { useRouter } from 'vue-router';

const router = useRouter();

const token = useTokenStore();

function logout() {
  token.deleteToken();
  router.push('/login');
}
</script>

<style scoped></style>
