<template>
  <div>
    <v-row class="mb-4">
      <v-col cols="12" md="6">
        <h1 class="text-h4">Полёты</h1>
      </v-col>
      <v-col cols="12" md="6" class="text-right">
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="showFlightDialog = true"
        >
          Добавить полёт
        </v-btn>
      </v-col>
    </v-row>

    <v-card v-if="loading">
      <v-card-text>
        <v-progress-circular
          indeterminate
          color="primary"
          class="d-block mx-auto"
        ></v-progress-circular>
      </v-card-text>
    </v-card>

    <v-card v-else>
      <v-card-text>
        <v-table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Дрон</th>
              <th>Начало</th>
              <th>Окончание</th>
              <th>Регион</th>
              <th>Дистанция</th>
              <th>Батарея</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="flight in flights"
              :key="flight.id"
              @click="$router.push(`/flights/${flight.id}`)"
              style="cursor: pointer;"
            >
              <td>{{ flight.id }}</td>
              <td>
                <div v-if="flight.drone_id">
                  <div v-if="typeof flight.drone_id === 'object'">
                    {{ flight.drone_id.manufacturer }} {{ flight.drone_id.model }}
                    <div class="text-caption text-grey">
                      {{ flight.drone_id.serial_number }}
                    </div>
                  </div>
                  <div v-else>
                    Дрон #{{ flight.drone_id }}
                  </div>
                </div>
                <span v-else class="text-grey">-</span>
              </td>
              <td>{{ formatDateTime(flight.start_datetime) }}</td>
              <td>{{ formatDateTime(flight.end_datetime) }}</td>
              <td>{{ flight.location }}</td>
              <td>{{ flight.distance }} км</td>
              <td>
                <v-progress-linear
                  :model-value="flight.battery_usage"
                  :color="getBatteryColor(flight.battery_usage)"
                  height="20"
                  rounded
                >
                  <template v-slot:default>
                    <strong>{{ flight.battery_usage }}%</strong>
                  </template>
                </v-progress-linear>
              </td>
              <td>
                <v-btn
                  icon
                  variant="text"
                  size="small"
                  @click.stop="editFlight(flight)"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn
                  icon
                  variant="text"
                  size="small"
                  color="error"
                  @click.stop="confirmDelete(flight)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </td>
            </tr>
            <tr v-if="flights.length === 0">
              <td colspan="8" class="text-center pa-8">
                Полётов не найдено
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>

    <!-- Диалог создания/редактирования полёта -->
    <FlightDialog
      v-model="showFlightDialog"
      :flight="editingFlight"
      @saved="loadFlights"
      @update:modelValue="(val) => { showFlightDialog = val; if (!val) editingFlight = null; }"
    />

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить полёт #{{ deletingFlight?.id }}?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showDeleteDialog = false">Отмена</v-btn>
          <v-btn color="error" @click="deleteFlight">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import * as flightsAPI from '@/api/flights'
import FlightDialog from '@/components/FlightDialog.vue'

const router = useRouter()
const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const flights = ref([])
const showFlightDialog = ref(false)
const editingFlight = ref(null)
const showDeleteDialog = ref(false)
const deletingFlight = ref(null)

const formatDateTime = (dateString) => {
  if (!dateString) return 'Не указано'
  return new Date(dateString).toLocaleString('ru-RU', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const getBatteryColor = (battery) => {
  if (battery >= 70) return 'success'
  if (battery >= 30) return 'warning'
  return 'error'
}

const loadFlights = async () => {
  loading.value = true
  try {
    flights.value = await flightsAPI.getFlights()
  } catch (error) {
    showSnackbar('Ошибка загрузки полётов', 'error')
  } finally {
    loading.value = false
  }
}

const editFlight = (flight) => {
  editingFlight.value = flight
  showFlightDialog.value = true
}

const confirmDelete = (flight) => {
  deletingFlight.value = flight
  showDeleteDialog.value = true
}

const deleteFlight = async () => {
  if (!deletingFlight.value) return

  try {
    await flightsAPI.deleteFlight(deletingFlight.value.id)
    showSnackbar('Полёт успешно удалён', 'success')
    showDeleteDialog.value = false
    deletingFlight.value = null
    loadFlights()
  } catch (error) {
    showSnackbar('Ошибка удаления полёта', 'error')
  }
}


onMounted(() => {
  loadFlights()
})
</script>
