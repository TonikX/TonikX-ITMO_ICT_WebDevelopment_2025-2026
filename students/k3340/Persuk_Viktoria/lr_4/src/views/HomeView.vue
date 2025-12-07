<template>
  <div>
    <v-card v-if="loading" class="mb-6">
      <v-card-text>
        <v-progress-circular
          indeterminate
          color="primary"
          class="d-block mx-auto"
        ></v-progress-circular>
      </v-card-text>
    </v-card>

    <template v-else>
    <h1 class="text-h3 mb-6">Добро пожаловать, {{ authStore.displayName || 'Пользователь' }}!</h1>

    <!-- Статистика -->
    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="3">
        <v-card color="primary" dark>
          <v-card-text>
            <div class="text-h4">{{ statistics.drones }}</div>
            <div class="text-body-1">Дронов</div>
          </v-card-text>
          <v-card-actions>
            <v-btn variant="text" @click="$router.push('/drones')">
              Перейти
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="success" dark>
          <v-card-text>
            <div class="text-h4">{{ statistics.flights }}</div>
            <div class="text-body-1">Полётов</div>
          </v-card-text>
          <v-card-actions>
            <v-btn variant="text" @click="$router.push('/flights')">
              Перейти
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="info" dark>
          <v-card-text>
            <div class="text-h4">{{ statistics.documents }}</div>
            <div class="text-body-1">Документов</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="warning" dark>
          <v-card-text>
            <div class="text-h4">{{ statistics.activeDrones }}</div>
            <div class="text-body-1">Активных дронов</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Быстрые действия -->
    <v-card class="mb-6">
      <v-card-title>Быстрые действия</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <v-btn
              color="primary"
              block
              size="large"
              prepend-icon="mdi-airplane-plus"
              @click="$router.push('/drones')"
            >
              Добавить дрон
            </v-btn>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-btn
              color="success"
              block
              size="large"
              prepend-icon="mdi-flight-takeoff"
              @click="showFlightDialog = true"
            >
              Создать полёт
            </v-btn>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-btn
              color="info"
              block
              size="large"
              prepend-icon="mdi-file-document-plus"
              @click="$router.push('/drones')"
            >
              Добавить документ
            </v-btn>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-btn
              color="purple"
              block
              size="large"
              prepend-icon="mdi-view-dashboard"
              @click="$router.push('/drones')"
            >
              Все дроны
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-row>
      <!-- Последние дроны -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Последние дроны</span>
            <v-btn variant="text" @click="$router.push('/drones')">
              Все дроны
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            <template v-if="recentDrones.length > 0">
              <v-list>
                <v-list-item
                  v-for="drone in recentDrones"
                  :key="drone.id"
                  @click="$router.push(`/drones/${drone.id}`)"
                >
                <template v-slot:prepend>
                  <v-avatar color="primary">
                    <v-icon>mdi-airplane</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title>
                  {{ drone.manufacturer }} {{ drone.model }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ drone.serial_number }}
                </v-list-item-subtitle>
                <template v-slot:append>
                  <v-chip
                    :color="getStatusColor(drone.status)"
                    size="small"
                  >
                    {{ getStatusLabel(drone.status) }}
                  </v-chip>
                </template>
                </v-list-item>
              </v-list>
            </template>
            <div v-else class="text-center pa-4">
              <p>Дронов пока нет</p>
              <v-btn color="primary" @click="$router.push('/drones')">
                Добавить первый дрон
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Последние полёты -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Последние полёты</span>
            <v-btn variant="text" @click="$router.push('/flights')">
              Все полёты
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            <template v-if="recentFlights.length > 0">
              <v-list>
                <v-list-item
                  v-for="flight in recentFlights"
                  :key="flight.id"
                  @click="$router.push(`/flights/${flight.id}`)"
                >
                <template v-slot:prepend>
                  <v-avatar color="success">
                    <v-icon>mdi-flight-takeoff</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title>
                  Полёт #{{ flight.id }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  <div v-if="flight.drone_id">
                    {{ typeof flight.drone_id === 'object'
                      ? `${flight.drone_id.manufacturer} ${flight.drone_id.model}`
                      : 'Дрон #' + flight.drone_id }}
                  </div>
                  <div>{{ flight.location }} | {{ formatDate(flight.start_datetime) }}</div>
                </v-list-item-subtitle>
                <template v-slot:append>
                  <div class="text-body-2">
                    {{ flight.distance }} км
                  </div>
                </template>
                </v-list-item>
              </v-list>
            </template>
            <div v-else class="text-center pa-4">
              <p>Полётов пока нет</p>
              <v-btn color="success" @click="showFlightDialog = true">
                Создать первый полёт
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалоги -->
    <FlightDialog
      v-model="showFlightDialog"
      @saved="loadStatistics"
    />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import * as dronesAPI from '@/api/drones'
import * as flightsAPI from '@/api/flights'
import * as documentsAPI from '@/api/documents'
import FlightDialog from '@/components/FlightDialog.vue'

const router = useRouter()
const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const drones = ref([])
const flights = ref([])
const documents = ref([])
const showFlightDialog = ref(false)

const statistics = computed(() => {
  try {
    const dronesList = Array.isArray(drones.value) ? drones.value : []
    const flightsList = Array.isArray(flights.value) ? flights.value : []
    const documentsList = Array.isArray(documents.value) ? documents.value : []
    const activeDrones = dronesList.filter(d => d && d.status === 'active').length
    return {
      drones: dronesList.length,
      flights: flightsList.length,
      documents: documentsList.length,
      activeDrones,
    }
  } catch (error) {
    console.error('Ошибка вычисления статистики:', error)
    return {
      drones: 0,
      flights: 0,
      documents: 0,
      activeDrones: 0,
    }
  }
})

const recentDrones = computed(() => {
  if (!Array.isArray(drones.value)) return []
  return drones.value.slice(0, 5)
})

const recentFlights = computed(() => {
  if (!Array.isArray(flights.value)) return []
  return flights.value.slice(0, 5)
})

const statusOptions = [
  { title: 'Активен', value: 'active' },
  { title: 'Требуется проверка', value: 'pending' },
  { title: 'Архивирован', value: 'archived' },
]

const getStatusLabel = (status) => {
  const option = statusOptions.find(opt => opt.value === status)
  return option ? option.title : status
}

const getStatusColor = (status) => {
  const colors = { active: 'success', pending: 'warning', archived: 'grey' }
  return colors[status] || 'grey'
}

const formatDate = (dateString) => {
  if (!dateString) return 'Не указано'
  return new Date(dateString).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

const loadStatistics = async () => {
  loading.value = true
  try {
    const [dronesData, flightsData, documentsData] = await Promise.all([
      dronesAPI.getDrones().catch(err => {
        console.error('Ошибка загрузки дронов:', err)
        return []
      }),
      flightsAPI.getFlights().catch(err => {
        console.error('Ошибка загрузки полётов:', err)
        return []
      }),
      documentsAPI.getDocuments().catch(err => {
        console.error('Ошибка загрузки документов:', err)
        return []
      }),
    ])
    drones.value = Array.isArray(dronesData) ? dronesData : []
    flights.value = Array.isArray(flightsData) ? flightsData : []
    documents.value = Array.isArray(documentsData) ? documentsData : []
  } catch (error) {
    console.error('Ошибка загрузки статистики:', error)
    showSnackbar('Ошибка загрузки статистики', 'error')
    drones.value = []
    flights.value = []
    documents.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStatistics()
})

onUnmounted(() => {
  // Очищаем данные при размонтировании для предотвращения ошибок
  showFlightDialog.value = false
})
</script>
