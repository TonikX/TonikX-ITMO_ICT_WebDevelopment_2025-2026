<template>
  <v-container class="dashboard">
    <!-- Заголовок -->
    <v-row>
      <v-col cols="12">
        <v-card class="mb-6" color="primary" theme="dark">
          <v-card-title class="text-h4">
            <v-icon icon="mdi-account" class="mr-3"></v-icon>
            Добро пожаловать, {{ username }}!
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <!-- Информация о станции -->
    <v-row v-if="gasStation">
      <v-col cols="12">
        <v-card class="fuel-card mb-4" elevation="3">
          <v-card-title class="d-flex align-center">
            <v-icon icon="mdi-gas-station" color="fuel" class="mr-2"></v-icon>
            <span>Информация о станции</span>
          </v-card-title>
          <v-card-text>
            <v-list density="comfortable">
              <v-list-item>
                <v-list-item-title>
                  <strong>Адрес:</strong>
                </v-list-item-title>
                <v-list-item-subtitle class="text-body-1 mt-1">
                  {{ stationAddress }}
                </v-list-item-subtitle>
              </v-list-item>
              <v-list-item v-if="stationId">
                <v-list-item-title>
                  <strong>ID станции:</strong>
                </v-list-item-title>
                <v-list-item-subtitle class="text-body-1 mt-1">
                  {{ stationId }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Информация о компании -->
    <v-row v-if="company">
      <v-col cols="12">
        <v-card class="fuel-card mb-4" elevation="3">
          <v-card-title class="d-flex align-center">
            <v-icon icon="mdi-office-building" color="primary" class="mr-2"></v-icon>
            <span>Информация о компании</span>
          </v-card-title>
          <v-card-text>
            <v-list density="comfortable">
              <v-list-item>
                <v-list-item-title>
                  <strong>Название:</strong>
                </v-list-item-title>
                <v-list-item-subtitle class="text-body-1 mt-1">
                  {{ companyTitle }}
                </v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>
                  <strong>Юридический адрес:</strong>
                </v-list-item-title>
                <v-list-item-subtitle class="text-body-1 mt-1">
                  {{ company.legal_address }}
                </v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>
                  <strong>Тип компании:</strong>
                </v-list-item-title>
                <v-list-item-subtitle class="text-body-1 mt-1">
                  {{ companyTypeText }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Доступные действия -->
    <v-row>
      <v-col cols="12">
        <v-card class="dashboard-content" elevation="3">
          <v-card-title class="d-flex align-center">
            <v-icon icon="mdi-menu" color="secondary" class="mr-2"></v-icon>
            <span>Доступные действия</span>
          </v-card-title>
          <v-card-text>
            <v-list lines="two">
              <v-list-item
                v-for="action in availableActions"
                :key="action.title"
                :to="action.route"
                class="mb-2 action-item"
                variant="outlined"
                rounded
              >
                <template v-slot:prepend>
                  <v-icon :icon="action.icon" :color="action.color"></v-icon>
                </template>
                <v-list-item-title class="text-h6">
                  {{ action.title }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ action.description }}
                </v-list-item-subtitle>
                <template v-slot:append>
                  <v-icon icon="mdi-chevron-right"></v-icon>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
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
    1: 'Фирма производитель топлива (поставщик топлива) - производит топливо',
  }
  
  return types[company.value.type_company] || `Тип ${company.value.type_company}`
})

// Доступные действия
const availableActions = computed(() => [
  {
    title: 'Продажа топлива',
    description: 'Оформление продажи топлива клиентам',
    route: '/fuel-sale',
    icon: 'mdi-gas-station',
    color: 'fuel'
  },
  {
    title: 'Анализ продаж',
    description: 'Анализ статистики продаж и отчеты',
    route: '/sales-summary',
    icon: 'mdi-chart-bar',
    color: 'info'
  },
  {
    title: 'Регистрация клиентов',
    description: 'Выдача карт лояльности новым клиентам',
    route: '/issue-card',
    icon: 'mdi-card-account-details',
    color: 'success'
  }
])
</script>

<style scoped>
.dashboard {
  max-width: 100%;
  margin: 0 auto;
  padding: 12px;
}

.dashboard-content {
  margin-top: 2rem;
}

.action-item {
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.12);
  margin-bottom: 8px;
}

.action-item:hover {
  background-color: rgba(255, 152, 0, 0.05);
  border-color: #FF9800;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Сохраняем стиль для fuel-card из variables.scss */
.fuel-card {
  border-left: 4px solid #FF9800;
}

.mb-4 {
  margin-bottom: 16px;
}
</style>