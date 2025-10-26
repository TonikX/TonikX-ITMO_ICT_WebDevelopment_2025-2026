<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h5">
            <v-icon left>mdi-account</v-icon>
            Профиль пользователя
          </v-card-title>
          <v-card-text v-if="user">
            <v-list>
              <v-list-item>
                <v-list-item-title>Имя пользователя</v-list-item-title>
                <v-list-item-subtitle>{{ user.username }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Email</v-list-item-title>
                <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>ID</v-list-item-title>
                <v-list-item-subtitle>{{ user.id }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-text v-else>
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            Загрузка данных пользователя...
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const user = computed(() => authStore.user)

onMounted(() => {
  if (!user.value) {
    authStore.fetchUser()
  }
})
</script>