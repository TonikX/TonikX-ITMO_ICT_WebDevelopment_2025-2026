<template>
  <div class="dashboard">
    <h1>Добро пожаловать, {{ username }}!</h1>
    
    <div v-if="gasStation" class="station-info">
      <h2>Информация о станции:</h2>
      <p><strong>Адрес:</strong> {{ stationAddress }}</p>
    </div>
    
    <div v-if="company" class="company-info">
      <h2>Информация о компании:</h2>
      <p><strong>Название:</strong> {{ companyTitle }}</p>
      <p><strong>Юридический адрес:</strong> {{ company.legal_address }}</p>
      <p><strong>Тип компании:</strong> {{ companyTypeText }}</p>
    </div>
    
    <div class="dashboard-content">
      <h2>Доступные действия:</h2>
      <ul>
        <li>
          <router-link to="/fuel-sale" class="action-link">
            Продажа топлива
          </router-link>
        </li>
        <li>
          <router-link to="/sales-summary" class="action-link">
            Анализ продаж
          </router-link>
        </li>
        <li>
          <router-link to="/issue-card" class="action-link">
            Регистрация клиентов
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const username = computed(() => authStore.user?.username || 'Пользователь')
const gasStation = computed(() => authStore.gasStation)
const stationAddress = computed(() => authStore.stationAddress)
const stationId = computed(() => authStore.stationId)
const company = computed(() => authStore.company)
const companyTitle = computed(() => authStore.companyTitle)

// Дополнительная логика для отображения типа компании
const companyTypeText = computed(() => {
  if (!company.value) return 'Неизвестно'
  
  const types = {
    0: 'Фирма владелец - владеет заправками',
    1: 'Ффирма производитель топлива (поставшик-топлива) - производит топливо',
  }
  
  return types[company.value.type_company] || `Тип ${company.value.type_company}`
})
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard h1 {
  margin-bottom: 1rem;
}

.station-info, .company-info, .dashboard-content {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}

.station-info h2, .company-info h2 {
  color: #333;
  margin-bottom: 1rem;
}

.station-info p, .company-info p {
  margin: 0.5rem 0;
  line-height: 1.5;
}
</style>