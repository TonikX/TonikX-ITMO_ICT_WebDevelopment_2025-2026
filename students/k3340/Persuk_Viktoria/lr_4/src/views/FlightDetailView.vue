<template>
  <div>
    <v-btn
      prepend-icon="mdi-arrow-left"
      variant="text"
      @click="$router.back()"
      class="mb-4"
    >
      Назад
    </v-btn>

    <v-card v-if="loading">
      <v-card-text>
        <v-progress-circular
          indeterminate
          color="primary"
          class="d-block mx-auto"
        ></v-progress-circular>
      </v-card-text>
    </v-card>

    <div v-else-if="flight">
      <v-card class="mb-4">
        <v-card-title class="d-flex justify-space-between align-center">
          <div>
            <h2 class="text-h4">Полёт #{{ flight.id }}</h2>
            <div class="text-body-2 text-grey" v-if="flight.drone_id">
              Дрон: {{ typeof flight.drone_id === 'object' ? `${flight.drone_id.manufacturer} ${flight.drone_id.model} (${flight.drone_id.serial_number})` : `Дрон #${flight.drone_id}` }}
            </div>
          </div>
          <div>
            <v-btn
              color="primary"
              prepend-icon="mdi-pencil"
              @click="editFlight"
              class="mr-2"
            >
              Редактировать
            </v-btn>
            <v-btn
              color="error"
              prepend-icon="mdi-delete"
              @click="confirmDelete"
            >
              Удалить
            </v-btn>
          </div>
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <div class="mb-2"><strong>Начало:</strong> {{ formatDateTime(flight.start_datetime) }}</div>
              <div class="mb-2"><strong>Окончание:</strong> {{ formatDateTime(flight.end_datetime) }}</div>
              <div class="mb-2"><strong>Регион:</strong> {{ flight.location }}</div>
              <div class="mb-2"><strong>Причина:</strong> {{ flight.purpose }}</div>
              <div class="mb-2"><strong>Дистанция:</strong> {{ flight.distance }} км</div>
              <div class="mb-2"><strong>Использовано батареи:</strong> {{ flight.battery_usage }}%</div>
              <div v-if="flight.notes" class="mb-2">
                <strong>Заметки:</strong>
                <div class="mt-1">{{ flight.notes }}</div>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Логи полёта -->
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span>Логи полёта ({{ flight.logs?.length || 0 }})</span>
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            @click="showLogDialog = true"
          >
            Добавить лог
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-table v-if="flight.logs && flight.logs.length > 0">
            <thead>
              <tr>
                <th>Время</th>
                <th>Широта</th>
                <th>Долгота</th>
                <th>Высота</th>
                <th>Батарея</th>
                <th>Сообщение</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in flight.logs" :key="log.id">
                <td>{{ formatDateTime(log.timestamp) }}</td>
                <td>{{ log.latitude }}</td>
                <td>{{ log.longtitude }}</td>
                <td>{{ log.altitude }} м</td>
                <td>{{ log.battery }}%</td>
                <td>{{ log.message || '-' }}</td>
                <td>
                  <v-btn
                    icon
                    variant="text"
                    size="small"
                    @click="editLog(log)"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn
                    icon
                    variant="text"
                    size="small"
                    color="error"
                    @click="deleteLog(log.id)"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
          <div v-else class="text-center text-h6 pa-4">
            Логи не найдены
          </div>
        </v-card-text>
      </v-card>

      <!-- Диалог создания/редактирования лога -->
      <LogDialog
        v-model="showLogDialog"
        :flight-id="parseInt($route.params.id)"
        :log="editingLog"
        @saved="loadFlight"
      />

      <!-- Диалог редактирования полёта -->
      <FlightDialog
        v-model="showFlightDialog"
        :flight="flight"
        @saved="loadFlight"
      />

      <!-- Диалог подтверждения удаления -->
      <v-dialog v-model="showDeleteDialog" max-width="400">
        <v-card>
          <v-card-title>Подтверждение удаления</v-card-title>
          <v-card-text>
            Вы уверены, что хотите удалить полёт #{{ flight.id }}?
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="showDeleteDialog = false">Отмена</v-btn>
            <v-btn color="error" @click="deleteFlight">Удалить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import * as flightsAPI from '@/api/flights'
import * as logsAPI from '@/api/logs'
import FlightDialog from '@/components/FlightDialog.vue'
import LogDialog from '@/components/LogDialog.vue'

const route = useRoute()
const router = useRouter()
const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const flight = ref(null)
const showLogDialog = ref(false)
const showFlightDialog = ref(false)
const showDeleteDialog = ref(false)
const editingLog = ref(null)

const formatDateTime = (dateString) => {
  if (!dateString) return 'Не указано'
  return new Date(dateString).toLocaleString('ru-RU')
}

const loadFlight = async () => {
  loading.value = true
  try {
    const flightData = await flightsAPI.getFlight(route.params.id)
    flight.value = flightData

    // Всегда загружаем логи отдельно для актуальности
    try {
      const logsData = await flightsAPI.getFlightLogs(route.params.id)
      flight.value.logs = Array.isArray(logsData) ? logsData : []
    } catch (logError) {
      console.error('Ошибка загрузки логов:', logError)
      flight.value.logs = flight.value.logs || []
    }
  } catch (error) {
    console.error('Ошибка загрузки полёта:', error)
    showSnackbar('Ошибка загрузки полёта', 'error')
    router.push('/drones')
  } finally {
    loading.value = false
  }
}

const editFlight = () => {
  showFlightDialog.value = true
}

const confirmDelete = () => {
  showDeleteDialog.value = true
}

const deleteFlight = async () => {
  try {
    await flightsAPI.deleteFlight(route.params.id)
    showSnackbar('Полёт успешно удалён', 'success')
    router.push('/drones')
  } catch (error) {
    showSnackbar('Ошибка удаления полёта', 'error')
  }
}

const editLog = (log) => {
  editingLog.value = log
  showLogDialog.value = true
}

const deleteLog = async (logId) => {
  try {
    await logsAPI.deleteLog(logId)
    showSnackbar('Лог успешно удалён', 'success')
    loadFlight()
  } catch (error) {
    showSnackbar('Ошибка удаления лога', 'error')
  }
}

const initializeFlight = () => {
  if (route.params.id) {
    loadFlight()
  }
}

watch(() => route.params.id, (newId, oldId) => {
  if (newId && newId !== oldId) {
    flight.value = null
    editingLog.value = null
    showLogDialog.value = false
    showFlightDialog.value = false
    showDeleteDialog.value = false
    loadFlight()
  }
})

// Сбрасываем editingLog при закрытии диалога
watch(showLogDialog, (newValue) => {
  if (!newValue) {
    editingLog.value = null
  }
})

onMounted(() => {
  initializeFlight()
})

onUnmounted(() => {
  // Очищаем состояние при размонтировании
  flight.value = null
  editingLog.value = null
  showLogDialog.value = false
  showFlightDialog.value = false
  showDeleteDialog.value = false
})
</script>
