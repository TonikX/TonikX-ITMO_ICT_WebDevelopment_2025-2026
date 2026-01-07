<template>
  <div class="dashboard">
    <h1>Добро пожаловать, {{ username }}!</h1>
    <p>Вы работаете на станции: {{ stationAddress }}</p>
    
    <div class="dashboard-content">
      <h2>Доступные действия:</h2>
      <ul>
        <li>Просмотр цен на топливо</li>
        <li>Продажа топлива</li>
        <li>Просмотр клиентов</li>
        <!-- Добавьте другие пункты меню -->
      </ul>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const username = computed(() => authStore.user?.username || 'Пользователь')
const stationAddress = computed(() => authStore.stationAddress || 'Не указана')
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard h1 {
  margin-bottom: 1rem;
}

.dashboard-content {
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}
</style>