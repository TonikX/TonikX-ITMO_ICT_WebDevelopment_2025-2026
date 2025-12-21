<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()

onMounted(() => {
  if (!auth.user && auth.token) {
    auth.fetchMe()
  }
})
</script>

<template>
  <v-row justify="center">
    <v-col cols="12" md="6">
      <v-card elevation="3">
        <v-card-title class="text-h6">Профиль</v-card-title>
        <v-card-subtitle>Текущий пользователь</v-card-subtitle>
        <v-card-text>
          <v-alert v-if="!auth.user" type="info" density="compact">
            Данные профиля загружаются...
          </v-alert>
          <v-list v-else lines="two">
            <v-list-item>
              <v-list-item-title>Имя пользователя</v-list-item-title>
              <v-list-item-subtitle>{{ auth.user.username }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Email</v-list-item-title>
              <v-list-item-subtitle>{{ auth.user.email || '—' }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Активен</v-list-item-title>
              <v-list-item-subtitle>{{ auth.user.is_active ? 'Да' : 'Нет' }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Суперпользователь</v-list-item-title>
              <v-list-item-subtitle>{{ auth.user.is_superuser ? 'Да' : 'Нет' }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>


