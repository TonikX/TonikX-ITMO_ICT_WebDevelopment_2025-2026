<template>
  <v-container fluid class="dashboard-container">
    <!-- Заголовок -->
    <v-row class="mb-6">
      <v-col cols="12">
        <div class="d-flex align-center">
          <v-icon size="x-large" color="primary" class="mr-3">mdi-view-dashboard</v-icon>
          <h1 class="text-h4 font-weight-bold text-primary">Панель управления</h1>
        </div>
        <p class="text-body-1 text-medium-emphasis mt-2">
          Добро пожаловать! Ваша роль: 
          <v-chip :color="getRoleColor(role)" size="small" class="ml-1">
            {{ getRoleLabel(role) }}
          </v-chip>
        </p>
      </v-col>
    </v-row>

    <!-- Индикатор загрузки -->
    <v-row v-if="isLoading" justify="center" class="my-12">
      <v-col cols="12" sm="8" md="6" lg="4" class="text-center">
        <v-progress-circular 
          indeterminate 
          color="primary" 
          size="64" 
          width="4"
          class="mb-4"
        />
        <h3 class="text-h6 mb-2">Загрузка профиля...</h3>
        <p class="text-medium-emphasis">Подготовка вашей персональной панели</p>
      </v-col>
    </v-row>

    <!-- Основной контент -->
    <div v-else>
      <!-- Сообщение о недоступности -->
      <v-alert 
        v-if="!hasAnyAccess"
        type="info"
        variant="tonal"
        icon="mdi-information-outline"
        class="mb-6"
      >
        <template v-slot:title>
          <div class="text-h6">Нет доступных разделов</div>
        </template>
        У вашей роли нет доступных разделов. Обратитесь к администратору.
      </v-alert>

      <!-- Карточки разделов -->
      <div v-else>
        <!-- Директор: отчёты -->
        <v-row v-if="role === 'director'" class="mb-6">
          <v-col cols="12">
            <v-card variant="flat" class="section-card">
              <v-card-item>
                <div class="d-flex align-center mb-4">
                  <div class="icon-wrapper bg-primary rounded-lg pa-3 mr-3">
                    <v-icon size="28" color="white">mdi-chart-bar</v-icon>
                  </div>
                  <div>
                    <h2 class="text-h5 font-weight-bold">Аналитика и отчёты</h2>
                    <p class="text-medium-emphasis">Статистика и аналитические данные</p>
                  </div>
                </div>
                
                <v-row>
                  <v-col 
                    v-for="report in reports" 
                    :key="report.to"
                    cols="12" 
                    sm="6" 
                    md="4" 
                    lg="3"
                  >
                    <v-card 
                      :to="report.to" 
                      class="feature-card"
                      hover
                      rounded="lg"
                    >
                      <v-card-item>
                        <div class="d-flex align-center">
                          <v-icon color="primary" class="mr-3">mdi-file-chart</v-icon>
                          <div>
                            <div class="text-subtitle-1 font-weight-medium">{{ report.title }}</div>
                            <div class="text-caption text-medium-emphasis mt-1">Просмотр отчёта</div>
                          </div>
                        </div>
                      </v-card-item>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-item>
            </v-card>
          </v-col>
        </v-row>

        <!-- Управление персоналом -->
        <v-row v-if="['director'].includes(role)" class="mb-6">
          <v-col cols="12">
          <v-card variant="flat" class="section-card">
            <v-card-item>
              <div class="d-flex align-center mb-4">
                <div class="icon-wrapper bg-teal rounded-lg pa-3 mr-3">
                  <v-icon size="28" color="white">mdi-account-group</v-icon>
                </div>
                <div>
                  <h2 class="text-h5 font-weight-bold">Управление персоналом</h2>
                  <p class="text-medium-emphasis">Сотрудники и их трудоустройство</p>
                </div>
              </div>
              
              <v-row>
                <v-col cols="12" sm="6" md="4" lg="3">
                  <v-card 
                    to="/employees"
                    class="feature-card"
                    hover
                    rounded="lg"
                  >
                    <v-card-item>
                      <div class="d-flex align-center">
                        <v-icon color="teal" class="mr-3">mdi-account-details</v-icon>
                        <div>
                          <div class="text-subtitle-1 font-weight-medium">Сотрудники</div>
                          <div class="text-caption text-medium-emphasis mt-1">Управление сотрудниками</div>
                        </div>
                      </div>
                    </v-card-item>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="6" md="4" lg="3">
                  <v-card 
                    to="/employments"
                    class="feature-card"
                    hover
                    rounded="lg"
                  >
                    <v-card-item>
                      <div class="d-flex align-center">
                        <v-icon color="teal" class="mr-3">mdi-file-document-multiple</v-icon>
                        <div>
                          <div class="text-subtitle-1 font-weight-medium">Трудоустройство</div>
                          <div class="text-caption text-medium-emphasis mt-1">Управление договорами</div>
                        </div>
                      </div>
                    </v-card-item>
                  </v-card>
                </v-col>
              </v-row>
            </v-card-item>
          </v-card>
          </v-col>
        </v-row>

        <!-- Управление фермой -->
        <v-row v-if="['employee', 'director'].includes(role)" class="mb-6">
          <v-col cols="12">
            <v-card variant="flat" class="section-card">
              <v-card-item>
                <div class="d-flex align-center mb-4">
                  <div class="icon-wrapper bg-green rounded-lg pa-3 mr-3">
                    <v-icon size="28" color="white">mdi-barn</v-icon>
                  </div>
                  <div>
                    <h2 class="text-h5 font-weight-bold">Управление фермой</h2>
                    <p class="text-medium-emphasis">Организация и инфраструктура фермы</p>
                  </div>
                </div>
                
                <v-row>
                  <v-col cols="12" sm="6" md="4" lg="3" v-for="item in farmManagementItems" :key="item.to">
                    <v-card 
                      :to="item.to"
                      class="feature-card"
                      hover
                      rounded="lg"
                    >
                      <v-card-item>
                        <div class="d-flex align-center">
                          <v-icon :color="item.color" class="mr-3">{{ item.icon }}</v-icon>
                          <div>
                            <div class="text-subtitle-1 font-weight-medium">{{ item.title }}</div>
                            <div class="text-caption text-medium-emphasis mt-1">{{ item.description }}</div>
                          </div>
                        </div>
                      </v-card-item>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-item>
            </v-card>
          </v-col>
        </v-row>

        <!-- Работа с курами -->
        <v-row v-if="['employee', 'director'].includes(role)" class="mb-6">
          <v-col cols="12">
            <v-card variant="flat" class="section-card">
              <v-card-item>
                <div class="d-flex align-center mb-4">
                  <div class="icon-wrapper bg-amber rounded-lg pa-3 mr-3">
                    <v-icon size="28" color="white">mdi-chicken</v-icon>
                  </div>
                  <div>
                    <h2 class="text-h5 font-weight-bold">Работа с курами</h2>
                    <p class="text-medium-emphasis">Управление курами и их продуктивностью</p>
                  </div>
                </div>
                
                <v-row>
                  <v-col cols="12" sm="6" md="4" lg="3" v-for="item in henManagementItems" :key="item.to">
                    <v-card 
                      :to="item.to"
                      class="feature-card"
                      hover
                      rounded="lg"
                    >
                      <v-card-item>
                        <div class="d-flex align-center">
                          <v-icon :color="item.color" class="mr-3">{{ item.icon }}</v-icon>
                          <div>
                            <div class="text-subtitle-1 font-weight-medium">{{ item.title }}</div>
                            <div class="text-caption text-medium-emphasis mt-1">{{ item.description }}</div>
                          </div>
                        </div>
                      </v-card-item>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-item>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </div>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()
const isLoading = ref(false)

// Данные для отчётов
const reports = [
  { to: '/reports/eggs-by-characteristics', title: 'Яйценоскость по характеристикам' },
  { to: '/reports/top-workshop', title: 'Цех с наибольшим количеством кур' },
  { to: '/reports/employee-average-eggs', title: 'Средняя яйценоскость на работника' },
  { to: '/reports/breed-distribution', title: 'Распределение пород по цехам' },
  { to: '/reports/breed-efficiency-difference', title: 'Разница показателей пород' },
  { to: '/reports/monthly', title: 'Ежемесячный отчёт' }
]

// Данные для управления фермой
const farmManagementItems = [
  { to: '/breeds', title: 'Породы', description: 'Управление породами кур', icon: 'mdi-cow', color: 'green' },
  { to: '/diets', title: 'Диеты', description: 'Рационы питания', icon: 'mdi-food-apple', color: 'green' },
  { to: '/breed-diets', title: 'Диеты по породам', description: 'Назначение диет', icon: 'mdi-food-variant', color: 'green' },
  { to: '/cages', title: 'Клетки', description: 'Управление клетками', icon: 'mdi-grid', color: 'green' },
  { to: '/hen-cages', title: 'Поселить курицу', description: 'Размещение кур в клетках', icon: 'mdi-home-plus', color: 'green' },
  { to: '/employee-cages/new', title: 'Закрепить клетку', description: 'Назначение клеток сотрудникам', icon: 'mdi-account-check', color: 'green' },
  { to: '/employee-cages', title: 'Текущие закрепления', description: 'Актуальные назначения клеток', icon: 'mdi-account-tie', color: 'green' }
]

// Данные для работы с курами
const henManagementItems = [
  { to: '/hens', title: 'Курицы', description: 'Управление списком кур', icon: 'mdi-chicken', color: 'amber' },
  { to: '/eggs/today', title: 'Записать яйценоскость', description: 'Внести данные за сегодня', icon: 'mdi-egg-easter', color: 'amber' }
]

const role = computed(() => authStore.role)

const hasAnyAccess = computed(() => {
  const r = role.value
  return r === 'director' ||
         r === 'employee'
})

// Вспомогательные функции
const getRoleColor = (role) => {
  const colors = {
    director: 'primary',
    hr_manager: 'teal',
    coordinator: 'green',
    employee: 'amber'
  }
  return colors[role] || 'grey'
}

const getRoleLabel = (role) => {
  const labels = {
    director: 'Директор',
    hr_manager: 'HR-менеджер',
    coordinator: 'Координатор',
    employee: 'Сотрудник'
  }
  return labels[role] || role
}

// Загрузка профиля
onMounted(async () => {
  if (authStore.isAuthenticated && !authStore.user) {
    isLoading.value = true
    await authStore.fetchProfile()
    isLoading.value = false
  }
})
</script>

<style scoped>
.dashboard-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}

.section-card {
  background: rgba(var(--v-theme-surface-variant), 0.1);
  border-radius: 16px;
  border: 1px solid rgba(var(--v-theme-outline), 0.1);
  transition: all 0.3s ease;
}

.section-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.feature-card {
  height: 100%;
  transition: transform 0.2s ease;
  border: 1px solid rgba(var(--v-theme-outline), 0.05);
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Адаптивные стили */
@media (max-width: 600px) {
  .dashboard-container {
    padding: 16px;
  }
  
  h1.text-h4 {
    font-size: 1.5rem;
  }
}
</style>